# DIABLO Immortal Assistant

A local-first helper for reviewing Diablo Immortal screenshots and organizing manually captured character/build information.

## Current capabilities

- Read local screenshots and attempt OCR with Tesseract.
- Parse conservative character-stat and equipment text candidates from OCR.
- Validate a manually completed character profile JSON file.
- Summarize recorded character attributes, equipment slots, legendary gems, and set-bonus entries.
- Generate a conservative PvE report from player-confirmed skills, combinations, and recorded upgraded equipment.
- Run automated tests with GitHub Actions.

## Character profile

Copy `data/character_profile.template.json` to `data/character_profile.json` and fill in values visible in your own game screens. Leave unknown values as `null`. Use the recognized character classes, equipment slots, and item rarities. Do not include passwords, recovery codes, or other account secrets.

Validate and summarize the profile locally:

```bash
python main.py --profile data/character_profile.json
```

Generate a PvE-focused report:

```bash
python main.py --profile data/character_profile.json --pve
```

The PvE report lists only player-confirmed skills, combinations, and known equipment. It highlights missing item essences, set bonuses, and gem details instead of guessing an optimal build.

Run screenshot OCR locally:

```bash
python main.py --image path/to/screenshot.png
```

Install dependencies with `pip install -r requirements.txt`. Tesseract OCR must also be installed on the computer for OCR to work.

## Android yardımcı uygulama planı

Android tablet üzerinde çalışabilecek ayrı yardımcı uygulamanın teknik planı ve kısıtları için [Android yardımcı uygulama planına](docs/ANDROID_COMPANION_PLAN_TR.md) bak. Bu plan henüz çalışan Android uygulaması veya otomatik oyun kontrolü değildir.

## Safety and limitations

This project does not log in to the game, inspect game memory, bypass protections, send touch/key inputs, or play automatically. GitHub Actions is used for code tests, not to control the game running on your tablet. OCR output may be inaccurate; verify all values against the game screen. The profile summary reports supplied data only; it does not claim an item or build is best without verified game rules and complete player data.

## Türkçe karakter profili girişi

Karakter bilgilerini toplamak için [Türkçe profil giriş kılavuzunu](data/profile_entry_guide_tr.md) kullan. JSON dosyasını tablette düzenlemek zorunda değilsin; bilgileri sohbet içinde bölüm bölüm paylaşabilirsin. Bilinmeyen değerler boş bırakılır ve hiçbir istatistik tahmin edilmez.
