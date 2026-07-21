from dataclasses import dataclass
from typing import cast

import pytest

from pseudonymize import Policy, Pseudonymizer
from pseudonymize.engine import Data
from pseudonymize.exceptions import UnsupportedDataError

KEY = b"k" * 32


def test_process_replaces_right_to_left_and_reports_output_offsets() -> None:
    result = Pseudonymizer(key=KEY).process("maria@example.com then 192.168.1.1")
    assert "maria@example.com" not in result.text
    assert "192.168.1.1" not in result.text
    assert tuple(
        result.text[item.output_start : item.output_end] for item in result.replacements
    ) == tuple(item.token for item in result.replacements)
    assert all(not hasattr(item.detection, "value") for item in result.replacements)


def test_process_is_idempotent() -> None:
    engine = Pseudonymizer(key=KEY)
    once = engine.process("maria@example.com").text
    assert engine.process(once).text == once
    assert tuple(result.text for result in engine.process_batch(["maria@example.com", once])) == (
        once,
        once,
    )


def test_nested_data_preserves_structure_and_primitives() -> None:
    engine = Pseudonymizer(key=KEY, policy=Policy.llm())
    payload = {
        "messages": [{"role": "user", "content": "maria@example.com"}],
        "temperature": 0.2,
        "flags": (True, None),
    }
    output = engine.process_data(payload)
    assert isinstance(output, dict)
    messages = cast(list[Data], output["messages"])
    first_message = cast(dict[str, Data], messages[0])
    assert first_message["content"] != "maria@example.com"
    assert output["temperature"] == 0.2
    assert output["flags"] == (True, None)


def test_nested_path_policy() -> None:
    policy = Policy.llm(include_paths=["messages.*.content"])
    output = Pseudonymizer(key=KEY, policy=policy).process_data(
        {"messages": [{"content": "maria@example.com"}], "metadata": "maria@example.com"}
    )
    assert isinstance(output, dict)
    assert output["metadata"] == "maria@example.com"
    assert output["messages"] != [{"content": "maria@example.com"}]


@dataclass
class Custom:
    value: str


def test_custom_serializer_and_unsupported_values() -> None:
    engine = Pseudonymizer(key=KEY)
    with pytest.raises(UnsupportedDataError):
        engine.process_data(Custom("maria@example.com"))
    output = engine.process_data(Custom("maria@example.com"), serializer=lambda item: item.__dict__)
    assert isinstance(output, dict)
    assert output["value"] != "maria@example.com"
    with pytest.raises(UnsupportedDataError, match="keys"):
        engine.process_data({1: "maria@example.com"})
