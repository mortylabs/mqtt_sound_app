# Use a minimal Python image
FROM --platform=linux/arm64 python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY mqtt_sound_app.py requirements.txt ./

# Install system dependencies (sometimes required for certain Python packages)
RUN apt-get update && apt-get install -y libffi-dev libssl-dev

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt --verbose

# Set default environment variables
ENV DIR_MUSIC="/music"

# Expose necessary ports
EXPOSE 1883

# Run the MQTT listener when the container starts
CMD ["python", "mqtt_sound_app.py"]
