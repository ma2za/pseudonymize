import typing

import pymupdf


def _source_text_style(page: object, rect: object) -> dict[str, typing.Any]:
    style: dict[str, typing.Any] = {
        "text_color": (0.0, 0.0, 0.0),
        "fontsize": 11.0,
        "fontname": "helv",
    }
    content = page.get_text("dict", clip=rect)  # type: ignore[attr-defined]
    for block in content.get("blocks", ()):
        for line in block.get("lines", ()):
            for span in line.get("spans", ()):
                color = span.get("color")
                if isinstance(color, int):
                    red, green, blue = pymupdf.sRGB_to_pdf(color)
                    style["text_color"] = (float(red), float(green), float(blue))

                size = span.get("size")
                if isinstance(size, (int, float)):
                    style["fontsize"] = float(size)

                font = span.get("font")
                if isinstance(font, str):
                    font_lower = font.lower()
                    if "times" in font_lower:
                        style["fontname"] = "tiro"
                    elif "courier" in font_lower:
                        style["fontname"] = "cour"
                    else:
                        style["fontname"] = "helv"
                return style
    return style


def _add_redaction(
    page: object,
    rect: object,
    text: str,
    style: dict[str, typing.Any],
) -> None:
    page.add_redact_annot(  # type: ignore[attr-defined]
        rect,
        text=text,
        fill=False,
        text_color=style["text_color"],
        fontsize=style["fontsize"],
        fontname=style["fontname"],
        align=0,  # TEXT_ALIGN_LEFT
        cross_out=False,
    )


doc = pymupdf.open("test.pdf")
page = doc[0]
r = page.search_for("REDACT")[0]
style = _source_text_style(page, r)
print(style)
_add_redaction(page, r, "[REDACTED]", style)
page.apply_redactions()
doc.save("test_redacted.pdf")
