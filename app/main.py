# FastAPI app for generating lip-synced avatar videos using fantasy-talking, then uploading to S3

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import uuid
import os
import sys
import tempfile
import subprocess
import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the S3 bucket name from environment
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Initialize FastAPI app
app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to a specific list for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to generate a lip-synced video using fantasy-talking model
def generate_lip_sync(audio_path: str, image_path: str, output_dir: str) -> str:
    subprocess.run([
        sys.executable, "fantasy-talking/infer.py",
        "--audio_path", audio_path,
        "--image_path", image_path,
        "--output_dir", output_dir,
    ], check=True)  # Raise error if command fails

    # Return path to the generated video
    return os.path.join(output_dir, "results", "lip_sync_video.mp4")

# Upload the generated video to S3 and return its public URL
def upload_to_s3(local_file: str, s3_path: str) -> str:
    s3 = boto3.client("s3")
    s3.upload_file(local_file, BUCKET_NAME, s3_path)
    return f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_path}"

# Endpoint: Accepts audio file, generates video, uploads it to S3, and returns the URL
@app.post("/video/generate-avatar")
async def generate_avatar(audio: UploadFile = File(...)):
    file_id = str(uuid.uuid4())  # Unique identifier for file naming

    # Set up paths for input/output using temp directory
    tmp_dir = tempfile.gettempdir()
    input_image_path = os.path.abspath("static/avatar.png")
    input_audio_path = os.path.abspath(os.path.join(tmp_dir, f"{file_id}.mp3"))
    output_dir = os.path.abspath(os.path.join(tmp_dir, f"{file_id}"))
    os.makedirs(output_dir, exist_ok=True)

    # Save uploaded audio file to temp path
    with open(input_audio_path, "wb") as f:
        f.write(await audio.read())

    try:
        # Run inference to generate lip-sync video
        output_video_path = generate_lip_sync(input_audio_path, input_image_path, output_dir)

        # Upload result to S3 and return public URL
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
        # Handle failure if subprocess (inference) fails
        return JSONResponse(status_code=500, content={
            "result": "error",
            "message": "Failed to generate video."
        })