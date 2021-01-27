"""Test functions to fetch files."""
import os
from pathlib import Path

import pytest

from werkzeug.datastructures import FileStorage

from word_counter.src.file_utils import (
    delete_files,
    get_files,
    read_files,
    upload_files,
)


def test_get_files(child_path: Path):
    """Test that the files returned are those expected."""
    files = get_files(child_path)

    assert len(files) == 3

    assert files == [os.path.join(child_path, f"doc_{i}.txt") for i in range(3, 0, -1)]


def test_recursive_get_files(tmpdir, child_path):
    """Test that files are recursively fetched."""
    parent_files = get_files(tmpdir)
    child_files = get_files(child_path)

    assert parent_files == child_files


@pytest.mark.parametrize(
    "count, expected",
    [
        (0, "content is 3"),
        (1, "content is 2"),
        (2, "content is 1"),
    ],
)
def test_read_files(file_list, count, expected):
    """Test reading in multiple files."""
    files = read_files(file_list)
    assert files[count] == expected


def test_delete_files(child_path):
    """Tests for deleting files."""
    delete_files(child_path)
    assert len(os.listdir(child_path)) == 0


@pytest.mark.parametrize(
    "file_name, saved_name",
    [("test_name.txt", "test_name.txt"), ("../../test_name.txt", "test_name.txt")],
)
def test_upload_files(tmpdir, file_name, saved_name):
    """Tests that files are correctly saved to a directory, with a secure filename."""
    file_storage = FileStorage(name="Test Storage", filename=file_name)

    upload_files(tmpdir, [file_storage])

    files = [
        file
        for file in os.listdir(tmpdir)
        if os.path.isfile(os.path.join(tmpdir, file))
    ]

    assert files == [saved_name]
