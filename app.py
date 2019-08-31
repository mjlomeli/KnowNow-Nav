from flask import Flask, render_template, redirect, request
from Activity.FileManager.Spreadsheet import Spreadsheet
app = Flask(__name__)
app.config["DEBUG"] = True

# HTML variables
__html_query = 'query'

# Python back-end variables
__python_query = 'query'
__python_insights = 'insights'
_conversion = False

posts = [
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://google.com', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
]


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

    return render_template('home.html', pair=pair)


@app.route("/form")
def results():
    # Gets from the HTML
    if request.method == 'POST':
        query = request.form(__html_query)
    else:
        query = request.args.get(__html_query)

    error = 'There doesn\'t exist a \'' + __html_query + '\' form in ' + "results.html"
    assert query is not None, error

    sheet = Spreadsheet()
    posts = sheet.convertToDict(sheet[query])

    if len(posts) > 0:
        query = [item for item in sheet[__python_query] if item != '']
        pair = list(zip(sheet.textLength(query, 50), query))
        return render_template("results.html", posts=posts, title='Results', query=pair)
    else:
        return render_template('results.html')

    return render_template('results.html',posts=posts, title='Results', query=query)


@app.route("/aboutus")
def about_us():
    return render_template('aboutus.html', title='About Us')


@app.route("/contactus")
def contact_us():
    return render_template('contactus.html', title='Contact Us')


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


if __name__ == "__main__":
    app.run()