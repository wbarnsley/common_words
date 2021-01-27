FROM python:3.8-slim

# Copy resources over and download the stopwords.
COPY resources /resources/
RUN pip install -r /resources/requirements.txt
RUN python -c "import nltk;nltk.download('punkt');nltk.download('stopwords')"

# Make output dir and copy ove app.
RUN mkdir -p output
RUN mkdir -p word_counter/static/uploads
COPY word_counter word_counter

# Set env for flask run and then run.
ENV FLASK_APP word_counter
CMD ["flask", "run", "--host=0.0.0.0"]