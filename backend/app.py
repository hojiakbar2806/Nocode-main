import os
from flask import Flask

app = Flask(__name__)

USERS = "backend/users"


@app.route("/<username>/<projectname>", method=["POST"])
def create(username, projectname):

    print(projectname)
    return "<p>Hello, World!</p>"


@app.route("/<username>", method=["GET"])
def get_projects(username, projectname):

    print(projectname)
    return "<p>Hello, World!</p>"


@app.route("/<username>/<projectname>", method=["GET"])
def get_projects(username, projectname):

    print(projectname)
    return "<p>Hello, World!</p>"



if __name__ == '__main__':
    os.makedirs(USERS, exist_ok=True)
    app.run(debug=True, port=5000)
