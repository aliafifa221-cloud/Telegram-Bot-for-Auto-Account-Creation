#!/usr/bin/env python3
"""
Setup validation script
Tests if all dependencies and configurations are correct
"""

import sys
import os


def check_python_version():
    """Check if Python version is 3.8 or higher"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'telegram',
        'selenium',
        'webdriver_manager',
        'dotenv',
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ Package '{package}' is installed")
        except ImportError:
            print(f"❌ Package '{package}' is NOT installed")
            all_installed = False
    
    return all_installed


def check_env_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("   Copy .env.example to .env and configure it")
        return False
    
    print("✅ .env file exists")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'TELEGRAM_BOT_TOKEN',
        'DASHBOARD_USERNAME',
        'DASHBOARD_PASSWORD',
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your_'):
            missing_vars.append(var)
            print(f"⚠️  {var} is not configured")
        else:
            # Show partial value for security
            masked_value = value[:5] + '...' if len(value) > 5 else '***'
            print(f"✅ {var} is set ({masked_value})")
    
    if missing_vars:
        print(f"\n❌ Please configure: {', '.join(missing_vars)}")
        return False
    
    return True


def check_files():
    """Check if required Python files exist"""
    required_files = ['bot.py', 'automation.py']
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ File '{file}' exists")
        else:
            print(f"❌ File '{file}' is missing")
            all_exist = False
    
    return all_exist


def main():
    """Run all checks"""
    print("🔍 Checking setup...\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Configuration", check_env_file),
        ("Required Files", check_files),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n--- {name} ---")
        results.append(check_func())
    
    print("\n" + "="*50)
    if all(results):
        print("✅ All checks passed! You can start the bot with:")
        print("   python bot.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nSetup instructions:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Copy .env.example to .env: cp .env.example .env")
        print("3. Edit .env with your credentials")
        print("4. Run this script again to verify")
    print("="*50)


if __name__ == '__main__':
    main()
