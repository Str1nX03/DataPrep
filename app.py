from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from tempfile import NamedTemporaryFile
from src.exception import CustomException
from src.logger import logging
from src.components.data_pre_processor import DataPreProcess
import os
import sys
import pandas as pd

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Global variable to store processed file path
processed_file_path = None  

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    global processed_file_path

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

        # Save uploaded file temporarily
        temp_file_path = NamedTemporaryFile(delete=False, suffix=".csv").name
        file.save(temp_file_path)

        # Get selected operations
        selected_operations = request.form.getlist("operations")
        df = pd.read_csv(temp_file_path)

        processor = DataPreProcess()

        # Apply selected operations
        if "data_structuring" in selected_operations:
            df = processor.data_structuring(temp_file_path)

        if "label_encoding" in selected_operations:
            df = processor.label_encoding(df)

        if "onehot_encoding" in selected_operations:
            df = processor.onehot_encoder(df)

        if "normalization" in selected_operations:
            df = processor.normalization(df)

        # Save processed data
        processed_file_path = NamedTemporaryFile(delete=False, suffix=".csv").name
        df.to_csv(processed_file_path, index=False)

        logging.info(f"File successfully processed with selected operations: {selected_operations}")
        flash("File uploaded and processed successfully!", "success")

        os.remove(temp_file_path)

        return render_template("success.html", download_link=url_for("download"))

    except Exception as e:
        logging.error(f"Error during file upload: {e}")
        flash("An error occurred while uploading the file.", "error")
        raise CustomException(e, sys)

@app.route("/download")
def download():
    if processed_file_path and os.path.exists(processed_file_path):
        return send_file(processed_file_path, as_attachment=True, download_name="processed_data.csv")
    else:
        flash("File not found or already deleted.", "error")
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
