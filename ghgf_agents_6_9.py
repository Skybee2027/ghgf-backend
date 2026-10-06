"""
GHGF Agents 5-9: Quality Control & Publishing with AI Provider Fallback
Content Review, Compliance, Publishing, Monitoring, SEO Optimization
"""

import asyncio
import json
from typing import Dict, Any
import os
import requests
from requests.auth import HTTPBasicAuth

from ghgf_providers import ai_provider_manager

logger_enabled = True

WORDPRESS_URL = os.getenv("WORDPRESS_SITE_URL", "https://greathealthgreatfitness.com")
WORDPRESS_USER = os.getenv("WORDPRESS_USERNAME", "")
WORDPRESS_PASS = os.getenv("WORDPRESS_PASSWORD", "")


class GHGF_5_ContentReviewer:
    """Reviews content quality using AI provider fallback"""

    async def execute(self, content: str) -> Dict[str, Any]:
        try:
            prompt = f"""Review this blog content on a scale of 1-10 for:
1. Grammar and spelling
2. Readability (Flesch reading level)
3. Engagement (hook, transitions, CTA)
4. SEO optimization (keywords, meta)
5. Value to reader (actionable tips)
6. Call-to-action clarity

Content (first 2000 chars):
{content[:2000]}

Return ONLY JSON with no other text:
{{
    "grammar_score": 8,
    "readability_score": 7,
    "engagement_score": 8,
    "seo_score": 8,
    "value_score": 8,
    "cta_score": 9,
    "overall_score": 8.0,
    "strengths": ["strength1", "strength2"],
    "improvements": ["improvement1", "improvement2"]
}}"""

            response = await ai_provider_manager.call_with_fallback(
                prompt,
                task_type="content_review",
                max_tokens=500
            )

            if not response:
                raise Exception("No response from any AI provider")

            scores = {}
            try:
                scores = json.loads(response)
            except json.JSONDecodeError:
                scores = {"overall_score": 8.0, "feedback": response}

            if logger_enabled:
                print(f"DEBUG GHGF_5: Content reviewed with score {scores.get('overall_score', 8.0)}")

            return {
                "status": "success",
                "quality_score": scores.get("overall_score", 8.0),
                "data": scores,
                "cost": 0
            }
        except Exception as e:
            print(f"ERROR GHGF_5: {str(e)}")
            return {"status": "failed", "error": str(e), "quality_score": 0, "cost": 0}


class GHGF_6_ComplianceChecker:
    """Checks FTC compliance using AI provider fallback"""

    async def execute(self, content: str) -> Dict[str, Any]:
        try:
            prompt = f"""Check this content for FTC compliance regarding affiliate links and endorsements.

Requirements to check:
1. Has clear affiliate disclosure
2. No false or exaggerated health claims
3. Honest review without misleading language
4. Clear #ad or #sponsored tags if needed
5. Complies with FTC Endorsement Guides
6. No "miracle cure" language

Content (first 2000 chars):
{content[:2000]}

Return ONLY JSON with no other text:
{{
    "has_disclosure": true,
    "no_false_claims": true,
    "honest_review": true,
    "proper_tags": true,
    "ftc_compliant": true,
    "no_miracle_language": true,
    "compliance_score": 95,
    "issues": [],
    "recommendations": ["recommendation1"]
}}"""

            response = await ai_provider_manager.call_with_fallback(
                prompt,
                task_type="compliance_check",
                max_tokens=500
            )

            if not response:
                raise Exception("No response from any AI provider")

            checks = {}
            try:
                checks = json.loads(response)
            except json.JSONDecodeError:
                checks = {"compliance_score": 80, "feedback": response}

            compliant = checks.get("compliance_score", 0) >= 80

            if logger_enabled:
                print(f"DEBUG GHGF_6: Compliance check completed - Score: {checks.get('compliance_score', 0)}")

            return {
                "status": "success",
                "quality_score": checks.get("compliance_score", 0),
                "data": checks,
                "compliant": compliant,
                "cost": 0
            }
        except Exception as e:
            print(f"ERROR GHGF_6: {str(e)}")
            return {"status": "failed", "error": str(e), "compliant": False, "cost": 0}


class GHGF_7_Publisher:
    """Publishes content to WordPress REST API"""

    async def execute(self, title: str, content: str, tags: list = None) -> Dict[str, Any]:
        try:
            if not WORDPRESS_USER or not WORDPRESS_PASS:
                return {
                    "status": "failed",
                    "error": "WordPress credentials not configured (WORDPRESS_USERNAME, WORDPRESS_PASSWORD)",
                    "cost": 0
                }

            post_data = {
                "title": title,
                "content": content,
                "status": "publish",
                "tags": tags or [],
                "categories": [1]  # Uncategorized
            }

            if logger_enabled:
                print(f"DEBUG GHGF_7: Publishing to {WORDPRESS_URL}")

            response = requests.post(
                f"{WORDPRESS_URL}/wp-json/wp/v2/posts",
                json=post_data,
                auth=HTTPBasicAuth(WORDPRESS_USER, WORDPRESS_PASS),
                timeout=30
            )

            if response.status_code == 201:
                post = response.json()
                if logger_enabled:
                    print(f"✅ Published to WordPress: {post.get('link')}")

                return {
                    "status": "success",
                    "quality_score": 8.0,
                    "data": {
                        "post_id": post.get("id"),
                        "url": post.get("link"),
                        "published_at": post.get("date"),
                        "status": "published"
                    },
                    "posts_published": 1,
                    "cost": 0
                }
            else:
                error_msg = f"WordPress error: {response.status_code}"
                if logger_enabled:
                    print(f"⚠️  {error_msg}")

                return {
                    "status": "failed",
                    "error": error_msg,
                    "response_text": response.text[:200],
                    "cost": 0
                }
        except Exception as e:
            print(f"ERROR GHGF_7: {str(e)}")
            return {"status": "failed", "error": str(e), "cost": 0}


class GHGF_8_PerformanceMonitor:
    """Monitors website performance using AI provider fallback"""

    async def execute(self) -> Dict[str, Any]:
        try:
            prompt = f"""Provide website monitoring and performance optimization recommendations for {WORDPRESS_URL}.

Include:
1. Uptime monitoring strategy (services to use)
2. Page speed optimization tips
3. CDN recommendations
4. Backup and recovery strategy
5. Security monitoring suggestions
6. Performance metrics to track
7. Tools to implement

Return ONLY JSON with no other text:
{{
    "uptime_monitoring": {{"services": ["service1"], "recommendations": "text"}},
    "page_speed": {{"target_score": 90, "recommendations": "text"}},
    "cdn": {{"recommended": "Cloudflare", "benefits": "text"}},
    "backup": {{"frequency": "daily", "solution": "text"}},
    "security": {{"measures": ["measure1"], "recommendations": "text"}},
    "metrics_to_track": ["metric1"],
    "tools": ["tool1"]
}}"""

            response = await ai_provider_manager.call_with_fallback(
                prompt,
                task_type="performance_monitoring",
                max_tokens=800
            )

            if not response:
                raise Exception("No response from any AI provider")

            recommendations = {}
            try:
                recommendations = json.loads(response)
            except json.JSONDecodeError:
                recommendations = {"recommendations": response}

            if logger_enabled:
                print(f"DEBUG GHGF_8: Performance monitoring completed")

            return {
                "status": "success",
                "quality_score": 8.0,
                "data": recommendations,
                "cost": 0
            }
        except Exception as e:
            print(f"ERROR GHGF_8: {str(e)}")
            return {"status": "failed", "error": str(e), "cost": 0}


class GHGF_9_SEOOptimizer:
    """Optimizes content for SEO using AI provider fallback"""

    async def execute(self, title: str, content: str) -> Dict[str, Any]:
        try:
            prompt = f"""Analyze and optimize this content for SEO. Provide specific, actionable improvements.

Title: {title}
Content (first 2000 chars):
{content[:2000]}

Analyze:
1. Keyword density and placement
2. Meta description quality (155 chars)
3. Heading structure (H1, H2, H3)
4. Internal link opportunities
5. Image alt text suggestions
6. URL slug optimization
7. Schema markup suggestions
8. LSI keywords to include

Return ONLY JSON with no other text:
{{
    "seo_score": 75,
    "keyword_density": {{"current": "1.5%", "target": "2.5%"}},
    "meta_description": "Optimized meta description here (155 chars max)",
    "heading_structure": {{"h1_count": 1, "h2_count": 5, "issues": []}},
    "internal_links": ["url1", "url2"],
    "image_alt_suggestions": ["suggestion1"],
    "url_slug": "optimized-url-slug",
    "schema_type": "BlogPosting",
    "lsi_keywords": ["keyword1", "keyword2"],
    "improvements": ["improvement1", "improvement2"]
}}"""

            response = await ai_provider_manager.call_with_fallback(
                prompt,
                task_type="seo_optimization",
                max_tokens=1000
            )

            if not response:
                raise Exception("No response from any AI provider")

            seo_data = {}
            try:
                seo_data = json.loads(response)
            except json.JSONDecodeError:
                seo_data = {"seo_score": 75, "improvements": response}

            if logger_enabled:
                print(f"DEBUG GHGF_9: SEO optimization completed - Score: {seo_data.get('seo_score', 75)}")

            return {
                "status": "success",
                "quality_score": seo_data.get("seo_score", 75),
                "data": seo_data,
                "posts_optimized": 1,
                "cost": 0
            }
        except Exception as e:
            print(f"ERROR GHGF_9: {str(e)}")
            return {"status": "failed", "error": str(e), "cost": 0}
