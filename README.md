# Woyage AI Avatar Backend

This FastAPI service accepts an MP3 file, uses a lip-sync model to generate a speaking avatar video, uploads it to S3, and returns the path.

## Installation

### Step 1: Open PowerShell or CMD and clone the repo
```bash
git clone https://github.com/adprimak/woyage-generate-avatar.git
cd woyage-generate-avatar
```

### Step 2: Clone the fantasy-talking repo
```bash
git clone https://github.com/Fantasy-AMAP/fantasy-talking
```

### Step 3: Download models to woyage-generate-avatar/models/ as documented [here](https://github.com/Fantasy-AMAP/fantasy-talking/blob/main/README.md#model-download)

### Step 4: Create a virtual environment
```bash
cd /path/to/woyage-generate-avatar
python -m venv venv
```

### Step 5: Activate the virtual environment
```bash
venv\Scripts\activate
```

### Step 6: Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -r fantasy-talking/requirements.txt
```

### Step 7: Add AWS credentials to your environment.
```bash
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_DEFAULT_REGION=us-east-1
```

### Step 8: Ensure the avatar image is placed in `static/avatar.png`.

## Run

### Step 1: Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

### Step 2: Open a browser and go to:
```bash
http://localhost:8000/docs
```

### Step 3: Expand the `POST /video/generate_avatar` endpoint

### Step 4: Click "Try it Out"

### Step 5: Upload an mp3 file

### Step 6: Click "Execute"

## Folder Structure
```bash
woyage-generate-avatar/
├── app/
│   └── main.py
├── static/
│   └── avatar.png
├── fantasy-talking/
│   └── models/
│   └── requirements.txt
├── requirements.txt
└── README.md
```
