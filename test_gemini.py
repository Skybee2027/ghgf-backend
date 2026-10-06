import os
import google.generativeai as genai

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("📋 Available Models:")
models = genai.list_models()
for m in models:
    if 'generateContent' in m.supported_generation_methods:
        print(f"✅ {m.name}")

print("\n🎯 Testing first available model...")
available = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
if available:
    model_name = available[0].split('/')[-1]
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Hello")
    print(f"✅ WORKING! Using: {model_name}")
else:
    print("❌ No models available")
