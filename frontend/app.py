from flask import Flask, render_template, url_for, redirect, request
from Cell import convert_to_cells
from Spreadsheet import Spreadsheet
app = Flask(__name__)
app.config["DEBUG"] = True

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
    sheet = Spreadsheet()

    # removes duplicates and empty responses
    query = [item for item in set(sheet[__python_query]) if item != '']

    # TODO: remove this when final, it is only for displaying purposes.
    query += ['Encouragement'] + ['Specific Conditions'] + ['Stage II BC']

    # returns a list(tuple) of (truncated text, full text)
    pair = list(zip(sheet.textLength(query, 50), query))

    return render_template(__HOME_HTML, pair=pair)
    return render_template('home.html')

@app.route("/form")
def results():
    query = request.args.get('query')
    return render_template('results.html',posts=posts, title='Results', query=query)

@app.route("/aboutus")
def about_us():
    return render_template('aboutus.html', title='About Us')

@app.route("/contactus")
def contact_us():
    return render_template('contactus.html', title='Contact Us')

if __name__ == "__main__":
    app.run()