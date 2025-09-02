#!/usr/bin/env python3
"""
Automated release script for qnty library.

This script:
1. Runs poetry version patch to increment the patch version
2. Gets the new version number
3. Creates a git tag with the version
4. Pushes the tag to origin
"""

import re
import subprocess
import sys


def run_command(cmd, description):
    """Run a command and return the output, or exit on failure."""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print(f"Output: {result.stdout.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error {description}: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        sys.exit(1)

def main():
    print("🚀 Starting automated release process...")
    
    # Step 1: Increment patch version
    print("\n📝 Step 1: Incrementing patch version...")
    version_output = run_command("poetry version patch", "incrementing version")
    
    # Step 2: Extract the new version number
    print("\n🔍 Step 2: Getting new version number...")
    # Poetry version patch outputs something like "Bumping version from 0.0.5 to 0.0.6"
    version_match = re.search(r'to (\d+\.\d+\.\d+)', version_output)
    if not version_match:
        print("❌ Could not extract version number from poetry output")
        sys.exit(1)
    
    new_version = version_match.group(1)
    tag_name = f"v{new_version}"
    print(f"New version: {new_version}")
    print(f"Tag name: {tag_name}")
    
    # Step 3: Create git tag
    print(f"\n🏷️  Step 3: Creating git tag {tag_name}...")
    run_command(f"git tag {tag_name}", "creating git tag")
    
    # Step 4: Push tag to origin
    print(f"\n⬆️  Step 4: Pushing tag {tag_name} to origin...")
    run_command(f"git push origin {tag_name}", "pushing tag to origin")
    
    print("\n✅ Release process completed successfully!")
    print(f"   Version: {new_version}")
    print(f"   Tag: {tag_name}")
    print("   Tag pushed to origin")

if __name__ == "__main__":
    main()
