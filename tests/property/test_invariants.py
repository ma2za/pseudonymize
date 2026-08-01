import copy

from hypothesis import given
from hypothesis import strategies as st

from pseudonymize import Pseudonymizer, pseudonymize

KEY = b"k" * 32


@given(st.from_regex(r"[A-Za-z][A-Za-z0-9]{0,20}@example\.com", fullmatch=True))
def test_determinism_namespace_isolation_and_idempotence(email: str) -> None:
    first = pseudonymize(email, mode="deterministic", key=KEY, namespace="a")
    assert first == pseudonymize(email, mode="deterministic", key=KEY, namespace="a")
    assert first != pseudonymize(email, mode="deterministic", key=KEY, namespace="b")
    assert first != pseudonymize(email, mode="deterministic", key=b"z" * 32, namespace="a")
    assert (
        Pseudonymizer().process(Pseudonymizer().process(email).text).text
        == Pseudonymizer().process(email).text
    )


@given(st.text(alphabet=st.characters(blacklist_characters="@"), max_size=200))
def test_unmatched_text_is_unchanged(text: str) -> None:
    assert Pseudonymizer().process(text).text == text


@given(st.text(max_size=500))
def test_arbitrary_unicode_is_idempotent(text: str) -> None:
    engine = Pseudonymizer()
    once = engine.process(text).text
    assert engine.process(once).text == once


JSON_DATA = st.recursive(
    st.none() | st.booleans() | st.integers() | st.floats(allow_nan=False) | st.text(max_size=50),
    lambda children: (
        st.lists(children, max_size=10)
        | st.dictionaries(st.text(max_size=20), children, max_size=10)
    ),
    max_leaves=50,
)


@given(JSON_DATA)
def test_arbitrary_nested_data_is_immutable_and_idempotent(data: object) -> None:
    original = copy.deepcopy(data)
    engine = Pseudonymizer()

    output = engine.process_data(data)

    assert data == original
    assert engine.process_data(output) == output
