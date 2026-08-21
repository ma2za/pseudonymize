from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, cast

import pytest

from pseudonymize import (
    BackendCapabilities,
    CompositeBackend,
    ContentBlock,
    Detection,
    DetectionBackend,
    EntityType,
    NetworkPolicy,
    Policy,
    Pseudonymizer,
    TextOffsetLocation,
)
from pseudonymize.backends import backend_capabilities
from pseudonymize.exceptions import (
    BackendContractError,
    BackendExecutionError,
    InvalidDetectionError,
    NetworkPolicyError,
)


@dataclass
class StubBackend:
    name: str
    detections: Sequence[Detection]
    remote: bool = False
    allow_remote_processing: bool = False
    failure: Exception | None = None
    calls: int = 0
    supported: frozenset[EntityType] | None = None

    @property
    def capabilities(self) -> BackendCapabilities:
        return BackendCapabilities(
            self.supported
            if self.supported is not None
            else frozenset(detection.entity_type for detection in self.detections),
            remote=self.remote,
        )

    def detect(self, block: ContentBlock, policy: Policy) -> Sequence[Detection]:
        self.calls += 1
        if self.failure is not None:
            raise self.failure
        return self.detections


def _email_detection(*, backend: str = "") -> Detection:
    return Detection(EntityType.EMAIL, 0, 17, 0.99, "stub", backend)


def test_backend_provenance_is_added_without_changing_detector() -> None:
    backend = StubBackend("local", (_email_detection(),))
    result = Pseudonymizer(backends=[backend]).process_with_report("maria@example.com")

    assert result.output == "<EMAIL_1>"
    assert result.detections[0].backend == "local"
    assert result.detections[0].detector == "stub"
    assert result.statistics.backend_invocations == 1
    assert result.statistics.local_block_calls == 1
    assert result.statistics.remote_block_calls == 0

    preserved = StubBackend("wrapper", (_email_detection(backend="leaf"),))
    assert Pseudonymizer(backends=[preserved]).detect("maria@example.com")[0].backend == "leaf"


def test_composite_resolution_is_independent_of_backend_order() -> None:
    alpha = StubBackend("alpha", (_email_detection(),))
    zulu = StubBackend("zulu", (_email_detection(),))
    block = ContentBlock("body", "maria@example.com", TextOffsetLocation(0, 17))
    policy = Policy()

    forward = CompositeBackend((zulu, alpha)).detect(block, policy)
    reverse = CompositeBackend((alpha, zulu)).detect(block, policy)

    assert forward == reverse
    assert forward[0].backend == "alpha"
    assert CompositeBackend((zulu, alpha)).capabilities == BackendCapabilities(
        frozenset({EntityType.EMAIL})
    )
    assert (
        Pseudonymizer(backends=[CompositeBackend((zulu, alpha))]).detect("maria@example.com")
        == forward
    )


def test_network_deny_and_allowlist_fail_before_remote_invocation() -> None:
    backend = StubBackend(
        "remote",
        (_email_detection(),),
        remote=True,
        allow_remote_processing=True,
    )
    with pytest.raises(NetworkPolicyError):
        Pseudonymizer(backends=[backend]).process("maria@example.com")
    with pytest.raises(NetworkPolicyError):
        Pseudonymizer(
            backends=[backend],
            policy=Policy(network_policy=NetworkPolicy.ALLOW_CONFIGURED),
        ).process("maria@example.com")
    assert backend.calls == 0


def test_allow_configured_copies_allowlist_and_counts_remote_blocks() -> None:
    allowed = {"remote"}
    backend = StubBackend(
        "remote",
        (_email_detection(),),
        remote=True,
        allow_remote_processing=True,
    )
    policy = Policy(
        network_policy=NetworkPolicy.ALLOW_CONFIGURED,
        allowed_remote_backends=allowed,
    )
    allowed.clear()
    result = Pseudonymizer(backends=[backend], policy=policy).process_data_with_report(
        {"first": "maria@example.com", "second": "maria@example.com"}
    )

    assert backend.calls == 2
    assert policy.allowed_remote_backends == {"remote"}
    assert result.statistics.backend_invocations == 2
    assert result.statistics.remote_block_calls == 2
    assert result.statistics.local_block_calls == 0


def test_allow_all_still_requires_backend_consent() -> None:
    backend = StubBackend("remote", (_email_detection(),), remote=True)
    engine = Pseudonymizer(
        backends=[backend],
        policy=Policy(network_policy=NetworkPolicy.ALLOW_ALL),
    )

    with pytest.raises(NetworkPolicyError, match="explicit consent"):
        engine.process("maria@example.com")
    assert backend.calls == 0


def test_backend_failures_and_contract_errors_are_sanitized() -> None:
    source_value = "maria@example.com"
    failing = StubBackend(
        "remote",
        (_email_detection(),),
        failure=RuntimeError(source_value),
    )
    with pytest.raises(BackendExecutionError) as execution_error:
        Pseudonymizer(backends=[failing]).process(source_value)
    assert source_value not in str(execution_error.value)
    assert execution_error.value.__cause__ is None

    out_of_range = StubBackend(
        "invalid",
        (Detection(EntityType.EMAIL, 0, 99, 0.9, "stub"),),
    )
    with pytest.raises(InvalidDetectionError) as detection_error:
        Pseudonymizer(backends=[out_of_range]).process(source_value)
    assert source_value not in str(detection_error.value)


def test_backend_must_return_declared_detection_values() -> None:
    undeclared = StubBackend(
        "undeclared",
        (_email_detection(),),
        supported=frozenset({EntityType.PERSON}),
    )
    with pytest.raises(BackendContractError, match="undeclared"):
        Pseudonymizer(backends=[undeclared]).process("maria@example.com")

    malformed = StubBackend(
        "malformed",
        cast(Sequence[Detection], (object(),)),
        supported=frozenset({EntityType.EMAIL}),
    )
    with pytest.raises(BackendContractError, match="not a Detection"):
        Pseudonymizer(backends=[malformed]).process("maria@example.com")

    empty_name = StubBackend(
        "",
        (),
        supported=frozenset({EntityType.EMAIL}),
    )
    with pytest.raises(BackendContractError, match="backend name must be a non-empty string"):
        Pseudonymizer(backends=[empty_name]).process("maria@example.com")

    bad_remote = StubBackend(
        "bad",
        (),
        supported=frozenset({EntityType.EMAIL}),
        allow_remote_processing="True",  # type: ignore
    )
    with pytest.raises(BackendContractError, match="backend remote consent must be a boolean"):
        Pseudonymizer(backends=[bad_remote]).process("maria@example.com")

    class BadCapsBackend:
        name = "bad_caps"
        capabilities = "True"  # type: ignore
        allow_remote_processing = False

        def detect(self, block: ContentBlock, policy: Policy) -> Sequence[Detection]:
            return ()

    with pytest.raises(BackendContractError, match="backend capabilities are invalid"):
        Pseudonymizer(backends=[cast(DetectionBackend, BadCapsBackend())]).process(
            "maria@example.com"
        )

    class RaisesExceptionBackend:
        @property
        def name(self) -> str:
            raise RuntimeError("broken")

        @property
        def capabilities(self) -> BackendCapabilities:
            raise RuntimeError("broken")

        @property
        def allow_remote_processing(self) -> bool:
            return False

        def detect(self, block: ContentBlock, policy: Policy) -> Sequence[Detection]:
            return ()

    with pytest.raises(
        BackendContractError, match="backend does not declare the required block-aware contract"
    ):
        Pseudonymizer(backends=[cast(DetectionBackend, RaisesExceptionBackend())]).process(
            "maria@example.com"
        )


def test_old_text_only_backend_fails_migration_contract() -> None:
    class OldBackend:
        name = "old"
        capabilities = BackendCapabilities(frozenset({EntityType.EMAIL}))
        allow_remote_processing = False

        def detect(self, text: str) -> tuple[Detection, ...]:
            return ()

    backend = cast(DetectionBackend, cast(Any, OldBackend()))
    with pytest.raises(BackendContractError, match="block-aware"):
        Pseudonymizer(backends=[backend]).process("maria@example.com")


@pytest.mark.parametrize(
    ("backend", "message"),
    [
        (
            cast(
                DetectionBackend,
                cast(
                    Any,
                    type(
                        "InvalidCapabilities",
                        (),
                        {
                            "name": "invalid",
                            "capabilities": object(),
                            "allow_remote_processing": False,
                        },
                    )(),
                ),
            ),
            "capabilities",
        ),
        (
            cast(
                DetectionBackend,
                cast(
                    Any,
                    type(
                        "InvalidConsent",
                        (),
                        {
                            "name": "invalid",
                            "capabilities": BackendCapabilities(frozenset()),
                            "allow_remote_processing": "yes",
                        },
                    )(),
                ),
            ),
            "consent",
        ),
        (
            cast(
                DetectionBackend,
                cast(
                    Any,
                    type(
                        "InvalidName",
                        (),
                        {
                            "name": "",
                            "capabilities": BackendCapabilities(frozenset()),
                            "allow_remote_processing": False,
                        },
                    )(),
                ),
            ),
            "name",
        ),
    ],
)
def test_backend_declarations_are_validated(backend: DetectionBackend, message: str) -> None:
    with pytest.raises(BackendContractError, match=message):
        backend_capabilities(backend)


def test_backend_capability_values_are_typed_and_immutable() -> None:
    entities = {EntityType.EMAIL}
    capabilities = BackendCapabilities(entities)  # type: ignore[arg-type]
    entities.add(EntityType.PHONE)
    assert capabilities.entity_types == {EntityType.EMAIL}
    with pytest.raises(TypeError, match="EntityType"):
        BackendCapabilities(cast(Any, {"EMAIL"}))
    with pytest.raises(TypeError, match="boolean"):
        BackendCapabilities(frozenset(), cast(Any, 1))


def test_backends_without_relevant_capabilities_are_not_invoked() -> None:
    backend = StubBackend(
        "person",
        (Detection(EntityType.PERSON, 0, 5, 0.9, "stub"),),
    )
    result = Pseudonymizer(
        backends=[backend],
        policy=Policy(entity_types={EntityType.EMAIL}),
    ).process_with_report("Maria")

    assert result.output == "Maria"
    assert backend.calls == 0
    assert result.statistics.backend_invocations == 0
