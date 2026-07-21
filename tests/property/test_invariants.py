from hypothesis import given
from hypothesis import strategies as st

from pseudonymize import Pseudonymizer, pseudonymize

KEY = b"k" * 32


@given(st.from_regex(r"[A-Za-z][A-Za-z0-9]{0,20}@example\.com", fullmatch=True))
def test_determinism_namespace_isolation_and_idempotence(email: str) -> None:
    first = pseudonymize(email, key=KEY, namespace="a")
    assert first == pseudonymize(email, key=KEY, namespace="a")
    assert first != pseudonymize(email, key=KEY, namespace="b")
    assert (
        Pseudonymizer(key=KEY).process(Pseudonymizer(key=KEY).process(email).text).text
        == Pseudonymizer(key=KEY).process(email).text
    )


@given(st.text(alphabet=st.characters(blacklist_characters="@"), max_size=200))
def test_unmatched_text_is_unchanged(text: str) -> None:
    assert Pseudonymizer(key=KEY).process(text).text == text
