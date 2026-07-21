import pseudonymize as package
from pseudonymize import Policy, Pseudonymizer, TransformationMode, pseudonymize, redact


def test_top_level_api() -> None:
    expected = {
        "Alias",
        "CompositeBackend",
        "Detection",
        "DetectionBackend",
        "EntityType",
        "EntityResolver",
        "ExactEntityResolver",
        "Policy",
        "ProcessingScope",
        "Pseudonymizer",
        "Replacement",
        "ResolvedEntity",
        "Result",
        "RulesBackend",
        "TransformationMode",
        "generate_key",
        "pseudonymize",
        "redact",
    }
    assert set(package.__all__) == expected
    assert pseudonymize("Email maria@example.com") == "Email <EMAIL_1>"
    assert pseudonymize("Email maria@example.com", mode="generic") == "Email <EMAIL>"
    assert redact("Email maria@example.com") == "Email [REDACTED]"
    assert Pseudonymizer(mode=TransformationMode.NUMBERED, policy=Policy.default())
