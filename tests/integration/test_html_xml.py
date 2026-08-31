from pathlib import Path

from pseudonymize import Pseudonymizer, TransformationMode
from pseudonymize.formats import FileFormat


def test_html_sanitization(tmp_path: Path) -> None:
    engine = Pseudonymizer(mode=TransformationMode.NUMBERED)

    html = """
    <html>
    <head><title>User Profile</title></head>
    <body>
        <div id="user-info">
            <p>Name: John Doe</p>
            <p>Email: <a href="mailto:john.doe@example.com">john.doe@example.com</a></p>
            <img src="avatar.jpg" alt="Profile of john.doe@example.com"/>
        </div>
        <script>
            var email = "john.doe@example.com";
        </script>
    </body>
    </html>
    """
    in_path = tmp_path / "test.html"
    in_path.write_text(html, encoding="utf-8")

    out_path = tmp_path / "test_safe.html"
    engine.process_file(in_path, out_path, format=FileFormat.HTML)

    result = out_path.read_text(encoding="utf-8")
    assert "<EMAIL_1>" in result
    assert "john.doe@example.com" not in result
    assert 'href="mailto:&lt;EMAIL_1&gt;"' in result
    assert 'alt="Profile of &lt;EMAIL_1&gt;"' in result
    assert "<script>" in result


def test_xml_sanitization(tmp_path: Path) -> None:
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)

    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <users>
        <user id="123">
            <email contact="secret@example.com">secret@example.com</email>
        </user>
    </users>
    """
    in_path = tmp_path / "test.xml"
    in_path.write_text(xml, encoding="utf-8")

    out_path = tmp_path / "test_safe.xml"
    engine.process_file(in_path, out_path, format=FileFormat.XML)

    result = out_path.read_text(encoding="utf-8")
    assert "[REDACTED]" in result
    assert "secret@example.com" not in result
    assert 'contact="[REDACTED]"' in result


def test_html_malformed(tmp_path: Path) -> None:
    engine = Pseudonymizer(mode=TransformationMode.NUMBERED)
    html = "<div> <span>Contact me at malformed@example.com <p> Unclosed tag"

    in_path = tmp_path / "malformed.html"
    in_path.write_text(html, encoding="utf-8")

    out_path = tmp_path / "malformed_safe.html"
    engine.process_file(in_path, out_path, format=FileFormat.HTML)

    result = out_path.read_text(encoding="utf-8")
    assert "&lt;EMAIL_1&gt;" in result or "<EMAIL_1>" in result
    assert "malformed@example.com" not in result


def test_html_nested_tags(tmp_path: Path) -> None:
    engine = Pseudonymizer(mode=TransformationMode.NUMBERED)
    html = "<div><p><span>Hello</span> my email is nested@example.com.</p></div>"

    in_path = tmp_path / "nested.html"
    in_path.write_text(html, encoding="utf-8")

    out_path = tmp_path / "nested_safe.html"
    engine.process_file(in_path, out_path, format=FileFormat.HTML)

    result = out_path.read_text(encoding="utf-8")
    assert "&lt;EMAIL_1&gt;" in result
    assert "nested@example.com" not in result
    assert "<span>Hello</span>" in result
