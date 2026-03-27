"""
Advanced Multiple Disease Prediction System
Main application with enhanced features including:
- Input validation and error handling
- Prediction confidence scores
- Feature importance visualization
- Batch prediction from CSV
- PDF report generation
- Modern UI with custom styling
- Prediction history tracking
- Health recommendations
"""

import os
import pickle
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Import custom modules
from config import (
    PAGE_CONFIG, DISEASE_FEATURES, DISEASE_INFO, 
    FEATURE_IMPORTANCE, MODEL_PATHS
)
from utils import (
    validate_all_inputs, get_risk_level, create_prediction_record,
    generate_csv_template, validate_csv_data, calculate_confidence_interval,
    get_health_recommendations, log_prediction, sanitize_filename
)
from components import (
    load_custom_css, render_header, render_risk_indicator,
    render_feature_importance_chart, render_recommendations_list,
    render_prediction_history_table, render_confidence_interval,
    render_footer, render_metric_card, render_progress_bar
)
from report_generator import generate_prediction_report, generate_batch_report

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(**PAGE_CONFIG)

# Load custom CSS
load_custom_css()

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
def init_session_state():
    """Initialize session state variables."""
    if 'prediction_history' not in st.session_state:
        st.session_state.prediction_history = []
    if 'batch_results' not in st.session_state:
        st.session_state.batch_results = None
    if 'current_disease' not in st.session_state:
        st.session_state.current_disease = "diabetes"

init_session_state()

# ============================================================================
# MODEL LOADING WITH ERROR HANDLING
# ============================================================================
@st.cache_resource(show_spinner=False)
def load_models():
    """Load all prediction models with error handling."""
    models = {}
    errors = []
    
    for disease, path in MODEL_PATHS.items():
        try:
            if os.path.exists(path):
                models[disease] = pickle.load(open(path, 'rb'))
            else:
                errors.append(f"Model file not found: {path}")
                models[disease] = None
        except Exception as e:
            errors.append(f"Error loading {disease} model: {str(e)}")
            models[disease] = None
    
    return models, errors

models, model_errors = load_models()

# Display model loading errors if any
if model_errors:
    with st.sidebar.expander("⚠️ Model Status", expanded=False):
        for error in model_errors:
            st.warning(error)

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h2 style="color: white; margin: 0;">🏥 Health AI</h2>
        <p style="color: #bdc3c7; font-size: 0.8rem;">Advanced Disease Prediction</p>
    </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title='Prediction Modules',
        options=[
            'Diabetes Prediction',
            'Heart Disease Prediction', 
            'Parkinsons Prediction',
            'Batch Prediction',
            'Prediction History',
            'Analytics Dashboard'
        ],
        menu_icon='hospital-fill',
        icons=['activity', 'heart', 'person', 'upload', 'clock-history', 'graph-up'],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#2c3e50"},
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "padding": "12px",
                "margin": "4px 0",
                "border-radius": "8px",
                "color": "#bdc3c7",
            },
            "nav-link-selected": {
                "background-color": "#667eea",
                "color": "white",
                "font-weight": "600",
            },
        }
    )
    
    st.markdown("---")
    st.markdown("""
    <div style="padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
        <p style="color: #bdc3c7; font-size: 0.8rem; margin: 0;">
            📊 <strong style="color: white;">Predictions Made:</strong><br/>
            {} this session
        </p>
    </div>
    """.format(len(st.session_state.prediction_history)), unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def get_prediction_with_proba(model, input_data):
    """Get prediction and probability from model."""
    try:
        prediction = model.predict([input_data])[0]
        
        # Try to get probability if model supports it
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba([input_data])[0]
            probability = proba[1] if prediction == 1 else proba[0]
        else:
            # Fallback: use decision function or default
            probability = 0.75 if prediction == 1 else 0.75
            
        return int(prediction), float(probability)
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        return None, 0.0

def render_prediction_form(disease_type: str, features: list, model):
    """Render a prediction form for a disease type."""
    disease_info = DISEASE_INFO[disease_type]
    
    st.markdown(f"""
    <h2 style="color: {disease_info['color']};">
        {disease_info['name']} using ML
    </h2>
    <p style="color: #7f8c8d; margin-bottom: 2rem;">
        {disease_info['description']}
    </p>
    """, unsafe_allow_html=True)
    
    # Create input form
    inputs = {}
    errors = []
    
    # Calculate columns needed
    n_features = len(features)
    n_cols = 3 if n_features <= 15 else 5
    
    rows = [features[i:i+n_cols] for i in range(0, n_features, n_cols)]
    
    for row in rows:
        cols = st.columns(n_cols)
        for i, feature in enumerate(row):
            with cols[i]:
                value = st.text_input(
                    feature.name,
                    value="",
                    help=f"{feature.help_text}\n\nValid range: {feature.min_value} - {feature.max_value} {feature.unit}"
                )
                inputs[feature.name] = value
    
    # Validation and Prediction
    col1, col2 = st.columns([1, 2])
    
    with col1:
        predict_btn = st.button(
            f'🚀 Predict {disease_type.title()}',
            use_container_width=True,
            type="primary"
        )
    
    with col2:
        # Download template button
        template_csv = generate_csv_template(features)
        st.download_button(
            label="📥 Download CSV Template",
            data=template_csv,
            file_name=f'{disease_type}_template.csv',
            mime='text/csv',
            use_container_width=True
        )
    
    if predict_btn:
        # Validate inputs
        all_valid, converted_values, error_messages = validate_all_inputs(inputs, features)
        
        if not all_valid:
            st.error("⚠️ Please fix the following errors:")
            for error in error_messages:
                st.markdown(f"- {error}")
            return
        
        # Show spinner during prediction
        with st.spinner('🧠 Analyzing your health data...'):
            if model is None:
                st.error("❌ Model not loaded. Please check if model files exist.")
                return
            
            # Make prediction
            prediction, probability = get_prediction_with_proba(model, converted_values)
            
            if prediction is None:
                return
            
            # Log prediction
            log_prediction(disease_type, prediction, probability)
            
            # Determine risk level
            risk_info = get_risk_level(probability)
            
            # Calculate confidence interval
            ci_lower, ci_upper = calculate_confidence_interval(probability)
            
            # Get recommendations
            recommendations = get_health_recommendations(
                disease_type, 
                risk_info["label"].lower().replace(" risk", "")
            )
            
            # Create result record
            feature_names = [f.name for f in features]
            result_record = create_prediction_record(
                disease_type, converted_values, prediction, 
                probability, feature_names
            )
            st.session_state.prediction_history.append(result_record)
            
            # Display results
            st.markdown("---")
            st.markdown("### 📊 Prediction Results")
            
            # Result columns
            res_col1, res_col2, res_col3 = st.columns(3)
            
            with res_col1:
                render_metric_card(
                    "Prediction",
                    "Positive" if prediction == 1 else "Negative",
                    f"for {disease_type.title()}",
                    disease_info['color']
                )
            
            with res_col2:
                render_metric_card(
                    "Confidence",
                    f"{probability:.1%}",
                    "Model confidence",
                    risk_info['color']
                )
            
            with res_col3:
                render_metric_card(
                    "Risk Level",
                    risk_info['label'],
                    "Based on confidence",
                    risk_info['color']
                )
            
            # Risk indicator
            st.markdown("---")
            result_text = f"The person {'IS' if prediction == 1 else 'is NOT'} likely to have {disease_type} disease"
            
            if prediction == 1:
                st.error(f"⚠️ {result_text}")
            else:
                st.success(f"✅ {result_text}")
            
            # Confidence interval visualization
            render_confidence_interval(ci_lower, ci_upper, probability)
            
            # Feature importance
            if disease_type in FEATURE_IMPORTANCE:
                with st.expander("🔍 Key Contributing Factors", expanded=True):
                    render_feature_importance_chart(
                        FEATURE_IMPORTANCE[disease_type], 
                        top_n=8
                    )
            
            # Health recommendations
            render_recommendations_list(recommendations, risk_info['label'].lower().replace(' risk', ''))
            
            # Download report button
            report_pdf = generate_prediction_report(
                disease_type=disease_type,
                inputs=dict(zip(feature_names, converted_values)),
                prediction="Positive" if prediction == 1 else "Negative",
                probability=probability,
                risk_level=risk_info['label'],
                risk_color=risk_info['color'],
                recommendations=recommendations,
                feature_importance=FEATURE_IMPORTANCE.get(disease_type)
            )
            
            st.download_button(
                label="📄 Download Detailed Report (PDF)",
                data=report_pdf,
                file_name=f"{disease_type}_prediction_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# ============================================================================
# MAIN PAGES
# ============================================================================

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.session_state.current_disease = "diabetes"
    render_prediction_form("diabetes", DISEASE_FEATURES["diabetes"], models.get("diabetes"))

# Heart Disease Prediction Page
elif selected == 'Heart Disease Prediction':
    st.session_state.current_disease = "heart"
    render_prediction_form("heart", DISEASE_FEATURES["heart"], models.get("heart"))

# Parkinson's Prediction Page
elif selected == 'Parkinsons Prediction':
    st.session_state.current_disease = "parkinsons"
    render_prediction_form("parkinsons", DISEASE_FEATURES["parkinsons"], models.get("parkinsons"))

# Batch Prediction Page
elif selected == 'Batch Prediction':
    st.markdown("""
    <h2>📤 Batch Prediction</h2>
    <p style="color: #7f8c8d; margin-bottom: 2rem;">
        Upload a CSV file with multiple patient records for bulk prediction.
    </p>
    """, unsafe_allow_html=True)
    
    # Disease selection for batch
    batch_disease = st.selectbox(
        "Select Disease for Batch Prediction",
        ["diabetes", "heart", "parkinsons"],
        format_func=lambda x: DISEASE_INFO[x]['name']
    )
    
    features = DISEASE_FEATURES[batch_disease]
    
    # Show template info
    with st.expander("📋 CSV Format Requirements", expanded=True):
        st.markdown("Your CSV file must contain the following columns:")
        
        req_cols = pd.DataFrame({
            'Column Name': [f.name for f in features],
            'Description': [f.description for f in features],
            'Min': [f.min_value for f in features],
            'Max': [f.max_value for f in features],
            'Unit': [f.unit for f in features]
        })
        st.dataframe(req_cols, use_container_width=True)
        
        # Download template
        template_csv = generate_csv_template(features)
        st.download_button(
            label="📥 Download CSV Template",
            data=template_csv,
            file_name=f'{batch_disease}_batch_template.csv',
            mime='text/csv'
        )
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload CSV file",
        type=['csv'],
        help="Upload a CSV file with patient data"
    )
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Validate CSV
            is_valid, errors = validate_csv_data(df, features)
            
            if not is_valid:
                st.error("❌ CSV Validation Failed:")
                for error in errors:
                    st.markdown(f"- {error}")
            else:
                st.success(f"✅ Valid CSV with {len(df)} records")
                
                # Preview data
                with st.expander("📊 Data Preview", expanded=False):
                    st.dataframe(df.head(10), use_container_width=True)
                
                # Run batch prediction
                if st.button("🚀 Run Batch Prediction", type="primary"):
                    with st.spinner(f'Processing {len(df)} records...'):
                        model = models.get(batch_disease)
                        
                        if model is None:
                            st.error("❌ Model not available")
                        else:
                            results = []
                            feature_names = [f.name for f in features]
                            
                            for idx, row in df.iterrows():
                                input_data = [float(row[f.name]) for f in features]
                                prediction, probability = get_prediction_with_proba(model, input_data)
                                
                                if prediction is not None:
                                    risk_info = get_risk_level(probability)
                                    
                                    results.append({
                                        'row': idx + 1,
                                        'prediction': 'Positive' if prediction == 1 else 'Negative',
                                        'probability': round(probability * 100, 2),
                                        'risk_level': risk_info['label']
                                    })
                            
                            # Store results
                            st.session_state.batch_results = {
                                'disease': batch_disease,
                                'results': results
                            }
                            
                            # Display results
                            st.markdown("---")
                            st.markdown("### 📊 Batch Prediction Results")
                            
                            # Summary metrics
                            total = len(results)
                            positive = sum(1 for r in results if r['prediction'] == 'Positive')
                            negative = total - positive
                            
                            met_col1, met_col2, met_col3 = st.columns(3)
                            with met_col1:
                                render_metric_card("Total Records", str(total), "Processed")
                            with met_col2:
                                render_metric_card("Positive Cases", str(positive), f"{positive/total*100:.1f}%")
                            with met_col3:
                                render_metric_card("Negative Cases", str(negative), f"{negative/total*100:.1f}%")
                            
                            # Results table
                            results_df = pd.DataFrame(results)
                            st.dataframe(results_df, use_container_width=True)
                            
                            # Download batch report
                            batch_pdf = generate_batch_report(batch_disease, results)
                            st.download_button(
                                label="📄 Download Batch Report (PDF)",
                                data=batch_pdf,
                                file_name=f"{batch_disease}_batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                            
                            # Download CSV results
                            csv_results = results_df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download Results (CSV)",
                                data=csv_results,
                                file_name=f"{batch_disease}_batch_results.csv",
                                mime="text/csv"
                            )
                            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

# Prediction History Page
elif selected == 'Prediction History':
    st.markdown("""
    <h2>⏰ Prediction History</h2>
    <p style="color: #7f8c8d; margin-bottom: 2rem;">
        View all predictions made during this session.
    </p>
    """, unsafe_allow_html=True)
    
    history = st.session_state.prediction_history
    
    if not history:
        st.info("📭 No predictions made yet in this session.")
    else:
        # Summary stats
        total = len(history)
        by_disease = {}
        risk_counts = {"Low Risk": 0, "Moderate Risk": 0, "High Risk": 0}
        
        for record in history:
            disease = record['disease_type']
            by_disease[disease] = by_disease.get(disease, 0) + 1
            risk_counts[record['risk_level']] = risk_counts.get(record['risk_level'], 0) + 1
        
        # Display stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            render_metric_card("Total Predictions", str(total), "This session")
        with col2:
            render_metric_card("Low Risk", str(risk_counts['Low Risk']), "Predictions", "#2ed573")
        with col3:
            render_metric_card("Moderate Risk", str(risk_counts['Moderate Risk']), "Predictions", "#ffa502")
        with col4:
            render_metric_card("High Risk", str(risk_counts['High Risk']), "Predictions", "#ff4757")
        
        # Disease breakdown chart
        if by_disease:
            st.markdown("### 📊 Predictions by Disease Type")
            disease_df = pd.DataFrame([
                {'Disease': k.title(), 'Count': v} 
                for k, v in by_disease.items()
            ])
            
            fig = px.bar(
                disease_df, 
                x='Disease', 
                y='Count',
                color='Disease',
                color_discrete_sequence=['#667eea', '#764ba2', '#f093fb']
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # History table
        st.markdown("### 📋 Prediction Details")
        render_prediction_history_table(history)
        
        # Clear history button
        if st.button("🗑️ Clear History", type="secondary"):
            st.session_state.prediction_history = []
            st.rerun()

# Analytics Dashboard Page
elif selected == 'Analytics Dashboard':
    st.markdown("""
    <h2>📈 Analytics Dashboard</h2>
    <p style="color: #7f8c8d; margin-bottom: 2rem;">
        Model performance metrics and feature analysis.
    </p>
    """, unsafe_allow_html=True)
    
    # Model accuracy overview
    st.markdown("### 🎯 Model Performance")
    
    accuracy_data = []
    for disease, info in DISEASE_INFO.items():
        accuracy_data.append({
            'Disease': info['name'],
            'Accuracy': info['accuracy'] * 100,
            'Model Type': info['model_type'],
            'Color': info['color']
        })
    
    acc_df = pd.DataFrame(accuracy_data)
    
    # Performance gauge chart
    fig = go.Figure()
    
    for i, row in acc_df.iterrows():
        fig.add_trace(go.Bar(
            name=row['Disease'],
            x=[row['Disease']],
            y=[row['Accuracy']],
            text=f"{row['Accuracy']:.0f}%",
            textposition='auto',
            marker_color=row['Color'],
            hovertemplate=f"Model: {row['Model Type']}<br>Accuracy: {row['Accuracy']:.1f}%<extra></extra>"
        ))
    
    fig.update_layout(
        title="Model Accuracy Comparison",
        yaxis_title="Accuracy (%)",
        yaxis_range=[0, 100],
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Feature importance comparison
    st.markdown("### 🔍 Feature Importance Analysis")
    
    for disease in ['diabetes', 'heart', 'parkinsons']:
        if disease in FEATURE_IMPORTANCE:
            with st.expander(f"{DISEASE_INFO[disease]['name']} - Top Features", expanded=False):
                render_feature_importance_chart(FEATURE_IMPORTANCE[disease], top_n=8)
    
    # Usage statistics
    history = st.session_state.prediction_history
    if history:
        st.markdown("### 📊 Session Activity")
        
        # Timeline of predictions
        timeline_df = pd.DataFrame([
            {
                'Time': datetime.strptime(h['timestamp'], "%Y-%m-%d %H:%M:%S"),
                'Disease': h['disease_type'].title(),
                'Risk Level': h['risk_level']
            }
            for h in history
        ])
        
        if not timeline_df.empty:
            fig = px.scatter(
                timeline_df,
                x='Time',
                y='Disease',
                color='Risk Level',
                color_discrete_map={
                    'Low Risk': '#2ed573',
                    'Moderate Risk': '#ffa502',
                    'High Risk': '#ff4757'
                },
                size=[20] * len(timeline_df),
                title="Prediction Timeline"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================
render_footer()
