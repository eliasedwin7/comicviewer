#!/bin/bash

echo "Starting start.sh script..."

# Navigate to app directory and pull the latest code
cd /app || { echo "Error navigating to /app directory"; exit 1; }
echo "Current directory: $(pwd)"
echo "Pulling latest code from repository..."
git pull || { echo "Error pulling from repository"; exit 1; }

# Compile using PyInstaller
pyinstaller --noconfirm --onedir --windowed --icon "/app/comic_logo.ico" --name "ComicViewer" "/app/main.py"

# The above command will create a "ComicViewer" folder in /app/dist
# We don't need to move it, as Docker volume mapping will handle it.
