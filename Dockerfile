FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg libsamplerate0-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD ["python", "main.py"]