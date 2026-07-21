import pytest

from pseudonymize import EntityType, Policy


def test_builtin_policies() -> None:
    assert EntityType.SECRET not in Policy.default().entity_types
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
