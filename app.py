from flask import Flask, render_template, request, redirect, url_for, flash
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from src.utils import save_dataset
from src.exception import CustomException
from src.logger import logging
import os
import sys


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():

    try:
        if "file" not in request.files:
            flash("No file part in the request.", "error")
            return redirect(request.url)

        file = request.files["file"]

        if not file.filename:
            flash("No file selected.", "error")
            return redirect(request.url)

        if not file.filename.lower().endswith(".csv"):
            flash("Only CSV files are allowed.", "error")
            return redirect(request.url)

        # Save the uploaded file and store it in artifacts/data.csv
        temp_path = "temp_upload.csv"
        file.save(temp_path)
        saved_file_path = save_dataset(temp_path)
        os.remove(temp_path)

        logging.info(f"File successfully stored at {saved_file_path}")
        flash("File uploaded successfully!", "success")
        return render_template("success.html", file_path=saved_file_path)

    except Exception as e:
        logging.error(f"Error during file upload: {e}")
        flash("An error occurred while uploading the file.", "error")
        raise CustomException(e, sys)

if __name__ == "__main__":
    app.run(debug=True)