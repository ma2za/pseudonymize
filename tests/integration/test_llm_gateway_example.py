from examples.llm_gateway import (
    sanitize_prompt,
    sanitize_retrieval,
    sanitize_tool_call,
    sanitize_tool_output,
)


def test_llm_gateway_boundaries() -> None:
    assert sanitize_prompt("Contact maria@example.com") == "Contact <EMAIL_1>"
    assert sanitize_retrieval(
        "Find maria@example.com",
        [{"id": "doc-1", "text": "Owner: maria@example.com"}],
    ) == {
        "query": "Find <EMAIL_1>",
        "documents": [{"id": "doc-1", "text": "Owner: <EMAIL_1>"}],
    }
    assert sanitize_tool_call("lookup_account", {"email": "maria@example.com", "limit": 5}) == {
        "name": "lookup_account",
        "arguments": {"email": "<EMAIL_1>", "limit": 5},
    }
    assert sanitize_tool_output(
        "lookup_account", {"email": "maria@example.com", "active": True}
    ) == {
        "name": "lookup_account",
        "output": {"email": "<EMAIL_1>", "active": True},
    }
