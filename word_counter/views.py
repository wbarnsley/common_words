"""View to navigate flask app."""
import os

from flask import Flask, make_response, render_template, request

from word_counter.src.file_utils import (
    delete_files,
    get_files,
    read_files,
    upload_files,
)
from word_counter.src.text_cleaning import clean_documents, format_additional_stopwords
from word_counter.src.text_counting import (
    find_common_in_documents,
    get_common_items,
    get_corpus,
)


def create_app():
    """Create a flask app, add the config and routes and then return app.

    Returns:
        (Flask): App with config added and routes.

    """
    app = Flask(__name__)

    app.config["UPLOAD_FOLDER"] = "word_counter/static/uploads/"
    app.config["OUTPUT_FOLDER"] = "output/"

    @app.route("/", methods=["GET", "POST"])
    def process_files():
        """Main method for flask app. If the method is post, save the files and process..

        Save each file to an upload folder inside the static dir. Fetch string paths and read to documents. Next clean
        the documents, before processing. Processing return the most common words across all documents, the counts of
        those words, and then the documents and sentences they appear in.

        """
        if request.method == "POST":

            upload_files(
                directory=app.config["UPLOAD_FOLDER"],
                files=request.files.getlist("file"),
            )
            additional_stopwords = format_additional_stopwords(
                request.form["stopwords"]
            )
            common_limit = int(request.form["set_n"])

            file_paths = get_files(app.config["UPLOAD_FOLDER"])
            documents = read_files(file_paths)

            cleaned_documents = clean_documents(documents, additional_stopwords)
            corpus = get_corpus(cleaned_documents)
            file_paths = [
                file.split("/")[-1].replace(".txt", "") for file in file_paths
            ]

            commonn_words = get_common_items(corpus, common_limit)
            df = find_common_in_documents(commonn_words, documents, file_paths)

            output_name = os.path.join(app.config["OUTPUT_FOLDER"], "common_words.csv")

            df.to_csv(output_name, index=False)

            print("aa")

            delete_files(app.config["UPLOAD_FOLDER"])

            return make_response(
                render_template(
                    "output.html",
                    tables=[df.to_html(classes="data", index=False)],
                    titles=df.columns.values,
                ),
                200,
            )

        else:
            return make_response(render_template("index.html"), 200)

    return app
