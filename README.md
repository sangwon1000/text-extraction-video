# Video Content Analysis Pipeline

A comprehensive pipeline for downloading, processing, and analyzing video content using various AI services.

## Overview

This project provides a suite of tools to:
1. Download videos from Instagram
2. Extract frames from videos
3. Perform OCR on extracted frames
4. Transcribe video audio
5. Combine and analyze all extracted data

## Features

### Instagram Video Download
- Downloads videos from specified Instagram profiles
- Tracks downloaded posts to avoid duplicates
- Organizes downloads by username

### Video Processing
- Extracts frames at 1-second intervals
- Saves frames as PNG images with timestamp-based naming
- Organizes frames in video-specific directories

### OCR Processing
- Uses Claude 3 (Anthropic) for text extraction from frames
- Processes images in batches
- Saves OCR results with timestamps
- Combines results into a single JSON file

### Audio Transcription
- Uses OpenAI Whisper for speech-to-text
- Generates timestamped transcriptions
- Supports multiple video formats
- Saves transcriptions in both JSON and TXT formats

### Data Mining & Analysis
- Combines OCR, transcription, and text data
- Groups content by timestamp
- Generates comprehensive analysis reports
- Saves combined data in structured JSON format

## Setup

1. Install required dependencies:

bash
pip install instaloader moviepy whisper anthropic openai pillow opencv-python python-dotenv

2. Create a `.env` file with your API keys:

INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
ANTHROPIC_API_KEY=your_anthropic_key
OPEN_AI_API_KEY=your_openai_key
```

## Usage

### 1. Download Videos
```bash
python main_instaloader.py
```

### 2. Extract Frames
```bash
python slice_video.py
```

### 3. Process Images with OCR
```bash
python image_ocr.py
```

### 4. Transcribe Videos
```bash
python main_transcribe.py
```

### 5. Combine and Analyze Data
```bash
python data_mining.py
```

## File Structure
```
.
├── videos/                 # Downloaded videos and transcriptions
├── images/                # Extracted video frames
├── combined_data.json     # Final processed data
├── ocr_results.json       # OCR results
└── downloaded_posts.json  # Tracking file for downloaded posts
```

## Output Format

The final combined data is stored in `combined_data.json` with the following structure:
```json
{
    "timestamp_string": {
        "timestamp": "2024-03-13_03-31-14_UTC",
        "ocr": "extracted text from frames",
        "transcription": "audio transcription",
        "description": "additional text content"
    }
}
```

## Notes

- All media files (videos, images) and JSON outputs are ignored in git
- Supports multiple video formats including MP4, AVI, MOV, MKV, and WEBM
- Processes files incrementally, skipping already processed content
- Uses timestamp-based naming for easy correlation between different data types

## Error Handling

- Each component includes robust error handling
- Failed operations are logged but don't stop the pipeline
- Partial results are saved even if some steps fail

## Dependencies

- Python 3.8+
- Instaloader for Instagram downloads
- MoviePy for video processing
- OpenAI Whisper for transcription
- Anthropic Claude 3 for OCR
- OpenCV for frame extraction
- Various utility libraries (pathlib, json, etc.)
```
