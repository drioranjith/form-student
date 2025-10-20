from flask import Flask, request, jsonify, send_from_directory
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder="static", static_url_path="")

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    roll = request.form.get("roll")
    reg = request.form.get("reg")
    dept = request.form.get("dept")
    photo = request.files.get("photo")

    if not name or not roll or not reg or not dept or not photo:
        return jsonify({"message": "Please fill all fields!"}), 400

    filename = secure_filename(photo.filename)
    photo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    photo.save(photo_path)

    student_data = {
        "name": name,
        "roll_number": roll,
        "register_number": reg,
        "department": dept,
        "photo_filename": filename
    }

    if os.path.exists("data.json"):
        with open("data.json", "r") as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    existing_data.append(student_data)

    with open("data.json", "w") as file:
        json.dump(existing_data, file, indent=4)

    return jsonify({"message": "Student data saved successfully!"})

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
