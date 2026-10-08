#!/usr/bin/env python3
"""
PHASE 3: BLOGGING ROBOT
Generates and publishes blog posts to WordPress.
"""

import os, sys, json, time, logging
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
import requests
import base64

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/blog_robot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BlogRobot:
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.wp_url = os.getenv("WORDPRESS_SITE_URL")
        self.wp_user = os.getenv("WORDPRESS_USERNAME")
        self.wp_pass = os.getenv("WORDPRESS_PASSWORD")
        self.client = OpenAI(api_key=self.openai_key)
        logger.info("🤖 Blog Robot initialized")
    
    def generate_topic(self):
        """Generate a blog post topic"""
        topics = [
            "Benefits of Regular Exercise for Health",
            "Nutrition Tips for Weight Management",
            "Best Workout Routines for Beginners",
            "Health Benefits of Meditation",
            "How to Stay Fit While Working from Home",
        ]
        return topics[int(time.time()) % len(topics)]
    
    def generate_content(self, topic):
        """Generate blog post content using OpenAI"""
        logger.info(f"📝 Generating content for: {topic}")
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional health and fitness blog writer. Write engaging, informative blog posts."},
                    {"role": "user", "content": f"Write a detailed blog post (500-800 words) about: {topic}. Include introduction, main points, and conclusion. Format as plain text, no markdown."}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            logger.info(f"✓ Content generated ({len(content)} characters)")
            return content
        except Exception as e:
            logger.error(f"✗ Failed to generate content: {e}")
            return None
    
    def publish_to_wordpress(self, title, content):
        """Publish post to WordPress"""
        logger.info(f"📤 Publishing to WordPress: {title}")
        
        try:
            auth = base64.b64encode(f"{self.wp_user}:{self.wp_pass}".encode()).decode()
            headers = {
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/json"
            }
            
            post_data = {
                "title": title,
                "content": content,
                "status": "publish",
                "categories": [1]
            }
            
            response = requests.post(
                f"{self.wp_url}/wp-json/wp/v2/posts",
                headers=headers,
                json=post_data,
                timeout=30
            )
            
            if response.status_code == 201:
                post_id = response.json().get("id")
                post_url = response.json().get("link")
                logger.info(f"✓ Published! Post ID: {post_id}")
                logger.info(f"✓ URL: {post_url}")
                return post_id
            else:
                logger.error(f"✗ Failed to publish (HTTP {response.status_code})")
                logger.error(f"  Response: {response.text[:200]}")
                return None
        except Exception as e:
            logger.error(f"✗ Publishing error: {e}")
            return None
    
    def run(self):
        """Main robot execution"""
        logger.info("=" * 70)
        logger.info("BLOG ROBOT STARTING".center(70))
        logger.info("=" * 70)
        
        # Step 1: Generate topic
        topic = self.generate_topic()
        logger.info(f"Topic: {topic}")
        
        # Step 2: Generate content
        content = self.generate_content(topic)
        if not content:
            logger.error("Cannot proceed without content")
            return False
        
        # Step 3: Publish to WordPress
        post_id = self.publish_to_wordpress(topic, content)
        if not post_id:
            logger.error("Failed to publish post")
            return False
        
        logger.info("=" * 70)
        logger.info("BLOG POST CREATED SUCCESSFULLY!".center(70))
        logger.info("=" * 70)
        return True

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    robot = BlogRobot()
    success = robot.run()
    sys.exit(0 if success else 1)
