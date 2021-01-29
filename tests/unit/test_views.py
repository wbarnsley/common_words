"""Test accessing main landing site of the app."""
import io
import os


def test_get_indexa(app, client):
    """Test get request to app."""
    res = client.get("/")
    assert res.status_code == 200


def test_post_index(app, client):
    """Test post request to app."""
    file_name = "fake-text-stream.txt"
    data = {
        "file": [(io.BytesIO(b"some initial text data"), file_name)],
        "stopwords": None,
        "set_n": "5",
    }

    response = client.post("/", data=data)

    assert response.status_code == 200

    assert len(os.listdir(app.config["OUTPUT_FOLDER"])) == 1
