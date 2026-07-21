import pseudonymize as package
from pseudonymize import Policy, Pseudonymizer, pseudonymize, redact

KEY = b"k" * 32


def test_top_level_api() -> None:
    expected = {
        "Detection",
        "EntityType",
        "Policy",
        "Pseudonymizer",
        "Replacement",
        "Result",
        "generate_key",
        "pseudonymize",
        "redact",
    }
    assert set(package.__all__) == expected
    assert pseudonymize("Email maria@example.com", key=KEY).startswith("Email <PZ1:EMAIL:")
    assert redact("Email maria@example.com") == "Email <EMAIL>"
    assert Pseudonymizer(key=KEY, policy=Policy.default())
