# Adopter-shaped source docs

Docs under this directory are authored for **post-adopt layout** in application repos (`.lsi/workflows/`, cross-tree paths to `.cursor/commands/`, etc.). `snippets/adopt.py` copies them instead of maintainer-facing bundle paths when the layouts diverge.

## Three-tier link policy

| Tier | When | Link style |
|------|------|------------|
| **1 — Installed, in daily use** | Target exists in the adopter repo after full adopt | **Relative path** valid from the containing file |
| **2 — Not installed (maintainer-only)** | Target never copied to adopter (`patches/`, `MAINTAINER.md`, bundle `overlays/lsi/…`) | **GitHub blob URL** with `v{{BUNDLE_VERSION}}`, or **plain prose** |
| **3 — Small install extras** | Adopters need a tiny artifact copied during adopt | **Copy in `adopt.py`**, then **tier 1 relative** link (e.g. `ci/check_version-*.yml`) |

### Authoring checklist

1. Does the target exist in the adopter tree after adopt? → tier **1** (relative).
2. Is the target bundle-maintainer-only? → tier **2** (GitHub URL or prose — never `../patches/`, `../../overlays/lsi/`, etc.).
3. Is it a small file adopters must copy-paste? → tier **3** (wire copy in `adopt.py`, link relatively).
4. Fix links **at source** in this tree or in aligned workflow docs — do not rely on `LINK_REWRITES` as the primary strategy (rewrites are a transition aid only).

## Dual-copy maintainer docs

When a maintainer superset exists (e.g. `docs/adopt-and-update.md`), edit adopter-facing sections here too — including **new `##` sections**. The maintainer doc banner points here for process.

## Long-term expansion rule

When a doc copied into adopters cannot be authored correctly in the maintainer tree without tier 2 hrefs or fragile rewrites, add an adopter-shaped copy under `overlays/lsi/adopter-docs/` (mirroring install path) and point `adopt.py` at it. Prefer in-place tier 1 fixes in `docs/workflows/` and `overlays/lsi/docs/workflows/` when maintainer and adopter layouts already align.

When a **second** dual doc enters this directory, add heading lint (compare adopter-relevant `##` headings between maintainer superset and adopter copy) — deferred until then.

**Current scope:** one dual doc (`adopt-and-update.md`). Checklist (1.5) + `test_adopt_links.py` suffice until a second doc triggers task 7.2.

## `which-workflow.md` canonicality

| Role | Path |
|------|------|
| **Adopter canonical (installed)** | `.lsi/workflows/which-workflow.md` after adopt |
| **Edit source (authoritative)** | `overlays/lsi/docs/workflows/which-workflow.md` — `merge_which_workflow_lsi()` overwrites core copy with this file |
| **Sync helper (not installed)** | `overlays/lsi/which-workflow-lsi.md` — keep row/link parity with overlay router |
| **Bundle dogfood (optional)** | Root `which-workflow.md` — maintainer navigation only; not adopter canon |
