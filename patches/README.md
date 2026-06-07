# Adopter patches

Each application repo has a `patches/<repo>.yaml` file consumed by `snippets/adopt.py`.

## Run adopt

```bash
cd cursor-dev-workflows
python3 snippets/adopt.py --target ../video-encoder --config patches/video-encoder.yaml --audit-only
python3 snippets/adopt.py --target ../video-encoder --config patches/video-encoder.yaml --accept-policy-defaults
```

## Files

| Patch | Repo |
|-------|------|
| `video-encoder.yaml` | video-encoder |
| `web.yaml` | web |
| `ai-agent.yaml` | ai-agent monorepo |
| `_template.yaml` | Copy for new repos |

Per-repo markdown overlays live in `patches/files/<repo>/`.

## Audit resolutions

Record human decisions in `patches/files/<repo>/audit-resolutions.yaml` when first adopt surfaces contradictions.
