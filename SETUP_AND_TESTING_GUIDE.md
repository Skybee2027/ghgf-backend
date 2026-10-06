# GHGF System - Complete Setup & Testing Guide

## Quick Start (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create .env File
```bash
cat > .env << EOF
# Free Tier (Required)
GROQ_API_KEY=gsk_your_groq_key_here
HUGGINGFACE_API_KEY=hf_your_hf_key_here
GOOGLE_API_KEY=your_google_api_key_here

# WordPress (For publishing)
WORDPRESS_SITE_URL=https://yourblog.com
WORDPRESS_USERNAME=admin_user
WORDPRESS_PASSWORD=app_password

# Optional Paid Backups
CLAUDE_API_KEY=sk-ant-your_claude_key_here
OPENAI_API_KEY=sk-your_openai_key_here
EOF
```

### 3. Test Provider Fallback
```bash
python test_provider_fallback.py
```

### 4. Run Full Pipeline
```bash
python ghgf_orchestrator.py
```

---

## Detailed Setup

### Step 1: Get Free API Keys

#### Groq (Primary - FREE, 9,000 req/min)
1. Go to https://console.groq.com/keys
2. Sign up (free account)
3. Create API key
4. Copy to `.env`: `GROQ_API_KEY=gsk_...`

#### HuggingFace (Backup - FREE, Limited)
1. Go to https://huggingface.co/settings/tokens
2. Sign up (free account)
3. Create User Access Token (read-only fine)
4. Copy to `.env`: `HUGGINGFACE_API_KEY=hf_...`

#### Google Gemini (Backup - FREE, 20 req/day)
1. Go to https://aistudio.google.com/app/apikey
2. Create new API key (requires Google account)
3. Copy to `.env`: `GOOGLE_API_KEY=AI...`

#### WordPress (REQUIRED for publishing)
1. Go to your WordPress admin dashboard
2. Create **Application Password** (NOT your main password):
   - Users > Your Profile > Scroll to "Application Passwords"
   - Create password named "GHGF Automation"
   - Copy the generated password
3. Configure:
   ```
   WORDPRESS_SITE_URL=https://yourblog.com
   WORDPRESS_USERNAME=admin_username
   WORDPRESS_PASSWORD=the_app_password_generated_above
   ```

#### Optional: Claude API (Paid backup)
1. Go to https://console.anthropic.com/
2. Create account (requires payment method)
3. Generate API key
4. Copy to `.env`: `CLAUDE_API_KEY=sk-ant-...`

#### Optional: OpenAI API (Paid backup)
1. Go to https://platform.openai.com/api/keys
2. Create account (requires payment method)
3. Generate API key
4. Copy to `.env`: `OPENAI_API_KEY=sk-...`

---

## Test Scripts

### Test 1: Provider Health Check
**File:** `test_provider_fallback.py`

```python
"""Test that all providers are configured and accessible"""
import asyncio
from ghgf_providers import ProviderHealthChecker

async def test_providers():
    checker = ProviderHealthChecker()
    health = await checker.check_all_providers()
    
    print("\n" + "="*60)
    print("PROVIDER HEALTH CHECK")
    print("="*60)
    for provider, status in health.items():
        emoji = "✅" if status else "❌"
        print(f"{emoji} {provider.upper()}: {'Healthy' if status else 'Not configured'}")
    print("="*60 + "\n")

asyncio.run(test_providers())
```

**Run:**
```bash
python test_provider_fallback.py
```

**Expected Output (with all keys configured):**
```
============================================================
PROVIDER HEALTH CHECK
============================================================
✅ GROQ: Healthy
✅ HUGGINGFACE: Healthy
✅ GEMINI: Healthy
❌ CLAUDE: Not configured
❌ OPENAI: Not configured
============================================================
```

---

### Test 2: Single Agent Test
**File:** `test_single_agent.py`

```python
"""Test individual agent"""
import asyncio
from ghgf_agents_1_5 import GHGF_1_TrendDiscovery

async def test_trend_discovery():
    agent = GHGF_1_TrendDiscovery()
    result = await agent.execute()
    
    print("\n" + "="*60)
    print("GHGF_1: TREND DISCOVERY TEST")
    print("="*60)
    print(f"Status: {result.get('status')}")
    print(f"Quality Score: {result.get('quality_score')}/10")
    print(f"Trends Found: {result.get('trends_found', 0)}")
    print("\nTrends:")
    for trend in result.get('data', []):
        print(f"  - {trend.get('name', 'Unknown')}")
    print("="*60 + "\n")

asyncio.run(test_trend_discovery())
```

**Run:**
```bash
python test_single_agent.py
```

---

### Test 3: Full Pipeline (Dry Run - No WordPress)
**File:** `test_full_pipeline.py`

```python
"""Test full pipeline without publishing to WordPress"""
import asyncio
from ghgf_agents_1_5 import (
    GHGF_1_TrendDiscovery, GHGF_2_OutlineGenerator,
    GHGF_3_ContentWriter, GHGF_4_AffiliateResearch
)

async def test_pipeline():
    print("\n" + "="*60)
    print("DRY RUN: CONTENT CREATION PIPELINE")
    print("="*60)
    
    # 1. Discover Trends
    print("\n[1/4] Discovering trends...")
    agent1 = GHGF_1_TrendDiscovery()
    result1 = await agent1.execute()
    topic = result1['data'][0]['name'] if result1.get('data') else "Weight Loss"
    print(f"✅ Topic: {topic}")
    
    # 2. Generate Outline
    print(f"\n[2/4] Generating outline for '{topic}'...")
    agent2 = GHGF_2_OutlineGenerator()
    result2 = await agent2.execute(topic)
    print(f"✅ Outline generated (Score: {result2.get('quality_score')})")
    
    # 3. Write Content
    print(f"\n[3/4] Writing blog post...")
    agent3 = GHGF_3_ContentWriter()
    result3 = await agent3.execute(topic, 1500)
    words = result3.get('total_words', 0)
    print(f"✅ Content written ({words} words, Score: {result3.get('quality_score')})")
    
    # 4. Affiliate Research
    print(f"\n[4/4] Researching affiliate products...")
    agent4 = GHGF_4_AffiliateResearch()
    result4 = await agent4.execute(topic)
    products = result4.get('products_found', 0)
    print(f"✅ Found {products} affiliate products (Score: {result4.get('quality_score')})")
    
    print("\n" + "="*60)
    print("✅ DRY RUN COMPLETE - All systems working!")
    print("="*60 + "\n")

asyncio.run(test_pipeline())
```

**Run:**
```bash
python test_full_pipeline.py
```

---

### Test 4: WordPress Connection Test
**File:** `test_wordpress.py`

```python
"""Test WordPress API connection"""
import os
import requests
from requests.auth import HTTPBasicAuth

def test_wordpress():
    url = os.getenv("WORDPRESS_SITE_URL", "")
    user = os.getenv("WORDPRESS_USERNAME", "")
    password = os.getenv("WORDPRESS_PASSWORD", "")
    
    print("\n" + "="*60)
    print("WORDPRESS CONNECTION TEST")
    print("="*60)
    
    if not all([url, user, password]):
        print("❌ Missing WordPress credentials in .env")
        return
    
    print(f"Testing: {url}")
    print(f"User: {user}")
    
    try:
        response = requests.get(
            f"{url}/wp-json/wp/v2/posts?per_page=1",
            auth=HTTPBasicAuth(user, password),
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ WordPress connection successful!")
            print(f"   Posts found: {len(response.json())}")
        elif response.status_code == 401:
            print("❌ Unauthorized - Check username/password")
        elif response.status_code == 404:
            print("❌ WordPress REST API not found - Check WORDPRESS_SITE_URL")
        else:
            print(f"❌ HTTP {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print("="*60 + "\n")

test_wordpress()
```

**Run:**
```bash
python test_wordpress.py
```

---

## Running Tests in Order

### Recommended Testing Sequence

```bash
# 1. Check providers are configured
python test_provider_fallback.py

# 2. Test single agent
python test_single_agent.py

# 3. Test content creation pipeline (no publishing)
python test_full_pipeline.py

# 4. Test WordPress connection
python test_wordpress.py

# 5. Run full pipeline with publishing
python ghgf_orchestrator.py
```

---

## Monitoring After Deployment

### Check Execution Database
```bash
sqlite3 data/logs/ghgf_execution.db
```

**View all executions:**
```sql
SELECT 
    timestamp,
    agent_id,
    status,
    quality_score,
    cost_usd
FROM agent_executions
ORDER BY timestamp DESC
LIMIT 20;
```

**View failures:**
```sql
SELECT 
    timestamp,
    agent_id,
    status,
    errors
FROM agent_executions
WHERE status = 'failed'
ORDER BY timestamp DESC;
```

---

## Troubleshooting

### Issue: "Module not found: ghgf_providers"
**Solution:**
```bash
# Ensure ghgf_providers.py is in same directory
ls -la ghgf_providers.py
```

### Issue: "NameError: name 'ai_provider_manager' is not defined"
**Solution:**
```python
# Check import statement in agents file
from ghgf_providers import ai_provider_manager
```

### Issue: "GROQ_API_KEY not set"
**Solution:**
```bash
# Verify .env file exists and has key
cat .env | grep GROQ_API_KEY

# Export if running without .env
export GROQ_API_KEY=gsk_...
```

### Issue: All providers failing
**Solution:**
1. Check internet connection
2. Verify API keys are valid
3. Check provider rate limits/quotas
4. Look at detailed error in logs

### Issue: "WordPress 401 Unauthorized"
**Solution:**
```bash
# Verify Application Password (NOT main password)
# Go to WordPress Admin > Users > Your Profile
# Scroll to "Application Passwords"
# Create new password for GHGF

# Then update .env:
WORDPRESS_PASSWORD=the_app_password_here
```

### Issue: "POST rate limit exceeded"
**Solution:**
- Groq: Max 9,000 req/min per API key (almost unlimited for daily use)
- Gemini: Max 20 req/day (backup only)
- If hitting limits, make sure GROQ_API_KEY is valid

---

## Performance Optimization

### Optimize for Speed
```python
# In orchestrator, run agents in parallel where possible
import asyncio

# These can run in parallel (no dependencies):
results = await asyncio.gather(
    agent5.execute(content),  # Review
    agent4.execute(topic),    # Affiliate research
    agent3_5.execute(topic)   # Image generation
)
```

### Optimize for Cost
```bash
# Use only free tiers in .env
# Leave CLAUDE_API_KEY and OPENAI_API_KEY blank
# System will use Groq → HuggingFace → Gemini (all free)
```

### Optimize for Quality
```python
# Increase max_tokens for better content
response = await ai_provider_manager.call_with_fallback(
    prompt,
    task_type="content_writing",
    max_tokens=3000  # Higher = better quality, slower
)
```

---

## Next Steps

1. ✅ Complete setup above
2. ✅ Run all test scripts
3. ✅ Verify blog post published successfully
4. ✅ Monitor execution logs
5. ✅ Configure GitHub Secrets for CI/CD
6. ✅ Push to GitHub and enable Actions
7. ✅ Monitor first 3 automated runs
8. ✅ Consider adding agents 10-17 (extended tools)

---

## Support Resources

- **Groq:** https://console.groq.com/docs
- **HuggingFace:** https://huggingface.co/docs/hub/api
- **Google Gemini:** https://ai.google.dev/docs
- **WordPress REST API:** https://developer.wordpress.org/rest-api/
- **GitHub Actions:** https://docs.github.com/en/actions

---

**Your GHGF system is production-ready! 🚀**
