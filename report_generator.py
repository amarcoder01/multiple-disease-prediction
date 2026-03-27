"""
PDF Report Generator for Multiple Disease Prediction System.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import io


def generate_prediction_report(
    disease_type: str,
    inputs: Dict[str, float],
    prediction: str,
    probability: float,
    risk_level: str,
    risk_color: str,
    recommendations: List[str],
    feature_importance: Optional[Dict[str, float]] = None
) -> bytes:
    """
    Generate a comprehensive PDF report for a prediction.
    
    Returns:
        PDF content as bytes
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    # Header
    elements.append(Paragraph("🏥 Advanced Health Assistant AI", title_style))
    elements.append(Paragraph("Disease Prediction Report", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Report metadata
    meta_data = [
        ['Report Generated:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        ['Disease Type:', disease_type.title()],
        ['Prediction ID:', f"PRED-{datetime.now().strftime('%Y%m%d%H%M%S')}"],
    ]
    
    meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Prediction Result Section
    elements.append(Paragraph("📊 Prediction Result", heading_style))
    
    # Risk level color mapping
    risk_color_map = {
        "Low Risk": colors.HexColor('#2ed573'),
        "Moderate Risk": colors.HexColor('#ffa502'),
        "High Risk": colors.HexColor('#ff4757'),
    }
    
    result_color = risk_color_map.get(risk_level, colors.HexColor('#667eea'))
    
    result_data = [
        ['Prediction Result:', prediction],
        ['Confidence Level:', f"{probability:.1%}"],
        ['Risk Assessment:', risk_level],
    ]
    
    result_table = Table(result_data, colWidths=[2*inch, 4*inch])
    result_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BACKGROUND', (1, 2), (1, 2), result_color),
        ('TEXTCOLOR', (1, 2), (1, 2), colors.white),
        ('FONTNAME', (1, 2), (1, 2), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(result_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Input Parameters Section
    elements.append(Paragraph("📋 Input Parameters", heading_style))
    
    input_data = [['Parameter', 'Value']]
    for param, value in inputs.items():
        input_data.append([param, f"{value:.4f}" if isinstance(value, float) else str(value)])
    
    input_table = Table(input_data, colWidths=[3*inch, 3*inch])
    input_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(input_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Feature Importance Section (if available)
    if feature_importance:
        elements.append(Paragraph("🔍 Key Contributing Factors", heading_style))
        
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:5]
        
        feature_data = [['Factor', 'Importance']]
        for feature, importance in sorted_features:
            feature_data.append([feature, f"{importance:.1%}"])
        
        feature_table = Table(feature_data, colWidths=[4*inch, 2*inch])
        feature_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(feature_table)
        elements.append(Spacer(1, 0.3*inch))
    
    # Recommendations Section
    elements.append(Paragraph("💡 Health Recommendations", heading_style))
    
    rec_items = []
    for i, rec in enumerate(recommendations, 1):
        rec_items.append(ListItem(Paragraph(rec, normal_style), bulletColor=result_color))
    
    rec_list = ListFlowable(rec_items, bulletType='1', start=1)
    elements.append(rec_list)
    elements.append(Spacer(1, 0.3*inch))
    
    # Disclaimer
    elements.append(Spacer(1, 0.2*inch))
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#7f8c8d'),
        alignment=TA_JUSTIFY,
        fontName='Helvetica-Oblique'
    )
    
    disclaimer_text = """
    <b>Disclaimer:</b> This prediction report is generated by an AI-based system for educational 
    and informational purposes only. It should NOT be considered as a substitute for professional 
    medical advice, diagnosis, or treatment. Always seek the guidance of qualified healthcare 
    providers with any questions you may have regarding your health condition. Never disregard 
    professional medical advice because of information you have received from this system.
    """
    elements.append(Paragraph(disclaimer_text, disclaimer_style))
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf


def generate_batch_report(
    disease_type: str,
    predictions: List[Dict[str, Any]]
) -> bytes:
    """
    Generate a batch prediction report.
    
    Returns:
        PDF content as bytes
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Header
    elements.append(Paragraph("🏥 Advanced Health Assistant AI", title_style))
    elements.append(Paragraph(f"Batch Prediction Report - {disease_type.title()}", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Summary statistics
    total = len(predictions)
    positive = sum(1 for p in predictions if p['prediction'] == 'Positive')
    negative = total - positive
    
    summary_data = [
        ['Report Generated:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        ['Total Predictions:', str(total)],
        ['Positive Cases:', str(positive)],
        ['Negative Cases:', str(negative)],
    ]
    
    summary_table = Table(summary_data, colWidths=[2.5*inch, 3.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Predictions table
    elements.append(Paragraph("📊 Prediction Results", heading_style))
    
    pred_data = [['#', 'Prediction', 'Confidence', 'Risk Level']]
    for i, pred in enumerate(predictions[:50], 1):  # Limit to 50 rows
        pred_data.append([
            str(i),
            pred['prediction'],
            f"{pred['probability']:.1f}%",
            pred['risk_level']
        ])
    
    pred_table = Table(pred_data, colWidths=[0.5*inch, 1.5*inch, 1.5*inch, 2*inch])
    pred_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(pred_table)
    
    # Disclaimer
    elements.append(Spacer(1, 0.3*inch))
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#7f8c8d'),
        alignment=TA_JUSTIFY,
        fontName='Helvetica-Oblique'
    )
    
    disclaimer_text = """
    <b>Disclaimer:</b> This batch prediction report is generated by an AI-based system for 
    educational purposes only. Always consult qualified healthcare professionals for medical decisions.
    """
    elements.append(Paragraph(disclaimer_text, disclaimer_style))
    
    # Build PDF
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf
