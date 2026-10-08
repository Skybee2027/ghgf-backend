#!/usr/bin/env python3
"""
PHASE 1: Dependency Verification Script
Checks that all required Python packages are installed
"""

import sys

REQUIRED_PACKAGES = {
    'groq': 'groq',
    'google.generativeai': 'google-generativeai',
    'anthropic': 'anthropic',
    'openai': 'openai',
    'cohere': 'cohere',
    'replicate': 'replicate',
    'requests': 'requests',
    'aiohttp': 'aiohttp',
    'httpx': 'httpx',
    'dotenv': 'python-dotenv',
    'pydantic': 'pydantic',
    'yaml': 'pyyaml',
}

def main():
    print("\n" + "="*70)
    print("PHASE 1: DEPENDENCY VERIFICATION")
    print("="*70 + "\n")
    
    passed = []
    failed = []
    
    for module_name, package_name in REQUIRED_PACKAGES.items():
        try:
            __import__(module_name)
            passed.append(package_name)
            print(f"✓ {package_name:30} INSTALLED")
        except ImportError:
            failed.append(package_name)
            print(f"✗ {package_name:30} MISSING")
    
    print("\n" + "="*70)
    print(f"RESULTS: {len(passed)}/{len(REQUIRED_PACKAGES)} packages installed")
    print("="*70 + "\n")
    
    if failed:
        print("FAILED PACKAGES:")
        for pkg in failed:
            print(f"  ✗ {pkg}")
        print("\nFIX: Run this command:")
        print("  pip install -r requirements.txt\n")
        return False
    else:
        print("✓ ALL DEPENDENCIES INSTALLED\n")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
import sys

REQUIRED_PACKAGES = {
    'groq': 'groq',
    'google.generativeai': 'google-generativeai',
    'anthropic': 'anthropic',
    'openai': 'openai',
    'cohere': 'cohere',
    'replicate': 'replicate',
    'requests': 'requests',
    'aiohttp': 'aiohttp',
    'httpx': 'httpx',
    'dotenv': 'python-dotenv',
    'pydantic': 'pydantic',
    'yaml': 'pyyaml',
}

def main():
    print("\n" + "="*70)
    print("PHASE 1: DEPENDENCY VERIFICATION")
    print("="*70 + "\n")
    
    passed = []
    failed = []
    
    for module_name, package_name in REQUIRED_PACKAGES.items():
        try:
            __import__(module_name)
            passed.append(package_name)
            print(f"✓ {package_name:30} INSTALLED")
        except ImportError:
            failed.append(package_name)
            print(f"✗ {package_name:30} MISSING")
    
    print("\n" + "="*70)
    print(f"RESULTS: {len(passed)}/{len(REQUIRED_PACKAGES)} packages installed")
    print("="*70 + "\n")
    
    if failed:
        print("FAILED PACKAGES:")
        for pkg in failed:
            print(f"  ✗ {pkg}")
        print("\nFIX: Run this command:")
        print("  pip install -r requirements.txt\n")
        return False
    else:
        print("✓ ALL DEPENDENCIES INSTALLED\n")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

