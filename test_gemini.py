#!/usr/bin/env python3
"""Test Gemini API connectivity"""

import os
import sys

try:
    import google.generativeai as genai
    
    # Get API key from environment
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        sys.exit(1)
    
    print("✅ API Key found")
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    print("✅ Gemini configured")
    
    # Test API call
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say hello in one sentence.")
    
    print("✅ Gemini API WORKING!")
    print(f"✅ Response: {response.text}")
    print("\n🎉 SUCCESS - Gemini API is fully functional!")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
