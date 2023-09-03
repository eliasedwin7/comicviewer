# Use a base image
FROM python:3.8

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Run the application
CMD ["python", "comic_viewer.py"]

