# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY app.py .

# Run the python file
CMD ["python", "app.py"]
