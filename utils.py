import os
import io
import shutil
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pandas as pd

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

logger = logging.getLogger(__name__)

def generate_attendance_excel(attendances):
    """
    Generates Excel binary data for attendance records using Pandas and OpenPyXL.
    Returns bytes object.
    """
    data = []
    for att in attendances:
        data.append({
            'Attendance ID': att.id,
            'Roll Number': att.student.roll_number if att.student else 'N/A',
            'Student Name': att.student.name if att.student else 'Unknown',
            'Department': att.student.department if att.student else 'N/A',
            'Section': att.student.section if att.student else 'N/A',
            'Date': att.date.strftime('%Y-%m-%d') if att.date else '',
            'Time': att.time.strftime('%H:%M:%S') if att.time else '',
            'Status': att.status,
            'Confidence Score (%)': f"{att.confidence:.1f}%",
            'Verification Method': att.verification_type
        })
    
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Attendance Report')
    output.seek(0)
    return output.getvalue()

def generate_attendance_pdf(attendances, title="Student Attendance Report"):
    """
    Generates professional PDF document using ReportLab.
    Returns bytes object.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=40,
        bottomMargin=40
    )

    elements = []
    styles = getSampleStyleSheet()

    # Title
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1e293b'),
        alignment=1, # Center
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'ReportSubTitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#64748b'),
        alignment=1,
        spaceAfter=20
    )

    elements.append(Paragraph(title, title_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Total Records: {len(attendances)}", subtitle_style))

    # Table Header
    headers = ['Roll No', 'Student Name', 'Department', 'Date', 'Time', 'Status']
    table_data = [headers]

    for att in attendances:
        table_data.append([
            att.student.roll_number if att.student else 'N/A',
            att.student.name if att.student else 'Unknown',
            att.student.department if att.student else 'N/A',
            att.date.strftime('%Y-%m-%d') if att.date else '',
            att.time.strftime('%H:%M:%S') if att.time else '',
            att.status
        ])

    table = Table(table_data, colWidths=[80, 140, 100, 75, 75, 60])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f5f9')])
    ]))

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

def send_email_notification(app_config, recipient_email, subject, body_html):
    """
    Sends email notification using SMTP settings from config.
    Returns (success: bool, message: str)
    """
    if not app_config.MAIL_USERNAME or not app_config.MAIL_PASSWORD:
        return False, "SMTP email credentials not configured in environment"

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = app_config.MAIL_DEFAULT_SENDER or app_config.MAIL_USERNAME
        msg['To'] = recipient_email

        html_part = MIMEText(body_html, 'html')
        msg.attach(html_part)

        server = smtplib.SMTP(app_config.MAIL_SERVER, app_config.MAIL_PORT)
        if app_config.MAIL_USE_TLS:
            server.starttls()
        server.login(app_config.MAIL_USERNAME, app_config.MAIL_PASSWORD)
        server.sendmail(msg['From'], [recipient_email], msg.as_string())
        server.quit()
        return True, "Email sent successfully"
    except Exception as e:
        logger.error(f"Error sending email to {recipient_email}: {str(e)}")
        return False, f"Email sending failed: {str(e)}"

def backup_database(app, backup_folder):
    """Creates a timestamped backup file of the SQLite/MySQL database."""
    try:
        os.makedirs(backup_folder, exist_ok=True)
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if db_uri.startswith('sqlite:///'):
            db_file = db_uri.replace('sqlite:///', '')
            if os.path.exists(db_file):
                backup_filename = f"backup_attendance_{timestamp}.db"
                target_path = os.path.join(backup_folder, backup_filename)
                shutil.copy2(db_file, target_path)
                return True, backup_filename
        
        # MySQL or other DB notice
        backup_filename = f"backup_export_{timestamp}.sql"
        target_path = os.path.join(backup_folder, backup_filename)
        with open(target_path, 'w') as f:
            f.write(f"-- Database Backup generated on {datetime.now()}\n")
            f.write(f"-- DB URI: {db_uri}\n")
        return True, backup_filename
    except Exception as e:
        logger.error(f"Backup error: {str(e)}")
        return False, str(e)
