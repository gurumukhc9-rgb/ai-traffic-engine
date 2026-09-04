import os
import google.generativeai as genai

# Master Script Base v1.0 - Zero-Cost AI Content Engine
print("Initializing AI Content Engine...")

# Configure Gemini API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is missing!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

print("Gemini API configured successfully. Ready for content generation workflow.")
