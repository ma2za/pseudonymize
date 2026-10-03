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
from pseudonymize.backends import (
    backend_capabilities,
    invoke_backend_batch,
)
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

    assert result.output == "<EML_1>"
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
    # assert execution_error.value.__cause__ is None

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
        capabilities = "True"
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


@dataclass
class BatchStubBackend:
    name: str
    results: Sequence[Sequence[Detection]]
    remote: bool = False
    allow_remote_processing: bool = False
    failure: Exception | None = None
    calls: int = 0
    supported: frozenset[EntityType] | None = None

    @property
    def capabilities(self) -> BackendCapabilities:
        if self.supported is not None:
            return BackendCapabilities(self.supported, remote=self.remote)
        all_ents = set()
        for res in self.results:
            for d in res:
                if hasattr(d, "entity_type"):
                    all_ents.add(d.entity_type)
        return BackendCapabilities(frozenset(all_ents or {EntityType.EMAIL}), remote=self.remote)

    def detect(self, block: ContentBlock, policy: Policy) -> Sequence[Detection]:
        raise NotImplementedError("detect should not be called when detect_batch is available")

    def detect_batch(
        self, blocks: Sequence[ContentBlock], policy: Policy
    ) -> Sequence[Sequence[Detection]]:
        self.calls += 1
        if self.failure is not None:
            raise self.failure
        return self.results


def test_invoke_backend_batch_empty() -> None:
    backend = StubBackend("stub", ())
    assert invoke_backend_batch(backend, (), Policy()) == ()


def test_invoke_backend_batch_fallback_when_detect_batch_missing() -> None:
    backend = StubBackend("stub", (_email_detection(),))
    b1 = ContentBlock("1", "maria@example.com", TextOffsetLocation(0, 17))
    b2 = ContentBlock("2", "paolo@example.com", TextOffsetLocation(0, 17))
    res = invoke_backend_batch(backend, (b1, b2), Policy())
    assert len(res) == 2
    assert backend.calls == 2
    assert res[0][0].entity_type == EntityType.EMAIL
    assert res[0][0].backend == "stub"
    assert res[1][0].entity_type == EntityType.EMAIL


def test_invoke_backend_batch_native() -> None:
    d1 = Detection(EntityType.EMAIL, 0, 17, 0.99, "d1")
    d2 = Detection(EntityType.EMAIL, 0, 17, 0.99, "d2")
    backend = BatchStubBackend("batch_stub", ((d1,), (d2,)))
    b1 = ContentBlock("1", "maria@example.com", TextOffsetLocation(0, 17))
    b2 = ContentBlock("2", "paolo@example.com", TextOffsetLocation(0, 17))
    res = invoke_backend_batch(backend, (b1, b2), Policy())
    assert len(res) == 2
    assert backend.calls == 1
    assert res[0][0].backend == "batch_stub"
    assert res[1][0].backend == "batch_stub"


def test_invoke_backend_batch_mismatch_length() -> None:
    d1 = Detection(EntityType.EMAIL, 0, 17, 0.99, "d1")
    backend = BatchStubBackend("batch_stub", ((d1,),))
    b1 = ContentBlock("1", "maria@example.com", TextOffsetLocation(0, 17))
    b2 = ContentBlock("2", "paolo@example.com", TextOffsetLocation(0, 17))
    with pytest.raises(BackendContractError, match="returned 1 results for 2 blocks"):
        invoke_backend_batch(backend, (b1, b2), Policy())


def test_invoke_backend_batch_invalid_detection() -> None:
    backend = BatchStubBackend("batch_stub", (("not-a-detection",),))  # type: ignore[arg-type]
    b1 = ContentBlock("1", "maria@example.com", TextOffsetLocation(0, 17))
    with pytest.raises(BackendContractError, match="not a Detection"):
        invoke_backend_batch(backend, (b1,), Policy())


def test_invoke_backend_batch_undeclared_entity_type() -> None:
    d = Detection(EntityType.PHONE, 0, 5, 0.9, "d")
    backend = BatchStubBackend("batch_stub", ((d,),), supported=frozenset({EntityType.EMAIL}))
    b1 = ContentBlock("1", "+1234", TextOffsetLocation(0, 5))
    with pytest.raises(BackendContractError, match="undeclared entity type"):
        invoke_backend_batch(backend, (b1,), Policy())


def test_invoke_backend_batch_bounds_error() -> None:
    d = Detection(EntityType.EMAIL, 0, 50, 0.9, "d")
    backend = BatchStubBackend("batch_stub", ((d,),))
    b1 = ContentBlock("1", "short", TextOffsetLocation(0, 5))
    with pytest.raises(InvalidDetectionError, match="offsets outside"):
        invoke_backend_batch(backend, (b1,), Policy())


def test_invoke_backend_batch_remote_policy_error() -> None:
    backend = BatchStubBackend("remote_stub", ((),), remote=True, allow_remote_processing=True)
    b1 = ContentBlock("1", "text", TextOffsetLocation(0, 4))
    with pytest.raises(NetworkPolicyError, match="denies remote processing"):
        invoke_backend_batch(backend, (b1,), Policy(network_policy=NetworkPolicy.DENY))


def test_invoke_backend_batch_failure_sanitized() -> None:
    backend = BatchStubBackend("batch_stub", ((),), failure=RuntimeError("sensitive query text"))
    b1 = ContentBlock("1", "text", TextOffsetLocation(0, 4))
    with pytest.raises(BackendExecutionError, match="failed during batch detection") as exc:
        invoke_backend_batch(backend, (b1,), Policy())
    assert "sensitive query text" not in str(exc.value)


def test_composite_backend_detect_batch() -> None:
    d1 = Detection(EntityType.EMAIL, 0, 17, 0.99, "stub1")
    d2 = Detection(EntityType.PHONE, 18, 25, 0.95, "stub2")
    b1 = StubBackend("s1", (d1,))
    b2 = StubBackend("s2", (d2,))
    composite = CompositeBackend((b1, b2))
    assert composite.detect_batch((), Policy()) == ()

    block = ContentBlock("b", "maria@example.com +123456", TextOffsetLocation(0, 25))
    res = composite.detect_batch((block,), Policy())
    assert len(res) == 1
    assert len(res[0]) == 2
    assert res[0][0].entity_type == EntityType.EMAIL
    assert res[0][1].entity_type == EntityType.PHONE
