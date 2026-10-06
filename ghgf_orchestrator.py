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
