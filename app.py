from flask_cors import CORS
from flask import Flask, request, jsonify
import os
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__, template_folder='templates',  static_folder='static')
CORS(app)


USERS_DIR = "backend/users"


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/append-component", methods=["GET"])
def home3():
    with open("templates/components/header/primary.html", "r") as f:
        component = f.read()

    with open("templates/users_template/hojiakbar/first/index.html", "r") as f:
        current_html = f.read()

    soup = BeautifulSoup(current_html, "html.parser")
    root_div = soup.find(id="root")
    print(root_div)

    if root_div:
        root_div.append(BeautifulSoup(component, "html.parser"))
    print(str(soup))

    with open("templates/users_template/hojiakbar/first/index.html", "w", encoding="utf-8") as file:
        file.write(str(soup))

    return jsonify({"status": "success", "message": "ok"}), 200


@app.route("/<username>/<projectname>", methods=["GET"])
def home_2(username, projectname):
    return render_template(f"users_template/{username}/{projectname}/index.html")


if __name__ == '__main__':
    os.makedirs(USERS_DIR, exist_ok=True)
    app.run(debug=True, port=5000)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
