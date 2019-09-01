from flask import Flask, render_template, redirect, request
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
    pair = None

    return render_template('home.html', pair=pair)


@app.route("/form")
def results():

    query = None
    return render_template('results.html', posts=posts, title='Results', query=query)


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
