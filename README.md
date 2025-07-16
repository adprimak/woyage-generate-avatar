# Woyage AI Avatar Backend

This FastAPI service accepts an MP3 file, uses a lip-sync model to generate a speaking avatar video, uploads it to S3, and returns the path.

## Setup

1. Clone the fantasy-talking repo inside this project.
2. Download models as per https://github.com/Fantasy-AMAP/fantasy-talking/blob/main/README.md#model-download
3. Add AWS credentials to your environment or ~/.aws/credentials.
4. Ensure the avatar image is placed in `static/avatar.png`.

## Run Locally

```bash
uvicorn app.main:app --reload
```