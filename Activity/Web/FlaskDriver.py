# !/usr/bin/env python

"""FlaskDriver

If the description is long, the first line should be a short summary of FlaskDriver.py
that makes sense on its own, separated from the rest by a newline.
"""

from Spreadsheet import Spreadsheet
from flask import Flask, render_template, redirect, request
from random import sample

# program's author information and licenses
__authors__ = ["Derek Eijansantos", "Dhruv Seth", "Mauricio Lomeli"]
__date__ = "9/3/2019"
__license__ = "MIT"
__version__ = "0.0.0.2"
__maintainer__ = ["Derek Eijansantos", "Druv Seth"]
__email__ = ["Derek & Druv enter your professional emails"]
__status__ = "Prototype"

app = Flask(__name__)
app.config["DEBUG"] = True

# Files
__HOME_HTML = 'home.html'
__RESULTS_HTML = 'results.html'
__CONTACT_HTML = 'contactus.html'
__ABOUT_HTML = 'aboutus.html'
__HISTOLOGY = ['HER2', 'HER', 'BRCA', 'ER', 'HR', 'PR', 'RP', 'RO']


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

    # Todo: need to make the HTML people chat bubbles a clickable event to link to suggestions
    others_asking = sample([query for query in sheet['query'] if query != ''], 4)

    # Gets the 2 most common and every query in the spreadsheet
    query = sheet.most_common(2)
    query += [item for item in set(sheet['query']) if item != '']

    # pairs a truncated version of the queries with the actual query
    pair = list(zip(sheet.trunc_text(query, 50), query))
    return render_template(__HOME_HTML, pair=pair)


@app.route("/form")
def results():
    # The front-end passed us their variable called query
    query = request.args.get('query')

    sheet = Spreadsheet()

    # Refine your results dropdown information
    stages = [cohort for cohort in set(sheet['cohort']) if cohort != '']
    prev_treatments = [sheet.trunc_text(profile, 20) for profile in set(sheet['profile']) if profile != '']
    posts = sheet.convertToDict(sheet[query], True)

    # The query needs to be truncated/shortened for large strings
    query = sheet.trunc_text(query, 25)
    return render_template(__RESULTS_HTML, posts=posts, title='Results', query=query,
                           stages=stages, histologies=__HISTOLOGY, prev_treatments=prev_treatments)


@app.route("/aboutus")
def about_us():
    return render_template(__ABOUT_HTML, title='About Us')


@app.route("/contactus")
def contact_us():
    return render_template(__CONTACT_HTML, title='Contact Us')


@app.route("/graph")
@app.route("/neo4j")
def graph():
    """
    Renders the homepage. While the program is running, if a user
    enters 'localhost:5000/' into their web browser, they'll be
    rerouted to the homepage: Homepage.html
    :return:
    """
    return redirect('http://localhost:7474')


def testFlaskDriver():
    """
    Raises an error and warns you to have everything installed in the appropriate places. If you fail any,
    it will output an error message of what could had happened.
    """
    from pathlib import Path
    templates = Path.cwd() / Path('templates')
    results = templates / Path(__RESULTS_HTML)
    home = templates / Path(__HOME_HTML)
    contact = templates / Path(__CONTACT_HTML)
    about = templates / Path(__ABOUT_HTML)

    pages = [results, home, contact, about]

    sheet = Spreadsheet()
    assert len(sheet) > 0, 'Spreadsheet size is 0 on FlaskDriver.py home function.'
    assert len(sheet['query']) > 0, 'FlaskDriver.py: \'' + 'query' + '\' is not a header in Spreadsheet'
    for page in pages:
        assert page.exists(), 'You\'r missing or misspelled the ' + page.name + ' in the templates folder.'


testFlaskDriver()


if __name__ == "__main__":
    app.run()
