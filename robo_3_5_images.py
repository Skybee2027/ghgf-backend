"""
GHGF Robot 3.5 - Image Generator
Generates featured images with intelligent fallback chains
OpenAI DALL-E is the LAST resort option - only when all free/cheap options fail
"""

import logging
import asyncio
from typing import Dict, Any
from ai_provider_manager import AIProviderManager

logger = logging.getLogger(__name__)

class ImageGeneratorRobot:
    """
    Generates images for GHGF blog posts using fallback chain:
    1. Stable Diffusion local (100% FREE)
    2. Bing Image Creator (100% FREE)
    3. Hugging Face (FREE tier)
    4. Replicate (cheap: ~$0.01)
    5. Together AI (cheap: ~$0.02)
    6. Stability AI (moderate: ~$0.015)
    7. OpenAI DALL-E 3 (MOST EXPENSIVE: $0.08) ← ABSOLUTE LAST RESORT
    """

    def __init__(self):
        self.provider_manager = AIProviderManager()
        self.generated_images = []
        self.fallback_stats = {
            "stable_diffusion_local": 0,
            "bing_free": 0,
            "huggingface": 0,
            "replicate": 0,
            "together_ai": 0,
            "stability_ai": 0,
            "openai_dalle": 0  # Track if we HAD to use expensive option
        }

    async def generate_featured_image(self, topic: str, blog_title: str) -> Dict[str, Any]:
        """
        Generate a featured image for a blog post.

        Fallback Chain Logic:
        - Try free options first
        - Skip to next provider if current fails
        - Track which providers succeeded/failed
        - Log WARNING if OpenAI was used
        """

        # Create a good prompt for image generation
        prompt = self._create_image_prompt(topic, blog_title)

        logger.info(f"Generating image for: {blog_title}")
        logger.info(f"Prompt: {prompt}")

        # Use the provider manager's fallback chain
        result = await self.provider_manager.generate_image(prompt, size="1024x1024")

        if result.get("success"):
            provider_used = result.get("provider", "unknown")
            cost = result.get("cost", 0)

            self.fallback_stats[provider_used] += 1

            # Check if we had to use expensive OpenAI
            if provider_used == "openai_dalle":
                logger.critical(f"🔴 EXPENSIVE: Used OpenAI DALL-E (${cost:.4f}) after free options exhausted!")
                logger.critical(f"   This suggests free tiers are hitting rate limits")
            else:
                logger.info(f"✓ Generated with {provider_used} (cost: ${cost:.4f})")

            return {
                "success": True,
                "image_url": result.get("image_url"),
                "image_base64": result.get("image"),
                "topic": topic,
                "blog_title": blog_title,
                "provider": provider_used,
                "cost": cost,
                "prompt": prompt
            }
        else:
            logger.error(f"❌ Image generation failed for: {blog_title}")
            return {
                "success": False,
                "error": "All image providers failed",
                "topic": topic,
                "blog_title": blog_title
            }

    async def generate_batch_images(self, blog_posts: list) -> Dict[str, Any]:
        """
        Generate images for multiple blog posts.
        Tracks which providers were used and logs if expensive options were needed.
        """

        results = {
            "successful": [],
            "failed": [],
            "total_cost": 0,
            "provider_usage": self.fallback_stats.copy(),
            "expensive_alerts": []
        }

        for post in blog_posts:
            image_result = await self.generate_featured_image(
                post.get("topic", ""),
                post.get("title", "")
            )

            if image_result["success"]:
                results["successful"].append(image_result)
                results["total_cost"] += image_result["cost"]

                # Alert if OpenAI was used
                if image_result["provider"] == "openai_dalle":
                    results["expensive_alerts"].append({
                        "title": image_result["blog_title"],
                        "cost": image_result["cost"],
                        "reason": "Free options exhausted"
                    })
            else:
                results["failed"].append(image_result)

        # Log summary
        logger.info(f"✓ Generated {len(results['successful'])} images")
        logger.info(f"✗ Failed to generate {len(results['failed'])} images")
        logger.info(f"💰 Total image cost: ${results['total_cost']:.2f}")

        if results["expensive_alerts"]:
            logger.warning(f"⚠️  WARNING: {len(results['expensive_alerts'])} images used expensive OpenAI DALL-E")
            for alert in results["expensive_alerts"]:
                logger.warning(f"   - {alert['title']}: ${alert['cost']:.4f}")

        return results

    def _create_image_prompt(self, topic: str, blog_title: str) -> str:
        """
        Create an optimized image generation prompt.
        This works with all providers' image models.
        """

        # Clean up the prompt to work with different models
        prompt = f"""
        Create a professional health and fitness blog featured image for the topic: "{topic}"
        Blog post title: "{blog_title}"

        Requirements:
        - Bright, clean background
        - Relevant health/fitness imagery
        - Professional quality
        - Blog-ready resolution
        - No text overlays
        - Modern design style
        - Vibrant colors

        Style: Professional health blog, stock photo quality, modern aesthetic
        """

        return prompt.strip()

    def get_fallback_report(self) -> Dict[str, Any]:
        """
        Get report on provider usage and fallback chain effectiveness.
        """

        total_generated = sum(self.fallback_stats.values())

        report = {
            "total_images_generated": total_generated,
            "provider_breakdown": self.fallback_stats,
            "free_tier_usage": {
                "stable_diffusion_local": self.fallback_stats["stable_diffusion_local"],
                "bing_free": self.fallback_stats["bing_free"],
                "huggingface": self.fallback_stats["huggingface"],
                "total_free": sum([
                    self.fallback_stats["stable_diffusion_local"],
                    self.fallback_stats["bing_free"],
                    self.fallback_stats["huggingface"]
                ])
            },
            "cheap_tier_usage": {
                "replicate": self.fallback_stats["replicate"],
                "together_ai": self.fallback_stats["together_ai"],
                "stability_ai": self.fallback_stats["stability_ai"],
                "total_cheap": sum([
                    self.fallback_stats["replicate"],
                    self.fallback_stats["together_ai"],
                    self.fallback_stats["stability_ai"]
                ])
            },
            "expensive_usage": {
                "openai_dalle": self.fallback_stats["openai_dalle"],
                "status": "CRITICAL" if self.fallback_stats["openai_dalle"] > 0 else "GOOD"
            },
            "fallback_effectiveness": {
                "free_tier_percentage": (self.fallback_stats.get("huggingface", 0) +
                                        self.fallback_stats.get("bing_free", 0) +
                                        self.fallback_stats.get("stable_diffusion_local", 0)) / total_generated * 100 if total_generated > 0 else 0,
                "expensive_fallback_percentage": self.fallback_stats["openai_dalle"] / total_generated * 100 if total_generated > 0 else 0
            }
        }

        return report


async def main():
    """
    Test the image generation robot with fallback chains.
    """

    logger.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    robot = ImageGeneratorRobot()

    # Test with sample blog posts
    sample_posts = [
        {
            "topic": "Intermittent Fasting",
            "title": "Ultimate Guide to Intermittent Fasting Benefits"
        },
        {
            "topic": "High Intensity Interval Training",
            "title": "HIIT Workouts for Maximum Fat Loss"
        },
        {
            "topic": "Muscle Recovery",
            "title": "Best Post-Workout Recovery Techniques"
        }
    ]

    print("\n" + "="*80)
    print("GHGF IMAGE GENERATION ROBOT - FALLBACK CHAIN TEST")
    print("="*80 + "\n")

    results = await robot.generate_batch_images(sample_posts)

    print("\n" + "="*80)
    print("FALLBACK CHAIN REPORT")
    print("="*80)

    report = robot.get_fallback_report()

    print(f"\nTotal images generated: {report['total_images_generated']}")
    print(f"\nProvider breakdown:")
    for provider, count in report['provider_breakdown'].items():
        print(f"  {provider}: {count}")

    print(f"\nFree tier usage: {report['free_tier_usage']['total_free']} images")
    print(f"Cheap tier usage: {report['cheap_tier_usage']['total_cheap']} images")
    print(f"Expensive (OpenAI) usage: {report['expensive_usage']['openai_dalle']} images")

    print(f"\nFallback effectiveness:")
    print(f"  Free tier success rate: {report['fallback_effectiveness']['free_tier_percentage']:.1f}%")
    print(f"  Expensive fallback rate: {report['fallback_effectiveness']['expensive_fallback_percentage']:.1f}%")

    if report['expensive_usage']['openai_dalle'] > 0:
        print(f"\n⚠️  WARNING: {report['expensive_usage']['openai_dalle']} images used expensive OpenAI DALL-E")
        print(f"   This means free/cheap options were exhausted!")


if __name__ == "__main__":
    asyncio.run(main())
