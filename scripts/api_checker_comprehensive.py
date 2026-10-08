#!/usr/bin/env python3
"""
Comprehensive API Health Checker for GHGF Autonomous Blogging System
Tests ALL 16 configured providers across text, image, content, affiliate, and distribution layers
"""

import os
import sys
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

class ComprehensiveAPIChecker:
    def __init__(self):
        self.results = {}
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.total_apis = 0
        self.working_apis = 0

    def print_header(self, text):
        print(f"\n{BOLD}{BLUE}{'='*90}{RESET}")
        print(f"{BOLD}{BLUE}{text}{RESET}")
        print(f"{BOLD}{BLUE}{'='*90}{RESET}\n")

    def print_result(self, provider, status, message, response_time=None, category=""):
        if status == "✓":
            color = GREEN
            icon = "✅"
            self.working_apis += 1
        elif status == "✗":
            color = RED
            icon = "❌"
        else:
            color = YELLOW
            icon = "⚠️"

        time_str = f" ({response_time:.2f}s)" if response_time else ""
        cat_str = f"[{category}] " if category else ""
        print(f"{icon} {color}{BOLD}{provider:25}{RESET} {status:10} {cat_str}{message}{time_str}")

        self.results[provider] = {
            "status": status,
            "message": message,
            "category": category,
            "timestamp": self.timestamp
        }
        self.total_apis += 1

    # ==================== TEXT GENERATION ====================
    def check_openai(self):
        """Test OpenAI API"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            self.print_result("OpenAI", "✗", "No API key configured", category="TEXT")
            return

        try:
            import openai
            openai.api_key = api_key
            start = time.time()
            response = openai.models.list()
            elapsed = time.time() - start
            self.print_result("OpenAI", "✓", "Connected successfully", elapsed, "TEXT")
        except ImportError:
            self.print_result("OpenAI", "✗", "openai package not installed", category="TEXT")
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg:
                self.print_result("OpenAI", "✗", "Invalid API key (401)", category="TEXT")
            else:
                self.print_result("OpenAI", "✗", f"Error: {error_msg[:50]}", category="TEXT")

    def check_groq(self):
        """Test Groq API"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            self.print_result("Groq", "✗", "No API key configured", category="TEXT")
            return

        try:
            from groq import Groq
            client = Groq(api_key=api_key)
            start = time.time()
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=10
            )
            elapsed = time.time() - start
            if response.choices[0].message.content:
                self.print_result("Groq", "✓", "Connected successfully", elapsed, "TEXT")
            else:
                self.print_result("Groq", "✗", "No response from API", category="TEXT")
        except ImportError:
            self.print_result("Groq", "✗", "groq package not installed", category="TEXT")
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg:
                self.print_result("Groq", "✗", "Invalid API key (401)", category="TEXT")
            else:
                self.print_result("Groq", "✗", f"Error: {error_msg[:50]}", category="TEXT")

    def check_google(self):
        """Test Google Gemini API"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            self.print_result("Google Gemini", "✗", "No API key configured", category="TEXT")
            return

        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            start = time.time()
            response = model.generate_content("test")
            elapsed = time.time() - start
            if response.text:
                self.print_result("Google Gemini", "✓", "Connected successfully", elapsed, "TEXT")
            else:
                self.print_result("Google Gemini", "✗", "No response from API", category="TEXT")
        except ImportError:
            self.print_result("Google Gemini", "✗", "google-generativeai not installed", category="TEXT")
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                self.print_result("Google Gemini", "⚠", "Free tier quota exceeded", category="TEXT")
            elif "401" in error_msg:
                self.print_result("Google Gemini", "✗", "Invalid API key (401)", category="TEXT")
            else:
                self.print_result("Google Gemini", "✗", f"Error: {error_msg[:50]}", category="TEXT")

    def check_cohere(self):
        """Test Cohere API"""
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            self.print_result("Cohere", "✗", "No API key configured", category="TEXT")
            return

        try:
            import cohere
            client = cohere.ClientV2(api_key=api_key)
            start = time.time()
            response = client.chat(
                model="command-r-plus",
                messages=[{"role": "user", "content": "test"}]
            )
            elapsed = time.time() - start
            if response.message.content:
                self.print_result("Cohere", "✓", "Connected successfully", elapsed, "TEXT")
            else:
                self.print_result("Cohere", "✗", "No response from API", category="TEXT")
        except ImportError:
            self.print_result("Cohere", "✗", "cohere package not installed", category="TEXT")
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg:
                self.print_result("Cohere", "✗", "Invalid API key (401)", category="TEXT")
            else:
                self.print_result("Cohere", "✗", f"Error: {error_msg[:50]}", category="TEXT")

    def check_together_ai(self):
        """Test Together AI API"""
        api_key = os.getenv("TOGETHER_AI_API_KEY")
        if not api_key:
            self.print_result("Together AI", "✗", "No API key configured", category="TEXT")
            return

        try:
            import together
            together.api_key = api_key
            start = time.time()
            response = together.Complete.create(
                prompt="test",
                model="mistralai/Mistral-7B-Instruct-v0.1",
                max_tokens=10
            )
            elapsed = time.time() - start
            if response:
                self.print_result("Together AI", "✓", "Connected successfully", elapsed, "TEXT")
            else:
                self.print_result("Together AI", "✗", "No response from API", category="TEXT")
        except ImportError:
            self.print_result("Together AI", "✗", "together package not installed", category="TEXT")
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg:
                self.print_result("Together AI", "✗", "Invalid API key (401)", category="TEXT")
            else:
                self.print_result("Together AI", "✗", f"Error: {error_msg[:50]}", category="TEXT")

    def check_buffer_ai(self):
        """Test Buffer AI API"""
        api_key = os.getenv("BUFFER_AI_API_KEY")
        if not api_key:
            self.print_result("Buffer AI", "✗", "No API key configured", category="TEXT")
            return

        try:
            start = time.time()
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            response = requests.get("https://api.bufferapp.com/1/user.json", headers=headers, timeout=10)
            elapsed = time.time() - start

            if response.status_code == 200:
                self.print_result("Buffer AI", "✓", "Connected successfully", elapsed, "TEXT")
            elif response.status_code == 401:
                self.print_result("Buffer AI", "✗", "Invalid API key (401)", category="TEXT")
            else:
                self.print_result("Buffer AI", "✗", f"HTTP {response.status_code}", category="TEXT")
        except Exception as e:
            self.print_result("Buffer AI", "✗", f"Error: {str(e)[:50]}", category="TEXT")

    def check_ollama(self):
        """Test Ollama local LLM"""
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        if not ollama_url:
            self.print_result("Ollama", "✗", "No Ollama URL configured", category="TEXT")
            return

        try:
            start = time.time()
            # Test if Ollama service is running
            response = requests.get(f"{ollama_url}/api/tags", timeout=5)
            elapsed = time.time() - start

            if response.status_code == 200:
                self.print_result("Ollama", "✓", "Local LLM running", elapsed, "TEXT")
            else:
                self.print_result("Ollama", "✗", f"HTTP {response.status_code}", category="TEXT")
        except requests.exceptions.ConnectionError:
            self.print_result("Ollama", "✗", "Not running (connection refused)", category="TEXT")
        except Exception as e:
            self.print_result("Ollama", "✗", f"Error: {str(e)[:50]}", category="TEXT")

    # ==================== IMAGE GENERATION ====================
    def check_openai_dalle(self):
        """Test OpenAI DALL-E"""
        api_key = os.getenv("DALLE_API_KEY")
        if not api_key:
            self.print_result("OpenAI DALL-E", "✗", "No API key configured", category="IMAGE")
            return

        try:
            import openai
            openai.api_key = api_key
            start = time.time()
            models = openai.models.list()
            elapsed = time.time() - start
            dalle_models = [m for m in models.data if 'dall-e' in m.id]
            if dalle_models:
                self.print_result("OpenAI DALL-E", "✓", "Connected successfully", elapsed, "IMAGE")
            else:
                self.print_result("OpenAI DALL-E", "⚠", "DALL-E models not available", category="IMAGE")
        except ImportError:
            self.print_result("OpenAI DALL-E", "✗", "openai package not installed", category="IMAGE")
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg:
                self.print_result("OpenAI DALL-E", "✗", "Invalid API key (401)", category="IMAGE")
            else:
                self.print_result("OpenAI DALL-E", "✗", f"Error: {error_msg[:50]}", category="IMAGE")

    def check_replicate(self):
        """Test Replicate API"""
        api_key = os.getenv("REPLICATE_API_KEY")
        if not api_key:
            self.print_result("Replicate", "✗", "No API key configured", category="IMAGE")
            return

        try:
            import replicate
            os.environ["REPLICATE_API_TOKEN"] = api_key
            start = time.time()
            models = replicate.models.list()
            elapsed = time.time() - start
            self.print_result("Replicate", "✓", "Connected successfully", elapsed, "IMAGE")
        except ImportError:
            self.print_result("Replicate", "✗", "replicate package not installed", category="IMAGE")
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "Unauthorized" in error_msg:
                self.print_result("Replicate", "✗", "Invalid API key (401)", category="IMAGE")
            else:
                self.print_result("Replicate", "✗", f"Error: {error_msg[:50]}", category="IMAGE")

    def check_huggingface(self):
        """Test Hugging Face API"""
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not api_key:
            self.print_result("Hugging Face", "✗", "No API key configured", category="IMAGE")
            return

        try:
            from huggingface_hub import HfApi
            api = HfApi(token=api_key)
            start = time.time()
            user = api.whoami()
            elapsed = time.time() - start
            self.print_result("Hugging Face", "✓", "Connected successfully", elapsed, "IMAGE")
        except ImportError:
            self.print_result("Hugging Face", "✗", "huggingface_hub not installed", category="IMAGE")
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "Unauthorized" in error_msg:
                self.print_result("Hugging Face", "✗", "Invalid API key (401)", category="IMAGE")
            else:
                self.print_result("Hugging Face", "✗", f"Error: {error_msg[:50]}", category="IMAGE")

    def check_unsplash(self):
        """Test Unsplash API"""
        api_key = os.getenv("UNSPLASH_API_KEY")
        if not api_key:
            self.print_result("Unsplash", "✗", "No API key configured", category="IMAGE")
            return

        try:
            start = time.time()
            headers = {"Authorization": f"Client-ID {api_key}"}
            response = requests.get("https://api.unsplash.com/me", headers=headers, timeout=10)
            elapsed = time.time() - start

            if response.status_code == 200:
                self.print_result("Unsplash", "✓", "Connected successfully", elapsed, "IMAGE")
            elif response.status_code == 401:
                self.print_result("Unsplash", "✗", "Invalid API key (401)", category="IMAGE")
            else:
                self.print_result("Unsplash", "✗", f"HTTP {response.status_code}", category="IMAGE")
        except Exception as e:
            self.print_result("Unsplash", "✗", f"Error: {str(e)[:50]}", category="IMAGE")

    def check_pixabay(self):
        """Test Pixabay API"""
        api_key = os.getenv("PIXABAY_API_KEY")
        if not api_key:
            self.print_result("Pixabay", "✗", "No API key configured", category="IMAGE")
            return

        try:
            start = time.time()
            response = requests.get(
                "https://pixabay.com/api/",
                params={"key": api_key, "q": "test", "per_page": 1},
                timeout=10
            )
            elapsed = time.time() - start

            if response.status_code == 200:
                data = response.json()
                if data.get("hits"):
                    self.print_result("Pixabay", "✓", "Connected successfully", elapsed, "IMAGE")
                else:
                    self.print_result("Pixabay", "⚠", "API working but no results", category="IMAGE")
            elif response.status_code == 400:
                self.print_result("Pixabay", "✗", "Invalid API key", category="IMAGE")
            else:
                self.print_result("Pixabay", "✗", f"HTTP {response.status_code}", category="IMAGE")
        except Exception as e:
            self.print_result("Pixabay", "✗", f"Error: {str(e)[:50]}", category="IMAGE")

    # ==================== CONTENT DISCOVERY ====================
    def check_reddit(self):
        """Test Reddit API"""
        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        username = os.getenv("REDDIT_USERNAME")
        password = os.getenv("REDDIT_PASSWORD")

        if not all([client_id, client_secret, username, password]):
            self.print_result("Reddit", "✗", "Credentials not configured", category="CONTENT")
            return

        try:
            import praw
            reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=f"GHGF-Bot/1.0 by {username}",
                username=username,
                password=password
            )
            start = time.time()
            user = reddit.user.me()
            elapsed = time.time() - start

            if user:
                self.print_result("Reddit", "✓", "Authenticated successfully", elapsed, "CONTENT")
            else:
                self.print_result("Reddit", "✗", "Authentication failed", category="CONTENT")
        except ImportError:
            self.print_result("Reddit", "✗", "praw package not installed", category="CONTENT")
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "Invalid" in error_msg:
                self.print_result("Reddit", "✗", "Invalid credentials (401)", category="CONTENT")
            else:
                self.print_result("Reddit", "✗", f"Error: {error_msg[:50]}", category="CONTENT")

    # ==================== AFFILIATE NETWORKS ====================
    def check_cj_affiliate(self):
        """Test CJ Affiliate API"""
        api_key = os.getenv("CJ_AFFILIATE_API_KEY")
        if not api_key:
            self.print_result("CJ Affiliate", "✗", "No API key configured", category="AFFILIATE")
            return

        try:
            start = time.time()
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json"
            }
            # Test with a simple endpoint
            response = requests.get(
                "https://api.cj.com/v2/advertisers",
                headers=headers,
                timeout=10
            )
            elapsed = time.time() - start

            if response.status_code == 200:
                self.print_result("CJ Affiliate", "✓", "Connected successfully", elapsed, "AFFILIATE")
            elif response.status_code == 401:
                self.print_result("CJ Affiliate", "✗", "Invalid API key (401)", category="AFFILIATE")
            else:
                self.print_result("CJ Affiliate", "✗", f"HTTP {response.status_code}", category="AFFILIATE")
        except Exception as e:
            self.print_result("CJ Affiliate", "✗", f"Error: {str(e)[:50]}", category="AFFILIATE")

    def check_shareasale(self):
        """Test ShareASale API"""
        api_token = os.getenv("SHAREASALE_API_TOKEN")
        user_id = os.getenv("SHAREASALE_USER_ID")

        if not all([api_token, user_id]):
            self.print_result("ShareASale", "✗", "Credentials not configured", category="AFFILIATE")
            return

        try:
            start = time.time()
            # ShareASale uses API token in URL
            response = requests.get(
                f"https://api.shareasale.com/x.php?action=apikey&userid={user_id}&token={api_token}&timeout=30",
                timeout=10
            )
            elapsed = time.time() - start

            if response.status_code == 200 and "error" not in response.text.lower():
                self.print_result("ShareASale", "✓", "Connected successfully", elapsed, "AFFILIATE")
            elif "error" in response.text.lower():
                self.print_result("ShareASale", "✗", "Invalid credentials", category="AFFILIATE")
            else:
                self.print_result("ShareASale", "✗", f"HTTP {response.status_code}", category="AFFILIATE")
        except Exception as e:
            self.print_result("ShareASale", "✗", f"Error: {str(e)[:50]}", category="AFFILIATE")

    # ==================== DISTRIBUTION ====================
    def check_mailchimp(self):
        """Test Mailchimp API"""
        api_key = os.getenv("MAILCHIMP_API_KEY")
        if not api_key:
            self.print_result("Mailchimp", "✗", "No API key configured", category="DISTRIB")
            return

        try:
            # Extract server from API key (format: key-serverX)
            server = api_key.split('-')[-1] if '-' in api_key else 'us1'
            start = time.time()
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(
                f"https://{server}.api.mailchimp.com/3.0/",
                headers=headers,
                timeout=10
            )
            elapsed = time.time() - start

            if response.status_code == 200:
                self.print_result("Mailchimp", "✓", "Connected successfully", elapsed, "DISTRIB")
            elif response.status_code == 401:
                self.print_result("Mailchimp", "✗", "Invalid API key (401)", category="DISTRIB")
            else:
                self.print_result("Mailchimp", "✗", f"HTTP {response.status_code}", category="DISTRIB")
        except Exception as e:
            self.print_result("Mailchimp", "✗", f"Error: {str(e)[:50]}", category="DISTRIB")

    def check_buffer(self):
        """Test Buffer social media API"""
        api_key = os.getenv("BUFFER_API_KEY")
        if not api_key:
            self.print_result("Buffer", "✗", "No API key configured", category="DISTRIB")
            return

        try:
            start = time.time()
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get("https://api.bufferapp.com/1/user.json", headers=headers, timeout=10)
            elapsed = time.time() - start

            if response.status_code == 200:
                self.print_result("Buffer", "✓", "Connected successfully", elapsed, "DISTRIB")
            elif response.status_code == 401:
                self.print_result("Buffer", "✗", "Invalid API key (401)", category="DISTRIB")
            else:
                self.print_result("Buffer", "✗", f"HTTP {response.status_code}", category="DISTRIB")
        except Exception as e:
            self.print_result("Buffer", "✗", f"Error: {str(e)[:50]}", category="DISTRIB")

    # ==================== SUMMARY ====================
    def generate_summary(self):
        """Generate summary report"""
        self.print_header("SUMMARY REPORT")

        by_category = {}
        for provider, data in self.results.items():
            cat = data.get("category", "OTHER")
            if cat not in by_category:
                by_category[cat] = {"working": [], "broken": [], "warning": []}

            if data["status"] == "✓":
                by_category[cat]["working"].append(provider)
            elif data["status"] == "✗":
                by_category[cat]["broken"].append(provider)
            else:
                by_category[cat]["warning"].append(provider)

        # Display by category
        for category in ["TEXT", "IMAGE", "CONTENT", "AFFILIATE", "DISTRIB"]:
            if category in by_category:
                print(f"\n{BOLD}{CYAN}{category} LAYER:{RESET}")
                cats = by_category[category]

                if cats["working"]:
                    for provider in cats["working"]:
                        print(f"  {GREEN}✅ {provider}{RESET}")

                if cats["warning"]:
                    for provider in cats["warning"]:
                        msg = self.results[provider]["message"]
                        print(f"  {YELLOW}⚠️  {provider} - {msg}{RESET}")

                if cats["broken"]:
                    for provider in cats["broken"]:
                        print(f"  {RED}❌ {provider}{RESET}")

        print(f"\n{BOLD}{GREEN}TOTAL: {self.working_apis}/{self.total_apis} APIs working{RESET}")

        # Priority fixes
        print(f"\n{BOLD}PRIORITY FIXES:{RESET}")
        broken = {p: d for p, d in self.results.items() if d["status"] == "✗"}

        if broken:
            for provider, data in list(broken.items())[:5]:
                msg = data["message"]
                if "not installed" in msg:
                    print(f"  • {provider}: Install package with pip")
                elif "No API key" in msg or "not configured" in msg:
                    print(f"  • {provider}: Add {provider.upper().replace(' ', '_')}_API_KEY to GitHub Secrets")
                elif "Invalid" in msg or "401" in msg:
                    print(f"  • {provider}: Check API credentials are valid")
                else:
                    print(f"  • {provider}: {msg}")
        else:
            print("  ✅ All APIs configured! Ready for automation.")

        # Automation strategy
        print(f"\n{BOLD}AUTOMATION STRATEGY:{RESET}")
        text_working = by_category.get("TEXT", {}).get("working", [])
        image_working = by_category.get("IMAGE", {}).get("working", [])
        content_working = by_category.get("CONTENT", {}).get("working", [])
        affiliate_working = by_category.get("AFFILIATE", {}).get("working", [])
        distrib_working = by_category.get("DISTRIB", {}).get("working", [])

        if text_working:
            print(f"  • Text Generation: Use fallback chain - {', '.join(text_working[:3])}")
        if image_working:
            print(f"  • Image Generation: Use - {', '.join(image_working[:2])}")
        if content_working:
            print(f"  • Content Discovery: Use {', '.join(content_working)}")
        if affiliate_working:
            print(f"  • Monetization: Use {', '.join(affiliate_working)}")
        if distrib_working:
            print(f"  • Distribution: Use {', '.join(distrib_working)}")

    def run_all_checks(self):
        """Run all API checks"""
        self.print_header("GHGF COMPREHENSIVE API HEALTH CHECK")
        print(f"Timestamp: {self.timestamp}\n")

        print(f"{BOLD}TEXT GENERATION LAYER:{RESET}")
        self.check_groq()
        self.check_google()
        self.check_cohere()
        self.check_together_ai()
        self.check_openai()
        self.check_buffer_ai()
        self.check_ollama()

        print(f"\n{BOLD}IMAGE GENERATION LAYER:{RESET}")
        self.check_replicate()
        self.check_huggingface()
        self.check_unsplash()
        self.check_pixabay()
        self.check_openai_dalle()

        print(f"\n{BOLD}CONTENT DISCOVERY LAYER:{RESET}")
        self.check_reddit()

        print(f"\n{BOLD}AFFILIATE NETWORKS LAYER:{RESET}")
        self.check_cj_affiliate()
        self.check_shareasale()

        print(f"\n{BOLD}DISTRIBUTION LAYER:{RESET}")
        self.check_mailchimp()
        self.check_buffer()

        self.generate_summary()
        self.print_header("CHECK COMPLETE")

if __name__ == "__main__":
    checker = ComprehensiveAPIChecker()
    checker.run_all_checks()
