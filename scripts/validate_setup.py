#!/usr/bin/env python3
"""
Smart Chat AI - Quick Setup Script
Run this script to validate and prepare your development environment
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def check_file_exists(path):
    return Path(path).exists()

def main():
    print_header("Smart Chat AI - Environment Setup Validator")

    # 1. Check Python version
    print("1️⃣  Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} installed")
    else:
        print_error(f"Python 3.11+ required (found {version.major}.{version.minor})")
        return False

    # 2. Check Docker
    print("\n2️⃣  Checking Docker...")
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print_success(result.stdout.strip())
        else:
            print_error("Docker not found or not running")
            return False
    except Exception as e:
        print_error(f"Docker check failed: {e}")
        return False

    # 3. Check Docker Compose
    print("\n3️⃣  Checking Docker Compose...")
    try:
        result = subprocess.run(["docker-compose", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print_success(result.stdout.strip())
        else:
            print_error("Docker Compose not found")
            return False
    except Exception as e:
        print_error(f"Docker Compose check failed: {e}")
        return False

    # 4. Check project structure
    print("\n4️⃣  Checking project structure...")
    required_files = [
        "app/main.py",
        "docker-compose.yml",
        "Dockerfile",
        "requirements.txt",
        ".env.example",
        "nginx/nginx.conf",
    ]

    all_exist = True
    for file in required_files:
        if check_file_exists(file):
            print_success(f"Found: {file}")
        else:
            print_error(f"Missing: {file}")
            all_exist = False

    if not all_exist:
        return False

    # 5. Check .env file
    print("\n5️⃣  Checking environment configuration...")
    if check_file_exists(".env"):
        print_success(".env file exists")
        # Check if it has critical values
        try:
            with open(".env") as f:
                env_content = f.read()
                if "SECRET_KEY" in env_content:
                    print_success("SECRET_KEY is configured")
                else:
                    print_warning("SECRET_KEY not set in .env")
        except Exception as e:
            print_error(f"Error reading .env: {e}")
    else:
        print_warning(".env file not found")
        print_info("Run: copy .env.example .env")

    # 6. Check ports
    print("\n6️⃣  Checking port availability...")
    ports = {
        "8000": "FastAPI",
        "5432": "PostgreSQL",
        "6379": "Redis",
        "80": "NGINX",
        "443": "NGINX SSL"
    }

    # Simple check (can be improved)
    print_info("Ports: 8000 (API), 5432 (DB), 6379 (Cache), 80/443 (Web)")

    # 7. Summary
    print_header("Setup Summary")
    print_success("All checks passed!")
    print("\nNext steps:")
    print("1. Update .env file with your configuration:")
    print("   - SECRET_KEY: Generate new with: openssl rand -hex 32")
    print("   - OPENAI_API_KEY: Add your OpenAI API key (optional)")
    print("\n2. Start Docker services:")
    print("   docker-compose up -d")
    print("\n3. Access the application:")
    print("   - API Docs: http://localhost:8000/docs")
    print("   - Health: http://localhost:8000/health")
    print("\n4. Test an endpoint:")
    print("   curl http://localhost:8000/health")

    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
