import os
import json
import shutil

from flask import jsonify, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, render_template, redirect, url_for, flash, abort

from utils import update_html_element


app = Flask(__name__,  template_folder="templates", static_folder='/nocode/static')
app.secret_key = "0d5b096deee48ee17e845c44a853784b77f2daf5ba8bb21e24842cb01e6a50c4"
USERS_FOLDER = "templates/users"
COMPONENTS = "templates/components"
APP_DIR = "app"


def auth_user():
    if "username" not in session:
        flash("User not logged in", category="danger")
        return redirect(url_for('login'))
    if not os.path.exists(f"{USERS_FOLDER}/{session['username']}"):
        flash("User not registered", category="danger")
        return redirect(url_for('register'))


@app.route('/nocode/')
def home():
    redirect_response = auth_user()
    if redirect_response:
        return redirect_response

    path = f"{USERS_FOLDER}/{session['username']}"
    folders = [f for f in os.listdir(path) if os.path.isdir(f"{path}/{f}")]

    name = open(path + "/name.txt", "r").read()
    data = {
        "username": session['username'],
        "folders": folders,
        "name": name,
        "btn": False,
    }
    return render_template(f"{APP_DIR}/dashboard/profile.html", data=data)


@app.route("/nocode/playground/<projectname>")
def playground(projectname):
    redirect_response = auth_user()
    if redirect_response:
        return redirect_response

    components = []
    folders = []

    for folder_name in os.listdir(COMPONENTS):
        folder_path = f"{COMPONENTS}/{folder_name}"
        if os.path.isdir(folder_path):
            folders.append(folder_name)

    for folder_name in folders:
        variant_files = []
        variant_folder_path = f"{COMPONENTS}/{folder_name}"

        for file_name in os.listdir(variant_folder_path):
            file_path = f"{COMPONENTS}/{folder_name}/{file_name}"
            if os.path.isfile(file_path):
                variant_files.append(file_name)

        component = {
            "name": folder_name,
            "variants": []
        }

        for file_name in variant_files:
            if file_name.endswith(".html"):
                component["variants"].append({
                    "name": file_name.split(".")[0],
                })

        components.append(component)

    path = f"{USERS_FOLDER}/{session['username']}"
    name = open(path + "/name.txt", "r").read()
    data = {
        "username": session["username"],
        "projectname": projectname,
        "components": components,
        "btn": True,
        "name": name
    }
    return render_template(f'{APP_DIR}/dashboard/playground.html', data=data)


@app.route("/nocode/login", methods=["POST", "GET"])
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
        flash("Xush kelibsiz", category="success")
        return redirect(url_for('home'))
    return render_template(f'{APP_DIR}/auth/login.html')


@app.route("/nocode/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        password = request.form.get('password')

        if username in os.listdir(USERS_FOLDER):
            flash(message='Bunday foydalanuvchi mavjud', category='danger')
            return redirect(url_for('register'))

        os.mkdir(f"{USERS_FOLDER}/{username}")
        with open(f"{USERS_FOLDER}/{username}/password.txt", "w") as f:
            f.write(generate_password_hash(password))

        with open(f"{USERS_FOLDER}/{username}/name.txt", "w") as f:
            f.write(full_name)

        flash(message="Muvafaqiyatli ro'yxatdan o'tdingiz", category="success")
        return redirect(url_for('login'))
    return render_template(f'{APP_DIR}/auth/register.html')


@app.route("/nocode/logout")
def logout():
    redirect_response = auth_user()
    if redirect_response:
        return redirect_response

    session.pop("username", None)
    flash("Tizimdan muvaffaqiyatli chiqdingiz!", "success")
    return redirect(url_for('login'))


@app.route("/nocode/create-project", methods=["POST"])
def create_project():
    projectname = request.form.get('projectname')
    projectname = projectname.capitalize()

    redirect_response = auth_user()
    if redirect_response:
        return redirect_response

    project_dir = f"{USERS_FOLDER}/{session['username']}/{projectname}"
    temple_dir = f"templates/components/temple.html"

    if os.path.exists(project_dir):
        return redirect(url_for("home"))

    os.mkdir(project_dir)

    with open(f"{project_dir}/index.html", "w") as f:
        with open(temple_dir, "r") as t:
            f.write(t.read())
    flash(f"{projectname} mivafaqiyatli yaratildi", "success")
    return redirect(url_for('home'))


@app.route("/nocode/delete-project/<projectname>", methods=["POST"])
def delete_project(projectname):
    redirect_response = auth_user()
    if redirect_response:
        return redirect_response

    project_dir = f"{USERS_FOLDER}/{session['username']}/{projectname}"

    shutil.rmtree(project_dir)
    flash(f"{projectname} muvafaqiyatli o'chirildi", "success")
    return redirect(url_for('home'))


@app.route("/nocode/append-component/<projectname>", methods=["GET", "POST"])
def append_component(projectname):
    redirect_response = auth_user()
    if redirect_response:
        return redirect_response

    data = json.loads(request.data)

    comp_name = data.get("component")
    comp_variant = data.get("variant")
    username = session["username"]

    comp_path = f"{COMPONENTS}/{comp_name}/{comp_variant}.html"
    file_path = f"{USERS_FOLDER}/{username}/{projectname}/index.html"

    with open(comp_path, "r") as f:
        component = f.read()

    status, message = update_html_element("append", file_path, component)
    flash(message, category="success" if status else "danger")
    return jsonify({"status": status})


@app.route("/nocode/<username>/<projectname>", methods=["GET"])
def users_page(username, projectname):
    users_dir = os.listdir(USERS_FOLDER)
    if username not in users_dir:
        abort(404)
    project_dir = os.listdir(USERS_FOLDER+"/"+username)
    if projectname not in project_dir:
        abort(404)
    return render_template(f"users/{username}/{projectname}/index.html")


@app.route("/nocode/update-element/<mode>/<projectname>", methods=["POST"])
def update_element(mode, projectname):
    redirect_response = auth_user()
    if redirect_response:
        return redirect_response

    indexes = json.loads(request.data).get("elementIndex")
    content = json.loads(request.data).get("content")
    username = session.get("username")
    file_path = f"{USERS_FOLDER}/{username}/{projectname}/index.html"

    status, message = update_html_element(mode, file_path, content, indexes)

    flash(message, category="success" if status else "danger")
    return jsonify({"status": status})


@app.route("/nocode/download/<projectname>")
def download(projectname):
    redirect_response = auth_user()
    if redirect_response:
        return redirect_response
    username = session.get("username")

    export_file_path = f"templates/users/{username}/{projectname}/export.html"
    render_file_path = f"users/{username}/{projectname}/index.html"

    html = render_template(render_file_path, projectname=projectname)

    with open(export_file_path, "w") as f:
        f.write(html)

    return send_file(export_file_path, download_name=f"{projectname}.html", as_attachment=True)


if __name__ == '__main__':
    os.makedirs(USERS_FOLDER, exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=8000)
