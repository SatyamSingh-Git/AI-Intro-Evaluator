"""
PDF Report Generator Module
Creates professional PDF reports for evaluation results
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime
import io

def generate_pdf_report(student_name, text_input, results, total_score):
    """
    Generate a professional PDF report
    
    Args:
        student_name: Name of the student
        text_input: The original introduction text
        results: Dictionary containing all evaluation results
        total_score: Overall score out of 100
        
    Returns:
        BytesIO object containing the PDF
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CustomTitle',
                             parent=styles['Heading1'],
                             fontSize=24,
                             textColor=colors.HexColor('#667eea'),
                             spaceAfter=30,
                             alignment=TA_CENTER,
                             fontName='Helvetica-Bold'))
    
    styles.add(ParagraphStyle(name='SectionHeader',
                             parent=styles['Heading2'],
                             fontSize=14,
                             textColor=colors.HexColor('#764ba2'),
                             spaceBefore=12,
                             spaceAfter=6,
                             fontName='Helvetica-Bold'))
    
    styles.add(ParagraphStyle(name='CustomBody',
                             parent=styles['BodyText'],
                             fontSize=10,
                             alignment=TA_LEFT))
    
    # Title
    title = Paragraph("AI Intro Evaluator Report", styles['CustomTitle'])
    elements.append(title)
    
    # Student info and date
    info_data = [
        ['Student Name:', student_name if student_name else 'N/A'],
        ['Date:', datetime.now().strftime('%B %d, %Y')],
        ['Overall Score:', f'{total_score}/100']
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#4B5563')),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Performance Overview
    elements.append(Paragraph("Performance Overview", styles['SectionHeader']))
    
    # Determine grade
    if total_score >= 90:
        grade = "A (Excellent)"
        grade_color = colors.HexColor('#10B981')
    elif total_score >= 80:
        grade = "B (Good)"
        grade_color = colors.HexColor('#3B82F6')
    elif total_score >= 70:
        grade = "C (Satisfactory)"
        grade_color = colors.HexColor('#F59E0B')
    elif total_score >= 60:
        grade = "D (Needs Improvement)"
        grade_color = colors.HexColor('#EF4444')
    else:
        grade = "F (Unsatisfactory)"
        grade_color = colors.HexColor('#991B1B')
    
    grade_data = [['Grade:', grade]]
    grade_table = Table(grade_data, colWidths=[2*inch, 4*inch])
    grade_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('TEXTCOLOR', (1, 0), (1, 0), grade_color),
    ]))
    elements.append(grade_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Score Breakdown
    elements.append(Paragraph("Detailed Score Breakdown", styles['SectionHeader']))
    
    score_data = [
        ['Category', 'Score', 'Max', 'Percentage'],
        ['Salutation', f"{results['salutation']['score']}", '5', f"{(results['salutation']['score']/5*100):.0f}%"],
        ['Keywords & Topics', f"{results['keywords']['score']}", '30', f"{(results['keywords']['score']/30*100):.0f}%"],
        ['Flow & Structure', f"{results['flow']['score']}", '5', f"{(results['flow']['score']/5*100):.0f}%"],
        ['Speech Rate', f"{results['speech_rate']['score']}", '10', f"{(results['speech_rate']['score']/10*100):.0f}%"],
        ['Grammar', f"{results['grammar']['score']}", '10', f"{(results['grammar']['score']/10*100):.0f}%"],
        ['Vocabulary', f"{results['vocabulary']['score']}", '10', f"{(results['vocabulary']['score']/10*100):.0f}%"],
        ['Clarity (Fillers)', f"{results['filler']['score']}", '15', f"{(results['filler']['score']/15*100):.0f}%"],
        ['Engagement', f"{results['sentiment']['score']}", '15', f"{(results['sentiment']['score']/15*100):.0f}%"],
        ['', 'Total:', f'{total_score}/100', '']
    ]
    
    score_table = Table(score_data, colWidths=[2.5*inch, 0.8*inch, 0.8*inch, 1.2*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('GRID', (0, 0), (-1, -2), 1, colors.black),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 11),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#667eea')),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#667eea')),
    ]))
    elements.append(score_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Key Metrics
    elements.append(Paragraph("Key Metrics", styles['SectionHeader']))
    
    # Calculate word count from text
    word_count = len(text_input.split())
    
    metrics_data = [
        ['Word Count:', f"{word_count}"],
        ['Speech Rate:', f"{results['speech_rate']['wpm']:.0f} WPM"],
        ['Grammar Errors:', f"{results['grammar']['count']}"],
        ['Filler Words:', f"{results['filler']['count']} ({results['filler']['rate']:.1f}%)"],
        ['Vocabulary Richness (TTR):', f"{results['vocabulary']['ttr']:.2f}"],
        ['Sentiment Score:', f"{results['sentiment']['positivity_score']:.2f}"],
    ]
    
    metrics_table = Table(metrics_data, colWidths=[2.5*inch, 3.5*inch])
    metrics_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9FAFB')),
    ]))
    elements.append(metrics_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Original Introduction Text
    elements.append(Paragraph("Your Introduction", styles['SectionHeader']))
    text_para = Paragraph(text_input.replace('\n', '<br/>'), styles['CustomBody'])
    elements.append(text_para)
    elements.append(Spacer(1, 0.3*inch))
    
    # Topics Coverage
    elements.append(Paragraph("Topics Coverage", styles['SectionHeader']))
    
    topics_data = [['Topic', 'Status']]
    for topic, found in results['keywords']['topics'].items():
        status = '✓ Found' if found else '✗ Missing'
        status_color = colors.HexColor('#10B981') if found else colors.HexColor('#EF4444')
        topics_data.append([topic.replace('_', ' '), status])
    
    topics_table = Table(topics_data, colWidths=[3*inch, 2*inch])
    topics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F9FAFB')),
    ]))
    
    # Color code the status column
    for i in range(1, len(topics_data)):
        is_found = results['keywords']['topics'][list(results['keywords']['topics'].keys())[i-1]]
        color = colors.HexColor('#10B981') if is_found else colors.HexColor('#EF4444')
        topics_table.setStyle(TableStyle([
            ('TEXTCOLOR', (1, i), (1, i), color),
            ('FONTNAME', (1, i), (1, i), 'Helvetica-Bold'),
        ]))
    
    elements.append(topics_table)
    elements.append(PageBreak())
    
    # Recommendations
    elements.append(Paragraph("Recommendations for Improvement", styles['SectionHeader']))
    
    from src.utils.feedback_generator import generate_comprehensive_feedback
    feedback_list = generate_comprehensive_feedback(results)
    
    if feedback_list:
        for idx, fb in enumerate(feedback_list[:8], 1):  # Limit to top 8
            severity_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(fb['severity'], '⚪')
            feedback_text = f"{severity_icon} <b>{fb['category']}:</b> {fb['issue']}<br/><i>Suggestion: {fb['suggestion']}</i>"
            feedback_para = Paragraph(feedback_text, styles['CustomBody'])
            elements.append(feedback_para)
            elements.append(Spacer(1, 0.15*inch))
    else:
        congrats_para = Paragraph("Excellent work! Your introduction is comprehensive and well-structured. Keep up the great work!", styles['CustomBody'])
        elements.append(congrats_para)
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer
    footer_style = ParagraphStyle(name='Footer',
                                 fontSize=8,
                                 textColor=colors.grey,
                                 alignment=TA_CENTER)
    footer = Paragraph(f"Generated by AI Intro Evaluator | {datetime.now().strftime('%Y-%m-%d %H:%M')}", footer_style)
    elements.append(Spacer(1, 0.5*inch))
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf
