#!/usr/bin/env python3
"""Re-sync LSI workflow bundle: maintainer local install and/or adopter adopt.

Used by /lsi:update. Run from bundle maintainer repo or an LSI adopter repo.

    python3 snippets/update-workflows.py              # auto-detect
    python3 snippets/update-workflows.py --dry-run
    python3 snippets/update-workflows.py --bundle /path/to/cursor-dev-workflows  # adopter self-update
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

BUNDLE_ROOT = Path(__file__).resolve().parents[1]
ADOPT = BUNDLE_ROOT / "snippets" / "adopt.py"
BOOTSTRAP = BUNDLE_ROOT / "snippets" / "bootstrap-maintainer-local.sh"
VERIFY = BUNDLE_ROOT / "snippets" / "verify-adopters.py"
AUDIT = BUNDLE_ROOT / "snippets" / "audit-agent-docs.py"
MAINTAINER_ADOPTERS_LOCAL = "maintainer-adopters.local.yaml"


def _load_adopt_yaml(path: Path) -> dict:
    import importlib.util

    spec = importlib.util.spec_from_file_location("adopt", ADOPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {ADOPT}")
    adopt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(adopt)
    data = adopt._load_yaml_text(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected mapping: {path}")
    return data


def load_maintainer_adopter_targets(bundle: Path) -> list[tuple[str, str]]:
    """Org-specific adopter paths — gitignored maintainer-adopters.local.yaml only."""
    path = bundle / MAINTAINER_ADOPTERS_LOCAL
    if not path.is_file():
        return []
    try:
        data = _load_adopt_yaml(path)
    except (OSError, ValueError) as exc:
        print(f"Invalid {MAINTAINER_ADOPTERS_LOCAL}: {exc}", file=sys.stderr)
        return []
    adopters = data.get("adopters")
    if not isinstance(adopters, list):
        print(
            f"Invalid {MAINTAINER_ADOPTERS_LOCAL}: expected adopters list",
            file=sys.stderr,
        )
        return []
    out: list[tuple[str, str]] = []
    for item in adopters:
        if not isinstance(item, dict):
            continue
        target = item.get("target")
        config = item.get("config")
        if isinstance(target, str) and isinstance(config, str):
            out.append((target, config))
    return out


def repo_root() -> Path:
    return Path.cwd().resolve()


def read_project_repo_name(root: Path) -> str | None:
    project = root / "PROJECT.md"
    if not project.is_file():
        return None
    text = project.read_text(encoding="utf-8")
    m = re.search(r"`REPO_NAME`\s*\|\s*`([^`]+)`", text)
    return m.group(1).strip() if m else None


def is_bundle_maintainer(root: Path) -> bool:
    return (
        (root / "snippets" / "adopt.py").is_file()
        and (root / "overlays" / "lsi").is_dir()
        and (root / "VERSION").is_file()
        and read_project_repo_name(root) == "cursor-dev-workflows"
    )


def is_adopter(root: Path) -> bool:
    return (root / ".lsi" / "workflows" / "which-workflow.md").is_file()


def find_patch_for_repo(bundle: Path, repo_name: str) -> Path | None:
    patches = bundle / "patches"
    if not patches.is_dir():
        return None
    for yaml_path in sorted(patches.glob("*.yaml")):
        if yaml_path.name.startswith("_"):
            continue
        text = yaml_path.read_text(encoding="utf-8")
        if re.search(rf"^repo:\s*{re.escape(repo_name)}\s*$", text, re.MULTILINE):
            return yaml_path
        if re.search(rf"REPO_NAME:\s*{re.escape(repo_name)}\b", text):
            return yaml_path
    return None


def run(cmd: list[str], *, cwd: Path | None = None, dry_run: bool = False) -> int:
    label = " ".join(cmd)
    print(f"→ {label}")
    if dry_run:
        return 0
    result = subprocess.run(cmd, cwd=cwd or BUNDLE_ROOT)
    return result.returncode


def bootstrap_maintainer(*, dry_run: bool = False) -> int:
    if not BOOTSTRAP.is_file():
        print(f"Missing {BOOTSTRAP}", file=sys.stderr)
        return 1
    return run([str(BOOTSTRAP)], dry_run=dry_run)


def run_parity_check(
    target: Path,
    config_path: Path,
    *,
    dry_run: bool = False,
    interactive: bool = True,
) -> int:
    """Run agent-stack parity check after adopt; ask adopter about surplus files.

    Returns 0 if clean or adopter resolved surplus, 1 if unresolved surplus remains.
    """
    if dry_run:
        print(f"→ parity check: {target.name} (dry-run)")
        return 0

    import importlib.util

    # Load audit module
    spec = importlib.util.spec_from_file_location("audit_agent_docs", AUDIT)
    if spec is None or spec.loader is None:
        print(f"Cannot load {AUDIT}", file=sys.stderr)
        return 1
    audit_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit_mod)

    # Load adopt module to read config
    adopt_spec = importlib.util.spec_from_file_location("adopt_mod", ADOPT)
    if adopt_spec is None or adopt_spec.loader is None:
        print(f"Cannot load {ADOPT}", file=sys.stderr)
        return 1
    adopt_mod = importlib.util.module_from_spec(adopt_spec)
    adopt_spec.loader.exec_module(adopt_mod)

    try:
        config = adopt_mod.load_config(config_path)
    except SystemExit as e:
        print(f"Config error: {e}", file=sys.stderr)
        return 1

    sync_opsx = config.get("sync_opsx", False)
    preserve_globs = list(config.get("preserve") or [])

    findings = audit_mod.check_agent_stack_parity(
        target,
        sync_opsx=sync_opsx,
        preserve_globs=preserve_globs,
    )

    surplus = [
        f for f in findings
        if f.category == "agent_stack_parity" and f.severity == audit_mod.SEVERITY_ERROR
    ]

    if not surplus:
        return 0

    print(f"\nParity check found {len(surplus)} unresolved surplus/alias item(s) in {target.name}:")
    for f in surplus:
        print(f"  {f.location}: {f.message}")
        if f.suggestion:
            print(f"    → {f.suggestion}")

    if not interactive:
        print("\nNon-interactive mode: surplus unresolved. Add to preserve_agent_stack or remove manually.")
        return 1

    print("\nWhich paths do you want to remove? Enter one path per line (blank line to finish, 'none' to skip all):")
    confirmed: list[str] = []
    while True:
        try:
            line = input("  remove> ").strip()
        except EOFError:
            break
        if not line or line.lower() == "none":
            break
        confirmed.append(line)

    if not confirmed:
        print("No paths confirmed for removal — surplus remains. Add to preserve_agent_stack in patch YAML to suppress.")
        return 1

    for rel in confirmed:
        path = target / rel
        if path.is_file():
            path.unlink()
            print(f"  Removed: {rel}")
        elif path.exists():
            print(f"  SKIP (not a file): {rel}")
        else:
            print(f"  SKIP (not found): {rel}")

    # Re-run parity after cleanup
    findings_after = audit_mod.check_agent_stack_parity(
        target, sync_opsx=sync_opsx, preserve_globs=preserve_globs
    )
    surplus_after = [
        f for f in findings_after
        if f.category == "agent_stack_parity" and f.severity == audit_mod.SEVERITY_ERROR
    ]
    if surplus_after:
        print(f"\nStill {len(surplus_after)} unresolved surplus item(s). Add to preserve_agent_stack to allowlist.")
        return 1

    print("Parity: OK after cleanup")
    return 0


def adopt_target(
    bundle: Path,
    target: Path,
    config: Path,
    *,
    dry_run: bool = False,
    accept_policy_defaults: bool = True,
) -> int:
    if not ADOPT.is_file():
        print(f"Missing {ADOPT}", file=sys.stderr)
        return 1
    if not target.is_dir():
        print(f"SKIP: adopter not found — {target}", file=sys.stderr)
        return 0
    if not config.is_file():
        print(f"Missing patch config {config}", file=sys.stderr)
        return 1
    cmd = [
        sys.executable,
        str(ADOPT),
        "--target",
        str(target.resolve()),
        "--config",
        str(config.resolve()),
    ]
    if dry_run:
        cmd.append("--dry-run")
    elif accept_policy_defaults:
        cmd.append("--accept-policy-defaults")
    return run(cmd, cwd=bundle, dry_run=False if not dry_run else dry_run)


def verify_adopter(target: Path, *, dry_run: bool = False) -> int:
    if dry_run:
        print(f"→ verify-adopters.py --repo-root {target}")
        return 0
    return run(
        [sys.executable, str(VERIFY), "--repo-root", str(target.resolve())],
        cwd=BUNDLE_ROOT,
    )


def sync_maintainer_adopters(bundle: Path, *, dry_run: bool = False) -> int:
    targets = load_maintainer_adopter_targets(bundle)
    if not targets:
        print(
            f"SKIP: no adopter targets — create {MAINTAINER_ADOPTERS_LOCAL} "
            "(see gitignored MAINTAINER.md)",
            file=sys.stderr,
        )
        return 0
    code = 0
    for rel_target, rel_config in targets:
        target = (bundle / rel_target).resolve()
        config = bundle / rel_config
        print(f"\n=== adopter: {target.name} ===")
        if adopt_target(bundle, target, config, dry_run=dry_run) != 0:
            code = 1
            continue
        if not dry_run:
            parity_code = run_parity_check(target, config, dry_run=dry_run, interactive=True)
            if parity_code != 0:
                code = 1
        if not dry_run and verify_adopter(target) != 0:
            code = 1
    return code


def verify_maintainer_adopters(bundle: Path, *, dry_run: bool = False) -> int:
    targets = load_maintainer_adopter_targets(bundle)
    if not targets:
        print(
            f"SKIP: no adopter targets — create {MAINTAINER_ADOPTERS_LOCAL} "
            "(see gitignored MAINTAINER.md)",
            file=sys.stderr,
        )
        return 0
    code = 0
    for rel_target, _rel_config in targets:
        target = (bundle / rel_target).resolve()
        print(f"\n=== verify: {target.name} ===")
        if not target.is_dir():
            print(f"SKIP: adopter not found — {target}", file=sys.stderr)
            continue
        if verify_adopter(target, dry_run=dry_run) != 0:
            code = 1
    return code


def sync_adopter_self(bundle: Path, adopter: Path, *, dry_run: bool = False) -> int:
    repo_name = read_project_repo_name(adopter)
    if not repo_name:
        print("Cannot read REPO_NAME from PROJECT.md", file=sys.stderr)
        return 1
    config = find_patch_for_repo(bundle, repo_name)
    if not config:
        print(
            f"No patches/<repo>.yaml for REPO_NAME={repo_name!r} under {bundle}",
            file=sys.stderr,
        )
        return 1
    print(f"=== adopter self-update: {repo_name} ===")
    if adopt_target(bundle, adopter, config, dry_run=dry_run) != 0:
        return 1
    if dry_run:
        return 0
    return verify_adopter(adopter)


def resolve_bundle(explicit: Path | None, cwd: Path) -> Path | None:
    if explicit:
        return explicit.resolve()
    if is_bundle_maintainer(cwd):
        return cwd
    env = __import__("os").environ.get("WORKFLOWS_BUNDLE_PATH")
    if env:
        p = Path(env).expanduser().resolve()
        if is_bundle_maintainer(p):
            return p
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Re-sync LSI workflows (/lsi:update helper).")
    parser.add_argument(
        "--bundle",
        type=Path,
        default=None,
        help="Path to cursor-dev-workflows (adopter repos)",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--adopters-only",
        action="store_true",
        help="Bundle maintainer: skip bootstrap, only adopt registered adopters",
    )
    parser.add_argument(
        "--local-only",
        action="store_true",
        help="Bundle maintainer: bootstrap only, skip adopter adopt loop",
    )
    parser.add_argument(
        "--verify-adopters-only",
        action="store_true",
        help="Bundle maintainer: verify registered adopters only (no bootstrap/adopt)",
    )
    args = parser.parse_args(argv)

    cwd = repo_root()
    bundle = resolve_bundle(args.bundle, cwd)

    if is_bundle_maintainer(cwd):
        print("Detected: bundle maintainer (cursor-dev-workflows)")
        bundle = cwd
        code = 0
        if args.verify_adopters_only:
            code = verify_maintainer_adopters(bundle, dry_run=args.dry_run)
            if code == 0 and not args.dry_run:
                print("\nOK: adopter verify complete")
            return code
        if not args.adopters_only:
            if bootstrap_maintainer(dry_run=args.dry_run) != 0:
                code = 1
        if not args.local_only:
            if sync_maintainer_adopters(bundle, dry_run=args.dry_run) != 0:
                code = 1
        if code == 0 and not args.dry_run:
            print("\nOK: maintainer local install + adopter sync complete")
        return code

    if is_adopter(cwd):
        print("Detected: LSI adopter repo")
        if not bundle:
            print(
                "Set WORKFLOWS_BUNDLE_PATH or pass --bundle /path/to/cursor-dev-workflows",
                file=sys.stderr,
            )
            return 1
        code = sync_adopter_self(bundle, cwd, dry_run=args.dry_run)
        if code == 0 and not args.dry_run:
            print("\nOK: adopter re-sync complete — review diff and commit when ready")
        return code

    print(
        "Unknown repo: not bundle maintainer (cursor-dev-workflows) or LSI adopter (.lsi/workflows/)",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
