import os
import subprocess

try:
    print("Installing dependencies from requirements.txt...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
    print("Dependencies installed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error during installation: {e}")
