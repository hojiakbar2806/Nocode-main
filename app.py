from flask_cors import CORS
from flask import Flask, request, jsonify
import os
from flask import Flask, render_template

app = Flask(__name__, template_folder='templates',  static_folder='static')


app = Flask(__name__)
CORS(app)
USERS_DIR = "backend/users"


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/a", methods=["GET"])
def home3():
    with open("templates/users_template/hojiakba/first/index.html", "w") as f:
        f.write(
            "<!DOCTYPE html>\n<html>\n<body>\n<h1>New Project</h1>\n</body>\n</html>")
    return jsonify({"status": "error", "message": "ok"}), 200


@app.route("/<username>/<projectname>", methods=["GET"])
def home_2(username, projectname):
    return render_template(f"users_template/{username}/{projectname}/index.html")


# @app.route("/<username>/<projectname>", methods=["POST"])
# def create_project(username, projectname):
#     try:
#         user_dir = os.path.join(USERS_DIR, username)
#         os.makedirs(user_dir, exist_ok=True)
#         project_dir = os.path.join(user_dir, projectname)
#         os.makedirs(project_dir, exist_ok=True)

#         with open(os.path.join(project_dir, "index.html"), "w") as f:
#             f.write(
#                 "<!DOCTYPE html>\n<html>\n<body>\n<h1>New Project</h1>\n</body>\n</html>")

#         with open(os.path.join(project_dir, "styles.css"), "w") as f:
#             f.write("body { font-family: Arial, sans-serif; }")

#         with open(os.path.join(project_dir, "script.js"), "w") as f:
#             f.write("console.log('Project initialized');")

#         return jsonify({"status": "success", "message": f"Project {projectname} created for {username}"})

#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500


# @app.route("/<username>", methods=["GET"])
# def get_user_projects(username):
#     try:
#         user_dir = os.path.join(USERS_DIR, username)

#         if not os.path.exists(user_dir):
#             return jsonify({"status": "error", "message": "User not found"}), 404

#         projects = [d for d in os.listdir(
#             user_dir) if os.path.isdir(os.path.join(user_dir, d))]

#         return jsonify({"status": "success", "projects": projects})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500


# @app.route("/<username>/<projectname>", methods=["GET"])
# def get_project_files(username, projectname):
#     try:
#         project_dir = os.path.join(USERS_DIR, username, projectname)
#         if not os.path.exists(project_dir):
#             return jsonify({"status": "error", "message": "Project not found"}), 404
#         files = os.listdir(project_dir)

#         return jsonify({"status": "success", "files": files})

#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    os.makedirs(USERS_DIR, exist_ok=True)
    app.run(debug=True, port=5000)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
