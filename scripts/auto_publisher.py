
    
import os
from google import genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_and_send():
    api_key = os.environ.get('GEMINI_API_KEY')
    sender_email = os.environ.get('BLOGGER_EMAIL')
    sender_password = os.environ.get('MAIL_APP_PASSWORD')
    
    blogger_email = "gurumukhc9.myblog2026@blogger.com"
    
    print(f"Checking Secrets -> GEMINI_API_KEY: {'Found' if api_key else 'Missing'}, BLOGGER_EMAIL: {'Found' if sender_email else 'Missing'}, MAIL_APP_PASSWORD: {'Found' if sender_password else 'Missing'}")
    
    if not api_key or not sender_email or not sender_password:
        print("Error: One or more required Secrets are missing in GitHub!")
        return

    client = genai.Client(api_key=api_key)
    
    prompt = (
        "Write a captivating, viral, SEO-optimized blog post about a mysterious, dark, "
        "or forgotten historical event or hidden American urban legend suitable for a blog "
        "named Dark and Forgotten America. Format with a catchy Title on the very first line "
        "starting with 'TITLE: ', followed by a blank line, and then the detailed HTML body "
        "content using <h2> and <p> tags."
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
        )
        text = response.text.strip()
    except Exception as e:
        print(f"Primary model failed, trying fallback: {e}")
        try:
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt,
            )
            text = response.text.strip()
        except Exception as e2:
            print(f"Both models failed: {e2}")
            return
    
    lines = text.split('\n')
    title = "Dark and Forgotten History Mystery"
    content = text
    
    for line in lines:
        if line.startswith("TITLE:"):
            title = line.replace("TITLE:", "").strip()
            content = text.replace(line, "").strip()
            break
            
    print(f"Generated Title: {title}")
    
    msg = MIMEMultipart()
    msg['Subject'] = title
    msg['From'] = sender_email
    msg['To'] = blogger_email
    msg.attach(MIMEText(content, 'html'))
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, blogger_email, msg.as_string())
        print("Email successfully sent to Blogger. Post will go live immediately!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    generate_and_send()
    
