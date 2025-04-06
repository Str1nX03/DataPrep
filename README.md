# 🧹 DataPrep

**DataPrep** is a Flask-based web application that allows users to upload their datasets and apply a variety of data preprocessing techniques. It simplifies and modularizes data cleaning steps such as **Label Encoding**, **Normalization**, **One-Hot Encoding**, and **Missing Value Handling**, returning a clean, preprocessed dataset that’s ready for machine learning tasks.

This tool is ideal for students, data science enthusiasts, and ML beginners who want to practice with clean datasets without having to write preprocessing code from scratch.

---

## 🌐 Live Demo

You can try the live version of DataPrep here:  
🔗 [https://dataprep-yu1h.onrender.com/](https://dataprep-yu1h.onrender.com/)

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python 3.12.1)
- **Frontend:** HTML, CSS
- **Deployment:** Render
- **Version Control:** Git & GitHub

---

## ✨ Features

- Upload your dataset in `.csv` format
- Choose one or more preprocessing options:
  - 🔤 Label Encoding
  - 🔢 Normalization
  - 🔠 One-Hot Encoding
  - 🧼 Drop or Impute Missing Values
- Fully modular Python codebase – easy to extend or integrate
- Download the processed dataset in one click
- Fast and easy to use UI

---

## 📦 Installation Instructions

> Ensure that Python 3.12.1+ is installed in your system before you begin.

### Step-by-step Setup

1. **Clone the repository:**
```
git clone https://github.com/Str1nX03/DataPrep.git
cd DataPrep
```
2. **Create and activate a virtual environment:**
```
# For Linux/macOS
python -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```
3. **Install project dependencies:**
```
pip install -r requirements.txt
```
4. **Run the application:**
```
python app.py
```
5. **Open your browser and go to:**
```
http://127.0.0.1:5000/
```
## 🧪 Usage
*Use Cases:*

- Students testing models with clean datasets
- ML beginners learning how preprocessing works
- Data science learners exploring small-scale structured datasets

*Limitations:*

- ❌ Not suitable for unstructured or high-dimensional data (e.g., images, audio, video)
- ❌ Large datasets may lead to performance issues

## 🧱 Architecture & Extensibility

*DataPrep is designed in a modular way to make it easy to integrate new preprocessing techniques such as:-*

- Outlier removal
- Binning
- Standard scaling
- Data balancing

You can extend the codebase to connect with ML pipelines or integrate it into larger platforms.

## 📬 Contact

*If you want to report bugs, request features, or collaborate:*

📧 Email: dravin.ksharma@gmail.com
