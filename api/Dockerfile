# Use a Python base image for x86_64
FROM --platform=linux/amd64 python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the API code into the container
COPY app/ ./app/

# Define the entry point for the container
CMD ["python", "app/main.py"]