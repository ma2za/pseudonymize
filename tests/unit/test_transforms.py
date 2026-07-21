import re

import pytest

from pseudonymize import Detection, EntityType, generate_key
from pseudonymize.exceptions import InvalidKeyError
from pseudonymize.resolution import ResolvedEntity
from pseudonymize.transforms import (
    AliasContext,
    DeterministicAliasAssigner,
    GenericAliasAssigner,
    NumberedAliasAssigner,
    PlaceholderTransformer,
    RedactTransformer,
)


def entity(
    entity_type: EntityType = EntityType.EMAIL, normalized: str = "maria@example.com"
) -> ResolvedEntity:
    return ResolvedEntity(Detection(entity_type, 0, 17, 1.0, "test"), normalized)


def test_numbered_assigner_reuses_normalized_identity() -> None:
    assigner = NumberedAliasAssigner()
    context = AliasContext()
    first = assigner.assign(entity(), context)
    assert assigner.assign(entity(), context) == first
    assert assigner.assign(entity(normalized="other@example.com"), context).identifier == "2"
    assert assigner.assign(entity(EntityType.PERSON, "maria"), context).identifier == "1"
    assert "maria@example.com" not in repr(context)


def test_generic_and_placeholder_rendering() -> None:
    resolved = entity()
    alias = GenericAliasAssigner().assign(resolved, AliasContext())
    assert PlaceholderTransformer().render(resolved, alias) == "<EMAIL>"


def test_deterministic_assigner_is_domain_separated() -> None:
    key = b"k" * 32
    first = DeterministicAliasAssigner(key, "a").assign(entity(), AliasContext())
    assert first == DeterministicAliasAssigner(key, "a").assign(entity(), AliasContext())
    assert first != DeterministicAliasAssigner(key, "b").assign(entity(), AliasContext())
    assert re.fullmatch(r"[A-Z2-7]{12}", first.identifier or "")


def test_key_validation_generation_and_redaction() -> None:
    with pytest.raises(InvalidKeyError):
        DeterministicAliasAssigner(b"short")
    with pytest.raises(ValueError, match="namespace"):
        DeterministicAliasAssigner(b"k" * 32, "invalid\0namespace")
    assert len(generate_key()) == 32
    resolved = entity()
    alias = GenericAliasAssigner().assign(resolved, AliasContext())
    assert RedactTransformer().render(resolved, alias) == "[REDACTED]"
    assert RedactTransformer(typed=True).render(resolved, alias) == "[REDACTED_EMAIL]"
