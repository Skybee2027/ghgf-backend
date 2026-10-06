import os
import google.generativeai as genai

print("🔍 Checking Gemini API...")

# Load API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY not found in environment")
    exit(1)

print("✅ API Key found")

# Configure Gemini
genai.configure(api_key=api_key)
print("✅ Gemini configured")

# List available models
print("\n📋 Available models:")
try:
    models = genai.list_models()
    available_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
    
    if available_models:
        for model in available_models:
            print(f"  ✓ {model}")
        
        # Use first available model
        model_name = available_models[0]
        print(f"\n🎯 Using model: {model_name}")
        
        # Test with the available model
        model = genai.GenerativeModel(model_name.split('/')[-1])
        response = model.generate_content("Say hello in one sentence.")
        
        print(f"✅ Gemini API WORKING!")
        print(f"Response: {response.text[:100]}...")
    else:
        print("❌ No models available for generateContent")
        
except Exception as e:
    print(f"❌ Error listing models: {e}")
