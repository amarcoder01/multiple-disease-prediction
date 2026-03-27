"""
Utility functions for the Multiple Disease Prediction System.
"""

import re
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def validate_numeric_input(value: str, min_val: float, max_val: float, field_name: str) -> Tuple[bool, float, str]:
    """
    Validate numeric input with range checking.
    
    Returns:
        Tuple of (is_valid, converted_value, error_message)
    """
    if not value or value.strip() == '':
        return False, 0.0, f"{field_name} is required"
    
    try:
        # Remove any whitespace
        value = value.strip()
        
        # Check for valid numeric format
        if not re.match(r'^-?\d*\.?\d+$', value):
            return False, 0.0, f"{field_name} must be a valid number"
        
        num_value = float(value)
        
        # Check range
        if num_value < min_val:
            return False, num_value, f"{field_name} must be at least {min_val}"
        if num_value > max_val:
            return False, num_value, f"{field_name} must not exceed {max_val}"
        
        return True, num_value, ""
        
    except ValueError:
        return False, 0.0, f"{field_name} must be a valid number"


def validate_all_inputs(inputs: Dict[str, str], features: List[Any]) -> Tuple[bool, List[float], List[str]]:
    """
    Validate all input fields for a disease prediction form.
    
    Returns:
        Tuple of (all_valid, converted_values, error_messages)
    """
    converted_values = []
    error_messages = []
    all_valid = True
    
    for feature in features:
        value = inputs.get(feature.name, '')
        is_valid, converted, error = validate_numeric_input(
            value, feature.min_value, feature.max_value, feature.name
        )
        
        if not is_valid:
            all_valid = False
            error_messages.append(error)
        
        converted_values.append(converted)
    
    return all_valid, converted_values, error_messages


def get_risk_level(probability: float) -> Dict[str, Any]:
    """
    Determine risk level based on prediction probability.
    """
    from config import RISK_LEVELS
    
    if probability < RISK_LEVELS["low"]["threshold"]:
        return RISK_LEVELS["low"]
    elif probability < RISK_LEVELS["moderate"]["threshold"]:
        return RISK_LEVELS["moderate"]
    else:
        return RISK_LEVELS["high"]


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format timestamp for display."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def create_prediction_record(
    disease_type: str,
    inputs: List[float],
    prediction: int,
    probability: float,
    features: List[str]
) -> Dict[str, Any]:
    """Create a structured prediction record for history."""
    return {
        "timestamp": format_timestamp(),
        "disease_type": disease_type,
        "inputs": dict(zip(features, inputs)),
        "prediction": "Positive" if prediction == 1 else "Negative",
        "probability": round(probability * 100, 2),
        "risk_level": get_risk_level(probability)["label"],
    }


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations."""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Limit length
    return filename[:100]


def generate_csv_template(features: List[Any]) -> str:
    """Generate CSV template content for batch upload."""
    headers = [f.name for f in features]
    # Add sample row with normal values
    sample_row = []
    for f in features:
        mid_val = (f.min_value + f.max_value) / 2
        sample_row.append(str(mid_val))
    
    return ','.join(headers) + '\n' + ','.join(sample_row) + '\n'


def validate_csv_data(df: pd.DataFrame, features: List[Any]) -> Tuple[bool, List[str]]:
    """
    Validate uploaded CSV data.
    
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    feature_names = [f.name for f in features]
    
    # Check required columns
    missing_cols = set(feature_names) - set(df.columns)
    if missing_cols:
        errors.append(f"Missing required columns: {', '.join(missing_cols)}")
    
    # Check for empty dataframe
    if df.empty:
        errors.append("CSV file contains no data rows")
    
    # Check for too many rows
    if len(df) > 1000:
        errors.append("Maximum 1000 rows allowed per batch")
    
    # Validate numeric data in each column
    for col in feature_names:
        if col in df.columns:
            try:
                df[col].astype(float)
            except ValueError:
                errors.append(f"Column '{col}' contains non-numeric values")
    
    return len(errors) == 0, errors


def calculate_confidence_interval(probability: float, n_samples: int = 100) -> Tuple[float, float]:
    """Calculate approximate confidence interval for probability."""
    # Simplified calculation - in production, use proper statistical methods
    std_error = np.sqrt(probability * (1 - probability) / n_samples)
    margin = 1.96 * std_error  # 95% CI
    
    lower = max(0, probability - margin)
    upper = min(1, probability + margin)
    
    return lower, upper


def get_health_recommendations(disease_type: str, risk_level: str) -> List[str]:
    """Get health recommendations based on disease type and risk level."""
    recommendations = {
        "diabetes": {
            "low": [
                "Maintain healthy diet with low sugar intake",
                "Exercise regularly (30 mins/day)",
                "Get annual health checkups",
                "Maintain healthy weight"
            ],
            "moderate": [
                "Reduce carbohydrate intake immediately",
                "Monitor blood glucose levels weekly",
                "Consult a doctor within 2 weeks",
                "Start daily 45-minute exercise routine",
                "Avoid sugary beverages completely"
            ],
            "high": [
                "URGENT: Consult an endocrinologist within 48 hours",
                "Start daily blood glucose monitoring",
                "Follow strict diabetic diet plan",
                "Consider medication as prescribed by doctor",
                "Get HbA1c test immediately"
            ]
        },
        "heart": {
            "low": [
                "Maintain heart-healthy Mediterranean diet",
                "Exercise 150 minutes per week",
                "Manage stress through meditation",
                "Get cholesterol checked annually"
            ],
            "moderate": [
                "Schedule cardiology appointment within 2 weeks",
                "Reduce sodium intake (< 2g/day)",
                "Start daily cardiovascular exercise",
                "Monitor blood pressure daily",
                "Quit smoking if applicable"
            ],
            "high": [
                "URGENT: Consult a cardiologist within 48 hours",
                "Get comprehensive cardiac evaluation",
                "Consider stress test and ECG",
                "Begin heart-healthy diet immediately",
                "Avoid strenuous activity until evaluated"
            ]
        },
        "parkinsons": {
            "low": [
                "Continue regular physical activity",
                "Practice balance and coordination exercises",
                "Maintain social engagement",
                "Get annual neurological checkup"
            ],
            "moderate": [
                "Schedule neurology appointment within 2 weeks",
                "Start speech therapy exercises",
                "Practice daily hand dexterity exercises",
                "Monitor for tremor progression",
                "Consider occupational therapy"
            ],
            "high": [
                "URGENT: Consult a neurologist within 1 week",
                "Get comprehensive movement disorder evaluation",
                "Begin medication evaluation with doctor",
                "Start physical therapy program",
                "Consider DAT scan for confirmation"
            ]
        }
    }
    
    return recommendations.get(disease_type, {}).get(risk_level, ["Consult a healthcare provider"])


def log_prediction(disease_type: str, prediction: int, probability: float):
    """Log prediction for analytics."""
    logger.info(f"Prediction made - Disease: {disease_type}, "
                f"Result: {'Positive' if prediction == 1 else 'Negative'}, "
                f"Probability: {probability:.3f}")
