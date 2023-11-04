# Use the official Python image which is based on Debian
FROM python:3.10

# Set work directory
WORKDIR /app

# Copy your application code and other necessary files including the build script
COPY . /app/

# Install PyInstaller and the zip utility
RUN apt-get update && \
    apt-get install -y zip && \
    pip install pyinstaller

# Ensure the build script is executable
RUN chmod +x /app/start.sh  # Or /app/build.sh if you've renamed it

# By default, run the build script
CMD ["/app/start.sh"]  # Or /app/build.sh if using build.sh
