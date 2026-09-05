import os
from google import genai
import datetime

def generate_post():
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY is missing!")
        return

    client = genai.Client(api_key=api_key)
    
    prompt = (
        "Write a captivating, viral, SEO-optimized blog post about a mysterious, dark, "
        "or forgotten historical event or hidden American urban legend suitable for a blog "
        "named Dark and Forgotten America. Format with a catchy Title on the very first line "
        "starting with 'TITLE: ', followed by a blank line, and then the detailed HTML body "
        "content using <h2> and <p> tags."
    )
    
    # सबसे सुरक्षित और लेटेस्ट मॉडल का इस्तेमाल
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        text = response.text.strip()
    except Exception as e:
        print(f"Primary failed, trying fallback: {e}")
        try:
            response = client.models.generate_content(
                model='gemini-2.5-pro',
                contents=prompt,
            )
            text = response.text.strip()
        except Exception as e2:
            print(f"All models failed: {e2}")
            return
            
    os.makedirs("posts", exist_ok=True)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"posts/post_{date_str}.html"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
        
    print(f"Article successfully saved to: {filename}")

if __name__ == "__main__":
    generate_post()
    
