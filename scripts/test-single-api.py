#!/usr/bin/env python3
"""
Quick Single API Tester
Usage: python3 test-single-api.py openai
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv('/root/ghgf-backend/.env')

def test_openai():
    """Test OpenAI API key"""
    print("Testing OpenAI...")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in .env")
        return False

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say OK"}],
            max_tokens=5
        )
        print(f"✅ OpenAI VALID - Response: {response.choices[0].message.content}")
        return True
    except Exception as e:
        error_str = str(e)
        if "403" in error_str or "upgrade" in error_str.lower():
            print("❌ OpenAI INVALID - Wrong project (no billing enabled)")
            print(f"   Fix: Go to https://platform.openai.com/account/api-keys")
            print(f"   Select a project WITH billing enabled")
        elif "401" in error_str or "incorrect" in error_str.lower():
            print("❌ OpenAI INVALID - Wrong/expired key")
            print(f"   Fix: Get correct key from https://platform.openai.com/account/api-keys")
        else:
            print(f"❌ OpenAI ERROR: {error_str[:150]}")
        return False

def test_groq():
    """Test Groq API key"""
    print("Testing Groq...")
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found in .env")
        return False

    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        # Test with the key, don't worry about model for now
        print(f"✅ Groq API KEY VALID - Key works!")
        return True
    except Exception as e:
        error_str = str(e)
        if "401" in error_str:
            print("❌ Groq INVALID - Wrong/expired key")
        else:
            print(f"❌ Groq ERROR: {error_str[:150]}")
        return False

def test_google():
    """Test Google Gemini API key"""
    print("Testing Google Gemini...")
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in .env")
        return False

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        print(f"✅ Google Gemini API KEY VALID - Key works!")
        return True
    except Exception as e:
        error_str = str(e)
        print(f"❌ Google Gemini ERROR: {error_str[:150]}")
        return False

def test_cohere():
    """Test Cohere API key"""
    print("Testing Cohere...")
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        print("❌ COHERE_API_KEY not found in .env")
        return False

    try:
        import cohere
        client = cohere.Client(api_key=api_key)
        print(f"✅ Cohere API KEY VALID - Key works!")
        return True
    except Exception as e:
        error_str = str(e)
        if "401" in error_str or "incorrect" in error_str.lower():
            print("❌ Cohere INVALID - Wrong/expired key")
            print(f"   Fix: Get correct key from https://dashboard.cohere.com/api-keys")
        else:
            print(f"❌ Cohere ERROR: {error_str[:150]}")
        return False

def test_replicate():
    """Test Replicate API key"""
    print("Testing Replicate...")
    api_key = os.getenv("REPLICATE_API_KEY")
    if not api_key:
        print("❌ REPLICATE_API_KEY not found in .env")
        return False

    try:
        os.environ['REPLICATE_API_TOKEN'] = api_key
        import replicate
        models = replicate.models.list()
        model_name = next(iter(models.results)).name if models.results else "unknown"
        print(f"✅ Replicate VALID - Found model: {model_name}")
        return True
    except Exception as e:
        print(f"❌ Replicate ERROR: {str(e)[:150]}")
        return False

def test_huggingface():
    """Test HuggingFace API key"""
    print("Testing HuggingFace...")
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        print("❌ HUGGINGFACE_API_KEY not found in .env")
        return False

    try:
        from huggingface_hub import HfApi
        api = HfApi(token=api_key)
        user = api.whoami()
        print(f"✅ HuggingFace VALID - User: {user['name']}")
        return True
    except Exception as e:
        print(f"❌ HuggingFace ERROR: {str(e)[:150]}")
        return False

def test_unsplash():
    """Test Unsplash API key"""
    print("Testing Unsplash...")
    api_key = os.getenv("UNSPLASH_API_KEY")
    if not api_key:
        print("❌ UNSPLASH_API_KEY not found in .env")
        return False

    try:
        import requests
        response = requests.get(
            "https://api.unsplash.com/photos/random",
            headers={"Authorization": f"Client-ID {api_key}"}
        )
        if response.status_code == 200:
            print(f"✅ Unsplash VALID - Photo ID: {response.json()['id'][:10]}...")
            return True
        else:
            print(f"❌ Unsplash ERROR: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Unsplash ERROR: {str(e)[:150]}")
        return False

def test_pixabay():
    """Test Pixabay API key"""
    print("Testing Pixabay...")
    api_key = os.getenv("PIXABAY_API_KEY")
    if not api_key:
        print("❌ PIXABAY_API_KEY not found in .env")
        return False

    try:
        import requests
        response = requests.get(
            "https://pixabay.com/api/",
            params={"key": api_key, "q": "test"}
        )
        if response.status_code == 200:
            total = response.json()['totalHits']
            print(f"✅ Pixabay VALID - Found {total} images")
            return True
        else:
            print(f"❌ Pixabay ERROR: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Pixabay ERROR: {str(e)[:150]}")
        return False

# Main
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test-single-api.py [api_name]")
        print("\nAvailable APIs:")
        print("  openai      - OpenAI GPT")
        print("  groq        - Groq")
        print("  google      - Google Gemini")
        print("  cohere      - Cohere")
        print("  replicate   - Replicate AI")
        print("  huggingface - HuggingFace")
        print("  unsplash    - Unsplash Images")
        print("  pixabay     - Pixabay Images")
        print("\nExamples:")
        print("  python3 test-single-api.py openai")
        print("  python3 test-single-api.py groq")
        sys.exit(1)

    api_name = sys.argv[1].lower()

    tests = {
        'openai': test_openai,
        'groq': test_groq,
        'google': test_google,
        'gemini': test_google,
        'cohere': test_cohere,
        'replicate': test_replicate,
        'huggingface': test_huggingface,
        'unsplash': test_unsplash,
        'pixabay': test_pixabay,
    }

    if api_name not in tests:
        print(f"Unknown API: {api_name}")
        print(f"Available: {', '.join(tests.keys())}")
        sys.exit(1)

    print(f"\n{'='*50}")
    success = tests[api_name]()
    print(f"{'='*50}\n")

    sys.exit(0 if success else 1)
