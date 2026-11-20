"""DIABLO Immortal Assistant: offline screenshot inspection only.

This module does not control the game, send inputs, or automate gameplay.
It extracts basic image metadata and, when available, OCR text for review.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from diablo_parser import parse_game_text


def analyze_image(image_path: str | Path) -> dict[str, Any]:
    """Return image metadata and optional OCR text from a local screenshot."""
    path = Path(image_path)
    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")

    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("Pillow is required. Install requirements.txt first.") from exc

    with Image.open(path) as image:
        result: dict[str, Any] = {
            "file": path.name,
            "format": image.format,
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "ocr_available": False,
            "text": "",
            "notes": [],
        }
        try:
            import pytesseract

            result["text"] = pytesseract.image_to_string(image).strip()
            result["ocr_available"] = True
        except ImportError:
            result["notes"].append("pytesseract is not installed; OCR was skipped.")
        except Exception as exc:  # Tesseract binary may not exist on this machine.
            result["notes"].append(f"OCR could not run: {exc}")

    result["game_data_candidates"] = parse_game_text(result["text"])
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect a Diablo Immortal screenshot.")
    parser.add_argument("image", help="Path to a screenshot image (PNG/JPG/WebP).")
    args = parser.parse_args()
    try:
        print(json.dumps(analyze_image(args.image), ensure_ascii=False, indent=2))
    except (FileNotFoundError, RuntimeError, OSError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
