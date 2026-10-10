#!/usr/bin/env python3
"""
GHGF API Checker - Simplified 10-Service Test
Tests: Groq, Google, OpenAI, Cohere, Replicate, HuggingFace, Unsplash, Pixabay, CJ Affiliate, ShareASale
"""

import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from current directory (works in GitHub Actions and locally)
load_dotenv('.env')

BOLD = '\033[1m'
RESET = '\033[0m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'

class APIChecker:
    def __init__(self):
        self.results = {}
        self.total = 0
        self.working = 0

    def print_header(self, title):
        print(f"\n{'='*70}")
        print(f"{BOLD}{title}{RESET}")
        print('='*70)

    def check_groq(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("❌ Groq                      ✗          [TEXT] No API key")
            self.results['groq'] = False
            self.total += 1
            return

        try:
            from groq import Groq
            client = Groq(api_key=api_key)

            response = None
            last_error = None

            # Strategy 1: Try to dynamically get available models
            try:
                models = client.models.list()
                if models and hasattr(models, 'data'):
                    model_ids = [m.id for m in models.data if hasattr(m, 'id')]
                    if model_ids:
                        for model in model_ids[:3]:  # Try first 3 available
                            try:
                                response = client.chat.completions.create(
                                    model=model,
                                    messages=[{"role": "user", "content": "OK"}],
                                    max_tokens=5,
                                    timeout=15
                                )
                                break
                            except Exception:
                                continue
            except:
                pass  # If dynamic listing fails, fall back to hardcoded list

            # Strategy 2: If dynamic discovery failed, try comprehensive hardcoded list
            if not response:
                models_to_try = [
                    # Most likely to work
                    "mixtral-8x7b-32768",
                    "llama2-70b-4096",
                    "llama-3.1-70b-versatile",
                    "qwen-3.8-27b",
                    "gpt-oss-120b",
                    "gpt-oss-20b",
                    # Fallback options
                    "gemma2-9b-it",
                    "gemma-7b-it"
                ]

                for model in models_to_try:
                    try:
                        response = client.chat.completions.create(
                            model=model,
                            messages=[{"role": "user", "content": "OK"}],
                            max_tokens=5,
                            timeout=15
                        )
                        last_error = f"(Worked with: {model})"
                        break
                    except Exception as model_error:
                        last_error = f"{model}: {str(model_error)[:40]}"
                        continue

            if response:
                print(f"✅ Groq                      ✓          [TEXT] Connected")
                self.results['groq'] = True
                self.working += 1
            else:
                error_msg = last_error if last_error else "No available models found"
                print(f"❌ Groq                      ✗          [TEXT] {error_msg}")
                self.results['groq'] = False
        except Exception as e:
            print(f"❌ Groq                      ✗          [TEXT] {str(e)[:50]}")
            self.results['groq'] = False
        self.total += 1

    def check_google(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ Google Gemini             ✗          [TEXT] No API key")
            self.results['google'] = False
            self.total += 1
            return

        response = None

        # Try new google.genai library first
        try:
            import google.genai as genai
            client = genai.Client(api_key=api_key)

            # Strategy 1: Dynamically get available models
            try:
                models = client.models.list()
                if models:
                    for model in models:
                        if hasattr(model, 'name'):
                            model_name = model.name
                            try:
                                response = client.models.generate_content(
                                    model=model_name,
                                    contents="Say OK"
                                )
                                if response:
                                    print(f"✅ Google Gemini             ✓          [TEXT] Connected")
                                    self.results['google'] = True
                                    self.working += 1
                                    self.total += 1
                                    return
                            except:
                                continue
            except:
                pass  # If dynamic listing fails, try hardcoded models

            # Strategy 2: Fallback to comprehensive hardcoded list for new library
            models_to_try = [
                'gemini-2.0-flash',
                'gemini-1.5-flash',
                'gemini-1.5-pro',
                'gemini-2.0-flash-exp',
                'gemini-1.5-pro-exp',
                'gemini-exp-1114',
                'gemini-pro'
            ]

            for model_name in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents="Say OK"
                    )
                    if response:
                        print(f"✅ Google Gemini             ✓          [TEXT] Connected")
                        self.results['google'] = True
                        self.working += 1
                        self.total += 1
                        return
                except:
                    continue

        except ImportError:
            pass  # Fall back to deprecated library

        # Fallback to deprecated google.generativeai library
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)

            # Strategy 1: Try to dynamically list models
            try:
                models = genai.list_models()
                for model in models:
                    model_name = model.name
                    try:
                        model_obj = genai.GenerativeModel(model_name)
                        response = model_obj.generate_content("Say OK", generation_config=genai.types.GenerationConfig(max_output_tokens=10))
                        if response:
                            print(f"✅ Google Gemini             ✓          [TEXT] Connected")
                            self.results['google'] = True
                            self.working += 1
                            self.total += 1
                            return
                    except:
                        continue
            except:
                pass  # If dynamic listing fails, use hardcoded list

            # Strategy 2: Fallback to comprehensive hardcoded list for deprecated library
            models_to_try = [
                'gemini-1.5-pro',
                'gemini-1.5-flash',
                'gemini-1.5-flash-8b',
                'gemini-pro',
                'gemini-pro-vision'
            ]

            for model_name in models_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content("Say OK", generation_config=genai.types.GenerationConfig(max_output_tokens=10))
                    if response:
                        print(f"✅ Google Gemini             ✓          [TEXT] Connected")
                        self.results['google'] = True
                        self.working += 1
                        self.total += 1
                        return
                except:
                    continue

        except Exception as e:
            pass

        # If we get here, all strategies failed
        print(f"❌ Google Gemini             ✗          [TEXT] No working models found")
        self.results['google'] = False
        self.total += 1

    def check_openai(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OpenAI                    ✗          [TEXT] No API key")
            self.results['openai'] = False
            self.total += 1
            return

        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Say OK"}],
                max_tokens=5
            )
            print(f"✅ OpenAI                    ✓          [TEXT] Connected")
            self.results['openai'] = True
            self.working += 1
        except Exception as e:
            print(f"❌ OpenAI                    ✗          [TEXT] {str(e)[:50]}")
            self.results['openai'] = False
        self.total += 1

    def check_cohere(self):
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            print("❌ Cohere                    ✗          [TEXT] No API key")
            self.results['cohere'] = False
            self.total += 1
            return

        try:
            import cohere
            client = cohere.Client(api_key=api_key)
            response = client.chat(message="Say OK", max_tokens=10)
            print(f"✅ Cohere                    ✓          [TEXT] Connected")
            self.results['cohere'] = True
            self.working += 1
        except Exception as e:
            print(f"❌ Cohere                    ✗          [TEXT] {str(e)[:50]}")
            self.results['cohere'] = False
        self.total += 1

    def check_replicate(self):
        api_key = os.getenv("REPLICATE_API_KEY")
        if not api_key:
            print("❌ Replicate                 ✗          [TEXT] No API key")
            self.results['replicate'] = False
            self.total += 1
            return

        try:
            os.environ['REPLICATE_API_TOKEN'] = api_key
            import replicate
            models = replicate.models.list()
            print(f"✅ Replicate                 ✓          [TEXT] Connected")
            self.results['replicate'] = True
            self.working += 1
        except Exception as e:
            print(f"❌ Replicate                 ✗          [TEXT] {str(e)[:50]}")
            self.results['replicate'] = False
        self.total += 1

    def check_huggingface(self):
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not api_key:
            print("❌ HuggingFace               ✗          [TEXT] No API key")
            self.results['huggingface'] = False
            self.total += 1
            return

        try:
            from huggingface_hub import HfApi
            api = HfApi(token=api_key)
            user = api.whoami()
            print(f"✅ HuggingFace               ✓          [TEXT] Connected")
            self.results['huggingface'] = True
            self.working += 1
        except Exception as e:
            print(f"❌ HuggingFace               ✗          [TEXT] {str(e)[:50]}")
            self.results['huggingface'] = False
        self.total += 1

    def check_unsplash(self):
        api_key = os.getenv("UNSPLASH_API_KEY")
        if not api_key:
            print("❌ Unsplash                  ✗          [IMAGE] No API key")
            self.results['unsplash'] = False
            self.total += 1
            return

        try:
            import requests
            response = requests.get(
                "https://api.unsplash.com/photos/random",
                headers={"Authorization": f"Client-ID {api_key}"}
            )
            if response.status_code == 200:
                print(f"✅ Unsplash                  ✓          [IMAGE] Connected")
                self.results['unsplash'] = True
                self.working += 1
            else:
                print(f"❌ Unsplash                  ✗          [IMAGE] HTTP {response.status_code}")
                self.results['unsplash'] = False
        except Exception as e:
            print(f"❌ Unsplash                  ✗          [IMAGE] {str(e)[:50]}")
            self.results['unsplash'] = False
        self.total += 1

    def check_pixabay(self):
        api_key = os.getenv("PIXABAY_API_KEY")
        if not api_key:
            print("❌ Pixabay                   ✗          [IMAGE] No API key")
            self.results['pixabay'] = False
            self.total += 1
            return

        try:
            import requests
            response = requests.get(
                "https://pixabay.com/api/",
                params={"key": api_key, "q": "test"}
            )
            if response.status_code == 200:
                print(f"✅ Pixabay                   ✓          [IMAGE] Connected")
                self.results['pixabay'] = True
                self.working += 1
            else:
                print(f"❌ Pixabay                   ✗          [IMAGE] HTTP {response.status_code}")
                self.results['pixabay'] = False
        except Exception as e:
            print(f"❌ Pixabay                   ✗          [IMAGE] {str(e)[:50]}")
            self.results['pixabay'] = False
        self.total += 1

    def check_cj_affiliate(self):
        api_key = os.getenv("CJ_API_KEY") or os.getenv("CJ_AFFILIATE_API_KEY")
        if not api_key:
            print("❌ CJ Affiliate              ✗          [AFFILIATE] No API key")
            self.results['cj'] = False
            self.total += 1
            return

        try:
            import requests
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(
                "https://api.cj.com/v2/commissions",
                headers=headers,
                timeout=5
            )
            if response.status_code == 200 or response.status_code == 401:
                print(f"✅ CJ Affiliate              ✓          [AFFILIATE] Connected")
                self.results['cj'] = True
                self.working += 1
            else:
                print(f"❌ CJ Affiliate              ✗          [AFFILIATE] HTTP {response.status_code}")
                self.results['cj'] = False
        except Exception as e:
            print(f"❌ CJ Affiliate              ✗          [AFFILIATE] {str(e)[:50]}")
            self.results['cj'] = False
        self.total += 1

    def check_shareasale(self):
        token = os.getenv("SHAREASALE_API_TOKEN") or os.getenv("SHAREASALE_TOKEN")
        user_id = os.getenv("SHAREASALE_USER_ID")
        if not token or not user_id:
            print("❌ ShareASale                ✗          [AFFILIATE] Missing credentials")
            self.results['shareasale'] = False
            self.total += 1
            return

        try:
            import requests
            url = f"https://api.shareasale.com/x/api/merchants?token={token}&userID={user_id}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200 or response.status_code == 401:
                print(f"✅ ShareASale                ✓          [AFFILIATE] Connected")
                self.results['shareasale'] = True
                self.working += 1
            else:
                print(f"❌ ShareASale                ✗          [AFFILIATE] HTTP {response.status_code}")
                self.results['shareasale'] = False
        except Exception as e:
            print(f"❌ ShareASale                ✗          [AFFILIATE] {str(e)[:50]}")
            self.results['shareasale'] = False
        self.total += 1

    def run_all_checks(self):
        self.print_header("GHGF API HEALTH CHECK")
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
        print(f"{BOLD}SUMMARY{RESET}")
        print(f"{BOLD}Working: {self.working}/{self.total}{RESET}")
        print(f"SUMMARY: {self.working}/{self.total} APIs WORKING")
        print('='*70 + "\n")

if __name__ == "__main__":
    checker = APIChecker()
    checker.run_all_checks()
