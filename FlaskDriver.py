# !/usr/bin/env python

"""FlaskDriver

If the description is long, the first line should be a short summary of FlaskDriver.py
that makes sense on its own, separated from the rest by a newline.
"""

from pathlib import Path
from flask import Flask, render_template, url_for, redirect, request, session
from Spreadsheet import Spreadsheet

PATH = Path.cwd()

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
    assert len(sheet) > 0, 'Spreadsheet size is 0 on FlaskDriver.py home function.'

    # removes duplicates and empty responses
    query = [item for item in set(sheet['query']) if item != '']
    assert len(sheet['query']) > 0, 'Need to change header name call in FlaskDriver.py home function'

    # remove this when final, it is only for displaying purposes.
    query += ['Encouragement'] + ['Specific Conditions'] + ['Stage II BC']

    # returns a list(tuple) of (truncated text, full text)
    pair = list(zip(sheet.textLength(query, 50), query))

    return render_template("Homepage.html", pair=pair)


@app.route('/form', methods=['GET', 'POST'])
def form():
    """
    Renders the results page. While the program is running, if a user
    submits/enters a dropdown menu selection, then enters the submission.
    This function activates and sends the info stored in the 'posts' variable
    to the ResultsPage.html.
    :return:
    """
    if request.method == 'POST':
        query = request.form('query')
    else:
        query = request.args.get('query')

    if query is None:
        print("You changed the name of the select list! Change it back to query.")

    sheet = Spreadsheet()
    posts = sheet.convertToDict(sheet[query])

    if len(posts) > 0:
        query = [item for item in sheet['query'] if item != '']
        pair = list(zip(sheet.textLength(query, 50), query))
        return render_template("ResultsPage.html", posts=posts, pair=pair)
    else:
        return render_template("ResultsPage.html")


app.run()


