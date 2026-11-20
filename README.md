# DIABLO Immortal Assistant

A local-first helper for reviewing Diablo Immortal screenshots and organizing manually captured character/build information.

## Current capabilities

- Read local screenshots and attempt OCR with Tesseract.
- Validate a manually completed character profile JSON file.
- Summarize known character attributes, equipment entries, legendary gems, and set-bonus entries.
- Run automated tests with GitHub Actions.

## Character profile

Copy `data/character_profile.template.json` to `data/character_profile.json` and fill in values visible in your own game screens. Leave unknown values as `null`. Do not include passwords, recovery codes, or other account secrets.

Run the profile summary locally:

```bash
python -c "from build_analyzer import load_profile, summarize_profile; import json; print(json.dumps(summarize_profile(load_profile('data/character_profile.json')), indent=2))"
```

Run screenshot OCR locally:

```bash
python main.py path/to/screenshot.png
```

Install dependencies with `pip install -r requirements.txt`. Tesseract OCR must also be installed on the computer for OCR to work.

## Safety and limitations

This project does not log in to the game, inspect game memory, bypass protections, send touch/key inputs, or play automatically. GitHub Actions is used for code tests, not to control the game running on your tablet. OCR output may be inaccurate; verify all values against the game screen. Build recommendations will only be added when the required game rules and player data can be verified.
