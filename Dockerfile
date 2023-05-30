FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y ffmpeg

# install requirements
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--log-level", "debug","--timeout", "0", "app:app" ]