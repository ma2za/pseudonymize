import pytest
from pseudonymize import Pseudonymizer, TransformationMode


def test_scope_process_stream_synchronous() -> None:
    engine = Pseudonymizer(mode=TransformationMode.NUMBERED)
    scope = engine.new_scope()
    chunks = ["Hello! My em", "ail is pao", "lo@example.com."]
    result = "".join(scope.process_stream(chunks))
    assert result == "Hello! My email is <EMAIL_1>."


@pytest.mark.asyncio
async def test_scope_process_stream_asynchronous() -> None:
    engine = Pseudonymizer(mode=TransformationMode.NUMBERED)
    scope = engine.new_scope()

    async def async_chunks():
        for c in ["Hello! My em", "ail is pao", "lo@example.com."]:
            yield c

    result = ""
    async for processed in scope.process_stream_async(async_chunks()):
        result += processed
    assert result == "Hello! My email is <EMAIL_1>."
