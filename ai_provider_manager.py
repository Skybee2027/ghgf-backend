"""
AI Provider Manager with Intelligent Fallback Chains
OpenAI is ALWAYS the last resort after all free/cheap options exhausted
"""

import os
import logging
from typing import Optional, Dict, Any
import anthropic
import openai
import google.generativeai as genai
import aiohttp
import asyncio

logger = logging.getLogger(__name__)

class AIProviderManager:
    """
    Multi-AI provider with intelligent fallback chains.
    Priority: Free → Paid (non-OpenAI) → OpenAI (LAST RESORT)
    """

    def __init__(self):
        self.costs_tracking = {}
        self.usage_tracking = {}
        self.provider_status = {}

        # Initialize all providers
        self.claude_free_available = self._check_claude_free()
        self.gemini_free_available = self._check_gemini_free()
        self.chatgpt_free_available = self._check_chatgpt_free()
        self.ollama_available = self._check_ollama()
        self.together_ai_available = os.getenv("TOGETHER_AI_API_KEY") is not None
        self.cohere_available = os.getenv("COHERE_API_KEY") is not None
        self.openai_available = os.getenv("OPENAI_API_KEY") is not None

        # Initialize clients
        # OpenAI: API key will be passed directly to client (no global config needed)

        if os.getenv("GOOGLE_API_KEY"):
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # ============================================================================
    # TEXT GENERATION WITH FALLBACK CHAIN
    # ============================================================================

    async def generate_text(self, prompt: str, task_type: str = "general") -> Dict[str, Any]:
        """
        Generate text with intelligent fallback chain.

        PRIORITY ORDER:
        1. Ollama (local, 100% free)
        2. Claude free (web automation)
        3. Gemini free (10k free requests/day)
        4. Together AI (free tier)
        5. Cohere (free tier)
        6. Claude API (paid)
        7. OpenAI (LAST RESORT - only when all exhausted)
        """

        fallback_chain = self._get_text_fallback_chain(task_type)

        for provider in fallback_chain:
            try:
                logger.info(f"Attempting text generation with {provider}...")

                if provider == "ollama":
                    result = await self._ollama_text(prompt)
                elif provider == "claude_free":
                    result = await self._claude_free_text(prompt)
                elif provider == "gemini_free":
                    result = await self._gemini_free_text(prompt)
                elif provider == "together_ai":
                    result = await self._together_ai_text(prompt)
                elif provider == "cohere":
                    result = await self._cohere_text(prompt)
                elif provider == "claude_api":
                    result = await self._claude_api_text(prompt)
                elif provider == "openai":
                    logger.warning("⚠️  USING OPENAI - ALL FREE OPTIONS EXHAUSTED!")
                    result = await self._openai_text(prompt)

                if result and result.get("success"):
                    self._track_usage(provider, result.get("tokens", 0), task_type)
                    return result

            except Exception as e:
                logger.error(f"❌ {provider} failed: {str(e)}")
                continue

        # If we get here, everything failed
        logger.critical("❌ ALL PROVIDERS FAILED - UNABLE TO GENERATE TEXT")
        return {"success": False, "error": "All providers exhausted"}

    def _get_text_fallback_chain(self, task_type: str) -> list:
        """
        Get provider fallback chain based on task type.
        IMPORTANT: OpenAI is ALWAYS last.
        """
        chain = []

        # Always try free first
        if self.ollama_available:
            chain.append("ollama")
        if self.claude_free_available:
            chain.append("claude_free")
        if self.gemini_free_available:
            chain.append("gemini_free")

        # Then try cheap alternatives
        if self.together_ai_available:
            chain.append("together_ai")
        if self.cohere_available:
            chain.append("cohere")

        # Then try Claude paid
        if os.getenv("ANTHROPIC_API_KEY"):
            chain.append("claude_api")

        # FINALLY add OpenAI as absolute last resort
        if self.openai_available:
            chain.append("openai")

        return chain

    # ============================================================================
    # IMAGE GENERATION WITH FALLBACK CHAIN
    # ============================================================================

    async def generate_image(self, prompt: str, size: str = "1024x1024") -> Dict[str, Any]:
        """
        Generate image with intelligent fallback chain.

        PRIORITY ORDER:
        1. Stable Diffusion local (100% free)
        2. Bing Image Creator (100% free)
        3. Hugging Face free (no API key needed)
        4. Replicate (free tier available)
        5. Together AI (free tier for image gen)
        6. Stability AI (paid, cheaper than OpenAI)
        7. OpenAI DALL-E (LAST RESORT - most expensive)
        """

        fallback_chain = self._get_image_fallback_chain()

        for provider in fallback_chain:
            try:
                logger.info(f"Attempting image generation with {provider}...")

                if provider == "stable_diffusion_local":
                    result = await self._stable_diffusion_local(prompt, size)
                elif provider == "bing_free":
                    result = await self._bing_image_creator(prompt)
                elif provider == "huggingface":
                    result = await self._huggingface_image(prompt)
                elif provider == "replicate":
                    result = await self._replicate_image(prompt, size)
                elif provider == "together_ai":
                    result = await self._together_ai_image(prompt, size)
                elif provider == "stability_ai":
                    result = await self._stability_ai_image(prompt, size)
                elif provider == "openai_dalle":
                    logger.warning("⚠️  USING OPENAI DALL-E - ALL FREE/CHEAP OPTIONS EXHAUSTED!")
                    result = await self._openai_image(prompt, size)

                if result and result.get("success"):
                    self._track_image_usage(provider, result.get("cost", 0))
                    return result

            except Exception as e:
                logger.error(f"❌ {provider} failed: {str(e)}")
                continue

        # If we get here, everything failed
        logger.critical("❌ ALL IMAGE PROVIDERS FAILED")
        return {"success": False, "error": "All image providers exhausted"}

    def _get_image_fallback_chain(self) -> list:
        """
        Get image provider fallback chain.
        CRITICAL: OpenAI DALL-E is LAST and MOST EXPENSIVE option.
        """
        chain = []

        # FREE LOCAL FIRST
        if self._check_stable_diffusion_local():
            chain.append("stable_diffusion_local")

        # FREE WEB SERVICES
        chain.append("bing_free")  # Always available
        chain.append("huggingface")  # Free tier

        # CHEAP ALTERNATIVES (if available)
        if os.getenv("REPLICATE_API_KEY"):
            chain.append("replicate")

        if os.getenv("TOGETHER_AI_API_KEY"):
            chain.append("together_ai")

        # Stability AI (cheaper than OpenAI)
        if os.getenv("STABILITY_AI_KEY"):
            chain.append("stability_ai")

        # LAST RESORT - OpenAI DALL-E (MOST EXPENSIVE)
        if self.openai_available:
            chain.append("openai_dalle")

        return chain

    # ============================================================================
    # IMPLEMENTATION: TEXT PROVIDERS
    # ============================================================================

    async def _ollama_text(self, prompt: str) -> Dict[str, Any]:
        """Local Ollama - 100% FREE"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:11434/api/generate",
                    json={"model": "mistral", "prompt": prompt, "stream": False}
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return {
                            "success": True,
                            "text": data.get("response", ""),
                            "tokens": data.get("eval_count", 0),
                            "cost": 0,  # 100% FREE
                            "provider": "ollama"
                        }
        except Exception as e:
            logger.error(f"Ollama error: {e}")
        return {"success": False}

    async def _claude_free_text(self, prompt: str) -> Dict[str, Any]:
        """Claude via web automation - FREE"""
        # This would use Selenium/Playwright to automate claude.ai web interface
        # For now, mock implementation
        logger.info("Using Claude free tier (web automation)")
        return {"success": False}  # Requires browser automation setup

    async def _gemini_free_text(self, prompt: str) -> Dict[str, Any]:
        """Google Gemini free tier - FREE (10k requests/day)"""
        try:
            # Use current Gemini model (gemini-pro is deprecated)
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)

            return {
                "success": True,
                "text": response.text,
                "tokens": len(prompt.split()) + len(response.text.split()),
                "cost": 0,  # FREE
                "provider": "gemini_free"
            }
        except Exception as e:
            logger.error(f"Gemini error: {e}")
        return {"success": False}

    async def _together_ai_text(self, prompt: str) -> Dict[str, Any]:
        """Together AI - FREE tier available"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {os.getenv('TOGETHER_AI_API_KEY')}"}
                async with session.post(
                    "https://api.together.xyz/inference",
                    json={
                        "model": "mistralai/Mistral-7B-Instruct-v0.1",
                        "prompt": prompt,
                        "max_tokens": 500
                    },
                    headers=headers
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return {
                            "success": True,
                            "text": data.get("output", {}).get("choices", [{}])[0].get("text", ""),
                            "tokens": 500,
                            "cost": 0,  # Free tier
                            "provider": "together_ai"
                        }
        except Exception as e:
            logger.error(f"Together AI error: {e}")
        return {"success": False}

    async def _cohere_text(self, prompt: str) -> Dict[str, Any]:
        """Cohere - Free tier available (using Chat API - Generate API is deprecated)"""
        try:
            import cohere
            co = cohere.Client(os.getenv("COHERE_API_KEY"))
            # Use Chat API instead of deprecated Generate API
            response = co.chat(message=prompt, max_tokens=500)

            return {
                "success": True,
                "text": response.text,
                "tokens": 500,
                "cost": 0,  # Free tier
                "provider": "cohere"
            }
        except Exception as e:
            logger.error(f"Cohere error: {e}")
        return {"success": False}

    async def _claude_api_text(self, prompt: str) -> Dict[str, Any]:
        """Claude API (Anthropic) - PAID but cheaper than OpenAI"""
        try:
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            return {
                "success": True,
                "text": message.content[0].text,
                "tokens": message.usage.output_tokens,
                "cost": (message.usage.input_tokens * 0.003 + message.usage.output_tokens * 0.015) / 1000,
                "provider": "claude_api"
            }
        except Exception as e:
            logger.error(f"Claude API error: {e}")
        return {"success": False}

    async def _openai_text(self, prompt: str) -> Dict[str, Any]:
        """
        OpenAI GPT-4 - EXPENSIVE, LAST RESORT ONLY
        This should ONLY be called when ALL other providers fail
        """
        try:
            logger.critical("⚠️⚠️⚠️  WARNING: USING OPENAI (EXPENSIVE) ⚠️⚠️⚠️")

            # Use new OpenAI client syntax (v1.0+)
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Use cheaper mini model instead of full GPT-4
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024
            )

            usage = response.usage
            input_tokens = usage.prompt_tokens
            output_tokens = usage.completion_tokens

            # OpenAI GPT-4 mini pricing (cheaper than full GPT-4)
            cost = (input_tokens * 0.00015 + output_tokens * 0.0006) / 1  # Divided by 1 since already per 1k tokens

            logger.warning(f"⚠️ OpenAI cost for this request: ${cost:.4f}")

            return {
                "success": True,
                "text": response.choices[0].message.content,
                "tokens": output_tokens,
                "cost": cost,
                "provider": "openai",
                "warning": "EXPENSIVE PROVIDER USED"
            }
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
        return {"success": False}

    # ============================================================================
    # IMPLEMENTATION: IMAGE PROVIDERS
    # ============================================================================

    async def _stable_diffusion_local(self, prompt: str, size: str) -> Dict[str, Any]:
        """Stable Diffusion local - 100% FREE"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:7860/run/predict",
                    json={"data": [prompt, 50, 7.5]}
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return {
                            "success": True,
                            "image_url": data.get("data", [None])[0],
                            "cost": 0,  # 100% FREE
                            "provider": "stable_diffusion_local"
                        }
        except Exception as e:
            logger.error(f"Stable Diffusion error: {e}")
        return {"success": False}

    async def _bing_image_creator(self, prompt: str) -> Dict[str, Any]:
        """Bing Image Creator - 100% FREE"""
        logger.info("Using Bing Image Creator (free)")
        # Would require browser automation with Playwright
        return {"success": False}

    async def _huggingface_image(self, prompt: str) -> Dict[str, Any]:
        """Hugging Face - FREE tier"""
        try:
            import requests
            from PIL import Image
            from io import BytesIO

            api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
            headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY', '')}"}

            response = requests.post(api_url, headers=headers, json={"inputs": prompt})

            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                return {
                    "success": True,
                    "image": img,
                    "cost": 0,  # FREE tier
                    "provider": "huggingface"
                }
        except Exception as e:
            logger.error(f"Hugging Face error: {e}")
        return {"success": False}

    async def _replicate_image(self, prompt: str, size: str) -> Dict[str, Any]:
        """Replicate - Has free tier"""
        try:
            import replicate

            output = replicate.run(
                "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21aef33d3e3b7f1024",
                input={"prompt": prompt, "width": int(size.split("x")[0])}
            )

            return {
                "success": True,
                "image_url": output[0] if output else None,
                "cost": 0.01,  # Replicate is cheap, ~$0.01 per image
                "provider": "replicate"
            }
        except Exception as e:
            logger.error(f"Replicate error: {e}")
        return {"success": False}

    async def _together_ai_image(self, prompt: str, size: str) -> Dict[str, Any]:
        """Together AI - Image generation (cheaper than OpenAI)"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {os.getenv('TOGETHER_AI_API_KEY')}"}
                async with session.post(
                    "https://api.together.xyz/inference",
                    json={
                        "model": "stabilityai/stable-diffusion-xl-base-1.0",
                        "prompt": prompt,
                        "width": int(size.split("x")[0]),
                        "height": int(size.split("x")[1])
                    },
                    headers=headers
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return {
                            "success": True,
                            "image_url": data.get("output", [None])[0],
                            "cost": 0.02,  # Cheap compared to OpenAI
                            "provider": "together_ai"
                        }
        except Exception as e:
            logger.error(f"Together AI image error: {e}")
        return {"success": False}

    async def _stability_ai_image(self, prompt: str, size: str) -> Dict[str, Any]:
        """Stability AI - Cheaper than OpenAI"""
        try:
            import requests

            response = requests.post(
                "https://api.stability.ai/v1/generate",
                headers={
                    "Authorization": f"Bearer {os.getenv('STABILITY_AI_KEY')}",
                    "Content-Type": "application/json"
                },
                json={
                    "text_prompts": [{"text": prompt}],
                    "height": int(size.split("x")[1]),
                    "width": int(size.split("x")[0]),
                    "steps": 30,
                    "cfg_scale": 7.5
                }
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "image": data.get("artifacts", [{}])[0].get("base64"),
                    "cost": 0.015,  # ~$0.015 per image (cheaper than OpenAI)
                    "provider": "stability_ai"
                }
        except Exception as e:
            logger.error(f"Stability AI error: {e}")
        return {"success": False}

    async def _openai_image(self, prompt: str, size: str) -> Dict[str, Any]:
        """
        OpenAI DALL-E 3 - MOST EXPENSIVE, ABSOLUTE LAST RESORT
        $0.08 per 1024x1024 image (vs $0.015 for Stability)
        Only use this when ALL other providers failed
        """
        try:
            logger.critical("⚠️⚠️⚠️  WARNING: USING OPENAI DALL-E (MOST EXPENSIVE) ⚠️⚠️⚠️")

            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size=size,
                model="dall-e-3"
            )

            logger.warning(f"⚠️ OpenAI DALL-E cost for this image: $0.08")

            return {
                "success": True,
                "image_url": response["data"][0]["url"],
                "cost": 0.08,  # EXPENSIVE!
                "provider": "openai_dalle",
                "warning": "MOST EXPENSIVE PROVIDER USED"
            }
        except Exception as e:
            logger.error(f"OpenAI DALL-E error: {e}")
        return {"success": False}

    # ============================================================================
    # UTILITIES
    # ============================================================================

    def _check_claude_free(self) -> bool:
        """Check if Claude free is available"""
        return bool(os.getenv("CLAUDE_FREE_LOGIN"))

    def _check_gemini_free(self) -> bool:
        """Check if Gemini free API is available"""
        return bool(os.getenv("GOOGLE_API_KEY"))

    def _check_chatgpt_free(self) -> bool:
        """Check if ChatGPT free is available"""
        return bool(os.getenv("CHATGPT_FREE_LOGIN"))

    def _check_ollama(self) -> bool:
        """Check if Ollama is running locally"""
        try:
            import requests
            requests.get("http://localhost:11434/api/tags", timeout=1)
            return True
        except:
            return False

    def _check_stable_diffusion_local(self) -> bool:
        """Check if Stable Diffusion is running locally"""
        try:
            import requests
            requests.get("http://localhost:7860/", timeout=1)
            return True
        except:
            return False

    def _track_usage(self, provider: str, tokens: int, task_type: str):
        """Track API usage for cost calculation"""
        if provider not in self.usage_tracking:
            self.usage_tracking[provider] = {"tokens": 0, "calls": 0, "tasks": {}}

        self.usage_tracking[provider]["tokens"] += tokens
        self.usage_tracking[provider]["calls"] += 1

        if task_type not in self.usage_tracking[provider]["tasks"]:
            self.usage_tracking[provider]["tasks"][task_type] = 0
        self.usage_tracking[provider]["tasks"][task_type] += 1

        logger.info(f"✓ Used {provider}: {tokens} tokens | Total calls: {self.usage_tracking[provider]['calls']}")

    def _track_image_usage(self, provider: str, cost: float):
        """Track image generation costs"""
        if provider not in self.costs_tracking:
            self.costs_tracking[provider] = {"images": 0, "cost": 0}

        self.costs_tracking[provider]["images"] += 1
        self.costs_tracking[provider]["cost"] += cost

        logger.info(f"✓ Image generated with {provider}: ${cost:.4f} | Total cost: ${self.costs_tracking[provider]['cost']:.2f}")

    def get_usage_report(self) -> Dict[str, Any]:
        """Get detailed usage report"""
        return {
            "text_usage": self.usage_tracking,
            "image_costs": self.costs_tracking,
            "total_image_cost": sum(v["cost"] for v in self.costs_tracking.values()),
            "total_image_count": sum(v["images"] for v in self.costs_tracking.values())
        }


if __name__ == "__main__":
    # Test fallback chains
    manager = AIProviderManager()
    print("Text providers order:", manager._get_text_fallback_chain("blog_post"))
    print("Image providers order:", manager._get_image_fallback_chain())
