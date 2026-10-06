"""
GHGF Base Agent Class
Abstract base for all agents with standard functionality
"""

import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class GHGFBaseAgent(ABC):
    """Base class for all GHGF agents"""

    def __init__(self, agent_id: str, config: Dict, providers_manager):
        self.agent_id = agent_id
        self.config = config
        self.providers = providers_manager
        self.logger = logging.getLogger(f"GHGF.{agent_id}")

    async def run(self) -> Dict[str, Any]:
        """Execute agent - must be implemented by subclass"""
        try:
            self.logger.info(f"Starting {self.agent_id}...")
            
            # Pre-execution checks
            await self._pre_execution_checks()
            
            # Run main agent logic
            result = await self._execute()
            
            # Quality checks
            await self._post_execution_checks(result)
            
            self.logger.info(f"✅ {self.agent_id} completed")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ {self.agent_id} failed: {e}")
            return {"status": "failed", "error": str(e)}

    async def _pre_execution_checks(self):
        """Pre-execution diagnostics"""
        self.logger.debug("Running pre-execution checks...")

    @abstractmethod
    async def _execute(self) -> Dict[str, Any]:
        """Main agent execution logic - implement in subclass"""
        pass

    async def _post_execution_checks(self, result: Dict):
        """Post-execution quality checks"""
        quality_score = result.get("quality_score", 0)
        if quality_score < 7.0:
            self.logger.warning(f"⚠️  Low quality score: {quality_score}")

    async def call_ai(self, prompt: str, task_type: str = "default") -> Optional[str]:
        """Call AI provider with automatic fallback"""
        return await self.providers.call_with_fallback(prompt, task_type)
