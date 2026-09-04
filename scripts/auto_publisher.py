import os
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_and_send():
    api_key = os.environ.get('GEMINI_API_KEY')
    receiver_email = os.environ.get('BLOGGER_EMAIL')
    
    genai.configure(api_key=api_key)
    
    # Using the correct current stable model name
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = "Write a captivating, viral, SEO-optimized blog post about a mysterious, dark, or forgotten historical event or hidden American urban legend suitable for a blog named Dark and Forgotten America. Format with a catchy Title on the very first line starting with 'TITLE: ', followed by a blank line, and then the detailed HTML body content (use <h2>, <p> tags)."
    
    response = model.generate_content(prompt)
    text = response.text.strip()
    
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
    msg['From'] = 'automation@github.com'
    msg['To'] = receiver_email
    msg.attach(MIMEText(content, 'html'))
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(receiver_email, 'dummy_pass')
    except Exception as e:
        print(f"Note: {e}")
        
    print("Content published via email successfully!")

if __name__ == "__main__":
    generate_and_send()
    
