# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required by spleeter (ffmpeg)
# The `ffmpeg` package is crucial for spleeter to process audio files.
RUN apt-get update && apt-get install -y ffmpeg libsamplerate0-dev

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create the directories for raw and processed audio
# This ensures the directories exist when the script runs.
RUN mkdir -p raw_videos splitted_audios

# Use the VOLUME instruction to create a managed volume
# This will prevent the data from being deleted when the container exits.
VOLUME /app/raw_videos
VOLUME /app/splitted_audios

# Copy the rest of the application code into the container at /app
COPY main.py .

# Run the python script
CMD ["python", "main.py"]