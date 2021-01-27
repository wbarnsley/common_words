"""Fixtures to be used across multiple tests."""
import os

import pytest

from word_counter.views import create_app


@pytest.fixture
def app(tmpdir):
    """Yield and app with temporary upload and output folders."""
    app = create_app()
    app.config["UPLOAD_FOLDER"] = tmpdir
    app.config["OUTPUT_FOLDER"] = tmpdir
    return app


@pytest.fixture
def client(app):
    """Yeild a client for the app."""
    yield app.test_client()


@pytest.fixture
def child_path(tmpdir):
    """Yield a nested temporary directory."""
    child_path = tmpdir.mkdir("sub")
    add_txt_files(child_path)
    yield child_path


def add_txt_files(path):
    """Add .txt files to a temporary directory."""
    for name in range(1, 4):
        file_name = f"doc_{name}.txt"
        p = path.join(file_name)
        p.write(f"content is {name}")
    return path


@pytest.fixture
def file_list(child_path):
    """Return a list of files within the temporary sub directory."""
    yield [os.path.join(child_path, txt_file) for txt_file in os.listdir(child_path)]
