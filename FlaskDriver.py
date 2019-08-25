# !/usr/bin/env python

"""FlaskDriver

If the description is long, the first line should be a short summary of FlaskDriver.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
from flask import Flask, render_template, url_for, redirect, request, session
from Spreadsheet import Spreadsheet
from Tokenizer import Tokenizer
import nltk

# program's author information and licenses
__author__ = "Mauricio Lomeli"
__credits__ = ["Derek Eijansantos", "Anne Wang", "Jennifer Kwon"]
__date__ = "8/15/2019"
__license__ = "MIT"
__version__ = "0.0.0.1"
__maintainer__ = "Mauricio Lomeli"
__email__ = "mjlomeli@uci.edu"
__status__ = "Prototype"


app = Flask(__name__)
app.config["DEBUG"] = True

# File variables
__HOME_HTML = 'Homepage.html'
__RESULT_HTML = 'ResultsPage.html'
__HOMEPAGE_PATH = Path.cwd() / Path('templates') / Path(__HOME_HTML)
__RESULT_PATH = Path.cwd() / Path('templates') / Path(__RESULT_HTML)

# HTML variables
__html_query = 'query'

# Python back-end variables
__python_query = 'query'
__python_insights = 'insights'


# Natural language processor
__tokenizer = Tokenizer()


@app.route("/")
@app.route("/home")
def home():
    """
    Renders the homepage. While the program is running, if a user
    enters 'localhost:5000/' into their web browser, they'll be
    rerouted to the homepage: Homepage.html
    :return:
    """
    sheet = Spreadsheet()

    # removes duplicates and empty responses
    query = [item for item in set(sheet[__python_query]) if item != '']

    # TODO: remove this when final, it is only for displaying purposes.
    query += ['Encouragement'] + ['Specific Conditions'] + ['Stage II BC']

    # returns a list(tuple) of (truncated text, full text)
    pair = list(zip(sheet.textLength(query, 50), query))

    return render_template(__HOME_HTML, pair=pair)


@app.route('/form', methods=['GET', 'POST'])
def form():
    """
    Renders the results page. While the program is running, if a user
    submits/enters a dropdown menu selection, then enters the submission.
    This function activates and sends the info stored in the 'posts' variable
    to the ResultsPage.html.
    :return:
    """
    # Gets from the HTML
    if request.method == 'POST':
        query = request.form(__html_query)
    else:
        query = request.args.get(__html_query)

    error = 'There doesn\'t exist a \'' + __html_query + '\' form in ' + __RESULT_HTML
    assert query is not None, error

    sheet = Spreadsheet()
    posts = sheet.convertToDict(sheet[query])

    if len(posts) > 0:
        query = [item for item in sheet[__python_query] if item != '']
        pair = list(zip(sheet.textLength(query, 50), query))
        return render_template("ResultsPage.html", posts=posts, pair=pair)
    else:
        return render_template(__RESULT_HTML)


@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('query', '')

    error = 'There doesn\'t exist a \'' + __html_query + '\' form in ' + __RESULT_HTML
    assert query is not None, error

    tokens = __tokenizer.keep_stop_words(query)

    # TODO: NEED a TFIDF instance here
    # posts = getStats(tokens) -> [list of the posts]
    sheet = Spreadsheet()
    posts = sheet.convertToDict(sheet[query])
    # delete line of code on top of this comment when ready


    if len(posts) > 0:
        # remove empties
        query = [item for item in sheet[__python_query] if item != '']
        pair = list(zip(sheet.textLength(query, 50), query))
        return render_template("ResultsPage.html", posts=posts, pair=pair)
    else:
        return render_template(__RESULT_HTML)


def __test_function():
    """
    Raises an error and warns you to have everything installed in the appropriate places. If you fail any,
    it will output an error message of what could had happened.
    """
    sheet = Spreadsheet()
    assert len(sheet) > 0, 'Spreadsheet size is 0 on FlaskDriver.py home function.'
    assert len(sheet[__python_query]) > 0, 'FlaskDriver.py: \'' + __python_query + '\' is not a header in Spreadsheet'
    assert __RESULT_PATH.exists(), 'You\'r missing or misspelled the ' + __RESULT_HTML + ' in the templates folder.'
    error = 'You\'r missing the ' + __HOME_HTML + ' in the templates folder. Or you misspelled it.'
    assert __HOMEPAGE_PATH.exists(), error


__test_function()

app.run()

