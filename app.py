import os
import pdfplumber

def extract_pdf_text(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

    return text

from flask import Flask, request, jsonify
from flask_cors import CORS
from summarizer import summarize_text
from database import collection
from tracker import detect_changes
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

CORS(app)

@app.route("/")
def home():
    return "TrackTerms Backend Running"


@app.route("/test")
def test():
    return {
        "message": "API Working"
    }


@app.route("/summarize", methods=["POST"])
def summarize():

    data = request.json

    text = data["text"]

    summary = summarize_text(text)

    return jsonify({
        "summary": summary
    })

@app.route("/upload", methods=["POST"])
def upload_pdf():

    if "file" not in request.files:

        return jsonify({
            "error": "No file uploaded"
        }), 400

    file = request.files["file"]

    if file.filename == "":

        return jsonify({
            "error": "Empty filename"
        }), 400

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(file_path)

    extracted_text = extract_pdf_text(file_path)

    summary = summarize_text(extracted_text)

    previous_document = collection.find_one(
        {"filename": file.filename},
        sort=[("_id", -1)]
    )

    changes = []

    if previous_document:

        changes = detect_changes(
            previous_document["text"],
            extracted_text
        )

    collection.insert_one({

        "filename": file.filename,

        "text": extracted_text,

        "summary": summary,

        "changes": changes,

        "uploaded_at":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    })

    return jsonify({
        "summary": summary,
        "changes": changes
    })

@app.route("/compare", methods=["POST"])
def compare_versions():

    data = request.json

    old_text = data.get("old_text")

    new_text = data.get("new_text")

    differences = detect_changes(
        old_text,
        new_text
    )

    return jsonify({
        "changes": differences
    })

@app.route('/history', methods=['GET'])
def get_history():

    data = list(

        collection.find().sort(
            "uploaded_at",
            -1
        )
    )

    for item in data:

        item["_id"] = str(item["_id"])

    return jsonify(data)

@app.route("/delete/<id>", methods=["DELETE"])
def delete_history(id):

    try:

        collection.delete_one({
            "_id": ObjectId(id)
        })

        return jsonify({
            "message": "Deleted successfully"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)