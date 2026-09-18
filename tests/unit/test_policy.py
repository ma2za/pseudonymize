import pytest

from pseudonymize import EntityType, Policy


def test_builtin_policies() -> None:
    assert EntityType.SECRET in Policy.default().entity_types
    assert EntityType.URL_CREDENTIAL in Policy.default().entity_types
    assert EntityType.NATIONAL_ID in Policy.default().entity_types
    assert EntityType.TAX_ID in Policy.default().entity_types
    assert Policy.strict().entity_types == frozenset(EntityType)
    assert Policy.financial().entity_types == {EntityType.IBAN, EntityType.PAYMENT_CARD}
    assert EntityType.SECRET in Policy.llm().entity_types


def test_policy_is_immutable_and_copies_inputs() -> None:
    entities = {EntityType.EMAIL}
    policy = Policy(entity_types=entities)
    entities.add(EntityType.PHONE)
    assert policy.entity_types == {EntityType.EMAIL}


def test_path_matching() -> None:
    policy = Policy.llm(
        include_paths=["messages.*.content", "metadata.*"], exclude_paths=["metadata.public"]
    )
    assert policy.allows_path(("messages", "0", "content"))
    assert policy.allows_path(("metadata", "private"))
    assert not policy.allows_path(("metadata", "public"))
    assert not policy.allows_path(("model",))


def test_invalid_confidence() -> None:
    with pytest.raises(ValueError, match="confidence"):
        Policy(minimum_confidence=-1)


def test_schema_preserving_agent_sanitation() -> None:
    policy = Policy.default()
    # Structural JSON-RPC and MCP schema fields must be bypassed (return False)
    assert not policy.allows_path(("params", "inputSchema", "properties", "email", "type"))
    assert not policy.allows_path(("jsonrpc",))
    assert not policy.allows_path(("method",))
    assert not policy.allows_path(("id",))

    # Standard data fields should still be allowed for redaction (return True)
    assert policy.allows_path(("params", "arguments", "email"))
    assert policy.allows_path(("params", "text"))

    # When disabled, schema fields can be redacted as normal
    unsafe_policy = Policy(schema_preserving=False)
    assert unsafe_policy.allows_path(("params", "inputSchema", "properties", "email", "type"))
