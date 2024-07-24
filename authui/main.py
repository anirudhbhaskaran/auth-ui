from flask import Flask, render_template, request

from authui.dbutils import authdb

app = Flask(__name__)


@app.route("/")
def render_ui():
    auth_list = authdb.AuthDb()._get_all_auths()
    return render_template("index.html", auth_list=auth_list)


@app.route("/createNewAuth")
def create_new_auth():
    authdb.AuthDb()._insert_new_auth()
    return {}


@app.route("/deleteAuth")
def delete_auth():
    data = request.args.get('clientId')
    print(data)
    authdb.AuthDb()._delete_auth(data)
    return {}


def run():
    app.run(debug=True)
