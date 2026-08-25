from pathlib import Path

from pseudonymize.document import ContentBlock, CoordinateLocation, Document
from pseudonymize.exceptions import AdapterContractError, AdapterExecutionError

try:
    import pytesseract
    from PIL import Image

    HAS_OCR = True
except ImportError:
    HAS_OCR = False


class ImageInspectionAdapter:
    """Extracts text from PNG and JPEG images using OCR."""

    def __init__(self, format_hint: str) -> None:
        if not HAS_OCR:
            raise RuntimeError(
                "The Image adapter requires the 'ocr' extra. "
                "Install it with `pip install pseudonymize[ocr]`."
            )
        self.format_hint = format_hint

    def extract(self, source: Path) -> Document:
        blocks: list[ContentBlock] = []
        try:
            img = Image.open(source)
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

            n_boxes = len(data["text"])
            for i in range(n_boxes):
                text = data["text"][i].strip()
                if text:
                    # Tesseract bounding box
                    left = data["left"][i]
                    top = data["top"][i]
                    width = data["width"][i]
                    height = data["height"][i]

                    location = CoordinateLocation(
                        page=0,
                        x0=float(left),
                        y0=float(top),
                        x1=float(left + width),
                        y1=float(top + height),
                    )
                    blocks.append(
                        ContentBlock(
                            id=f"img-ocr-{i:06d}",
                            text=text,
                            location=location,
                        )
                    )
        except Exception:
            raise AdapterExecutionError(
                f"input adapter failed while reading the {self.format_hint.upper()} image"
            ) from None

        metadata = {"format": self.format_hint}
        return Document("file", tuple(blocks), metadata)

    def render(self, document: Document) -> bytes:
        raise AdapterContractError(
            f"{self.format_hint.upper()} format-preserving rendering is not yet supported. "
            "Image extraction is for inspection only."
        )
