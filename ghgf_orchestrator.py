"""
GHGF Orchestrator - Main Autonomous Controller
Manages all 9 agents with free-first AI provider fallback
Handles scheduling, costs, diagnostics, and quality gates
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GHGFOrchestrator:
    """Main orchestrator managing all GHGF agents with quality gates"""

    def __init__(self):
        self.data_dir = Path("data")
        self.logs_dir = self.data_dir / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        self._init_database()
        logger.info("✅ GHGF Orchestrator initialized")

    def _init_database(self):
        """Initialize SQLite database for execution logging"""
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

    def _log_execution(self, agent_id: str, agent_name: str, result: Dict[str, Any]):
        """Log agent execution to database"""
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO agent_executions
                (timestamp, agent_id, agent_name, status, quality_score, cost_usd, output_data, errors)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                agent_id,
                agent_name,
                result.get("status", "unknown"),
                result.get("quality_score", 0),
                result.get("cost", 0),
                json.dumps(result.get("data", {}))[:1000],  # Truncate for DB
                result.get("error", "")
            ))
            self.db.commit()
        except Exception as e:
            logger.error(f"Failed to log execution: {e}")

    async def run_once(self):
        """Execute one complete pipeline run"""
        logger.info("\n" + "="*70)
        logger.info("🚀 GHGF AUTONOMOUS PIPELINE STARTING")
        logger.info("="*70)

        start_time = datetime.now()
        total_cost = 0
        executed_agents = []

        try:
            # ============================================================
            # STAGE 1: DISCOVERY & RESEARCH
            # ============================================================

            # Step 1: Discover Trends
            logger.info("\n▶️  STAGE 1: DISCOVERY")
            logger.info("▶️  GHGF_1: Trend Discovery")
            agent1 = GHGF_1_TrendDiscovery()
            result1 = await agent1.execute()
            self._log_execution("GHGF_1", "Trend Discovery", result1)
            executed_agents.append(result1)
            total_cost += result1.get("cost", 0)

            logger.info(f"   Status: {result1.get('status')} | Quality: {result1.get('quality_score')} | Trends: {result1.get('trends_found', 0)}")

            if result1.get("status") != "success":
                logger.error("❌ Trend Discovery failed, stopping pipeline")
                self._print_summary(start_time, total_cost, executed_agents)
                return

            trend = result1.get("data", [{}])[0] if result1.get("data") else {"name": "Weight Loss"}
            topic = trend.get("name", "Weight Loss")
            logger.info(f"   Topic selected: '{topic}'")

            # ============================================================
            # STAGE 2: CONTENT CREATION
            # ============================================================

            logger.info("\n▶️  STAGE 2: CONTENT CREATION")

            # Step 2: Generate Outline
            logger.info(f"▶️  GHGF_2: Outline Generation")
            agent2 = GHGF_2_OutlineGenerator()
            result2 = await agent2.execute(topic)
            self._log_execution("GHGF_2", "Outline Generator", result2)
            executed_agents.append(result2)
            total_cost += result2.get("cost", 0)
            logger.info(f"   Status: {result2.get('status')} | Quality: {result2.get('quality_score')}")

            # Step 3: Write Content
            logger.info(f"▶️  GHGF_3: Content Writing")
            agent3 = GHGF_3_ContentWriter()
            result3 = await agent3.execute(topic, 1500)
            self._log_execution("GHGF_3", "Content Writer", result3)
            executed_agents.append(result3)
            total_cost += result3.get("cost", 0)

            word_count = result3.get("total_words", 0)
            logger.info(f"   Status: {result3.get('status')} | Quality: {result3.get('quality_score')} | Words: {word_count}")

            content = result3.get("data", {}).get("content", "")
            title = result3.get("data", {}).get("title", topic)

            if not content:
                logger.error("❌ Content writing failed, stopping pipeline")
                self._print_summary(start_time, total_cost, executed_agents)
                return

            # Step 3.5: Generate Image
            logger.info(f"▶️  GHGF_3.5: Image Prompt Generation")
            agent3_5 = GHGF_3_5_ImageGenerator()
            result3_5 = await agent3_5.execute(topic)
            self._log_execution("GHGF_3.5", "Image Generator", result3_5)
            executed_agents.append(result3_5)
            total_cost += result3_5.get("cost", 0)
            logger.info(f"   Status: {result3_5.get('status')} | Quality: {result3_5.get('quality_score')}")

            # Step 4: Affiliate Research
            logger.info(f"▶️  GHGF_4: Affiliate Product Research")
            agent4 = GHGF_4_AffiliateResearch()
            result4 = await agent4.execute(topic)
            self._log_execution("GHGF_4", "Affiliate Research", result4)
            executed_agents.append(result4)
            total_cost += result4.get("cost", 0)

            products_found = result4.get("products_found", 0)
            logger.info(f"   Status: {result4.get('status')} | Quality: {result4.get('quality_score')} | Products: {products_found}")

            # ============================================================
            # STAGE 3: QUALITY CONTROL & COMPLIANCE
            # ============================================================

            logger.info("\n▶️  STAGE 3: QUALITY CONTROL")

            # Step 5: Content Review
            logger.info(f"▶️  GHGF_5: Content Quality Review")
            agent5 = GHGF_5_ContentReviewer()
            result5 = await agent5.execute(content)
            self._log_execution("GHGF_5", "Content Reviewer", result5)
            executed_agents.append(result5)
            total_cost += result5.get("cost", 0)

            quality_score = result5.get("quality_score", 0)
            logger.info(f"   Status: {result5.get('status')} | Quality Score: {quality_score}/10")

            # Step 6: Compliance Check (QUALITY GATE)
            logger.info(f"▶️  GHGF_6: FTC Compliance Check")
            agent6 = GHGF_6_ComplianceChecker()
            result6 = await agent6.execute(content)
            self._log_execution("GHGF_6", "Compliance Checker", result6)
            executed_agents.append(result6)
            total_cost += result6.get("cost", 0)

            compliance_score = result6.get("quality_score", 0)
            compliant = result6.get("compliant", False)
            logger.info(f"   Status: {result6.get('status')} | Compliance Score: {compliance_score}/100 | Compliant: {compliant}")

            # COMPLIANCE GATE: Stop if not compliant
            if not compliant:
                logger.warning("⚠️  ⛔ COMPLIANCE GATE FAILED - Content not FTC compliant")
                logger.warning("   This post will NOT be published")
                self._print_summary(start_time, total_cost, executed_agents)
                return

            logger.info("   ✅ COMPLIANCE GATE PASSED - Proceeding to publication")

            # ============================================================
            # STAGE 4: PUBLISHING & OPTIMIZATION
            # ============================================================

            logger.info("\n▶️  STAGE 4: PUBLISHING & OPTIMIZATION")

            # Step 7: Publish to WordPress
            logger.info(f"▶️  GHGF_7: Publishing to WordPress")
            agent7 = GHGF_7_Publisher()
            result7 = await agent7.execute(
                title=title,
                content=content,
                tags=["health", "fitness"]
            )
            self._log_execution("GHGF_7", "WordPress Publisher", result7)
            executed_agents.append(result7)
            total_cost += result7.get("cost", 0)

            if result7.get("status") == "success":
                post_url = result7.get("data", {}).get("url", "N/A")
                logger.info(f"   ✅ Published! URL: {post_url}")
            else:
                logger.warning(f"   ⚠️  Publication failed: {result7.get('error', 'Unknown error')}")

            # Step 8: Performance Monitoring
            logger.info(f"▶️  GHGF_8: Performance Monitoring Recommendations")
            agent8 = GHGF_8_PerformanceMonitor()
            result8 = await agent8.execute()
            self._log_execution("GHGF_8", "Performance Monitor", result8)
            executed_agents.append(result8)
            total_cost += result8.get("cost", 0)
            logger.info(f"   Status: {result8.get('status')} | Quality: {result8.get('quality_score')}")

            # Step 9: SEO Optimization
            logger.info(f"▶️  GHGF_9: SEO Optimization")
            agent9 = GHGF_9_SEOOptimizer()
            result9 = await agent9.execute(title, content)
            self._log_execution("GHGF_9", "SEO Optimizer", result9)
            executed_agents.append(result9)
            total_cost += result9.get("cost", 0)

            seo_score = result9.get("quality_score", 0)
            logger.info(f"   Status: {result9.get('status')} | SEO Score: {seo_score}/100")

        except Exception as e:
            logger.error(f"❌ Pipeline error: {str(e)}")
            import traceback
            traceback.print_exc()

        # Print final summary
        self._print_summary(start_time, total_cost, executed_agents)

    def _print_summary(self, start_time: datetime, total_cost: float, executed_agents: List[Dict]):
        """Print execution summary"""
        duration = (datetime.now() - start_time).total_seconds()
        successful = sum(1 for a in executed_agents if a.get("status") == "success")
        avg_quality = sum(a.get("quality_score", 0) for a in executed_agents) / len(executed_agents) if executed_agents else 0

        logger.info("\n" + "="*70)
        logger.info("📊 PIPELINE EXECUTION SUMMARY")
        logger.info("="*70)
        logger.info(f"Duration: {duration:.1f} seconds")
        logger.info(f"Agents Executed: {len(executed_agents)}")
        logger.info(f"Successful: {successful}/{len(executed_agents)}")
        logger.info(f"Average Quality Score: {avg_quality:.1f}/10")
        logger.info(f"Total Cost: ${total_cost:.2f}")
        logger.info("="*70 + "\n")

    async def run_continuous(self, interval_minutes: int = 1440):
        """Run pipeline continuously on schedule (default: daily)"""
        logger.info(f"Starting continuous mode - Running every {interval_minutes} minutes")

        while True:
            try:
                await self.run_once()
                logger.info(f"\n⏳ Next run in {interval_minutes} minutes...")
                await asyncio.sleep(interval_minutes * 60)
            except Exception as e:
                logger.error(f"Error in continuous mode: {e}")
                await asyncio.sleep(60)  # Wait before retry


async def main():
    """Main entry point"""
    orchestrator = GHGFOrchestrator()

    # Run once (suitable for GitHub Actions)
    await orchestrator.run_once()

    # Optionally, uncomment for local continuous testing:
    # await orchestrator.run_continuous(interval_minutes=60)


if __name__ == "__main__":
    asyncio.run(main())
