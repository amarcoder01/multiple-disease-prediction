"""
Configuration module for Multiple Disease Prediction System.
Contains all constants, feature definitions, and model metadata.
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Create directories if they don't exist
for directory in [MODELS_DIR, REPORTS_DIR, ASSETS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Model file paths
MODEL_PATHS = {
    "diabetes": os.path.join(BASE_DIR, "diabetes_model.sav"),
    "heart": os.path.join(BASE_DIR, "heart_disease_model.sav"),
    "parkinsons": os.path.join(BASE_DIR, "parkinsons_model.sav"),
}

# Feature definitions with descriptions and valid ranges
@dataclass
class FeatureConfig:
    name: str
    description: str
    min_value: float
    max_value: float
    unit: str
    help_text: str

DISEASE_FEATURES: Dict[str, List[FeatureConfig]] = {
    "diabetes": [
        FeatureConfig("Pregnancies", "Number of Pregnancies", 0, 20, "count", 
                     "Number of times pregnant. 0 for males."),
        FeatureConfig("Glucose", "Glucose Level", 50, 300, "mg/dL",
                     "Plasma glucose concentration after 2 hours in an oral glucose tolerance test. Normal: 70-100 mg/dL"),
        FeatureConfig("BloodPressure", "Blood Pressure", 30, 200, "mm Hg",
                     "Diastolic blood pressure. Normal: 60-80 mm Hg"),
        FeatureConfig("SkinThickness", "Skin Thickness", 0, 100, "mm",
                     "Triceps skin fold thickness. Normal: 10-50 mm"),
        FeatureConfig("Insulin", "Insulin Level", 0, 900, "μU/mL",
                     "2-Hour serum insulin. Normal: 16-166 μU/mL"),
        FeatureConfig("BMI", "BMI", 10, 70, "kg/m²",
                     "Body Mass Index. Normal: 18.5-24.9 kg/m²"),
        FeatureConfig("DiabetesPedigreeFunction", "Diabetes Pedigree Function", 0.0, 3.0, "score",
                     "Diabetes pedigree function - genetic risk score"),
        FeatureConfig("Age", "Age", 1, 120, "years", "Age in years"),
    ],
    "heart": [
        FeatureConfig("age", "Age", 1, 120, "years", "Age in years"),
        FeatureConfig("sex", "Sex", 0, 1, "0=F, 1=M", "Sex: 0 = Female, 1 = Male"),
        FeatureConfig("cp", "Chest Pain Type", 0, 3, "type",
                     "Chest pain type: 0=Typical angina, 1=Atypical angina, 2=Non-anginal pain, 3=Asymptomatic"),
        FeatureConfig("trestbps", "Resting BP", 50, 250, "mm Hg",
                     "Resting blood pressure. Normal: 90-120 mm Hg"),
        FeatureConfig("chol", "Cholesterol", 50, 600, "mg/dL",
                     "Serum cholesterol. Normal: <200 mg/dL"),
        FeatureConfig("fbs", "Fasting Blood Sugar", 0, 1, "0/1",
                     "Fasting blood sugar > 120 mg/dL: 1 = True, 0 = False"),
        FeatureConfig("restecg", "Resting ECG", 0, 2, "type",
                     "Resting ECG results: 0=Normal, 1=ST-T abnormality, 2=LV hypertrophy"),
        FeatureConfig("thalach", "Max Heart Rate", 50, 250, "bpm",
                     "Maximum heart rate achieved during exercise"),
        FeatureConfig("exang", "Exercise Angina", 0, 1, "0/1",
                     "Exercise induced angina: 1 = Yes, 0 = No"),
        FeatureConfig("oldpeak", "ST Depression", 0, 10, "mm",
                     "ST depression induced by exercise relative to rest"),
        FeatureConfig("slope", "ST Slope", 0, 2, "type",
                     "Slope of peak exercise ST segment: 0=Upsloping, 1=Flat, 2=Downsloping"),
        FeatureConfig("ca", "Major Vessels", 0, 4, "count",
                     "Number of major vessels colored by fluoroscopy (0-4)"),
        FeatureConfig("thal", "Thalassemia", 0, 3, "type",
                     "Thalassemia: 0=Normal, 1=Fixed defect, 2=Reversible defect, 3=Unknown"),
    ],
    "parkinsons": [
        FeatureConfig("fo", "MDVP:Fo(Hz)", 50, 300, "Hz", "Average vocal fundamental frequency"),
        FeatureConfig("fhi", "MDVP:Fhi(Hz)", 50, 600, "Hz", "Maximum vocal fundamental frequency"),
        FeatureConfig("flo", "MDVP:Flo(Hz)", 50, 300, "Hz", "Minimum vocal fundamental frequency"),
        FeatureConfig("Jitter_percent", "MDVP:Jitter(%)", 0, 1, "%", "Variation in fundamental frequency"),
        FeatureConfig("Jitter_Abs", "MDVP:Jitter(Abs)", 0, 0.1, "abs", "Absolute jitter value"),
        FeatureConfig("RAP", "MDVP:RAP", 0, 0.1, "ratio", "Relative amplitude perturbation"),
        FeatureConfig("PPQ", "MDVP:PPQ", 0, 0.1, "ratio", "Five-point period perturbation quotient"),
        FeatureConfig("DDP", "Jitter:DDP", 0, 0.5, "ratio", "Average absolute difference of differences between periods"),
        FeatureConfig("Shimmer", "MDVP:Shimmer", 0, 1, "ratio", "Variation in amplitude"),
        FeatureConfig("Shimmer_dB", "MDVP:Shimmer(dB)", 0, 5, "dB", "Shimmer in decibels"),
        FeatureConfig("APQ3", "Shimmer:APQ3", 0, 0.5, "ratio", "Three-point amplitude perturbation quotient"),
        FeatureConfig("APQ5", "Shimmer:APQ5", 0, 0.5, "ratio", "Five-point amplitude perturbation quotient"),
        FeatureConfig("APQ", "MDVP:APQ", 0, 0.5, "ratio", "Amplitude perturbation quotient"),
        FeatureConfig("DDA", "Shimmer:DDA", 0, 1, "ratio", "Average absolute difference between consecutive differences"),
        FeatureConfig("NHR", "NHR", 0, 1, "ratio", "Noise-to-harmonics ratio"),
        FeatureConfig("HNR", "HNR", 0, 50, "dB", "Harmonics-to-noise ratio"),
        FeatureConfig("RPDE", "RPDE", 0, 1, "ratio", "Recurrence period density entropy"),
        FeatureConfig("DFA", "DFA", 0, 2, "ratio", "Detrended fluctuation analysis"),
        FeatureConfig("spread1", "spread1", -10, 10, "ratio", "Nonlinear measure of fundamental frequency variation"),
        FeatureConfig("spread2", "spread2", 0, 10, "ratio", "Nonlinear measure of fundamental frequency variation"),
        FeatureConfig("D2", "D2", 0, 5, "ratio", "Correlation dimension"),
        FeatureConfig("PPE", "PPE", 0, 1, "ratio", "Pitch period entropy"),
    ],
}

# Disease metadata
DISEASE_INFO = {
    "diabetes": {
        "name": "Diabetes Prediction",
        "icon": "activity",
        "color": "#FF6B6B",
        "description": "Predict diabetes risk based on health metrics",
        "accuracy": 0.85,
        "model_type": "SVM Classifier",
    },
    "heart": {
        "name": "Heart Disease Prediction",
        "icon": "heart",
        "color": "#FF4757",
        "description": "Predict heart disease risk using cardiac indicators",
        "accuracy": 0.88,
        "model_type": "Logistic Regression",
    },
    "parkinsons": {
        "name": "Parkinson's Prediction",
        "icon": "person",
        "color": "#5352ED",
        "description": "Detect Parkinson's disease from voice measurements",
        "accuracy": 0.92,
        "model_type": "SVM Classifier",
    },
}

# Feature importance data (approximate values for visualization)
FEATURE_IMPORTANCE = {
    "diabetes": {
        "Glucose": 0.35,
        "BMI": 0.18,
        "Age": 0.15,
        "DiabetesPedigreeFunction": 0.12,
        "Insulin": 0.08,
        "BloodPressure": 0.05,
        "SkinThickness": 0.04,
        "Pregnancies": 0.03,
    },
    "heart": {
        "cp": 0.28,
        "thalach": 0.20,
        "oldpeak": 0.15,
        "ca": 0.12,
        "thal": 0.10,
        "chol": 0.08,
        "age": 0.04,
        "trestbps": 0.02,
        "exang": 0.01,
    },
    "parkinsons": {
        "PPE": 0.25,
        "spread1": 0.18,
        "D2": 0.12,
        "RPDE": 0.10,
        "DFA": 0.08,
        "HNR": 0.07,
        "NHR": 0.06,
        "Shimmer": 0.05,
        "Jitter_percent": 0.04,
        "fo": 0.05,
    },
}

# Risk levels
RISK_LEVELS = {
    "low": {"threshold": 0.3, "color": "#2ED573", "label": "Low Risk"},
    "moderate": {"threshold": 0.6, "color": "#FFA502", "label": "Moderate Risk"},
    "high": {"threshold": 1.0, "color": "#FF4757", "label": "High Risk"},
}

# Page configuration
PAGE_CONFIG = {
    "page_title": "Advanced Health Assistant AI",
    "page_icon": "🏥",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}
