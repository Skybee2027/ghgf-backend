import os
import google.generativeai as genai

# Get API key from environment
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in environment")
    exit(1)

try:
    # Configure Gemini
    genai.configure(api_key=api_key)
    
    # Test API call
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say 'Hello, GHGF System!' in one sentence.")
    
    print("✅ Gemini API is WORKING!")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"❌ Gemini API Error: {e}")
    exit(1)
