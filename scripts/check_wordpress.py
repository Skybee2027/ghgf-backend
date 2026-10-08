#!/usr/bin/env python3
import os, sys, requests, base64
from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv()

def print_header(title):
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)

def print_result(name, success, detail):
    symbol = "✓" if success else "✗"
    status = "OK" if success else "FAILED"
    print(f"  {symbol} {name:25} {status:10} {detail}")

def test_wordpress():
    print_header("PHASE 2: WORDPRESS CONNECTION TEST")
    
    site_url = os.getenv('WORDPRESS_SITE_URL')
    username = os.getenv('WORDPRESS_USERNAME')
    password = os.getenv('WORDPRESS_PASSWORD')
    
    if not site_url or not username or not password:
        print("\n❌ Missing WordPress credentials in .env")
        return False
    
    print("\nTesting WordPress connection...\n")
    
    # Test 1: Site is reachable
    try:
        response = requests.head(site_url, timeout=5)
        site_ok = response.status_code < 500
        print_result("Site Reachability", site_ok, f"HTTP {response.status_code}")
    except Exception as e:
        print_result("Site Reachability", False, str(e)[:40])
        return False
    
    # Test 2: REST API is available
    rest_url = urljoin(site_url, '/wp-json/')
    try:
        response = requests.get(rest_url, timeout=5)
        rest_ok = response.status_code == 200
        print_result("REST API Available", rest_ok, f"HTTP {response.status_code}")
    except Exception as e:
        print_result("REST API Available", False, str(e)[:40])
        return False
    
    # Test 3: Authentication works
    auth_string = base64.b64encode(f"{username}:{password}".encode()).decode()
    headers = {"Authorization": f"Basic {auth_string}"}
    
    try:
        response = requests.get(
            urljoin(site_url, '/wp-json/wp/v2/users/me'),
            headers=headers,
            timeout=5
        )
        auth_ok = response.status_code == 200
        if auth_ok:
            user_info = response.json()
            user_name = user_info.get('name', 'Unknown')
            print_result("Authentication", True, f"User: {user_name}")
        else:
            print_result("Authentication", False, f"HTTP {response.status_code}")
    except Exception as e:
        print_result("Authentication", False, str(e)[:40])
        return False
    
    # Test 4: Can create a test post (draft)
    try:
        post_data = {
            "title": "Test Post - Do Not Publish",
            "content": "This is an automated test.",
            "status": "draft"
        }
        response = requests.post(
            urljoin(site_url, '/wp-json/wp/v2/posts'),
            headers=headers,
            json=post_data,
            timeout=10
        )
        post_ok = response.status_code == 201
        if post_ok:
            post_id = response.json().get('id')
            print_result("Create Draft Post", True, f"Post ID: {post_id}")
            # Delete the test post immediately
            del_response = requests.delete(
                urljoin(site_url, f'/wp-json/wp/v2/posts/{post_id}?force=true'),
                headers=headers,
                timeout=5
            )
        else:
            print_result("Create Draft Post", False, f"HTTP {response.status_code}")
    except Exception as e:
        print_result("Create Draft Post", False, str(e)[:40])
        post_ok = False
    
    print_header("WORDPRESS TEST RESULTS")
    if site_ok and rest_ok and auth_ok and post_ok:
        print("\n✓ WORDPRESS CONNECTION VERIFIED")
        print("  Your WordPress site is ready for publishing")
        return True
    else:
        print("\n❌ WORDPRESS CONNECTION FAILED")
        print("  Fix the issues above and try again")
        return False

if __name__ == "__main__":
    success = test_wordpress()
    sys.exit(0 if success else 1)
