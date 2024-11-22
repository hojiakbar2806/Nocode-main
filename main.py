import json
from flask import Flask, request, jsonify, session
import os
from bs4 import BeautifulSoup
from flask import Flask, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, render_template, redirect, url_for, flash, abort


app = Flask(__name__, template_folder='templates',  static_folder='static')
app.secret_key = "0d5b096deee48ee17e845c44a853784b77f2daf5ba8bb21e24842cb01e6a50c4"
USERS_FOLDER = "templates/users_template"


def auth_user():
    if "username" not in session:
        return redirect(url_for('login'))
    if not os.path.exists(f"{USERS_FOLDER}/{session['username']}"):
        return redirect(url_for('register'))


@app.route('/')
def home():
    redirect_response = auth_user()
    if redirect_response:
        return redirect_response
    path = f"{USERS_FOLDER}/{session['username']}"
    folders = [f for f in os.listdir(path) if os.path.isdir(f"{path}/{f}")]
    return render_template('dashboard/profile.html', folders=folders, username=session["username"])


@app.route("/playground/<projectname>")
def playground(projectname):
    redirect_response = auth_user()
    if redirect_response:
        return redirect_response

    return render_template('dashboard/playground.html', username=session["username"], projectname=projectname)


@app.route("/login", methods=["POST", "GET"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if request.method == 'POST':
        users = os.listdir(USERS_FOLDER)
        if username not in users:
            flash(message='Foydalanuvchi mavjud emas', category='danger')
            return redirect(url_for('register'))

        with open(f"{USERS_FOLDER}/{username}/password.txt", "r") as f:
            stored_password = f.read()

        if not check_password_hash(stored_password, password):
            flash(message='Parol noto\'g\'ri', category='danger')
            return redirect(url_for('login'))
        session["username"] = username
        return redirect(url_for('home'))
    return render_template('auth/login.html')


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        password = request.form.get('password')

        if username in os.listdir(USERS_FOLDER):
            flash(message='Foydalanuvchi mavjud', category='danger')
            return redirect(url_for('register'))

        os.mkdir(f"{USERS_FOLDER}/{username}")
        with open(f"{USERS_FOLDER}/{username}/password.txt", "w") as f:
            f.write(generate_password_hash(password))

        with open(f"{USERS_FOLDER}/{username}/name.txt", "w") as f:
            f.write(full_name)

        return redirect(url_for('login'))
    return render_template('auth/register.html')


@app.route("/logout")
def logout():
    redirect_response = auth_user()
    if redirect_response:
        return redirect_response

    session.pop("username", None)
    flash("Siz muvaffaqiyatli tarzda chiqdingiz!", "success")
    return redirect(url_for('login'))


@app.route("/create-project", methods=["POST", "GET"])
def create_project():
    projectname = request.form.get('projectname')
    users = os.listdir(USERS_FOLDER)

    if session['username'] not in users:
        return flash(message='Foydalanuvchi mavjud emas', category='danger')

    project_dir = f"{USERS_FOLDER}/{session['username']}/{projectname}"
    temple_dir = f"templates/components/temple.html"

    os.mkdir(project_dir)

    with open(f"{project_dir}/index.html", "w", encoding="utf-8") as f:
        with open(temple_dir, "r") as t:
            f.write(t.read())

    return redirect(url_for('home'))


@app.route("/append-component/<projectname>", methods=["GET", "POST"])
def append_component(projectname):
    redirect_response = auth_user()
    if redirect_response:
        return redirect_response

    username = session["username"]
    data = json.loads(request.data)
    component_name = data.get("component")
    component_variant = data.get("component")

    print(component_name, component_variant)

    component_temple = f"templates/components/{component_name}/primary.html"

    with open(component_temple, "r") as f:
        component = f.read()

    with open(f"{USERS_FOLDER}/{username}/{projectname}/index.html", "r") as f:
        current_html = f.read()

    soup = BeautifulSoup(current_html, "html.parser")
    root_div = soup.find(id="root")

    if root_div:
        root_div.append(BeautifulSoup(component, "html.parser"))

    with open(f"{USERS_FOLDER}/{username}/{projectname}/index.html", "w", encoding="utf-8") as file:
        file.write(str(soup))

    return jsonify({"status": "success", "message": "ok"}), 200


@app.route("/<username>/<projectname>", methods=["GET"])
def users_page(username, projectname):
    users_dir = os.listdir(USERS_FOLDER)
    if username not in users_dir:
        abort(404)
    return render_template(f"users_template/{username}/{projectname}/index.html")


if __name__ == '__main__':
    os.makedirs(USERS_FOLDER, exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=8000)
