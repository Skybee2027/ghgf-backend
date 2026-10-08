#!/usr/bin/env python3
import os, sys, time
from dotenv import load_dotenv
load_dotenv()

def test_groq():
    try:
        from groq import Groq
        key = os.getenv('GROQ_API_KEY')
        if not key: return False, "No API key"
        client = Groq(api_key=key)
        start = time.time()
        response = client.chat.completions.create(model="mixtral-8x7b-32768", messages=[{"role": "user", "content": "Say OK"}], max_tokens=10)
        latency = time.time() - start
        return True, f"{latency:.2f}s"
    except Exception as e: return False, str(e)[:50]

def test_google():
    try:
        import google.generativeai as genai
        key = os.getenv('GOOGLE_API_KEY')
        if not key: return False, "No API key"
        genai.configure(api_key=key)
        start = time.time()
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Say OK")
        latency = time.time() - start
        return True, f"{latency:.2f}s"
    except Exception as e: return False, str(e)[:50]

def test_openai():
    try:
        from openai import OpenAI
        key = os.getenv('OPENAI_API_KEY')
        if not key: return False, "No API key"
        client = OpenAI(api_key=key)
        start = time.time()
        response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": "Say OK"}], max_tokens=10)
        latency = time.time() - start
        return True, f"{latency:.2f}s"
    except Exception as e: return False, str(e)[:50]

def print_header(title):
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)

def print_result(name, success, detail):
    symbol = "✓" if success else "✗"
    status = "OK" if success else "FAILED"
    print(f"  {symbol} {name:20} {status:10} {detail}")

def main():
    print_header("PHASE 2: API HEALTH CHECK")
    tests = [("Groq", test_groq), ("Google Gemini", test_google), ("OpenAI GPT", test_openai)]
    results = []
    print("\nTesting configured API providers...\n")
    for name, test_func in tests:
        success, detail = test_func()
        results.append(success)
        print_result(name, success, detail)
    print_header("HEALTH CHECK RESULTS")
    working = sum(results)
    total = len(results)
    print(f"\n  {working}/{total} API providers working")
    if working > 0:
        print("\n✓ System has at least one working AI provider")
        return True
    else:
        print("\n❌ No working AI providers found!")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
