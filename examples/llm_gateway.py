from typing import cast

from pseudonymize import Policy, Pseudonymizer


def _require(condition: bool) -> None:
    if not condition:
        raise RuntimeError("LLM gateway example failed")


def sanitize_prompt(prompt: str) -> str:
    return Pseudonymizer().process(prompt).text


def sanitize_retrieval(query: str, documents: list[dict[str, str]]) -> dict[str, object]:
    payload = {"query": query, "documents": documents}
    return cast(dict[str, object], Pseudonymizer(policy=Policy.llm()).process_data(payload))


def sanitize_tool_call(name: str, arguments: dict[str, object]) -> dict[str, object]:
    payload = {"name": name, "arguments": arguments}
    return cast(dict[str, object], Pseudonymizer(policy=Policy.llm()).process_data(payload))


def sanitize_tool_output(name: str, output: object) -> dict[str, object]:
    payload = {"name": name, "output": output}
    return cast(dict[str, object], Pseudonymizer(policy=Policy.llm()).process_data(payload))


def main() -> None:
    prompt = sanitize_prompt("Contact maria@example.com")
    retrieval = sanitize_retrieval(
        "Find maria@example.com",
        [{"id": "doc-1", "text": "Owner: maria@example.com"}],
    )
    tool_call = sanitize_tool_call(
        "lookup_account",
        {"email": "maria@example.com", "limit": 5},
    )
    tool_output = sanitize_tool_output(
        "lookup_account",
        {"email": "maria@example.com", "active": True},
    )

    _require(prompt == "Contact <EMAIL_1>")
    _require(retrieval["query"] == "Find <EMAIL_1>")
    _require(retrieval["documents"][0]["text"] == "Owner: <EMAIL_1>")  # type: ignore[index]
    _require(tool_call["arguments"]["email"] == "<EMAIL_1>")  # type: ignore[index]
    _require(tool_output["output"]["email"] == "<EMAIL_1>")  # type: ignore[index]


if __name__ == "__main__":
    main()
