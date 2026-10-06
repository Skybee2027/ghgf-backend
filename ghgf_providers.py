"""
GHGF AI Provider Management - REAL API Implementation
Implements free-first strategy with automatic fallback to real providers:
Groq → HuggingFace → Gemini → Claude → OpenAI
"""

import asyncio
import os
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class AIProviderManager:
    """Manages all AI providers with free-first strategy - REAL API CALLS"""

    def __init__(self, providers_config: Dict = None):
        self.config = providers_config or {}
        self.fallback_chain = providers_config.get("fallback_chain", [
            "groq", "huggingface", "gemini", "claude", "openai"
        ]) if providers_config else ["groq", "huggingface", "gemini", "claude", "openai"]

        self.provider_stats = {}
        self._init_clients()

    def _init_clients(self):
        """Initialize all provider clients"""

        # Groq Client
        try:
            from groq import Groq
            groq_key = os.getenv("GROQ_API_KEY")
            if groq_key:
                self.groq_client = Groq(api_key=groq_key)
                logger.info("✅ Groq client initialized")
            else:
                self.groq_client = None
                logger.warning("⚠️  GROQ_API_KEY not set")
        except Exception as e:
            self.groq_client = None
            logger.warning(f"⚠️  Groq init failed: {e}")

        # HuggingFace Client
        try:
            from huggingface_hub import InferenceClient
            hf_key = os.getenv("HUGGINGFACE_API_KEY")
            if hf_key:
                self.hf_client = InferenceClient(token=hf_key)
                logger.info("✅ HuggingFace client initialized")
            else:
                self.hf_client = None
                logger.warning("⚠️  HUGGINGFACE_API_KEY not set")
        except Exception as e:
            self.hf_client = None
            logger.warning(f"⚠️  HuggingFace init failed: {e}")

        # Gemini Client
        try:
            import google.generativeai as genai
            gemini_key = os.getenv("GOOGLE_API_KEY")
            if gemini_key:
                genai.configure(api_key=gemini_key)
                self.genai = genai
                logger.info("✅ Gemini client initialized")
            else:
                self.genai = None
                logger.warning("⚠️  GOOGLE_API_KEY not set")
        except Exception as e:
            self.genai = None
            logger.warning(f"⚠️  Gemini init failed: {e}")

        # Claude Client
        try:
            import anthropic
            claude_key = os.getenv("CLAUDE_API_KEY")
            if claude_key:
                self.claude_client = anthropic.Anthropic(api_key=claude_key)
                logger.info("✅ Claude client initialized (paid backup)")
            else:
                self.claude_client = None
                logger.info("ℹ️  Claude API key not set (optional paid backup)")
        except Exception as e:
            self.claude_client = None
            logger.warning(f"⚠️  Claude init failed: {e}")

        # OpenAI Client
        try:
            import openai
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key:
                self.openai_client = openai.AsyncOpenAI(api_key=openai_key)
                logger.info("✅ OpenAI client initialized (paid backup)")
            else:
                self.openai_client = None
                logger.info("ℹ️  OpenAI API key not set (optional paid backup)")
        except Exception as e:
            self.openai_client = None
            logger.warning(f"⚠️  OpenAI init failed: {e}")

    async def call_with_fallback(self, prompt: str, task_type: str = "default", max_tokens: int = 1000) -> Optional[str]:
        """Call AI with automatic fallback on failure"""

        logger.info(f"🔄 Starting fallback chain for {task_type}")
        logger.info(f"📋 Fallback order: {' → '.join(self.fallback_chain)}")

        for provider_id in self.fallback_chain:
            logger.info(f"\n▶️  Trying {provider_id.upper()}...")

            try:
                result = await self._call_provider(provider_id, prompt, max_tokens)
                if result:
                    logger.info(f"✅ SUCCESS: {provider_id.upper()} generated {len(result.split())} words")
                    return result
            except Exception as e:
                logger.warning(f"⚠️  {provider_id.upper()} failed: {str(e)[:100]}")
                continue

        logger.error("❌ All providers exhausted - no AI provider could generate content")
        return None

    async def _call_provider(self, provider_id: str, prompt: str, max_tokens: int) -> Optional[str]:
        """Call a specific provider"""

        if provider_id == "groq":
            return await self._call_groq(prompt, max_tokens)
        elif provider_id == "huggingface":
            return await self._call_huggingface(prompt, max_tokens)
        elif provider_id == "gemini":
            return await self._call_gemini(prompt, max_tokens)
        elif provider_id == "claude":
            return await self._call_claude(prompt, max_tokens)
        elif provider_id == "openai":
            return await self._call_openai(prompt, max_tokens)

        return None

    async def _call_groq(self, prompt: str, max_tokens: int) -> Optional[str]:
        """Call Groq API (Free: 9,000 req/min)"""
        if not self.groq_client:
            raise Exception("Groq client not initialized")

        try:
            response = self.groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": "You are a professional blog writer. Write high-quality, engaging content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=min(max_tokens, 4096),
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")

    async def _call_huggingface(self, prompt: str, max_tokens: int) -> Optional[str]:
        """Call HuggingFace Inference API (Free: Limited)"""
        if not self.hf_client:
            raise Exception("HuggingFace client not initialized")

        try:
            response = self.hf_client.text_generation(
                prompt,
                model="mistralai/Mistral-7B-Instruct-v0.1",
                max_new_tokens=min(max_tokens, 1024),
                temperature=0.7
            )
            return response
        except Exception as e:
            raise Exception(f"HuggingFace API error: {str(e)}")

    async def _call_gemini(self, prompt: str, max_tokens: int) -> Optional[str]:
        """Call Gemini API (Free: 20 req/day)"""
        if not self.genai:
            raise Exception("Gemini client not initialized")

        try:
            model = self.genai.GenerativeModel("gemini-3.8-flash")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

    async def _call_claude(self, prompt: str, max_tokens: int) -> Optional[str]:
        """Call Claude API (Paid: Requires API key)"""
        if not self.claude_client:
            raise Exception("Claude client not initialized - set CLAUDE_API_KEY")

        try:
            response = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")

    async def _call_openai(self, prompt: str, max_tokens: int) -> Optional[str]:
        """Call OpenAI API (Paid: Requires API key)"""
        if not self.openai_client:
            raise Exception("OpenAI client not initialized - set OPENAI_API_KEY")

        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional blog writer. Write high-quality, engaging content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")


class ProviderHealthChecker:
    """Monitors provider health and quota"""

    def __init__(self, providers_config: Dict = None):
        self.config = providers_config or {}
        self.health_status = {}
        self.manager = AIProviderManager(providers_config)

    async def check_all_providers(self) -> Dict[str, bool]:
        """Check health of all providers"""
        logger.info("🏥 Starting provider health check...")

        test_prompt = "Say 'OK' in one word only."

        providers = ["groq", "huggingface", "gemini", "claude", "openai"]

        for provider_id in providers:
            try:
                result = await self.manager._call_provider(provider_id, test_prompt, max_tokens=10)
                self.health_status[provider_id] = result is not None
                if result:
                    logger.info(f"✅ {provider_id.upper()}: Healthy")
                else:
                    logger.warning(f"⚠️  {provider_id.upper()}: No response")
            except Exception as e:
                self.health_status[provider_id] = False
                logger.warning(f"❌ {provider_id.upper()}: {str(e)[:80]}")

        return self.health_status

    async def _check_provider(self, provider_id: str, provider: Dict) -> bool:
        """Check single provider health"""
        try:
            result = await self.manager._call_provider(provider_id, "Test", max_tokens=10)
            return result is not None
        except Exception as e:
            logger.warning(f"Health check failed for {provider_id}: {e}")
            return False


# Global instance for use in agents
ai_provider_manager = AIProviderManager()
