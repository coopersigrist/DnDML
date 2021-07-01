from flask import Flask, render_template, request, session
from markupsafe import escape
import os, math

TEMPLATE_DIR = os.path.abspath('../templates')
STATIC_DIR = os.path.abspath('../static')

# app = Flask(__name__) # to make the app run without any
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#session is a dict unique to you.


@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html", answer = "")
    elif request.method == "POST":
        answerNum = math.sqrt(int(request.form.get("name")))
        return render_template("index.html", answer = f"{answerNum:0.2f}")

if __name__ == "__main__":
    app.run(debug=True)