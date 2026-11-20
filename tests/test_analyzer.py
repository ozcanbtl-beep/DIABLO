from pathlib import Path

from PIL import Image

from main import analyze_image


def test_analyze_image_returns_basic_metadata(tmp_path: Path) -> None:
    image_path = tmp_path / "sample.png"
    Image.new("RGB", (320, 200), "white").save(image_path)

    result = analyze_image(image_path)

    assert result["file"] == "sample.png"
    assert result["format"] == "PNG"
    assert result["width"] == 320
    assert result["height"] == 200
    assert "text" in result
    assert "ocr_available" in result


def test_missing_image_raises_file_not_found(tmp_path: Path) -> None:
    missing = tmp_path / "missing.png"

    try:
        analyze_image(missing)
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("Expected FileNotFoundError")
