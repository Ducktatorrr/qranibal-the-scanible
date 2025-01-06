# Use an official Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libzbar0 \
    libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create and set the working directory
WORKDIR /app

# Copy the application code to the working directory
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Set the default command to run the app
CMD ["python", "app.py"]
