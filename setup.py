#!/usr/bin/env python3
"""
Setup script for Task Manager API
This script helps set up the project quickly
"""

import os
import sys
import subprocess
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def main():
    """Main setup function"""
    print("🚀 Task Manager API Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies. Please check your internet connection.")
        sys.exit(1)
    
    # Run migrations
    if not run_command("python manage.py migrate", "Running database migrations"):
        print("❌ Failed to run migrations.")
        sys.exit(1)
    
    # Create superuser if it doesn't exist
    print("\n🔄 Creating superuser...")
    try:
        result = subprocess.run(
            "python manage.py createsuperuser --username admin --email admin@example.com --noinput",
            shell=True, capture_output=True, text=True
        )
        if result.returncode == 0:
            print("✅ Superuser created successfully!")
            print("   Username: admin")
            print("   Email: admin@example.com")
            print("   Password: (you'll need to set this manually)")
        else:
            print("⚠️  Superuser creation failed (might already exist)")
    except Exception as e:
        print(f"⚠️  Superuser creation failed: {e}")
    
    # Run tests
    if not run_command("python manage.py test", "Running tests"):
        print("❌ Tests failed. Please check the code.")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the server: python manage.py runserver")
    print("2. Access the API at: http://localhost:8000/api/")
    print("3. View documentation at: http://localhost:8000/swagger/")
    print("4. Access admin at: http://localhost:8000/admin/")
    print("5. Run the test script: python test_api.py")
    
    # Ask if user wants to start the server
    response = input("\n🤔 Would you like to start the server now? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        print("\n🚀 Starting development server...")
        print("Press Ctrl+C to stop the server")
        try:
            subprocess.run("python manage.py runserver", shell=True)
        except KeyboardInterrupt:
            print("\n👋 Server stopped. Goodbye!")

if __name__ == "__main__":
    main() 