import os
import google.generativeai as genai

print("🔍 Testing Gemini API...")

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY not found")
    exit(1)

print("✅ API Key found")

genai.configure(api_key=api_key)
print("✅ Gemini configured")

try:
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content("Say hello in one sentence.")
    print(f"✅ Gemini API WORKING!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ ERROR: {e}")
    exit(1)
