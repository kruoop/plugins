# Kruoop shared marketplace

Keep new skills and plugins in this repository; do not create a separate repository.

- Canonical skill sources belong in `skills/<skill-name>/`.
- Plugin packages belong in `plugins/<plugin-name>/` and must be registered in `.claude-plugin/marketplace.json`.
- `plugins/bbn-video-studio/skills/` is a generated distribution copy. Edit `skills/`, run `python3 scripts/sync_bbn_plugin.py`, then `python3 scripts/sync_bbn_plugin.py --check`.
- Validate affected manifests with `claude plugin validate` and check relative skill links before delivery. Preserve unrelated plugin entries and skills.
- Keep credentials, account sessions, model caches and episode footage out of this repository. Existing shared skill assets are separate from episode footage.
- Browser interaction defaults to ego-browser CLI with TaskSpace. Read the installed ego-browser skill before browser control.
