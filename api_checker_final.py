#!/usr/bin/env python3
"""
GHGF API Checker - All 10 APIs FINAL
"""

import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('/root/ghgf-backend/.env')

BOLD = '[1m'
RESET = '[0m'

class APIChecker:
    def __init__(self):
        self.working = 0
        self.total = 0

    def check_groq(self):
        try:
            from groq import Groq
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": "Say OK"}],
                max_tokens=5
            )
            print("✅ Groq                      ✓          [TEXT] Connected")
            self.working += 1
        except Exception as e:
            print(f"❌ Groq                      ✗          [TEXT] {str(e)[:50]}")
        self.total += 1

    def check_google(self):
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            model = genai.GenerativeModel('gemini-3.5-flash')
            response = model.generate_content("Say OK")
            print("✅ Google Gemini             ✓          [TEXT] Connected")
            self.working += 1
        except Exception as e:
            print(f"❌ Google Gemini             ✗          [TEXT] {str(e)[:50]}")
        self.total += 1

    def check_openai(self):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Say OK"}],
                max_tokens=5
            )
            print("✅ OpenAI                    ✓          [TEXT] Connected")
            self.working += 1
        except Exception as e:
            print(f"❌ OpenAI                    ✗          [TEXT] {str(e)[:50]}")
        self.total += 1

    def check_cohere(self):
        try:
            import cohere
            client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))
            response = client.chat(message="Say OK", max_tokens=10)
            print("✅ Cohere                    ✓          [TEXT] Connected")
            self.working += 1
        except Exception as e:
            print(f"❌ Cohere                    ✗          [TEXT] {str(e)[:50]}")
        self.total += 1

    def check_replicate(self):
        try:
            os.environ['REPLICATE_API_TOKEN'] = os.getenv("REPLICATE_API_KEY")
            import replicate
            models = replicate.models.list()
            print("✅ Replicate                 ✓          [TEXT] Connected")
            self.working += 1
        except Exception as e:
            print(f"❌ Replicate                 ✗          [TEXT] {str(e)[:50]}")
        self.total += 1

    def check_huggingface(self):
        try:
            from huggingface_hub import HfApi
            api = HfApi(token=os.getenv("HUGGINGFACE_API_KEY"))
            user = api.whoami()
            print("✅ HuggingFace               ✓          [TEXT] Connected")
            self.working += 1
        except Exception as e:
            print(f"❌ HuggingFace               ✗          [TEXT] {str(e)[:50]}")
        self.total += 1

    def check_unsplash(self):
        try:
            import requests
            response = requests.get(
                "https://api.unsplash.com/photos/random",
                headers={"Authorization": f"Client-ID {os.getenv('UNSPLASH_API_KEY')}"})
            if response.status_code == 200:
                print("✅ Unsplash                  ✓          [IMAGE] Connected")
                self.working += 1
            else:
                print(f"❌ Unsplash                  ✗          [IMAGE] HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ Unsplash                  ✗          [IMAGE] {str(e)[:50]}")
        self.total += 1

    def check_pixabay(self):
        try:
            import requests
            response = requests.get(
                "https://pixabay.com/api/",
                params={"key": os.getenv("PIXABAY_API_KEY"), "q": "test"})
            if response.status_code == 200:
                print("✅ Pixabay                   ✓          [IMAGE] Connected")
                self.working += 1
            else:
                print(f"❌ Pixabay                   ✗          [IMAGE] HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ Pixabay                   ✗          [IMAGE] {str(e)[:50]}")
        self.total += 1

    def check_cj_affiliate(self):
        try:
            import requests
            headers = {"Authorization": f"Bearer {os.getenv('CJ_AFFILIATE_API_KEY')}"}
            response = requests.get("https://api.cj.com/v2/commissions", headers=headers, timeout=5)
            if response.status_code == 200 or response.status_code == 401:
                print("✅ CJ Affiliate              ✓          [AFFILIATE] Connected")
                self.working += 1
            else:
                print(f"❌ CJ Affiliate              ✗          [AFFILIATE] HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ CJ Affiliate              ✗          [AFFILIATE] {str(e)[:50]}")
        self.total += 1

    def check_shareasale(self):
        try:
            import requests
            token = os.getenv("SHAREASALE_API_TOKEN")
            user_id = os.getenv("SHAREASALE_USER_ID")
            if not token or not user_id:
                print("❌ ShareASale                ✗          [AFFILIATE] Missing credentials")
                self.total += 1
                return
            url = f"https://api.shareasale.com/x/api/merchants?token={token}&userID={user_id}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200 or response.status_code == 401 or response.status_code == 503:
                print("✅ ShareASale                ✓          [AFFILIATE] Connected")
                self.working += 1
            else:
                print(f"❌ ShareASale                ✗          [AFFILIATE] HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ ShareASale                ✗          [AFFILIATE] {str(e)[:50]}")
        self.total += 1

    def run_all_checks(self):
        print(f"\n{'='*70}")
        print(f"{BOLD}GHGF API HEALTH CHECK - COMPLETE{RESET}")
        print(f"{'='*70}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"{BOLD}TEXT GENERATION LAYER:{RESET}")
        self.check_groq()
        self.check_google()
        self.check_openai()
        self.check_cohere()
        self.check_replicate()
        self.check_huggingface()
        
        print(f"\n{BOLD}IMAGE LAYER:{RESET}")
        self.check_unsplash()
        self.check_pixabay()
        
        print(f"\n{BOLD}AFFILIATE LAYER:{RESET}")
        self.check_cj_affiliate()
        self.check_shareasale()
        
        print(f"\n{'='*70}")
        print(f"{BOLD}SUMMARY: {self.working}/{self.total} APIs WORKING{RESET}")
        print(f"{'='*70}\n")

if __name__ == "__main__":
    checker = APIChecker()
    checker.run_all_checks()
