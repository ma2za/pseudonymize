from unittest.mock import patch

import pytest

from pseudonymize import Policy, Pseudonymizer
from pseudonymize.backends.remote import HTTPRemoteBackend
from pseudonymize.exceptions import NetworkPolicyError
from pseudonymize.policy import NetworkPolicy
from pseudonymize.result import EntityType


def test_default_and_strict_policy_audit() -> None:
    """Audit default and strict policy configurations across all entity types."""
    default_policy = Policy.default()
    strict_policy = Policy.strict()

    # Network policy must be DENY by default
    assert default_policy.network_policy == NetworkPolicy.DENY
    assert strict_policy.network_policy == NetworkPolicy.DENY
    assert default_policy.allowed_remote_backends == frozenset()
    assert strict_policy.allowed_remote_backends == frozenset()

    # Check every declared EntityType
    all_entity_types = frozenset(EntityType)
    assert len(all_entity_types) == 12

    # Verify each entity type is accounted for
    for entity_type in all_entity_types:
        assert entity_type in default_policy.entity_types
        assert entity_type in strict_policy.entity_types

    assert default_policy.entity_types == all_entity_types
    assert strict_policy.entity_types == all_entity_types

    # Strict policy catches more candidates with lower threshold (higher recall)
    assert default_policy.minimum_confidence == 0.80
    assert strict_policy.minimum_confidence == 0.75


def test_denied_remote_paths_never_touch_network() -> None:
    """Prove that denied network paths fail before creating any socket or resolving DNS."""
    endpoint = "https://unreachable.destination.internal:9999/detect"
    backend = HTTPRemoteBackend(
        name="isolated_backend",
        endpoint=endpoint,
        entity_types=frozenset({EntityType.EMAIL}),
    )

    # Policy denies network egress
    engine = Pseudonymizer(
        backends=[backend],
        policy=Policy(
            entity_types=frozenset({EntityType.EMAIL}),
            network_policy=NetworkPolicy.DENY,
        ),
    )

    with patch("socket.socket") as mock_socket, patch("socket.getaddrinfo") as mock_getaddrinfo:
        with pytest.raises(NetworkPolicyError, match="network policy denies remote processing"):
            engine.process("Contact maria@example.com.")

        # Neither socket instantiation nor DNS lookup may ever occur
        mock_socket.assert_not_called()
        mock_getaddrinfo.assert_not_called()
