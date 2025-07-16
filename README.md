# Woyage AI Avatar Backend

This FastAPI service accepts an MP3 file, uses a lip-sync model to generate a speaking avatar video, uploads it to S3, and returns the path.

## Setup

1. Clone the fantasy-talking repo inside this project.
2. Add AWS credentials to your environment or ~/.aws/credentials.
3. Place the avatar image in `static/avatar.png`.

## Run Locally

```bash
uvicorn app.main:app --reload
```

## Build with Docker

```bash
docker build -t woyage-backend .
docker run -p 8000:8000 woyage-backend
```
