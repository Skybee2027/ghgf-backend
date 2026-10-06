# GHGF - Autonomous Blog System

100% fully autonomous, zero human intervention required backend system for greathealthgreatfitness.com

## 🚀 Quick Start

### Prerequisites
- GitHub account
- WordPress site with REST API enabled
- Free API keys:
  - Google Gemini: https://makersuite.google.com/app/apikey
  - WordPress app password (from WordPress admin)

### Setup (5 minutes)

1. **Get API Keys**
   - Google Gemini Free: https://makersuite.google.com/app/apikey
   - Create WordPress app password: Admin → Users → Profile → App Passwords

2. **Add GitHub Secrets**
   - Go to: Settings → Secrets and variables → Actions
   - Add 4 secrets:
     - `GOOGLE_API_KEY`: Your Gemini key
     - `WORDPRESS_SITE_URL`: Your site URL
     - `WORDPRESS_USERNAME`: admin
     - `WORDPRESS_PASSWORD`: Your app password

3. **Run First Test**
   - Go to: Actions tab
   - Click: "GHGF Daily Automation"
   - Click: "Run workflow"
   - Wait 2-3 minutes

4. **That's It!**
   - System runs automatically at 8 AM UTC daily
   - Check WordPress dashboard for new posts

## 🤖 System Architecture
