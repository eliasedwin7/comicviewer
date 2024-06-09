#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e
# Build the application
pyinstaller --noconfirm --onedir --icon=comic_logo.ico --name=ComicViewer main.py --distpath ./dist/ComicViewer

#!/bin/bash
# Exit script on any error
set -e 

# Run PyInstaller to build the application
pyinstaller --noconfirm --onedir --icon=comic_logo.ico --name=ComicViewer main.py --distpath /app/dist/ComicViewer

# Check if the executable directory was created
if [ -d "/app/dist/ComicViewer/ComicViewer" ]; then
    echo "Build was successful, zipping now."
    # Navigate to the directory containing the output of PyInstaller
    cd /app/dist/ComicViewer
    # Zip the compiled directory into one file
    zip -r ComicViewer.zip ComicViewer
    # Move the ZIP file to the /app directory so it's easy to find and copy
    mv ComicViewer.zip /app/
else
    echo "Build failed. /app/dist/ComicViewer/ComicViewer directory not found."
    exit 1
fi

# Clean up
apt-get clean && rm -rf /var/lib/apt/lists/*
