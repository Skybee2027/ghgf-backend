"""
GHGF Orchestrator - Main Entry Point
Runs all 10 robots with intelligent provider fallback chains
"""

import asyncio
import logging
import json
import os
from datetime import datetime
from typing import Dict, Any, List
from ai_provider_manager import AIProviderManager
from robo_3_5_images import ImageGeneratorRobot
from ghgf_agents_6_9 import GHGF_7_Publisher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/logs/ghgf_orchestration.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class GHGFOrchestrator:
    """
    Main orchestrator for GHGF autonomous blogging system.
    Manages all robots and provider fallback chains.
    """

    def __init__(self):
        self.ai_provider_manager = AIProviderManager()
        self.execution_log = {
            "timestamp": datetime.now().isoformat(),
            "robots_executed": [],
            "total_cost": 0,
            "provider_usage": {},
            "expensive_fallbacks": [],
            "warnings": []
        }

    async def run_daily_pipeline(self) -> Dict[str, Any]:
        """
        Run the complete daily GHGF pipeline.

        Execution order:
        1. ROBO 1 (08:00) - Trends Discovery
        2. ROBO 2 (08:45) - Outline Generation
        3. ROBO 3 (09:30) - Content Writer
        4. ROBO 3.5 (10:15) - Image Generator ← Uses fallback chain with OpenAI last
        5. ROBO 4 (10:45) - Affiliate Research
        6. ROBO 5 (11:15) - Content Reviewer
        7. ROBO 6 (11:45) - Compliance Checker
        8. ROBO 7 (12:30) - Auto Publisher
        9. ROBO 8 (14:00+) - Monitor (hourly)
        10. ROBO 9 (17:00) - Optimizer
        """

        logger.info("="*80)
        logger.info("GHGF DAILY AUTOMATION PIPELINE STARTED")
        logger.info("="*80)

        # Execute robots in sequence
        try:
            # ROBO 1: Trends Discovery
            logger.info("\n[ROBO 1] Starting Trends Discovery...")
            trends = await self._robo_1_trends()
            self.execution_log["robots_executed"].append({
                "robot": "ROBO 1 - Trends",
                "status": "success" if trends else "failed",
                "timestamp": datetime.now().isoformat()
            })

            # ROBO 2: Outline Generation
            logger.info("\n[ROBO 2] Starting Outline Generation...")
            outlines = await self._robo_2_outlines(trends)
            self.execution_log["robots_executed"].append({
                "robot": "ROBO 2 - Outlines",
                "status": "success" if outlines else "failed",
                "timestamp": datetime.now().isoformat()
            })

            # ROBO 3: Content Writer
            logger.info("\n[ROBO 3] Starting Content Writer...")
            blogs = await self._robo_3_writer(outlines)
            self.execution_log["robots_executed"].append({
                "robot": "ROBO 3 - Writer",
                "status": "success" if blogs else "failed",
                "timestamp": datetime.now().isoformat()
            })

            # ROBO 3.5: Image Generator (with fallback chain)
            logger.info("\n[ROBO 3.5] Starting Image Generator...")
            images = await self._robo_3_5_images(blogs)
            self.execution_log["robots_executed"].append({
                "robot": "ROBO 3.5 - Images",
                "status": "success" if images else "failed",
                "timestamp": datetime.now().isoformat(),
                "provider_stats": self._extract_image_stats(images)
            })

            # Check for expensive fallbacks
            if images and self._has_expensive_fallbacks(images):
                self.execution_log["expensive_fallbacks"] = self._extract_expensive_fallbacks(images)
                logger.warning(f"⚠️  {len(self.execution_log['expensive_fallbacks'])} images used expensive OpenAI DALL-E")

            # ROBO 4: Affiliate Research
            logger.info("\n[ROBO 4] Starting Affiliate Research...")
            affiliates = await self._robo_4_affiliate(blogs)
            self.execution_log["robots_executed"].append({
                "robot": "ROBO 4 - Affiliate",
                "status": "success" if affiliates else "failed",
                "timestamp": datetime.now().isoformat()
            })

            # ROBO 5: Content Reviewer
            logger.info("\n[ROBO 5] Starting Content Reviewer...")
            reviewed = await self._robo_5_reviewer(blogs)
            self.execution_log["robots_executed"].append({
                "robot": "ROBO 5 - Reviewer",
                "status": "success" if reviewed else "failed",
                "timestamp": datetime.now().isoformat()
            })

            # ROBO 6: Compliance Checker
            logger.info("\n[ROBO 6] Starting Compliance Checker...")
            compliant = await self._robo_6_compliance(reviewed)
            self.execution_log["robots_executed"].append({
                "robot": "ROBO 6 - Compliance",
                "status": "success" if compliant else "failed",
                "timestamp": datetime.now().isoformat()
            })

            # ROBO 7: Auto Publisher
            logger.info("\n[ROBO 7] Starting Auto Publisher...")
            published = await self._robo_7_publisher(compliant, images, affiliates)
            self.execution_log["robots_executed"].append({
                "robot": "ROBO 7 - Publisher",
                "status": "success" if published else "failed",
                "timestamp": datetime.now().isoformat()
            })

            # ROBO 8: Monitor
            logger.info("\n[ROBO 8] Starting Monitor...")
            monitored = await self._robo_8_monitor(published)
            self.execution_log["robots_executed"].append({
                "robot": "ROBO 8 - Monitor",
                "status": "success" if monitored else "failed",
                "timestamp": datetime.now().isoformat()
            })

            # ROBO 9: Optimizer
            logger.info("\n[ROBO 9] Starting Optimizer...")
            optimized = await self._robo_9_optimizer(published)
            self.execution_log["robots_executed"].append({
                "robot": "ROBO 9 - Optimizer",
                "status": "success" if optimized else "failed",
                "timestamp": datetime.now().isoformat()
            })

            # Calculate totals
            self.execution_log["total_cost"] = self._calculate_total_cost()

            logger.info("\n" + "="*80)
            logger.info("DAILY PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("="*80)

            return self.execution_log

        except Exception as e:
            logger.error(f"❌ Pipeline failed: {str(e)}", exc_info=True)
            self.execution_log["error"] = str(e)
            return self.execution_log

    # ========================================================================
    # ROBOT IMPLEMENTATIONS (Stubs - integrate with actual implementations)
    # ========================================================================

    async def _robo_1_trends(self) -> List[str]:
        """ROBO 1: Discover trending health topics"""
        logger.info("Finding trending health topics...")

        prompt = """
        Identify 5-10 currently trending health and fitness topics that:
        1. Are searchable on Google
        2. Have commercial intent (people buy solutions)
        3. Are not overly saturated with content
        4. Have affiliate opportunities

        Return as a numbered list.
        """

        # Use free-first fallback chain for text generation
        result = await self.ai_provider_manager.generate_text(prompt, task_type="trends")

        if result.get("success"):
            logger.info(f"✓ Found trends using {result.get('provider')}")
            return result.get("text", "").split("\n")
        else:
            logger.error("✗ Failed to generate trends")
            return []

    async def _robo_2_outlines(self, trends: List[str]) -> List[Dict]:
        """ROBO 2: Generate blog outlines for each trend"""
        logger.info(f"Generating outlines for {len(trends)} trends...")

        outlines = []
        for trend in trends[:5]:  # Limit to 5 for daily
            prompt = f"Create a detailed blog outline for: {trend}\nInclude 7-10 sections with SEO keywords."

            result = await self.ai_provider_manager.generate_text(prompt, task_type="outline")

            if result.get("success"):
                outlines.append({
                    "topic": trend,
                    "outline": result.get("text"),
                    "provider": result.get("provider")
                })

        logger.info(f"✓ Generated {len(outlines)} outlines")
        return outlines

    async def _robo_3_writer(self, outlines: List[Dict]) -> List[Dict]:
        """ROBO 3: Write full blog posts"""
        logger.info(f"Writing {len(outlines)} blog posts...")

        blogs = []
        for outline in outlines[:3]:  # Limit to 3 posts per day
            prompt = f"""
            Write a comprehensive 1500+ word blog post based on this outline:

            {outline.get('outline', '')}

            Requirements:
            - SEO optimized
            - Engaging and informative
            - Include call-to-action
            - Professional tone
            """

            result = await self.ai_provider_manager.generate_text(prompt, task_type="blog_post")

            if result.get("success"):
                blogs.append({
                    "title": outline.get("topic"),
                    "content": result.get("text"),
                    "provider": result.get("provider"),
                    "cost": result.get("cost", 0)
                })

        logger.info(f"✓ Wrote {len(blogs)} blog posts")
        self.execution_log["total_cost"] += sum(b.get("cost", 0) for b in blogs)
        return blogs

    async def _robo_3_5_images(self, blogs: List[Dict]) -> List[Dict]:
        """ROBO 3.5: Generate featured images with fallback chain"""
        logger.info(f"Generating images for {len(blogs)} blog posts...")

        image_robot = ImageGeneratorRobot()

        results = await image_robot.generate_batch_images(
            [{"topic": b.get("title"), "title": b.get("title")} for b in blogs]
        )

        logger.info(f"✓ Generated {len(results.get('successful', []))} images")
        self.execution_log["total_cost"] += results.get("total_cost", 0)

        return results

    async def _robo_4_affiliate(self, blogs: List[Dict]) -> List[Dict]:
        """ROBO 4: Research affiliate products"""
        logger.info(f"Researching affiliates for {len(blogs)} posts...")

        affiliates = []
        for blog in blogs:
            prompt = f"""
            Find 5 best affiliate products/services for this blog topic: {blog.get('title')}

            Return format:
            1. Product Name | Affiliate Network | Commission | Link

            Focus on ClickBank, Amazon Associates, ShareASale
            """

            result = await self.ai_provider_manager.generate_text(prompt, task_type="affiliate_research")

            if result.get("success"):
                affiliates.append({
                    "topic": blog.get("title"),
                    "products": result.get("text"),
                    "provider": result.get("provider")
                })

        logger.info(f"✓ Found affiliates for {len(affiliates)} posts")
        return affiliates

    async def _robo_5_reviewer(self, blogs: List[Dict]) -> List[Dict]:
        """ROBO 5: Review content quality"""
        logger.info("Reviewing content quality...")

        reviewed = []
        for blog in blogs:
            prompt = f"""
            Review this blog content for:
            1. Readability (Flesch-Kincaid)
            2. SEO optimization
            3. Engagement level
            4. Factual accuracy

            Content:
            {blog.get('content', '')[:500]}...

            Score 1-10 and list improvements.
            """

            result = await self.ai_provider_manager.generate_text(prompt, task_type="review")

            if result.get("success"):
                reviewed.append({
                    "title": blog.get("title"),
                    "original_content": blog.get("content"),
                    "review": result.get("text"),
                    "provider": result.get("provider")
                })

        logger.info(f"✓ Reviewed {len(reviewed)} posts")
        return reviewed

    async def _robo_6_compliance(self, reviewed: List[Dict]) -> List[Dict]:
        """ROBO 6: Check FTC compliance"""
        logger.info("Checking FTC compliance...")

        compliant = []
        for item in reviewed:
            prompt = f"""
            Check this health content for FTC compliance:

            {item.get('review', '')[:500]}

            1. Add affiliate disclosure if missing
            2. Flag any false health claims
            3. Ensure proper formatting

            Return compliance report.
            """

            result = await self.ai_provider_manager.generate_text(prompt, task_type="compliance")

            if result.get("success"):
                compliant.append({
                    "title": item.get("title"),
                    "content": item.get("original_content"),
                    "compliance_check": result.get("text"),
                    "provider": result.get("provider"),
                    "approved": "BLOCKED" not in result.get("text", "")
                })

        logger.info(f"✓ Compliance check complete - {len(compliant)} approved")
        return compliant

    async def _robo_7_publisher(self, posts: List[Dict], images: Dict, affiliates: List[Dict]) -> List[Dict]:
        """ROBO 7: Publish to WordPress"""
        logger.info(f"Publishing {len(posts)} posts to WordPress...")

        published = []
        publisher = GHGF_7_Publisher()

        for post in posts:
            if post.get("approved"):
                title = post.get("title", "Untitled")
                content = post.get("content", "")
                tags = post.get("tags", [])

                logger.info(f"Publishing: {title}")

                # Call the actual WordPress publisher
                result = await publisher.execute(title, content, tags)

                if result.get("status") == "success":
                    published.append({
                        "title": title,
                        "status": "published",
                        "post_id": result.get("data", {}).get("post_id"),
                        "url": result.get("data", {}).get("url"),
                        "timestamp": datetime.now().isoformat()
                    })
                    logger.info(f"✓ Published: {title}")
                else:
                    logger.error(f"✗ Failed to publish: {title} - {result.get('error', 'Unknown error')}")

        logger.info(f"✓ Published {len(published)}/{len([p for p in posts if p.get('approved')])} approved posts")
        return published

    async def _robo_8_monitor(self, published: List[Dict]) -> Dict:
        """ROBO 8: Monitor website health"""
        logger.info("Running system monitoring...")

        # Check website uptime, performance, etc.
        logger.info("✓ System monitoring complete")
        return {"status": "healthy", "uptime": "99.9%"}

    async def _robo_9_optimizer(self, published: List[Dict]) -> Dict:
        """ROBO 9: Optimize published content"""
        logger.info("Running post-publication optimization...")

        logger.info("✓ Optimization complete")
        return {"optimized_posts": len(published)}

    # ========================================================================
    # UTILITIES
    # ========================================================================

    def _extract_image_stats(self, images: Dict) -> Dict:
        """Extract image generation statistics"""
        return {
            "successful": len(images.get("successful", [])),
            "failed": len(images.get("failed", [])),
            "total_cost": images.get("total_cost", 0),
            "providers_used": images.get("provider_usage", {})
        }

    def _has_expensive_fallbacks(self, images: Dict) -> bool:
        """Check if expensive OpenAI DALL-E was used"""
        return images.get("provider_usage", {}).get("openai_dalle", 0) > 0

    def _extract_expensive_fallbacks(self, images: Dict) -> List[Dict]:
        """Extract details on expensive fallback usage"""
        return images.get("expensive_alerts", [])

    def _calculate_total_cost(self) -> float:
        """Calculate total daily cost"""
        usage_report = self.ai_provider_manager.get_usage_report()
        return usage_report.get("total_image_cost", 0)

    def save_execution_log(self):
        """Save execution log to file"""
        log_file = f"data/logs/execution_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"

        with open(log_file, 'w') as f:
            json.dump(self.execution_log, f, indent=2)

        logger.info(f"✓ Execution log saved to {log_file}")


async def main():
    """Main entry point"""

    orchestrator = GHGFOrchestrator()

    # Run the daily pipeline
    result = await orchestrator.run_daily_pipeline()

    # Save logs
    orchestrator.save_execution_log()

    # Print summary
    print("\n" + "="*80)
    print("EXECUTION SUMMARY")
    print("="*80)
    print(json.dumps({
        "timestamp": result.get("timestamp"),
        "robots_executed": len(result.get("robots_executed", [])),
        "total_cost": result.get("total_cost", 0),
        "expensive_fallbacks": len(result.get("expensive_fallbacks", [])),
        "status": "SUCCESS" if "error" not in result else "FAILED"
    }, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
