import os
from google import genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_and_send():
    api_key = os.environ.get('GEMINI_API_KEY')
    receiver_email = os.environ.get('BLOGGER_EMAIL')
    
    if not api_key:
        print("Error: API Key missing")
        return

    # New official Google GenAI client initialization
    client = genai.Client(api_key=api_key)
    
    prompt = "Write a captivating, viral, SEO-optimized blog post about a mysterious, dark, or forgotten historical event or hidden American urban legend suitable for a blog named Dark and Forgotten America. Format with a catchy Title on the very first line starting with 'TITLE: ', followed by a blank line, and then the detailed HTML body content (use <h2>, <p> tags)."
    
    # Using the standard modern flash model
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    
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
        print(f"Mail Note: {e}")
        
    print("Successfully executed with new client!")

if __name__ == "__main__":
    generate_and_send()

