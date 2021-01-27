"""Functions to handle interactions with files."""

import os
from pathlib import Path
from typing import List, Union

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


def get_files(directory: Union[Path, str], file_type: str = "txt") -> List[str]:
    """Get all file paths ending with the given suffix from a given directory.

    Args:
        directory (Union[Path, str]): Directory to recursively search.
        file_type (str): Suffix indicating the type of file to fetch.

    Returns:
        List[str]: List of file paths.

    """
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(file_type):
                file_list.append(os.path.join(root, file))

    return file_list


def delete_files(directory: Union[Path, str], file_type: str = "txt") -> None:
    """Delete all file paths ending with the given suffix from a given directory.

    Args:
        directory (Union[Path, str]): Directory to recursively search.
        file_type (str): Suffix indicating the type of file to delete.

    Returns:
        None

    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(file_type):
                os.remove(os.path.join(root, file))


def read_files(file_paths: List[str]) -> List[str]:
    """Read all of the files in the list of files provided, returning a list of strings.

    Args:
        file_paths List[str]: List of files to be read.

    Returns:
        List[str]: List of documents as strings.

    """
    documents = []
    for file in file_paths:
        with open(file, "r") as f:
            documents.append(f.read())
    return documents


def upload_files(directory: str, files: List[FileStorage]) -> None:
    """Upload files using the secure filename request to a directory.

    Args:
        directory (str): String path to the upload folder
        files (List[FileStorage]): List of files to uploads

    Returns:
        None

    """
    for file in files:
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(directory, filename))
