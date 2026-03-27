# 🏥 Advanced Multiple Disease Prediction System

<div align="center">

<img src="https://img.shields.io/badge/Version-2.0-blue.svg" alt="Version">
<img src="https://img.shields.io/badge/Language-Python-yellow.svg" alt="Language">
<img src="https://img.shields.io/badge/Framework-Streamlit-red.svg" alt="Framework">
<img src="https://img.shields.io/badge/ML-Scikit--learn-green.svg" alt="ML">
<img src="https://img.shields.io/badge/Features-Advanced-purple.svg" alt="Features">
<img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="License">

<h3>
🚀 Advanced AI-powered disease prediction with confidence scoring, batch processing, and comprehensive health analytics.
</h3>

</div>

---

## 📌 Table of Contents

1. [💡 Project Overview](#-project-overview)
2. [✨ Advanced Features](#-advanced-features)
3. [🧱 Tech Stack](#-tech-stack)
4. [⚙️ Installation](#️-installation)
5. [🚀 Usage](#-usage)
6. [📊 Feature Details](#-feature-details)
7. [📚 Use Cases](#-use-cases)
8. [🤝 Contributing](#-contributing)
9. [📄 License](#-license)
10. [📬 Contact](#-contact)

---

## 💡 Project Overview

The **Advanced Multiple Disease Prediction System** is a next-generation healthcare AI platform that provides:

* 🔍 **Multi-disease prediction** (Diabetes, Heart Disease, Parkinson's)
* 📊 **Confidence scoring** with probability analysis
* 📈 **Feature importance visualization** for explainable AI
* 📤 **Batch prediction** for processing multiple patients
* 📄 **PDF report generation** for professional documentation
* 💡 **Personalized health recommendations** based on risk levels
* 📱 **Modern responsive UI** with custom styling
* 📚 **Prediction history tracking** with analytics dashboard

> 👨‍⚕️ Built to support healthcare professionals, researchers, and patients with actionable health insights.

---

## ✨ Advanced Features

### 🎯 Core Prediction Features
- **Input Validation** - Smart validation with helpful error messages and range checking
- **Confidence Scoring** - Probability scores with 95% confidence intervals
- **Risk Stratification** - Low, Moderate, and High risk classifications with color coding
- **Feature Importance** - Visual charts showing which factors most influence predictions

### 📊 Data & Analytics
- **Batch Prediction** - Upload CSV files to process multiple patients at once
- **Analytics Dashboard** - Model performance metrics and prediction timelines
- **Prediction History** - Track all predictions made during a session
- **Data Visualization** - Interactive charts using Plotly

### 📄 Reporting & Export
- **PDF Reports** - Professional PDF generation with patient data and recommendations
- **CSV Templates** - Download templates for easy data entry
- **Export Results** - Download batch predictions as CSV or PDF

### 🎨 User Experience
- **Modern UI** - Custom CSS with gradient styling and animations
- **Help Tooltips** - Detailed help text for every medical field
- **Responsive Design** - Optimized for desktop and tablet
- **Progress Indicators** - Visual feedback during processing

---

## 🧱 Tech Stack

| Category                | Technologies                           |
| ----------------------- | -------------------------------------- |
| 💻 Programming Language | Python 3.9+                            |
| 🤖 Machine Learning     | Scikit-learn                           |
| 📈 Data Handling        | Pandas, NumPy                          |
| 🎨 Interface/UI         | Streamlit, Streamlit-Option-Menu       |
| 📊 Visualization        | Plotly                                 |
| 📄 PDF Generation       | ReportLab                              |
| 🧪 Models Used          | SVM Classifier, Logistic Regression    |

### 📁 Project Structure
```
multiple-disease-prediction/
├── app.py                  # Main application
├── config.py               # Configuration and feature definitions
├── utils.py                # Utility functions and validation
├── components.py           # UI components and styling
├── report_generator.py   # PDF report generation
├── requirements.txt        # Dependencies
├── README.md              # Documentation
├── diabetes_model.sav     # Diabetes prediction model
├── heart_disease_model.sav # Heart disease prediction model
└── parkinsons_model.sav   # Parkinson's prediction model
```

---

## ⚙️ Installation

### 🔧 Prerequisites

* Python 3.9+ installed
* pip package manager
* Git (optional)

### 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/amarcoder01/multiple-disease-prediction.git
cd multiple-disease-prediction

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### 📦 Dependencies

```
numpy==1.26.3
pandas==2.1.4
scikit-learn==1.3.2
streamlit==1.29.0
streamlit-option-menu==0.3.6
plotly==5.18.0
reportlab==4.0.8
Pillow==10.1.0
```

---

## 🚀 Usage

### Single Patient Prediction

1. Launch the application: `streamlit run app.py`
2. Select a disease prediction module from the sidebar
3. Enter patient health metrics in the input fields
4. Click **"Predict"** to get results
5. View confidence scores, risk levels, and recommendations
6. Download a detailed PDF report if needed

### Batch Prediction

1. Navigate to **"Batch Prediction"** from the sidebar
2. Select the disease type
3. Download the CSV template
4. Fill in patient data and upload the file
5. Click **"Run Batch Prediction"**
6. Download results as CSV or PDF

### Analytics Dashboard

1. Go to **"Analytics Dashboard"**
2. View model accuracy comparisons
3. Explore feature importance for each disease
4. Review session activity timeline

### Viewing Prediction History

1. Click **"Prediction History"** in the sidebar
2. See all predictions made in the current session
3. View summary statistics by risk level
4. Clear history if needed

---

## 📊 Feature Details

### 🩺 Supported Diseases

#### Diabetes Prediction
- **Features**: Pregnancies, Glucose, Blood Pressure, Skin Thickness, Insulin, BMI, Diabetes Pedigree Function, Age
- **Model**: SVM Classifier
- **Accuracy**: 85%

#### Heart Disease Prediction
- **Features**: Age, Sex, Chest Pain Type, Resting BP, Cholesterol, Fasting Blood Sugar, ECG, Max Heart Rate, Exercise Angina, ST Depression, Slope, Major Vessels, Thalassemia
- **Model**: Logistic Regression
- **Accuracy**: 88%

#### Parkinson's Disease Prediction
- **Features**: 22 voice measurement parameters (MDVP, Jitter, Shimmer, NHR, HNR, RPDE, DFA, etc.)
- **Model**: SVM Classifier
- **Accuracy**: 92%

### 📊 Input Validation

All input fields include:
- **Range validation** - Ensures values are within medically valid ranges
- **Type checking** - Validates numeric inputs
- **Help tooltips** - Explains each medical parameter
- **Error messages** - Clear guidance when inputs are invalid

### 📄 PDF Report Contents

Generated PDF reports include:
- Report metadata (timestamp, prediction ID)
- Prediction result with risk level
- Confidence level and interval
- All input parameters
- Key contributing factors (feature importance)
- Personalized health recommendations
- Medical disclaimer

---

## 📚 Use Cases

| 🏥 Use Case            | Description                                        |
| ---------------------- | -------------------------------------------------- |
| 👨‍⚕️ Healthcare Providers | Early diagnosis support and patient risk assessment |
| 🧪 Medical Researchers  | Model evaluation and feature importance analysis   |
| 📊 Data Scientists      | Benchmarking ML models on medical datasets         |
| 🏫 Academic Learning  | Demonstrating practical healthcare ML applications |
| 🏢 Health Clinics      | Batch processing patient screening data            |

---

## 🤝 Contributing

We welcome contributions to improve the Advanced Health Assistant AI!

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/your-username/multiple-disease-prediction.git
cd multiple-disease-prediction

# Create development branch
git checkout -b feature/your-feature-name

# Make your changes and test
streamlit run app.py

# Commit and push
git add .
git commit -m "Add: Description of your changes"
git push origin feature/your-feature-name

# Create a Pull Request
```

### Contribution Ideas

- 🌍 Add multi-language support
- 🧠 Implement additional ML models
- 📱 Enhance mobile responsiveness
- 🔐 Add user authentication
- 📊 Create more visualization types
- 🏥 Add more disease predictions

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 Amar Pawar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## ⚠️ Medical Disclaimer

**IMPORTANT**: This application is for educational and informational purposes only.

- Always consult qualified healthcare professionals for medical decisions
- This tool should not replace professional medical advice, diagnosis, or treatment
- Never disregard professional medical advice because of information from this system
- The predictions are based on machine learning models and may not be 100% accurate
- Always seek the guidance of qualified healthcare providers for health concerns

---

## 📬 Contact

**Author**: Amar Pawar

* 📧 Email: [amar01pawar80@gmail.com](mailto:amar01pawar80@gmail.com)
* 🔗 GitHub: [@amarcoder01](https://github.com/amarcoder01)
* 💼 LinkedIn: [Amar Pawar](https://www.linkedin.com/in/amar-pawar)

---

## 🙏 Acknowledgments

- Thanks to the Streamlit team for the amazing framework
- Scikit-learn for machine learning tools
- Plotly for interactive visualizations
- ReportLab for PDF generation capabilities

---

> © 2025 Amar Pawar - Advanced Health Assistant AI | Built with ❤️ and Python
> 
> **Version 2.0** - Advanced Edition with AI-Powered Insights
