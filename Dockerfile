# Use the official Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app files
COPY . .

# Set environment variable for Flask
ENV FLASK_APP=main.py

# Expose the port Cloud Run expects
EXPOSE 8080

# Command to run the app using Gunicorn (production-ready)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
