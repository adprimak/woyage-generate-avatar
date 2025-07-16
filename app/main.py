from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import uuid
import os
import sys
import tempfile
import subprocess
import boto3

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to specific origins like ["http://localhost:8000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BUCKET_NAME = "your-s3-bucket-name"

def generate_lip_sync(audio_path: str, image_path: str, output_dir: str) -> str:
    subprocess.run([
        sys.executable, "fantasy-talking/infer.py",
        "--audio_path", audio_path,
        "--image_path", image_path,
        "--output_dir", output_dir,
    ], check=True)
    return os.path.join(output_dir, "results", "driving_video.mp4")

def upload_to_s3(local_file: str, s3_path: str) -> str:
    s3 = boto3.client("s3")
    s3.upload_file(local_file, BUCKET_NAME, s3_path)
    return f"s3://{BUCKET_NAME}/{s3_path}"

@app.post("/video/generate-avatar")
async def generate_avatar(audio: UploadFile = File(...)):
    file_id = str(uuid.uuid4())

    # Get absolute paths for audio input and output dir
    tmp_dir = tempfile.gettempdir()  # returns Windows temp dir path
    input_image_path = "static/avatar.png"
    input_audio_path = os.path.abspath(os.path.join(tmp_dir, f"{file_id}.mp3"))
    output_dir = os.path.abspath(os.path.join(tmp_dir, f"{file_id}"))
    os.makedirs(output_dir, exist_ok=True)

    with open(input_audio_path, "wb") as f:
            f.write(await audio.read())

    try:
        output_video_path = generate_lip_sync(input_audio_path, input_image_path, output_dir)
        s3_key = f"audio_data/{file_id}.mp4"
        s3_url = upload_to_s3(output_video_path, s3_key)
        
        return JSONResponse(content={
            "result": "success",
            "message": "Audio extracted.",
            "data": {
                "video_path": s3_url
            }
        })
    
    except subprocess.CalledProcessError:
        return JSONResponse(status_code=500, content={
            "result": "error",
            "message": "Failed to generate video."
        })