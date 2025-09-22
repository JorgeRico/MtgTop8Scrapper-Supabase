# syntax=docker/dockerfile:1
# Base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /scrapper

# Copy the requirements file
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 5000

# Start the application
CMD ["python3", "app.py"]