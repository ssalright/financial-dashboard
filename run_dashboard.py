#!/usr/bin/env python3
"""
Simple script to run the Financial Dashboard application.
This script provides an easy way to start the dashboard with proper configuration.
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import dash
        import plotly
        import pandas
        import numpy
        import flask_cors
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def main():
    """Main function to run the dashboard."""
    print("Financial Dashboard Launcher")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('financial_dashboard.py'):
        print("✗ financial_dashboard.py not found in current directory")
        print("Please run this script from the project root directory")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("\nStarting Financial Dashboard...")
    print("The dashboard will be available at:")
    print("  Local: http://localhost:12001")
    print("  Network: http://0.0.0.0:12001")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 40)
    
    try:
        # Run the dashboard
        subprocess.run([sys.executable, 'financial_dashboard.py'])
    except KeyboardInterrupt:
        print("\n\nDashboard stopped by user")
    except Exception as e:
        print(f"\nError running dashboard: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()