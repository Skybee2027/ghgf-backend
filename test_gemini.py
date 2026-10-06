import os
import google.generativeai as genai

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("🎯 Testing gemini-3.8-flash...")
try:
    model = genai.GenerativeModel("gemini-3.8-flash")
    response = model.generate_content("Say hello in one sentence.")
    print(f"✅ Gemini API WORKING!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ ERROR: {e}")
