#!/usr/bin/env python3
import os, sys, subprocess
from dotenv import load_dotenv

load_dotenv()

def print_header(title):
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)

def run_check(script_name, description):
    print(f"\n→ Running {description}...")
    try:
        result = subprocess.run(
            [sys.executable, f"scripts/{script_name}"],
            capture_output=True,
            timeout=60
        )
        return result.returncode == 0
    except Exception as e:
        print(f"  Error: {e}")
        return False

def main():
    print_header("PREFLIGHT VALIDATION - ALL SYSTEMS CHECK")
    
    checks = [
        ("check_dependencies.py", "Dependency Verification"),
        ("check_env_vars.py", "Environment Variables"),
        ("check_api_health.py", "API Health Check"),
        ("check_wordpress.py", "WordPress Connection"),
    ]
    
    results = {}
    for script, desc in checks:
        results[desc] = run_check(script, desc)
    
    print_header("PREFLIGHT RESULTS SUMMARY")
    
    passed = sum(results.values())
    total = len(results)
    
    for desc, status in results.items():
        symbol = "✓" if status else "✗"
        status_text = "PASS" if status else "FAIL"
        print(f"  {symbol} {desc:30} {status_text}")
    
    print(f"\n  Overall: {passed}/{total} checks passed")
    
    if passed == total:
        print_header("✓ SYSTEM READY FOR PHASE 3")
        print("\nAll infrastructure verified!")
        print("Ready to deploy blogging robots.")
        return True
    else:
        print_header("❌ SOME CHECKS FAILED")
        print("\nFix the failed checks and run again:")
        print("  python3 scripts/preflight_check.py")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
