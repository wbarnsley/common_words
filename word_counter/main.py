"""Main script to run the analysis of documents.

The following steps are completed in order to analysis the documents;  fetch the files_names form the provided file
 path, read the files in into a list, clean the text and then process the data to fetch the most common words and the
 documents  and sentences they appear in.

The current cleaning pipeline is as follows; turn to lower case, remove punctuation, tokenise text and remove the
 stopwords. Any additional stopwords can be included using the environment variable stopwords. Stopwords as an env var
 should be a comma separated string of the words to be add


"""
import os

from word_counter.src.file_utils import get_files, read_files
from word_counter.src.text_cleaning import clean_documents
from word_counter.src.text_counting import (
    find_common_in_documents,
    get_common_items,
    get_corpus,
)

if __name__ == "__main__":
    # set in env vars file location, additional stopwrods, 10 the number of key words
    file_location = os.getenv("file_path", "resources/test_docs")
    additional_stopwords = os.getenv("stopwords", ["us"])
    common_limit = os.getenv("common_limit", 10)

    file_paths = get_files(file_location)
    print(file_paths)
    documents = read_files(file_paths)

    # add this as an env variable
    clean_documents = clean_documents(documents, additional_stopwords)

    corpus = get_corpus(clean_documents)
    commonn_words = get_common_items(corpus, common_limit)
    df = find_common_in_documents(commonn_words, documents, file_paths)
