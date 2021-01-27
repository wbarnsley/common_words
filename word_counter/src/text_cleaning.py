"""Functions to clean text."""

import string
from typing import List, Optional

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def tokenise_text(text: str) -> List[str]:
    """Tokenise a string into words.

    Args:
        text (str): Text to be tokenised.

    Returns:
        List[str]: Tokenised text.

    """
    return word_tokenize(text)


def lower_text(text: str) -> str:
    """Lower case all of the uppercase characters in a string.

    Args:
        text (str): String to be lowered.

    Returns:
        str: string with no uppercase characters.
    """
    return text.lower()


def remove_punctuation(text: str) -> str:
    """Remove punctuation characters from a string.

    Args:
        text (str): String containing punctuation to be removed.

    Returns:
        str: String with all punctuation removed.

    """
    return text.translate(str.maketrans("", "", string.punctuation))


def get_stopwords(additional_stopwords: Optional[List[str]] = None) -> List[str]:
    """Get the stopwords to be removed, where any optional are added to the set.

    Args:
        additional_stopwords (Optional[List[str]]): The additional stopwords to add to the set if not None.

    Returns:
        List[str]: List of stopwords to remove.

    """
    stop_words = stopwords.words()
    if additional_stopwords is not None:
        stop_words += additional_stopwords
    return stop_words + ["us"]


def remove_stopwords(text: List[str], stopwords: List[str]) -> List[str]:
    """Remove any word in text which appears in the list of stopwords.

    Args:
        text (List[str]): List of tokens.
        stopwords (List[str]): List of words to be removed.

    Returns:
        List[str]: Text with stop words removed.

    """
    return [word for word in text if word not in stopwords]


def clean_documents(
    files: List[str], additional_stopwords: Optional[List[str]] = None
) -> List[List[str]]:
    """Clean each document in the list of documents, additional stopwords can be added.

    A document is cleaned by (in order); converting all characters to lowercase, remove stopwords, tokenise text to
    words, and removing stopwords. NLTK's standard set of stopwords can be extended using additional_stopwords.

    Args:
        files List[str]: List of files to be cleaned.
        additional_stopwords List[str]: Words to be added to the standard set, if not none.

    Returns:
        List[List[str]]: List of documents which have been cleaned and tokenised.

    """
    clean_txt = []
    stopwords = get_stopwords(additional_stopwords)

    for file in files:
        lowered = lower_text(file)
        cleaned = remove_punctuation(lowered)
        tokens = tokenise_text(cleaned)
        cleaned = remove_stopwords(tokens, stopwords)
        clean_txt.append(cleaned)
    return clean_txt


def format_additional_stopwords(stopwords: str) -> List[str]:
    """Take the additional stopwords input by the user and return the correct the format.

    Args:
        stopwords (str): Additional stopwords input by the user. Extra precaution taken in case user error occurs.

    Returns:
        List[str]: The additional stopwords input by the user in the correct format.

    """
    stopwords = stopwords.replace(",", ", ")
    lowered = lower_text(stopwords)
    cleaned = remove_punctuation(lowered)
    stop_tokens = tokenise_text(cleaned)
    return stop_tokens
