# 🧠 Multiple Disease Prediction System

<div align="center">

<img src="https://img.shields.io/badge/Version-1.0-blue.svg" alt="Version">
<img src="https://img.shields.io/badge/Language-Python-yellow.svg" alt="Language">
<img src="https://img.shields.io/badge/Framework-Streamlit-red.svg" alt="Framework">
<img src="https://img.shields.io/badge/ML-Scikit--learn|TensorFlow-green.svg" alt="ML">
<img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="License">

<h3>
🚀 Predict multiple diseases (Diabetes, Heart Disease, Parkinson's) using advanced Machine Learning models.
</h3>

🔗 <b>Live Demo:</b> [Try it Now](https://multiple-disease-prediction-xasrpbvqrsrcb7rou8zr62.streamlit.app/)

</div>

---

## 📌 Table of Contents

1. [💡 Project Overview](#-project-overview)  
2. [✨ Features](#-features)  
3. [🧱 Tech Stack](#-tech-stack)  
4. [⚙️ Installation](#️-installation)  
5. [🚀 Usage](#-usage)  
6. [📚 Use Cases](#-use-cases)  
7. [📈 Future Roadmap](#-future-roadmap)  
8. [🤝 Contributing](#-contributing)  
9. [📄 License](#-license)  
10. [📬 Contact](#-contact)

---

## 💡 Project Overview

In today's fast-paced healthcare landscape, **timely and accurate diagnosis** is crucial. Manual assessments based on patient records can be inconsistent and time-consuming. This project solves that with:

- 🔍 **Multi-disease prediction** from structured patient data  
- 💡 **High accuracy** through multiple ML models including ensembles  
- ⚡ **Fast results** to assist medical professionals in early decision-making

> 👨‍⚕️ Built to support doctors, researchers, and data scientists in predictive diagnosis.

---

## ✨ Features

- 🧠 **Multi-Disease Support**: Predicts **Diabetes**, **Heart Disease**, and **Parkinson's**.
- 🧪 **Multiple ML Models**: Random Forest, SVM, Neural Networks for comparative accuracy.
- 🖥️ **Interactive Interface**: Built with **Streamlit** for intuitive web usage.
- 📊 **Data Visualization**: Charts and metrics to explain predictions.
- 🔄 **Scalable**: Easily extensible for more diseases and data formats.
- 📥 **Real-Time Input**: Users can enter new data and get live results.
- 🧾 **Clean Reporting**: Visual and textual outputs for quick decision support.

---

## 🧱 Tech Stack

| Category              | Technologies                       |
|-----------------------|------------------------------------|
| 💻 Programming Language | Python                            |
| 🤖 Machine Learning    | Scikit-learn, TensorFlow           |
| 📊 Data Handling       | Pandas, NumPy                      |
| 🎨 Interface/UI        | Streamlit                          |
| 📈 Visualization       | Matplotlib, Seaborn                |
| 🧪 Models Used         | Random Forest, SVM, Neural Net     |

---

## ⚙️ Installation

### 🔧 Prerequisites

- Python 3.9+ installed  
- Git installed  
- (Optional) Create and activate a virtual environment using `venv` or `conda`

### 🚀 Steps

```bash
# Clone the repository
git clone https://github.com/amarcoder01/multiple-disease-prediction.git
cd multiple-disease-prediction

# Create and activate virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
