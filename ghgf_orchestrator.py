"""
GHGF Orchestrator - Main Autonomous Controller
Manages all 9 agents, handles scheduling, costs, diagnostics
"""

import asyncio
import json
import yaml
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GHGFOrchestrator:
    """Main orchestrator managing all GHGF agents"""

    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(__file__).parent / config_dir
        self.data_dir = Path("data")
        self.logs_dir = self.data_dir / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        self._init_database()
        self._load_config()
        
        logger.info("✅ GHGF Orchestrator initialized")

    def _init_database(self):
        """Initialize SQLite database for logging"""
        db_path = self.logs_dir / "ghgf_execution.db"
        self.db = sqlite3.connect(str(db_path))
        cursor = self.db.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_executions (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                agent_id TEXT,
                agent_name TEXT,
                status TEXT,
                duration_seconds REAL,
                quality_score REAL,
                cost_usd REAL,
                output_data TEXT,
                errors TEXT
            )
        """)
        self.db.commit()

    def _load_config(self):
        """Load YAML configurations"""
        try:
            with open(self.config_dir / "ghgf_agents.yaml") as f:
                self.agents_config = yaml.safe_load(f)
            
            with open(self.config_dir / "ghgf_providers.yaml") as f:
                self.providers_config = yaml.safe_load(f)
            
            with open(self.config_dir / "ghgf_strategy.yaml") as f:
                self.strategy_config = yaml.safe_load(f)
            
            logger.info("✅ Configurations loaded")
        except Exception as e:
            logger.error(f"❌ Config loading failed: {e}")
            raise

    async def run_once(self):
        """Execute one complete pipeline run"""
        logger.info("\n" + "="*60)
        logger.info("🚀 GHGF PIPELINE STARTING")
        logger.info("="*60)
        
        start_time = datetime.now()
        total_cost = 0
        executed_agents = []

        # Execute agents in order
        agent_order = [
            "GHGF_1", "GHGF_2", "GHGF_3", "GHGF_3_5", 
            "GHGF_4", "GHGF_5", "GHGF_6", "GHGF_7", "GHGF_8", "GHGF_9"
        ]

        for agent_id in agent_order:
            if agent_id not in self.agents_config.get("agents", {}):
                continue
            
            agent_config = self.agents_config["agents"][agent_id]
            
            if not agent_config.get("enabled", True):
                logger.info(f"⏭️  {agent_id}: Disabled - Skipping")
                continue

            logger.info(f"\n▶️  {agent_id}: {agent_config.get('name', 'Unknown')}")
            
            # Execute agent
            result = await self._execute_agent(agent_id, agent_config)
            
            # Log result
            self._log_execution(agent_id, agent_config, result)
            
            executed_agents.append({
                "agent_id": agent_id,
                "status": result.get("status", "unknown"),
                "quality": result.get("quality_score", 0)
            })
            
            total_cost += result.get("cost", 0)

        # Summary
        duration = (datetime.now() - start_time).total_seconds()
        logger.info("\n" + "="*60)
        logger.info("📊 PIPELINE SUMMARY")
        logger.info("="*60)
        logger.info(f"✅ Agents Executed: {len(executed_agents)}")
        logger.info(f"⏱️  Total Duration: {duration:.1f} seconds")
        logger.info(f"💰 Total Cost: ${total_cost:.2f}")
        logger.info(f"⭐ Average Quality: {sum(a['quality'] for a in executed_agents) / len(executed_agents) if executed_agents else 0:.1f}/10")
        logger.info("="*60 + "\n")

    async def _execute_agent(self, agent_id: str, config: Dict) -> Dict[str, Any]:
        """Execute a single agent"""
        try:
            # Simulate agent execution
            await asyncio.sleep(0.5)
            
            return {
                "status": "success",
                "quality_score": 8.0,
                "cost": 0.0,
                "tasks_executed": 1,
                "output": f"{agent_id} completed successfully"
            }
        except Exception as e:
            logger.error(f"❌ {agent_id} failed: {e}")
            return {
                "status": "failed",
                "quality_score": 0,
                "cost": 0,
                "error": str(e)
            }

    def _log_execution(self, agent_id: str, config: Dict, result: Dict):
        """Log agent execution to database"""
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO agent_executions 
            (timestamp, agent_id, agent_name, status, duration_seconds, quality_score, cost_usd, output_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            agent_id,
            config.get("name", "Unknown"),
            result.get("status", "unknown"),
            1.0,
            result.get("quality_score", 0),
            result.get("cost", 0),
            json.dumps(result.get("output", ""))
        ))
        self.db.commit()
        
        status_emoji = "✅" if result.get("status") == "success" else "❌"
        quality = result.get("quality_score", 0)
        logger.info(f"{status_emoji} {agent_id}: Quality {quality:.1f}/10")


async def main():
    """Main entry point"""
    orchestrator = GHGFOrchestrator()
    await orchestrator.run_once()


if __name__ == "__main__":
    asyncio.run(main())
