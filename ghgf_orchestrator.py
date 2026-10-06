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
import sys
import os

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ghgf_agents_1_5 import (
    GHGF_1_TrendDiscovery, GHGF_2_OutlineGenerator, 
    GHGF_3_ContentWriter, GHGF_3_5_ImageGenerator, GHGF_4_AffiliateResearch
)
from ghgf_agents_6_9 import (
    GHGF_5_ContentReviewer, GHGF_6_ComplianceChecker, 
    GHGF_7_Publisher, GHGF_8_PerformanceMonitor, GHGF_9_SEOOptimizer
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GHGFOrchestrator:
    """Main orchestrator managing all GHGF agents"""

    def __init__(self):
        self.data_dir = Path("data")
        self.logs_dir = self.data_dir / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        self._init_database()
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

    async def run_once(self):
        """Execute one complete pipeline run"""
        logger.info("\n" + "="*60)
        logger.info("🚀 GHGF PIPELINE STARTING")
        logger.info("="*60)
        
        start_time = datetime.now()
        total_cost = 0
        executed_agents = []
        
        # Step 1: Discover Trends
        logger.info("\n▶️  GHGF_1: Trend Discovery")
        agent1 = GHGF_1_TrendDiscovery()
        result1 = await agent1.execute()
        self._log_execution("GHGF_1", "Trend Discovery", result1)
        executed_agents.append(result1)
        total_cost += result1.get("cost", 0)
        
        if result1.get("status") != "success":
            logger.error("❌ Trend Discovery failed, stopping pipeline")
            return
        
        trend = result1.get("data", [{}])[0] if result1.get("data") else {"name": "Weight Loss"}
        topic = trend.get("name", "Weight Loss")
        
        # Step 2: Generate Outline
        logger.info(f"\n▶️  GHGF_2: Outline Generation for '{topic}'")
        agent2 = GHGF_2_OutlineGenerator()
        result2 = await agent2.execute(topic)
        self._log_execution("GHGF_2", "Outline Generator", result2)
        executed_agents.append(result2)
        total_cost += result2.get("cost", 0)
        
        # Step 3: Write Content
        logger.info(f"\n▶️  GHGF_3: Content Writing")
        agent3 = GHGF_3_ContentWriter()
        result3 = await agent3.execute(topic, 1500)
        self._log_execution("GHGF_3", "Content Writer", result3)
        executed_agents.append(result3)
        total_cost += result3.get("cost", 0)
        
        content = result3.get("data", {}).get("content", "")
        
        # Step 3.5: Generate Image
        logger.info(f"\n▶️  GHGF_3.5: Image Generation")
        agent3_5 = GHGF_3_5_ImageGenerator()
        result3_5 = await agent3_5.execute(topic)
        self._log_execution("GHGF_3.5", "Image Generator", result3_5)
        executed_agents.append(result3_5)
        total_cost += result3_5.get("cost", 0)
        
        # Step 4: Affiliate Research
        logger.info(f"\n▶️  GHGF_4: Affiliate Research")
        agent4 = GHGF_4_AffiliateResearch()
        result4 = await agent4.execute(topic)
        self._log_execution("GHGF_4", "Affiliate Research", result4)
        executed_agents.append(result4)
        total_cost += result4.get("cost", 0)
        
        # Step 5: Content Review
        logger.info(f"\n▶️  GHGF_5: Content Review")
        agent5 = GHGF_5_ContentReviewer()
        result5 = await agent5.execute(content)
        self._log_execution("GHGF_5", "Content Reviewer", result5)
        executed_agents.append(result5)
        total_cost += result5.get("cost", 0)
        
        # Step 6: Compliance Check
        logger.info(f"\n▶️  GHGF_6: Compliance Check")
        agent6 = GHGF_6_ComplianceChecker()
        result6 = await agent6.execute(content)
        self._log_execution("GHGF_6", "Compliance Checker", result6)
        executed_agents.append(result6)
        total_cost += result6.get("cost", 0)
        
        if not result6.get("compliant", False):
            logger.warning("⚠️  Content not compliant, skipping publication")
            return
        
        # Step 7: Publish to WordPress
        logger.info(f"\n▶️  GHGF_7: Publishing to WordPress")
        agent7 = GHGF_7_Publisher()
        result7 = await agent7.execute(
            title=result3.get("data", {}).get("title", topic),
            content=content,
            tags=[topic, "health", "fitness"]
        )
        self._log_execution("GHGF_7", "Publisher", result7)
        executed_agents.append(result7)
        total_cost += result7.get("cost", 0)
        
        # Step 8: Monitor Performance
        logger.info(f"\n▶️  GHGF_8: Performance Monitoring")
        agent8 = GHGF_8_PerformanceMonitor()
        result8 = await agent8.execute()
        self._log_execution("GHGF_8", "Performance Monitor", result8)
        executed_agents.append(result8)
        total_cost += result8.get("cost", 0)
        
        # Step 9: SEO Optimization
        logger.info(f"\n▶️  GHGF_9: SEO Optimization")
        agent9 = GHGF_9_SEOOptimizer()
        result9 = await agent9.execute(
            title=result3.get("data", {}).get("title", topic),
            content=content
        )
        self._log_execution("GHGF_9", "SEO Optimizer", result9)
        executed_agents.append(result9)
        total_cost += result9.get("cost", 0)
        
        # Summary
        duration = (datetime.now() - start_time).total_seconds()
        logger.info("\n" + "="*60)
        logger.info("📊 PIPELINE SUMMARY")
        logger.info("="*60)
        logger.info(f"✅ Agents Executed: {len(executed_agents)}")
        logger.info(f"⏱️  Total Duration: {duration:.1f} seconds")
        logger.info(f"💰 Total Cost: ${total_cost:.2f}")
        avg_quality = sum(a.get('quality_score', 0) for a in executed_agents) / len(executed_agents) if executed_agents else 0
        logger.info(f"⭐ Average Quality: {avg_quality:.1f}/10")
        
        if result7.get("status") == "success":
            logger.info(f"📝 Post Published: {result7.get('data', {}).get('url', 'N/A')}")
        
        logger.info("="*60 + "\n")

    def _log_execution(self, agent_id: str, agent_name: str, result: Dict):
        """Log agent execution to database"""
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO agent_executions 
            (timestamp, agent_id, agent_name, status, duration_seconds, quality_score, cost_usd, output_data, errors)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            agent_id,
            agent_name,
            result.get("status", "unknown"),
            1.0,
            result.get("quality_score", 0),
            result.get("cost", 0),
            json.dumps(result.get("data", {})),
            result.get("error", "")
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
