from pseudonymize import Pseudonymizer, TransformationMode


def test_session_round_trip_text() -> None:
    engine = Pseudonymizer(mode=TransformationMode.NUMBERED)
    session = engine.session()

    prompt = "Tell bob@example.com that Alice will arrive at 5 PM."
    safe_prompt = session.forward(prompt)
    assert safe_prompt == "Tell <EMAIL_1> that Alice will arrive at 5 PM."

    # Fake LLM response that references the alias
    llm_response = "I have sent an email to <EMAIL_1> about Alice's arrival."
    restored = session.restore(llm_response)
    assert restored == "I have sent an email to bob@example.com about Alice's arrival."


def test_session_round_trip_structured() -> None:
    engine = Pseudonymizer(mode=TransformationMode.NUMBERED)
    session = engine.session()

    prompt_data = [{"role": "user", "content": "My name is John, contact me at john@example.com."}]
    safe_data = session.forward(prompt_data)
    assert isinstance(safe_data, list)
    assert safe_data[0]["content"] == "My name is John, contact me at <EMAIL_1>."

    llm_response = "Hello! I will send an update to <EMAIL_1>."
    restored = session.restore(llm_response)
    assert restored == "Hello! I will send an update to john@example.com."


def test_session_restore_streaming() -> None:
    engine = Pseudonymizer(mode=TransformationMode.NUMBERED)
    session = engine.session()

    prompt = "Alert alice@example.com immediately."
    session.forward(prompt)  # Memorize mapping

    # Simulate LLM response stream where the alias '<EMAIL_1>' is split across chunks
    chunks = ["Sending alert to <EMA", "IL_1> right", " now."]

    restored = ""
    for chunk in chunks:
        restored += session.restore(chunk)
    restored += session.flush()

    assert restored == "Sending alert to alice@example.com right now."
