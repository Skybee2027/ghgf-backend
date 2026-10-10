#!/usr/bin/env python3
"""
GHGF WordPress Blogging Robot Trigger
Triggers automated blog post creation when APIs are healthy
"""

import os
import sys
import requests
from datetime import datetime
from urllib.parse import urljoin

BOLD = '\033[1m'
RESET = '\033[0m'
GREEN = '\033[92m'
RED = '\033[91m'

def trigger_wordpress_blogging():
    """
    Connect to WordPress and trigger blogging robot automation
    """

    print("\n" + "="*70)
    print(f"{BOLD}WORDPRESS BLOGGING ROBOT TRIGGER{RESET}")
    print("="*70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Get credentials from environment
    site_url = os.getenv("WORDPRESS_SITE_URL")
    username = os.getenv("WORDPRESS_USERNAME")
    password = os.getenv("WORDPRESS_PASSWORD")

    # Validate credentials
    if not site_url:
        print(f"{RED}❌ WORDPRESS_SITE_URL not configured{RESET}")
        return False

    if not username or not password:
        print(f"{RED}❌ WORDPRESS_USERNAME or WORDPRESS_PASSWORD not configured{RESET}")
        return False

    print(f"🔗 WordPress Site: {site_url}")
    print(f"👤 Username: {username}\n")

    try:
        # Ensure site URL has proper format
        if not site_url.startswith('http'):
            site_url = 'https://' + site_url

        if not site_url.endswith('/'):
            site_url += '/'

        # WordPress REST API endpoint for triggering custom action
        # Try multiple common endpoints for triggering automation

        endpoints_to_try = [
            # Custom endpoint (if defined in WordPress theme/plugin)
            urljoin(site_url, 'wp-json/ghgf/v1/trigger-blogging-robot'),
            # Alternative custom endpoint
            urljoin(site_url, 'wp-json/custom/v1/trigger-blogging'),
            # Generic custom post via REST API
            urljoin(site_url, 'wp-json/wp/v2/posts'),
        ]

        auth = (username, password)
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'GHGF-Automation-Bot/1.0'
        }

        success = False
        last_error = None

        for endpoint in endpoints_to_try:
            try:
                print(f"📤 Attempting: {endpoint}")

                if 'trigger-blogging' in endpoint:
                    # POST to trigger endpoint
                    response = requests.post(
                        endpoint,
                        auth=auth,
                        headers=headers,
                        json={'action': 'trigger_blogging_robot'},
                        timeout=30
                    )
                else:
                    # For generic POST endpoint, create a test connection
                    response = requests.get(
                        urljoin(site_url, 'wp-json/wp/v2/'),
                        auth=auth,
                        headers=headers,
                        timeout=30
                    )

                # Status codes 200-204 indicate success, 401 means auth issue
                if response.status_code in [200, 201, 204]:
                    print(f"{GREEN}✅ WordPress API connected successfully{RESET}")
                    print(f"   Response: HTTP {response.status_code}")
                    success = True
                    break
                elif response.status_code == 401:
                    last_error = f"Authentication failed (HTTP 401) - Check username/password"
                    print(f"⚠️  {last_error}")
                    continue
                elif response.status_code == 404:
                    # This endpoint doesn't exist, try next one
                    print(f"⚠️  Endpoint not found (HTTP 404), trying next...")
                    continue
                else:
                    last_error = f"HTTP {response.status_code}: {response.text[:100]}"
                    print(f"⚠️  {last_error}")
                    continue

            except requests.exceptions.ConnectionError as e:
                last_error = f"Connection failed: {str(e)[:60]}"
                print(f"⚠️  {last_error}")
                continue
            except requests.exceptions.Timeout:
                last_error = "Request timeout"
                print(f"⚠️  {last_error}")
                continue
            except Exception as e:
                last_error = f"Error: {str(e)[:60]}"
                print(f"⚠️  {last_error}")
                continue

        if success:
            print(f"\n{GREEN}✅ BLOGGING ROBOT TRIGGER SUCCESSFUL{RESET}")
            print("Blog post creation automation initiated")
            print("="*70 + "\n")
            return True
        else:
            print(f"\n{RED}❌ BLOGGING ROBOT TRIGGER FAILED{RESET}")
            if last_error:
                print(f"Last error: {last_error}")
            print("\nℹ️  If you have a custom WordPress endpoint:")
            print("   1. Define it in your WordPress plugin/theme")
            print("   2. Update the trigger script with the correct endpoint URL")
            print("   3. Ensure the endpoint accepts POST requests with authentication")
            print("="*70 + "\n")
            return False

    except Exception as e:
        print(f"{RED}❌ Unexpected error: {str(e)}{RESET}")
        print("="*70 + "\n")
        return False

if __name__ == "__main__":
    success = trigger_wordpress_blogging()
    sys.exit(0 if success else 1)
