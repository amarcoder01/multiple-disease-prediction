"""
UI Components and styling for the Multiple Disease Prediction System.
"""

import streamlit as st
import base64
from typing import Dict, List, Any, Optional


def load_custom_css():
    """Load custom CSS for modern UI styling."""
    st.markdown("""
    <style>
        /* Main container styling */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
        }
        
        /* Card styling */
        .css-1r6slb0 {
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        /* Header styling */
        h1 {
            color: #2c3e50;
            font-weight: 700;
            text-align: center;
            margin-bottom: 2rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        h2 {
            color: #34495e;
            font-weight: 600;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.5rem;
            margin-top: 2rem;
        }
        
        h3 {
            color: #2c3e50;
            font-weight: 600;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
        }
        
        /* Input field styling */
        .stTextInput > div > div > input {
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            padding: 0.75rem;
            transition: border-color 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* Success message styling */
        .stSuccess {
            background: linear-gradient(135deg, #2ed573 0%, #26d0ce 100%);
            color: white;
            border-radius: 10px;
            padding: 1rem;
            font-weight: 600;
        }
        
        /* Error message styling */
        .stError {
            background: linear-gradient(135deg, #ff6b6b 0%, #ff4757 100%);
            color: white;
            border-radius: 10px;
            padding: 1rem;
            font-weight: 600;
        }
        
        /* Warning message styling */
        .stWarning {
            background: linear-gradient(135deg, #ffa502 0%, #ff6348 100%);
            color: white;
            border-radius: 10px;
            padding: 1rem;
        }
        
        /* Info message styling */
        .stInfo {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            border-radius: 10px;
            padding: 1rem;
        }
        
        /* Metric cards */
        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
        }
        
        /* Risk indicator */
        .risk-indicator {
            border-radius: 20px;
            padding: 0.5rem 1rem;
            font-weight: 700;
            text-align: center;
            color: white;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        
        /* Progress bar styling */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
        }
        
        /* Dataframe styling */
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: #f8f9fa;
            border-radius: 8px 8px 0 0;
            padding: 1rem 2rem;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
        }
        
        /* Animation for loading */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .loading-pulse {
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        /* Help tooltip styling */
        .help-icon {
            color: #667eea;
            cursor: help;
            font-size: 0.9em;
        }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Render the application header."""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">
            🏥 Advanced Health Assistant AI
        </h1>
        <p style="font-size: 1.2rem; color: #7f8c8d;">
            Multi-Disease Prediction & Risk Assessment Platform
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(title: str, value: str, subtitle: str = "", color: str = "#667eea"):
    """Render a metric card."""
    st.markdown(f"""
    <div class="metric-card" style="border-top: 4px solid {color};">
        <h3 style="margin: 0; color: #7f8c8d; font-size: 0.9rem;">{title}</h3>
        <p style="margin: 0.5rem 0; font-size: 2rem; font-weight: 700; color: {color};">{value}</p>
        <p style="margin: 0; font-size: 0.8rem; color: #95a5a6;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_risk_indicator(risk_level: str, color: str, probability: float):
    """Render a risk level indicator."""
    st.markdown(f"""
    <div class="risk-indicator" style="background-color: {color};">
        {risk_level} - {probability:.1%} Confidence
    </div>
    """, unsafe_allow_html=True)


def render_progress_bar(value: float, color: str = "#667eea"):
    """Render a custom progress bar."""
    percentage = int(value * 100)
    st.markdown(f"""
    <div style="background-color: #ecf0f1; border-radius: 10px; height: 20px; margin: 10px 0;">
        <div style="background: linear-gradient(90deg, {color} 0%, {color}aa 100%); 
                    width: {percentage}%; height: 100%; border-radius: 10px;
                    transition: width 0.5s ease;">
        </div>
    </div>
    <div style="text-align: center; font-weight: 600; color: {color};">{percentage}%</div>
    """, unsafe_allow_html=True)


def render_feature_importance_chart(feature_importance: Dict[str, float], top_n: int = 10):
    """Render a horizontal bar chart for feature importance."""
    sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    for feature, importance in sorted_features:
        percentage = importance * 100
        st.markdown(f"""
        <div style="margin: 8px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-weight: 600; color: #2c3e50;">{feature}</span>
                <span style="color: #7f8c8d;">{percentage:.1f}%</span>
            </div>
            <div style="background-color: #ecf0f1; border-radius: 5px; height: 12px;">
                <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                            width: {percentage}%; height: 100%; border-radius: 5px;">
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_recommendations_list(recommendations: List[str], risk_level: str):
    """Render health recommendations as a styled list."""
    color_map = {
        "low": "#2ed573",
        "moderate": "#ffa502",
        "high": "#ff4757"
    }
    color = color_map.get(risk_level.lower(), "#667eea")
    
    st.markdown(f"<h4 style='color: {color}; margin-top: 1.5rem;'>📋 Health Recommendations</h4>", unsafe_allow_html=True)
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"""
        <div style="display: flex; align-items: flex-start; margin: 10px 0; padding: 10px; 
                    background: #f8f9fa; border-radius: 8px; border-left: 4px solid {color};">
            <span style="background: {color}; color: white; border-radius: 50%; 
                        width: 24px; height: 24px; display: flex; align-items: center; 
                        justify-content: center; font-size: 0.8rem; margin-right: 10px; flex-shrink: 0;">
                {i}
            </span>
            <span style="color: #2c3e50;">{rec}</span>
        </div>
        """, unsafe_allow_html=True)


def render_prediction_history_table(history: List[Dict[str, Any]]):
    """Render prediction history in a styled table."""
    if not history:
        st.info("No predictions made yet in this session.")
        return
    
    for record in reversed(history[-10:]):  # Show last 10
        risk_color = {
            "Low Risk": "#2ed573",
            "Moderate Risk": "#ffa502",
            "High Risk": "#ff4757"
        }.get(record["risk_level"], "#667eea")
        
        st.markdown(f"""
        <div style="background: white; border-radius: 10px; padding: 15px; margin: 10px 0; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-left: 4px solid {risk_color};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="color: #2c3e50;">{record['disease_type'].title()}</strong>
                    <span style="color: #7f8c8d; font-size: 0.8rem; margin-left: 10px;">
                        {record['timestamp']}
                    </span>
                </div>
                <span style="background: {risk_color}; color: white; padding: 4px 12px; 
                            border-radius: 12px; font-size: 0.8rem; font-weight: 600;">
                    {record['risk_level']}
                </span>
            </div>
            <div style="margin-top: 8px; color: #7f8c8d; font-size: 0.9rem;">
                Prediction: <strong style="color: {risk_color};">{record['prediction']}</strong> 
                (Confidence: {record['probability']}%)
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_confidence_interval(lower: float, upper: float, probability: float):
    """Render confidence interval visualization."""
    lower_pct = int(lower * 100)
    upper_pct = int(upper * 100)
    prob_pct = int(probability * 100)
    
    st.markdown(f"""
    <div style="margin: 20px 0;">
        <p style="color: #7f8c8d; margin-bottom: 8px;">95% Confidence Interval</p>
        <div style="position: relative; height: 30px; background: #ecf0f1; border-radius: 15px;">
            <div style="position: absolute; left: {lower_pct}%; right: {100-upper_pct}%; 
                        height: 100%; background: linear-gradient(90deg, #667eea33 0%, #764ba233 100%); 
                        border-radius: 15px;">
            </div>
            <div style="position: absolute; left: {prob_pct}%; top: 50%; transform: translate(-50%, -50%); 
                        width: 12px; height: 12px; background: #667eea; border-radius: 50%; 
                        border: 3px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 5px; font-size: 0.8rem; color: #7f8c8d;">
            <span>{lower_pct}%</span>
            <span style="font-weight: 600; color: #667eea;">{prob_pct}% (Point Estimate)</span>
            <span>{upper_pct}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    """Render application footer."""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; margin-top: 3rem; 
                border-top: 1px solid #ecf0f1; color: #7f8c8d;">
        <p>🏥 Advanced Health Assistant AI | Built with ❤️ for better healthcare</p>
        <p style="font-size: 0.8rem;">
            ⚠️ <strong>Disclaimer:</strong> This tool is for educational purposes only. 
            Always consult qualified healthcare professionals for medical decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)
