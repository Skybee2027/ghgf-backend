import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import time

load_dotenv('/root/ghgf-backend/.env')

BOLD = '\033[1m'
RESET = '\033[0m'

class ComprehensiveAPIChecker:
    def __init__(self):
        self.results = {
            'text': {},
            'image': {},
            'affiliate': {},
        }

    def print_header(self, title):
        print(f"\n{'='*90}")
        print(f"{BOLD}{title}{RESET}")
        print('='*90)

    def check_groq(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print(f"❌ Groq                      ✗          [TEXT] No API key configured")
            self.results['text']['groq'] = False
            return

        try:
            from groq import Groq
            client = Groq(api_key=api_key)
            start = time.time()
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=10
            )
            elapsed = time.time() - start
            print(f"✅ Groq                      ✓          [TEXT] Connected successfully ({elapsed:.2f}s)")
            self.results['text']['groq'] = True
        except Exception as e:
            print(f"❌ Groq                      ✗          [TEXT] Error: {str(e)[:80]}")
            self.results['text']['groq'] = False

    def check_google(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print(f"❌ Google Gemini             ✗          [TEXT] No API key configured")
            self.results['text']['google'] = False
            return

        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            start = time.time()
            model = genai.GenerativeModel("models/gemini-3.5-flash")
            response = model.generate_content("test", stream=False)
            elapsed = time.time() - start
            print(f"✅ Google Gemini             ✓          [TEXT] Connected successfully ({elapsed:.2f}s)")
            self.results['text']['google'] = True
        except Exception as e:
            print(f"❌ Google Gemini             ✗          [TEXT] Error: {str(e)[:80]}")
            self.results['text']['google'] = False

    def check_cohere(self):
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            print(f"❌ Cohere                    ✗          [TEXT] No API key configured")
            self.results['text']['cohere'] = False
            return

        try:
            import cohere
            client = cohere.Client(api_key=api_key)
            start = time.time()
            # Simple test without max_tokens
            response = client.chat(message="test")
            elapsed = time.time() - start
            print(f"✅ Cohere                    ✓          [TEXT] Connected successfully ({elapsed:.2f}s)")
            self.results['text']['cohere'] = True
        except Exception as e:
            error_str = str(e)
            print(f"❌ Cohere                    ✗          [TEXT] Error: {error_str[:80]}")
            self.results['text']['cohere'] = False

    def check_openai(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print(f"❌ OpenAI                    ✗          [TEXT] No API key configured")
            self.results['text']['openai'] = False
            return

        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            start = time.time()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=10
            )
            elapsed = time.time() - start
            print(f"✅ OpenAI                    ✓          [TEXT] Connected successfully ({elapsed:.2f}s)")
            self.results['text']['openai'] = True
        except Exception as e:
            print(f"❌ OpenAI                    ✗          [TEXT] Error: {str(e)[:80]}")
            self.results['text']['openai'] = False

    def check_replicate(self):
        api_key = os.getenv("REPLICATE_API_KEY")
        if not api_key:
            print(f"❌ Replicate                 ✗          [IMAGE] No API key configured")
            self.results['image']['replicate'] = False
            return

        try:
            os.environ['REPLICATE_API_TOKEN'] = api_key
            import replicate
            start = time.time()
            models = replicate.models.list()
            elapsed = time.time() - start
            print(f"✅ Replicate                 ✓          [IMAGE] Connected successfully ({elapsed:.2f}s)")
            self.results['image']['replicate'] = True
        except Exception as e:
            print(f"❌ Replicate                 ✗          [IMAGE] Error: {str(e)[:80]}")
            self.results['image']['replicate'] = False

    def check_huggingface(self):
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not api_key:
            print(f"❌ Hugging Face              ✗          [IMAGE] No API key configured")
            self.results['image']['huggingface'] = False
            return

        try:
            from huggingface_hub import HfApi
            api = HfApi(token=api_key)
            start = time.time()
            user = api.whoami()
            elapsed = time.time() - start
            print(f"✅ Hugging Face              ✓          [IMAGE] Connected successfully ({elapsed:.2f}s)")
            self.results['image']['huggingface'] = True
        except Exception as e:
            print(f"❌ Hugging Face              ✗          [IMAGE] Error: {str(e)[:80]}")
            self.results['image']['huggingface'] = False

    def check_unsplash(self):
        api_key = os.getenv("UNSPLASH_API_KEY")
        if not api_key:
            print(f"❌ Unsplash                  ✗          [IMAGE] No API key configured")
            self.results['image']['unsplash'] = False
            return

        try:
            import requests
            headers = {"Authorization": f"Client-ID {api_key}"}
            response = requests.get("https://api.unsplash.com/users/me", headers=headers, timeout=5)
            if response.status_code == 200:
                print(f"✅ Unsplash                  ✓          [IMAGE] Connected successfully ({response.elapsed.total_seconds():.2f}s)")
                self.results['image']['unsplash'] = True
            else:
                print(f"❌ Unsplash                  ✗          [IMAGE] Invalid API key ({response.status_code})")
                self.results['image']['unsplash'] = False
        except Exception as e:
            print(f"❌ Unsplash                  ✗          [IMAGE] {str(e)[:80]}")
            self.results['image']['unsplash'] = False

    def check_pixabay(self):
        api_key = os.getenv("PIXABAY_API_KEY")
        if not api_key:
            print(f"❌ Pixabay                   ✗          [IMAGE] No API key configured")
            self.results['image']['pixabay'] = False
            return

        try:
            import requests
            response = requests.get(f"https://pixabay.com/api/?key={api_key}&q=test", timeout=5)
            if response.status_code == 200:
                print(f"✅ Pixabay                   ✓          [IMAGE] Connected successfully ({response.elapsed.total_seconds():.2f}s)")
                self.results['image']['pixabay'] = True
            else:
                print(f"❌ Pixabay                   ✗          [IMAGE] Invalid API key ({response.status_code})")
                self.results['image']['pixabay'] = False
        except Exception as e:
            print(f"❌ Pixabay                   ✗          [IMAGE] {str(e)[:80]}")
            self.results['image']['pixabay'] = False

    def check_cj_affiliate(self):
        api_key = os.getenv("CJ_AFFILIATE_API_KEY")
        if not api_key:
            print(f"❌ CJ Affiliate              ✗          [AFFILIATE] No API key configured")
            self.results['affiliate']['cj'] = False
            return

        try:
            import requests
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get("https://api.cj.com/v2/advertiser-lookup?website-url=example.com", headers=headers, timeout=5)
            if response.status_code in [200, 400]:
                print(f"✅ CJ Affiliate              ✓          [AFFILIATE] Connected successfully ({response.elapsed.total_seconds():.2f}s)")
                self.results['affiliate']['cj'] = True
            else:
                print(f"❌ CJ Affiliate              ✗          [AFFILIATE] Invalid API key ({response.status_code})")
                self.results['affiliate']['cj'] = False
        except Exception as e:
            print(f"❌ CJ Affiliate              ✗          [AFFILIATE] {str(e)[:80]}")
            self.results['affiliate']['cj'] = False

    def generate_summary(self):
        self.print_header("SUMMARY REPORT")

        for layer_name, layer_data in self.results.items():
            if layer_name == 'text':
                print(f"\n{BOLD}TEXT GENERATION LAYER:{RESET}")
            elif layer_name == 'image':
                print(f"\n{BOLD}IMAGE GENERATION LAYER:{RESET}")
            elif layer_name == 'affiliate':
                print(f"\n{BOLD}AFFILIATE NETWORKS LAYER:{RESET}")

            for service, status in layer_data.items():
                if status is True:
                    print(f"  ✅ {service.title()}")
                else:
                    print(f"  ❌ {service.title()}")

        total = sum(1 for layer in self.results.values() for s in layer.values() if s is True)
        total_all = sum(len(layer) for layer in self.results.values())
        print(f"\n{BOLD}TOTAL: {total}/{total_all} APIs working{RESET}")

    def run_all_checks(self):
        self.print_header("GHGF CORE API HEALTH CHECK")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        print(f"{BOLD}TEXT GENERATION LAYER:{RESET}")
        self.check_groq()
        self.check_google()
        self.check_cohere()
        self.check_openai()

        print(f"\n{BOLD}IMAGE GENERATION LAYER:{RESET}")
        self.check_replicate()
        self.check_huggingface()
        self.check_unsplash()
        self.check_pixabay()

        print(f"\n{BOLD}AFFILIATE NETWORKS LAYER:{RESET}")
        self.check_cj_affiliate()

        self.generate_summary()
        self.print_header("CHECK COMPLETE")

if __name__ == "__main__":
    checker = ComprehensiveAPIChecker()
    checker.run_all_checks()
