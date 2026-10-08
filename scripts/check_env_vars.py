#!/usr/bin/env python3
"""
PHASE 1: Environment Variable Verification
Checks that all required API keys and credentials are configured.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Define required and optional variables
REQUIRED_VARS = {
    'WORDPRESS_SITE_URL': 'WordPress site URL',
    'WORDPRESS_USERNAME': 'WordPress username',
    'WORDPRESS_PASSWORD': 'WordPress application password',
}

# At least ONE AI provider is required
AI_PROVIDERS = {
    'GROQ_API_KEY': 'Groq (fastest, free tier)',
    'GOOGLE_API_KEY': 'Google Generative AI',
    'COHERE_API_KEY': 'Cohere',
    'ANTHROPIC_API_KEY': 'Anthropic Claude',
    'OPENAI_API_KEY': 'OpenAI GPT',
}

# Image generation providers (optional)
IMAGE_PROVIDERS = {
    'REPLICATE_API_KEY': 'Replicate',
    'HUGGINGFACE_API_KEY': 'Hugging Face',
}

OPTIONAL_VARS = {
    'DISABLE_DALLE': 'Disable DALL-E for image generation',
}

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)

def print_check(status, name, description=""):
    """Print a status check result."""
    symbol = "✓" if status else "✗"
    detail = f" - {description}" if description else ""
    print(f"  {symbol} {name}{detail}")

def main():
    """Main verification function."""
    print_header("PHASE 1: ENVIRONMENT VARIABLE VERIFICATION")
    
    # Check if .env file exists
    env_path = Path('.env')
    if not env_path.exists():
        print("\n⚠️  WARNING: .env file not found!")
        print(f"   Expected location: {env_path.absolute()}")
        print("   Create .env from .env.example:")
        print("   cp .env.example .env")
        print("   Then edit .env with your API keys\n")
        return False
    
    # Load environment variables
    load_dotenv()
    
    all_passed = True
    
    # Check WordPress configuration (REQUIRED)
    print_header("WORDPRESS CONFIGURATION (REQUIRED)")
    wordpress_ok = True
    for var, description in REQUIRED_VARS.items():
        value = os.getenv(var)
        is_set = value and len(str(value).strip()) > 0
        print_check(is_set, var, description)
        if not is_set:
            wordpress_ok = False
            all_passed = False
    
    if not wordpress_ok:
        print("\n❌ WordPress configuration incomplete!")
    
    # Check AI providers (AT LEAST ONE REQUIRED)
    print_header("AI PROVIDERS (AT LEAST ONE REQUIRED)")
    ai_providers_found = []
    for var, description in AI_PROVIDERS.items():
        value = os.getenv(var)
        is_set = value and len(str(value).strip()) > 0
        print_check(is_set, var, description)
        if is_set:
            ai_providers_found.append(description)
    
    if not ai_providers_found:
        print("\n❌ No AI provider configured! At least one is required.")
        all_passed = False
    else:
        print(f"\n✓ AI Providers configured: {', '.join(ai_providers_found)}")
    
    # Check image generation providers (OPTIONAL)
    print_header("IMAGE GENERATION PROVIDERS (OPTIONAL)")
    image_providers_found = []
    for var, description in IMAGE_PROVIDERS.items():
        value = os.getenv(var)
        is_set = value and len(str(value).strip()) > 0
        print_check(is_set, var, description)
        if is_set:
            image_providers_found.append(description)
    
    if image_providers_found:
        print(f"\n✓ Image providers configured: {', '.join(image_providers_found)}")
    else:
        print("\n⚠️  No image provider configured (optional)")
    
    # Check optional settings
    print_header("OPTIONAL SETTINGS")
    for var, description in OPTIONAL_VARS.items():
        value = os.getenv(var)
        is_set = value and len(str(value).strip()) > 0
        print_check(is_set, var, description)
    
    # Final results
    print_header("VERIFICATION RESULTS")
    if all_passed:
        print("\n✓ ALL REQUIRED VARIABLES CONFIGURED")
        print("\nYour system is ready for Phase 2: API Health Checks")
        return True
    else:
        print("\n❌ CONFIGURATION INCOMPLETE")
        print("\nFix the issues above and run this script again:")
        print("  python3 scripts/check_env_vars.py\n")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
import os, sys
from pathlib import Path
from dotenv import load_dotenv

REQUIRED_VARS = {
    'WORDPRESS_SITE_URL': 'WordPress site URL',
    'WORDPRESS_USERNAME': 'WordPress username',
    'WORDPRESS_PASSWORD': 'WordPress application password',
}

AI_PROVIDERS = {
    'GROQ_API_KEY': 'Groq (fastest, free tier)',
    'GOOGLE_API_KEY': 'Google Generative AI',
    'COHERE_API_KEY': 'Cohere',
    'ANTHROPIC_API_KEY': 'Anthropic Claude',
    'OPENAI_API_KEY': 'OpenAI GPT',
}

IMAGE_PROVIDERS = {
    'REPLICATE_API_KEY': 'Replicate',
    'HUGGINGFACE_API_KEY': 'Hugging Face',
}

def print_header(title):
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)

def print_check(status, name, desc=""):
    symbol = "✓" if status else "✗"
    detail = f" - {desc}" if desc else ""
    print(f"  {symbol} {name}{detail}")

def main():
    print_header("PHASE 1: ENVIRONMENT VARIABLE VERIFICATION")
    
    env_path = Path('.env')
    if not env_path.exists():
        print("\n⚠️  WARNING: .env file not found!")
        print("   cp .env.example .env")
        print("   Then edit .env with your API keys\n")
        return False
    
    load_dotenv()
    all_passed = True
    
    print_header("WORDPRESS CONFIGURATION (REQUIRED)")
    wordpress_ok = True
    for var, desc in REQUIRED_VARS.items():
        value = os.getenv(var)
        is_set = value and len(str(value).strip()) > 0
        print_check(is_set, var, desc)
        if not is_set:
            wordpress_ok = False
            all_passed = False
    
    if not wordpress_ok:
        print("\n❌ WordPress configuration incomplete!")
    
    print_header("AI PROVIDERS (AT LEAST ONE REQUIRED)")
    ai_found = []
    for var, desc in AI_PROVIDERS.items():
        value = os.getenv(var)
        is_set = value and len(str(value).strip()) > 0
        print_check(is_set, var, desc)
        if is_set:
            ai_found.append(desc)
    
    if not ai_found:
        print("\n❌ No AI provider configured!")
        all_passed = False
    else:
        print(f"\n✓ AI Providers: {', '.join(ai_found)}")
    
    print_header("IMAGE PROVIDERS (OPTIONAL)")
    img_found = []
    for var, desc in IMAGE_PROVIDERS.items():
        value = os.getenv(var)
        is_set = value and len(str(value).strip()) > 0
        print_check(is_set, var, desc)
        if is_set:
            img_found.append(desc)
    
    if img_found:
        print(f"\n✓ Image providers: {', '.join(img_found)}")
    else:
        print("\n⚠️  No image provider configured (optional)")
    
    print_header("VERIFICATION RESULTS")
    if all_passed:
        print("\n✓ ALL REQUIRED VARIABLES CONFIGURED")
        print("\nYour system is ready for Phase 2!")
        return True
    else:
        print("\n❌ CONFIGURATION INCOMPLETE")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
