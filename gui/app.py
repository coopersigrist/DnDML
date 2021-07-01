from flask import Flask, render_template, request, session
from flask_session import Session
from markupsafe import escape
import os
import math

TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        if session.get('backgroundColor') != None:
            return render_template("index.html", backgroundColor = session['backgroundColor'])
        else:
            return render_template("index.html", backgroundColor = "steelblue")
    elif request.method == "POST":
        session['backgroundColor'] = request.form.get("colorOptions")
        return render_template("index.html", backgroundColor = session['backgroundColor'])

@app.route("/math", methods = ["GET", "POST"])
def calcSqrt():
    if request.method == "GET":
        if session.get('backgroundColor') != None:
            return render_template("index.html", backgroundColor = session['backgroundColor'])
        else:
            return render_template("index.html", backgroundColor = "steelblue")
    elif request.method == "POST":
        answerNum = math.sqrt(int(request.form.get("name")))
        return render_template("index.html", answer = f"{answerNum:10.2f}", backgroundColor = session['backgroundColor'])


if __name__ == "__main__":
    app.run(debug=True)