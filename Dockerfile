# Use an official Python runtime as the base image
FROM python:3.11-slim

# Install ffmpeg (this installs the ffmpeg binary)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory (where your Python script is) to the container
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (optional, depending on your needs)
EXPOSE 8080

# Run the Python script
CMD ["python", "main.py"]