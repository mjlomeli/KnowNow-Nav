from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)
app.config["DEBUG"] = True

posts = [
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
    {'topic': 'Pain after almost 5 years.', 'Discussion URL': 'https://community.breastcancer.org/forum/145/topics/827291', 'Patient Insight': 'Other patients report same feeling of pain as well as tightness. As for an explanation, nerve growth was presented as a possible factor which is know to create muscle soreness.'},
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/form")
def results():
    return render_template('results.html',posts=posts, title='Results')

if __name__ == "__main__":
    app.run()