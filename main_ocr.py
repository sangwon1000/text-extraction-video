# Installation requirements section
# Install OpenCV for image and video processing operations
# pip install opencv-python
# Install PyTesseract as a Python wrapper for Google's Tesseract-OCR Engine
# pip install pytesseract
# Tesseract OCR engine is required as the core OCR processor:
# Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki
# Linux: Install via package manager using: sudo apt install tesseract-ocr
# Mac: Install via Homebrew using: brew install tesseract

import cv2
import os
from pathlib import Path

def process_video():
    # Locate the most recently downloaded MP4 file in the 'downloads' directory
    downloads_dir = Path("downloads")
    mp4_files = list(downloads_dir.glob("*.mp4"))
    
    if not mp4_files:
        print("No MP4 files found in downloads directory")
        return
    
    # Get the most recent file based on creation time
    video_path = max(mp4_files, key=lambda x: x.stat().st_ctime)
    
    # Open the video file
    cap = cv2.VideoCapture(str(video_path))
    
    # Create output directory for saved images
    output_dir = Path("saved_images")
    output_dir.mkdir(exist_ok=True)
    
    frame_number = 0
    last_saved_second = -1  # Initialize with an invalid second
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Calculate timestamp in seconds
        timestamp = frame_number / fps
        current_second = int(timestamp)
        timestamp_str = f"{int(timestamp // 3600):02}:{int((timestamp % 3600) // 60):02}:{int(timestamp % 60):02}"
        
        # Save the frame every second
        if current_second != last_saved_second:
            image_filename = output_dir / f"frame_{current_second}.png"
            cv2.imwrite(str(image_filename), frame)
            last_saved_second = current_second
        
        # Display the frame (optional)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_number += 1  # Increment the frame counter
    
    # Cleanup: Release video resources and close display windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    process_video()
