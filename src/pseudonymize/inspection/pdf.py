from dataclasses import dataclass
from difflib import SequenceMatcher
from io import BytesIO
from pathlib import Path

from pseudonymize.document import ContentBlock, CoordinateLocation, Document, StructuralLocation
from pseudonymize.exceptions import AdapterExecutionError

try:
    import pymupdf

    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    import pytesseract

    HAS_OCR = True
except ImportError:
    HAS_OCR = False


@dataclass(frozen=True, slots=True)
class _ChangedSpan:
    source_start: int
    source_end: int
    output_start: int
    output_end: int


def _changed_spans(source: str, output: str) -> tuple[_ChangedSpan, ...]:
    raw = [
        _ChangedSpan(source_start, source_end, output_start, output_end)
        for tag, source_start, source_end, output_start, output_end in SequenceMatcher(
            a=source,
            b=output,
            autojunk=False,
        ).get_opcodes()
        if tag != "equal"
    ]
    merged: list[_ChangedSpan] = []
    for span in raw:
        if (
            merged
            and span.source_start - merged[-1].source_end <= 4
            and span.output_start - merged[-1].output_end <= 4
            and "\n" not in source[merged[-1].source_end : span.source_start]
            and "\n" not in source[span.source_start : span.source_end]
            and "\n" not in source[merged[-1].source_start : merged[-1].source_end]
        ):
            previous = merged[-1]
            merged[-1] = _ChangedSpan(
                previous.source_start,
                span.source_end,
                previous.output_start,
                span.output_end,
            )
        else:
            merged.append(span)
    return tuple(merged)


class PDFInspectionAdapter:
    """Extracts and format-preserves PDF documents using secure redaction."""

    def __init__(self) -> None:
        if not HAS_PDF:
            raise RuntimeError(
                "The PDF adapter requires the 'pdf' extra. "
                "Install it with `pip install pseudonymize[pdf]`."
            )
        self._source_path: Path | None = None
        self._source_text: dict[str, str] = {}

    def extract(self, source: Path) -> Document:
        blocks: list[ContentBlock] = []
        self._source_path = source
        try:
            doc = pymupdf.open(source)
            for page_index, page in enumerate(doc):
                # get_text("blocks") returns tuples: (x0, y0, x1, y1, "text", block_no, block_type)
                # block_type == 0 means text, 1 means image
                page_blocks = page.get_text("blocks")
                page_had_text = False
                for b in page_blocks:
                    if len(b) >= 7 and b[6] == 0:
                        x0, y0, x1, y1, text, block_no, _ = b
                        text = text.strip()
                        if text:
                            page_had_text = True
                            location = CoordinateLocation(
                                page=page_index,
                                x0=float(x0),
                                y0=float(y0),
                                x1=float(x1),
                                y1=float(y1),
                            )
                            blocks.append(
                                ContentBlock(
                                    id=f"page-{page_index}-block-{block_no:06d}",
                                    text=text,
                                    location=location,
                                )
                            )

                # Fallback to OCR if the page has no extractable text and OCR is available
                if not page_had_text and HAS_OCR:
                    dpi = 300
                    pix = page.get_pixmap(dpi=dpi)
                    img = pix.pil_image()

                    # PSM 11: Sparse text. Find as much text as possible in no particular order.
                    # This is ideal for degraded, noisy, or skewed medical faxes / legacy scans
                    # where traditional paragraph detection (PSM 3) fails due to watermarks or skew.
                    custom_oem_psm_config = r"--oem 3 --psm 11"
                    data = pytesseract.image_to_data(
                        img, output_type=pytesseract.Output.DICT, config=custom_oem_psm_config
                    )

                    # Tesseract coordinates are in pixels at the specified DPI.
                    # PDF coordinates are in points (72 points per inch).
                    scale = 72.0 / dpi

                    n_boxes = len(data["text"])
                    for i in range(n_boxes):
                        text = data["text"][i].strip()
                        if text:
                            # Tesseract bounding box
                            left = data["left"][i]
                            top = data["top"][i]
                            width = data["width"][i]
                            height = data["height"][i]

                            # Convert to PDF points
                            x0 = left * scale
                            y0 = top * scale
                            x1 = (left + width) * scale
                            y1 = (top + height) * scale

                            location = CoordinateLocation(
                                page=page_index,
                                x0=float(x0),
                                y0=float(y0),
                                x1=float(x1),
                                y1=float(y1),
                            )
                            blocks.append(
                                ContentBlock(
                                    id=f"page-{page_index}-ocr-{i:06d}",
                                    text=text,
                                    location=location,
                                )
                            )

            for key, val in doc.metadata.items():
                if val and isinstance(val, str) and key not in {"format", "encryption"}:
                    blocks.append(
                        ContentBlock(
                            id=f"pdf-info-{key}",
                            text=val.strip(),
                            location=StructuralLocation(path=("info", key)),
                        )
                    )

            xmp = doc.get_xml_metadata()
            if xmp:
                blocks.append(
                    ContentBlock(
                        id="pdf-xmp",
                        text=xmp.strip(),
                        location=StructuralLocation(path=("xmp",)),
                    )
                )

            doc.close()
        except Exception:
            raise AdapterExecutionError("input adapter failed while reading the PDF") from None

        metadata = {"format": "pdf"}
        document = Document("file", tuple(blocks), metadata)
        self._source_text = {block.id: block.text for block in document.blocks}
        return document

    def render(self, document: Document) -> bytes:
        if not self._source_path:
            raise AdapterExecutionError("Cannot render before extraction")

        try:
            doc = pymupdf.open(self._source_path)

            page_blocks: dict[int, list[ContentBlock]] = {}
            metadata_updates: dict[str, str] = {}
            xmp_update: str | None = None

            for block in document.blocks:
                loc = block.location
                if isinstance(loc, StructuralLocation):
                    if loc.path and loc.path[0] == "info":
                        metadata_updates[str(loc.path[1])] = block.text
                    elif loc.path and loc.path[0] == "xmp":
                        xmp_update = block.text
                    continue

                if isinstance(loc, CoordinateLocation):
                    if self._source_text.get(block.id) == block.text:
                        continue
                    page_blocks.setdefault(loc.page, []).append(block)

            for page_index, page in enumerate(doc):
                if page_index in page_blocks:
                    for block in page_blocks[page_index]:
                        loc = block.location
                        if not isinstance(loc, CoordinateLocation):
                            continue

                        rect = pymupdf.Rect(loc.x0, loc.y0, loc.x1, loc.y1)
                        original = self._source_text.get(block.id)
                        replacements = (
                            _located_replacements(page, rect, original, block.text)
                            if original is not None
                            else ()
                        )
                        if replacements:
                            for replacement_rect, replacement_text in replacements:
                                _add_redaction(
                                    page,
                                    replacement_rect,
                                    replacement_text,
                                    _source_text_color(page, replacement_rect),
                                )
                        else:
                            # Fail closed if an exact changed span cannot be located.
                            _add_redaction(page, rect, block.text, _source_text_color(page, rect))

                    # Preserve page artwork for text PDFs. OCR detections originate in page
                    # images, so their intersecting pixels must still be blanked securely.
                    redact_image_pixels = any(
                        "-ocr-" in block.id for block in page_blocks[page_index]
                    )
                    page.apply_redactions(
                        images=2 if redact_image_pixels else 0,
                        graphics=0,
                        text=0,
                    )

            # Apply metadata updates and clear missing fields to prevent leaks
            new_metadata = {
                "author": metadata_updates.get("author", "pseudonymize"),
                "creator": metadata_updates.get("creator", "pseudonymize"),
                "producer": metadata_updates.get("producer", "pseudonymize"),
                "title": metadata_updates.get("title", "Sanitized Document"),
                "subject": metadata_updates.get("subject", ""),
                "keywords": metadata_updates.get("keywords", ""),
                "creationDate": metadata_updates.get("creationDate", ""),
                "modDate": metadata_updates.get("modDate", ""),
            }
            doc.set_metadata(new_metadata)

            if xmp_update is not None:
                doc.set_xml_metadata(xmp_update)
            else:
                doc.set_xml_metadata("")

            out = BytesIO()
            # Save securely to purge unused objects and streams
            doc.save(out, garbage=4, deflate=True, clean=True)
            doc.close()
            return out.getvalue()
        except Exception:
            raise AdapterExecutionError("output adapter failed while rendering the PDF") from None


def _located_replacements(
    page: object, clip: object, source: str, output: str
) -> tuple[tuple[object, str], ...]:
    replacements: list[tuple[object, str]] = []
    for span in _changed_spans(source, output):
        source_value = source[span.source_start : span.source_end]
        output_value = output[span.output_start : span.output_end]
        if not source_value or not output_value or "\n" in source_value:
            return ()
        matches = page.search_for(source_value, clip=clip)  # type: ignore[attr-defined]
        occurrence = source.count(source_value, 0, span.source_start)
        if occurrence >= len(matches):
            return ()
        replacements.append((matches[occurrence], output_value))
    return tuple(replacements)


def _source_text_color(page: object, rect: object) -> tuple[float, float, float]:
    content = page.get_text("dict", clip=rect)  # type: ignore[attr-defined]
    for block in content.get("blocks", ()):
        for line in block.get("lines", ()):
            for span in line.get("spans", ()):
                color = span.get("color")
                if isinstance(color, int):
                    red, green, blue = pymupdf.sRGB_to_pdf(color)
                    return (float(red), float(green), float(blue))
    return (0, 0, 0)


def _add_redaction(
    page: object,
    rect: object,
    text: str,
    text_color: tuple[float, float, float],
) -> None:
    page.add_redact_annot(  # type: ignore[attr-defined]
        rect,
        text=text,
        fill=False,
        text_color=text_color,
        cross_out=False,
    )
