"""Tests for text cleaning functions."""
from nltk.corpus import stopwords

import pytest

from word_counter.src.text_cleaning import (
    clean_documents,
    format_additional_stopwords,
    get_stopwords,
    lower_text,
    remove_punctuation,
    remove_stopwords,
    tokenise_text,
)


@pytest.mark.parametrize(
    "additional_words, expected",
    [
        (["one", "two"], stopwords.words() + ["one", "two"] + ["us"]),
        ([], stopwords.words() + ["us"]),
        ([1, 2], stopwords.words() + [1, 2] + ["us"]),
    ],
)
def test_adding_stopwords(additional_words, expected):
    """Test that stopwords can be extended as expected."""
    stop_words = get_stopwords()
    assert stop_words == stopwords.words() + ["us"]
    #
    stop_words = get_stopwords(additional_words)

    assert stop_words == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("one, two", ["one", ",", "two"]),
        ("test. test.", ["test", ".", "test", "."]),
        ("", []),
        ("I'm a test", ["I", "'m", "a", "test"]),
    ],
)
def test_cleaner_tokenise(text, expected):
    """Test text is tokenised as expected."""
    assert tokenise_text(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("TEST test", "test test"),
        ("test test", "test test"),
    ],
)
def test_cleaner_lower(text, expected):
    """Test text is lowercased as expected."""
    assert lower_text(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [("test test", "test test"), ("! , I've", "  Ive"), (",>/?!", "")],
)
def test_remove_punctuation(text, expected):
    """Test punctuation is correctly stripped."""
    assert remove_punctuation(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        (["test", "the"], ["test"]),
        (["the", "the"], []),
        (["i", "a", "the"], []),
    ],
)
def test_remove_stopwords(text, expected):
    """Test stop words are correctly stripped from a list of strings."""
    assert remove_stopwords(text, stopwords.words()) == expected


@pytest.mark.parametrize(
    "documents, expected",
    [
        (["Hi, this IS A TEST case!!"], [["hi", "test", "case"]]),
        ([], []),
    ],
)
def test_clean_documents(documents, expected):
    """Test documents are correctly cleaned."""
    assert clean_documents(documents) == expected


@pytest.mark.parametrize(
    "stopwords, expected",
    [
        ("perfect, input", ["perfect", "input"]),
        ("no,spaces,input", ["no", "spaces", "input"]),
        ("ALLCAPS,    input", ["allcaps", "input"]),
        ("PUNCT!!!!, test?!'", ["punct", "test"]),
    ],
)
def test_format_additional_stopwords(stopwords, expected):
    """Test the formatting of input stopwords by user."""
    assert format_additional_stopwords(stopwords) == expected
