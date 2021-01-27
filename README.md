# Most Common Words

Containerise Flask app to extract the most common words from multiple uploaded .txt files.

### Starting the App
First you must build and run the docker container with the following commands

```
docker build  -t app:latest .
docker run --rm -p 5000:5000 -v $(pwd):/output app
```
If you then go http://localhost:5000/ you will see the sanding site to upload files.
Changing the Top N paramtes controls the number of common words returned, and additional 
stopwords can be added. These stopwords should be comma-separated, although the app has 
methods to ensure the correct format.

### Output
When you click submit you will be taken to an output site displaying the results, similarly a csv will be
saved to the directory where the app is run from.

### Testing Suite
In order to run the test suite, which include pytest, bandit and flake8 simply install tox and run it as per the below 
commands.
```
pip install tox
tox
```
