from flask import Flask, request, render_template
from stego import embed_message, extract_message
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ---------------- EMBED ----------------
@app.route("/embed", methods=["POST"])
def embed():
    file = request.files["image"]
    message = request.form["message"]
    password = request.form.get("password") or "default123"

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    try:
        output_path = embed_message(path, message, password=password)
        result = f"Message Embedded Successfully! Saved as: {output_path}"
    except Exception as e:
        result = f"Error: {str(e)}"

    # render same UI with result
    return render_template("index.html", message=result)


# ---------------- EXTRACT ----------------
@app.route("/extract", methods=["POST"])
def extract():
    file = request.files["image"]
    password = request.form.get("password") or "default123"

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    try:
        message = extract_message(path, password=password)
        result = message
    except Exception as e:
        result = f"Extraction Failed: {str(e)}"

    # render same UI with extracted message
    return render_template("index.html", message=result)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)