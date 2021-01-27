"""Functions for counting, and fetching common words, and helper functions for this."""
from collections import Counter
from typing import Any, Dict, List

from nltk.tokenize import sent_tokenize

import pandas as pd


def get_common_items(list_to_count: List[Any], top_n: int) -> Dict[Any, int]:
    """Get the n most common items in descending order in a list of items.

    Args:
        text (List[Any]): List of items to be counted.
        top_n (int): This sets the limit for how many of the common items to return.

    Returns:
        Dict[str, int]: Dictionary with keys given by the item, and the value being count of the item in the list.

    """
    counts = Counter(list_to_count)
    return {item: count for item, count in Counter(counts).most_common(top_n)}


def get_corpus(documents: List[List[str]]) -> List[str]:
    """Get a list of all of the words in each document (includes duplicates).

    Args:
        documents (List[List[str]]): List where each element is a list of tokens in a given document.

    Returns:
        List[str]: List of all of the tokens appearing in each document,

    """
    return [word for document in documents for word in document]


def get_sentences_with_word(document: str, word: str) -> List[str]:
    """Get a list of all of the sentences in a document which contain the specified word.

    Args:
        document (str): Document to fetch sentecnes from
        word (str): Word to be looked for.

    Returns:
        List[str]: List where each item is a sentence from the document containing the input word.

    """
    sentences = sent_tokenize(document)
    return [sentence for sentence in sentences if word in sentence]


def find_common_in_documents(
    cmn_word_dict: Dict[str, int], documents: List[str], document_names: List[str]
) -> pd.DataFrame:
    """Find the sentences and documents which contain each of the common words.

    Args:
        cmn_word_dict (Dict[str, int]): Dictionary with key:value pairs given by common word:common word counts.
        documents (List[str]): List of raw documents.
        document_names (List[str]): List of document names.

    Returns:
        pd.DataFrame: Dataframe with columns detailing; the word, counts across the corpus, the documents it
        appears in, and sentences it appears in.

    """
    word_list, count_list, all_documents, all_sentences = [], [], [], []
    for word, count in cmn_word_dict.items():
        word_list.append(word)
        count_list.append(count)
        document_list, sentence_list = [], []
        for document, document_name in zip(documents, document_names):
            document = document.lower()
            if word in document:
                document_list.append(document_name)
                sentence_list += get_sentences_with_word(document, word)

        all_documents.append(document_list)
        all_sentences.append(sentence_list)

    return pd.DataFrame(
        data={
            "word": word_list,
            "count": count_list,
            "documents": all_documents,
            "sentences": all_sentences,
        }
    )
