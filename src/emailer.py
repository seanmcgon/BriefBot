import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown

def build_html_email(content):
    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            .category { margin-bottom: 40px; }
            .title { font-size: 24px; font-weight: bold; color: #333; margin-bottom: 10px; }
            .links { font-size: 14px; margin-top: 10px; }
            .links a { color: #1a0dab; text-decoration: none; }
            .links a:hover { text-decoration: underline; }
            .text { white-space: pre-wrap; line-height: 1.5; font-size: 16px; color: #444; }
        </style>
    </head>
    <body>
        <h1>📰 Your Daily Brief</h1>
    """

    for category, data in content.items():
        html += f"""
        <div class="category">
            <div class="title">{category.upper()}</div>
            <div class="text">{markdown.markdown(data['text'])}</div>
            <div class="links">
                <b>Sources:</b><br>
                {''.join(f'<a href="{link}">{link}</a><br>' for link in data['links'])}
            </div>
        </div>
        """

    html += """
    </body>
    </html>
    """
    return html

def send_email(subject, html_body, from_email, to_email, smtp_server, smtp_port, login, password):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    html_part = MIMEText(html_body, 'html')
    msg.attach(html_part)

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(login, password)
        server.sendmail(from_email, to_email, msg.as_string())