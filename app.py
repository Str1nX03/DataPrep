from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from tempfile import NamedTemporaryFile
from src.exception import CustomException
from src.logger import logging
from src.components.data_pre_processor import DataPreProcess
import os
import sys

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Global variable to store processed file path
processed_file_path = None  

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    global processed_file_path  # Store temp file path globally

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

        # Perform Data Pre-Processing
        pre_processed_data = DataPreProcess().initiate_data_pre_processing(temp_file_path)

        # Save processed data to a new temporary file
        processed_file_path = NamedTemporaryFile(delete=False, suffix=".csv").name  
        pre_processed_data.to_csv(processed_file_path, index=False)

        logging.info(f"File successfully processed and saved at {processed_file_path}")
        flash("File uploaded and processed successfully!", "success")

        # Remove the original temp file after processing
        os.remove(temp_file_path)

        # Pass download link to success page
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
    app.run(debug=True)
