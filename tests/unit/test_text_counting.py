"""Test for functions which count, and fetch common words, and helper functions for this."""
import pandas as pd

import pytest

from word_counter.src.text_counting import (
    find_common_in_documents,
    get_common_items,
    get_corpus,
    get_sentences_with_word,
)


@pytest.mark.parametrize(
    "list_to_count, top_n, expected",
    [
        ([1, 2, 3, 4, 1, 1], 1, {1: 3}),
        ([1, 2, 4, 4, 1, 1], 2, {1: 3, 4: 2}),
        (["hi", "hi", "hi", 1, 1, "test"], 3, {"hi": 3, 1: 2, "test": 1}),
    ],
)
def test_get_common_items(list_to_count, top_n, expected):
    """Test that n most common items are returned as expected."""
    assert get_common_items(list_to_count, top_n) == expected


@pytest.mark.parametrize(
    "documents, expected",
    [
        (
            [
                ["document"],
                ["document_2"],
                ["document_3"],
            ],
            ["document", "document_2", "document_3"],
        ),
        (
            [["document", "document"], ["document_2", "document_2"], ["document_3"]],
            ["document", "document", "document_2", "document_2", "document_3"],
        ),
    ],
)
def test_get_corpus(documents, expected):
    """Test a corpus is correctly constructed from a list of strings."""
    assert get_corpus(documents) == expected


@pytest.mark.parametrize(
    "document, word, expected",
    [
        ("test sentence. test. sentence.", "test", ["test sentence.", "test."]),
        ("test sentence. test. sentence.", "python", []),
    ],
)
def test_get_sentences_with_word(document, word, expected):
    """Test that sentences containing a given word are correctly returned."""
    assert get_sentences_with_word(document, word) == expected


@pytest.mark.parametrize("column", [("word"), ("count"), ("documents"), ("sentences")])
def test_find_common_in_documents(column):
    """Test that the sentences and words with the common words are correctly returned."""
    cmn_word_dict = {"common": 2, "rare": 1}
    documents = [
        "This is the first common document.",
        "This is the second common document.",
        "This is the third rare document.",
    ]
    document_names = ["document 1", "document 2", "document 3"]

    expected_df = pd.DataFrame(
        data={
            "word": ["common", "rare"],
            "count": [2, 1],
            "documents": [
                [
                    "document 1",
                    "document 2",
                ],
                ["document 3"],
            ],
            "sentences": [
                [
                    "this is the first common document.",
                    "this is the second common document.",
                ],
                ["this is the third rare document."],
            ],
        }
    )

    df = find_common_in_documents(cmn_word_dict, documents, document_names)

    assert df[column].to_list() == expected_df[column].to_list()
