from flask import Flask, render_template, request, session
from flask_session import Session
from markupsafe import escape
#from classes import workspace
import os
import math

TEMPLATE_DIR = os.path.abspath('gui/templates')
STATIC_DIR = os.path.abspath('gui/static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

class Element:
    def __init__(self):
        self.type = ''
        self.kernelSize = ''
        self.stride = ''
        self.channels = ''

    def changeParameters(self, args: dict):
        for key, value in args.items():
            if key == 'type':
                self.type = value
            elif key == 'kernelSize':
                self.kernelSize = value
            elif key == 'stride':
                self.stride = value
            elif key == 'channels':
                self.channels = value

class ElementManager:
    storage = {}

    @staticmethod
    def addNew(ID):
        ElementManager.storage[ID] = Element()

    @staticmethod
    def change(json):
        ElementManager.storage[json["id"]].changeParameters(json)

graph = []

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        requestType = request.headers.get("Action-Type", default = None)
        print(requestType)
        print(request.get_json())
        if requestType == 'elementCreate':
           ElementManager.addNew(request.get_json()["id"])
        elif requestType == 'elementChange':
            ElementManager.change(request.get_json())
        elif requestType == "graph":
            graph = request.get_json()

        return 'OK', 200
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)