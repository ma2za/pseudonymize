from collections.abc import AsyncIterator

import pytest

from pseudonymize import Pseudonymizer, TransformationMode


def test_process_stream_synchronous() -> None:
    engine = Pseudonymizer(mode=TransformationMode.NUMBERED)

    chunks = [
        "Hello! My em",
        "ail is pao",
        "lo@example.com.",
        " Please write back to pao",
        "lo@example.com when you have",
        " time.",
    ]

    result = "".join(engine.process_stream(chunks))

    assert (
        result == "Hello! My email is <EMAIL_1>. Please write back to <EMAIL_1> when you have time."
    )


@pytest.mark.asyncio
async def test_process_stream_asynchronous() -> None:
    engine = Pseudonymizer(mode=TransformationMode.NUMBERED)

    async def async_chunks() -> AsyncIterator[str]:
        chunks = [
            "Hello! My em",
            "ail is pao",
            "lo@example.com.",
            " Please write back to pao",
            "lo@example.com when you have",
            " time.",
        ]
        for c in chunks:
            yield c

    result = ""
    async for processed in engine.process_stream_async(async_chunks()):
        result += processed

    assert (
        result == "Hello! My email is <EMAIL_1>. Please write back to <EMAIL_1> when you have time."
    )


def test_stream_context_overlap() -> None:
    engine = Pseudonymizer(mode=TransformationMode.NUMBERED)

    # "Passport No: " provides context. ABC12345 alone might not trigger without context.
    chunks = ["My info is Passport No: ", "ABC12", "345. Thanks!"]

    result = "".join(engine.process_stream(chunks))
    # It might be <NATIONAL_ID_1> or another ID.
    assert "<" in result and ">" in result


def test_stream_long_chunk() -> None:
    engine = Pseudonymizer()

    chunks = ["A" * 5000 + " paolo@example.com " + "B" * 5000]
    result = "".join(engine.process_stream(chunks))
    assert "<EMAIL_1>" in result
    assert len(result) > 9000


def test_stream_tiny_chunks() -> None:
    engine = Pseudonymizer(mode=TransformationMode.NUMBERED)
    text = "My email is tiny@example.com."
    chunks = list(text)

    result = "".join(engine.process_stream(chunks))
    assert result == "My email is <EMAIL_1>."


def test_stream_empty_chunks() -> None:
    engine = Pseudonymizer(mode=TransformationMode.NUMBERED)
    chunks = ["", "Hello ", "", "empty@example.com", ""]

    result = "".join(engine.process_stream(chunks))
    assert result == "Hello <EMAIL_1>"
def test_detection_stream() -> None:
    engine = Pseudonymizer(mode=TransformationMode.NUMBERED)
    stream = engine.stream()
    
    chunks = [
        "Hello! My em",
        "ail is pao",
        "lo@example.com.",
        " Please write back to pao",
        "lo@example.com when you have",
        " time.",
    ]
    
    result = ""
    for c in chunks:
        result += stream.feed(c)
    result += stream.flush()
    
    assert result == "Hello! My email is <EMAIL_1>. Please write back to <EMAIL_1> when you have time."
