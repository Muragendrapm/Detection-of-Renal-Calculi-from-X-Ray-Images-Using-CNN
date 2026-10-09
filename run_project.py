#!/usr/bin/env python3
"""
Kidney Stone Detection System Launcher
This script provides multiple ways to run the kidney stone detection system.
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        'tensorflow', 'keras', 'numpy', 'PIL', 'cv2', 'flask', 'sklearn'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            elif package == 'cv2':
                import cv2
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def run_web_version():
    """Run the web-based version with Flask."""
    print("Starting web-based kidney stone detection system...")
    print("Open your browser and go to: http://localhost:5000")
    print("Default login - Username: mpm, Password: 12345")
    subprocess.run([sys.executable, 'login.py'])

def run_desktop_version():
    """Run the desktop version with Tkinter."""
    print("Starting desktop kidney stone detection system...")
    if os.path.exists('detect_left_backup.py'):
        subprocess.run([sys.executable, 'detect_left_backup.py'])
    elif os.path.exists('kidney_stone_detection/detect.py'):
        subprocess.run([sys.executable, 'kidney_stone_detection/detect.py'])
    else:
        print("Error: Detection script not found!")

def run_simple_version():
    """Run the simple version from kidney_stone_detection folder."""
    print("Starting simple kidney stone detection system...")
    os.chdir('kidney_stone_detection')
    subprocess.run([sys.executable, 'detect.py'])

def train_model():
    """Train a new model."""
    print("Training new model...")
    if os.path.exists('detection_model.py'):
        subprocess.run([sys.executable, 'detection_model.py'])
    else:
        print("Error: Training script not found!")

def main():
    """Main launcher interface."""
    print("=" * 60)
    print("    KIDNEY STONE DETECTION SYSTEM LAUNCHER")
    print("=" * 60)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"Warning: Missing packages: {', '.join(missing)}")
        print("Please install them using: pip install " + " ".join(missing))
        print()
    
    # Check if model exists
    if not os.path.exists('model.h5'):
        print("Warning: model.h5 not found in current directory!")
        if os.path.exists('kidney_stone_detection/model.h5'):
            print("Found model in kidney_stone_detection folder.")
        else:
            print("You may need to train the model first.")
        print()
    
    while True:
        print("\nChoose an option:")
        print("1. Run Web Version (Flask + Browser)")
        print("2. Run Desktop Version (Tkinter GUI)")
        print("3. Run Simple Version")
        print("4. Train New Model")
        print("5. Check System Info")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            run_web_version()
            break
        elif choice == '2':
            run_desktop_version()
            break
        elif choice == '3':
            run_simple_version()
            break
        elif choice == '4':
            train_model()
            break
        elif choice == '5':
            print(f"\nPython version: {sys.version}")
            print(f"Current directory: {os.getcwd()}")
            print(f"Files in directory: {os.listdir('.')}")
            if os.path.exists('model.h5'):
                size = os.path.getsize('model.h5') / (1024*1024)
                print(f"Model file size: {size:.1f} MB")
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()