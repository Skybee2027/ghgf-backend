"""
GHGF AI Provider Management
Implements free-first strategy with automatic fallback
"""

import asyncio
import aiohttp
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class AIProviderManager:
    """Manages all AI providers with free-first strategy"""

    def __init__(self, providers_config: Dict):
        self.config = providers_config
        self.fallback_chain = providers_config.get("fallback_chain", [])
        self.provider_stats = {}

    async def call_with_fallback(self, prompt: str, task_type: str = "default") -> Optional[str]:
        """Call AI with automatic fallback on failure"""
        
        for provider_id in self.fallback_chain:
            provider = self.config.get("ai_providers", {}).get(provider_id)
            
            if not provider:
                continue
            
            logger.info(f"Trying provider: {provider.get('name')}")
            
            try:
                result = await self._call_provider(provider_id, provider, prompt)
                if result:
                    logger.info(f"✅ Success with {provider.get('name')}")
                    return result
            except Exception as e:
                logger.warning(f"⚠️  {provider.get('name')} failed: {e}")
                continue
        
        logger.error("❌ All providers exhausted")
        return None

    async def _call_provider(self, provider_id: str, provider: Dict, prompt: str) -> Optional[str]:
        """Call a specific provider"""
        provider_type = provider.get("type")
        
        if provider_type == "api":
            return await self._call_api_provider(provider_id, provider, prompt)
        elif provider_type == "web":
            return await self._call_web_provider(provider_id, provider, prompt)
        elif provider_type == "local":
            return await self._call_local_provider(provider_id, provider, prompt)
        
        return None

    async def _call_api_provider(self, provider_id: str, provider: Dict, prompt: str) -> Optional[str]:
        """Call API-based provider"""
        # Simulated API call
        await asyncio.sleep(0.1)
        return f"Response from {provider.get('name')}"

    async def _call_web_provider(self, provider_id: str, provider: Dict, prompt: str) -> Optional[str]:
        """Call web-based provider"""
        # Simulated web call
        await asyncio.sleep(0.1)
        return f"Response from {provider.get('name')}"

    async def _call_local_provider(self, provider_id: str, provider: Dict, prompt: str) -> Optional[str]:
        """Call local provider"""
        # Simulated local call
        await asyncio.sleep(0.1)
        return f"Response from {provider.get('name')}"


class ProviderHealthChecker:
    """Monitors provider health and quota"""

    def __init__(self, providers_config: Dict):
        self.config = providers_config
        self.health_status = {}

    async def check_all_providers(self) -> Dict[str, bool]:
        """Check health of all providers"""
        for provider_id, provider in self.config.get("ai_providers", {}).items():
            self.health_status[provider_id] = await self._check_provider(provider_id, provider)
        
        return self.health_status

    async def _check_provider(self, provider_id: str, provider: Dict) -> bool:
        """Check single provider health"""
        # Simulated health check
        return True
