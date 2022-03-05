from flask import Flask
import flask
import os
import requests

if not os.path.isfile("cllg/data.csv"):
    r = requests.get("https://github.com/TheRealchr1s/College4U/blob/master/cllg/data.csv?raw=true")
    with open("cllg/data.csv", 'wb') as f:
        f.write(r.content)


from cllg.cllg import get_sheet

app = Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/info", methods=["POST"])
def info_page():
    cllg_list = flask.request.form["cllg"].split("\n")
    names = get_sheet(cllg_list)
    return flask.render_template("info.html", cllgnames=names)

@app.route("/dl")
def dl():
    return flask.send_file("cllg/colleges.xlsx")