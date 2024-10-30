# Install required packages:
# pip install opencv-python
# pip install pytesseract
# You also need to install Tesseract OCR engine:
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
# Linux: sudo apt install tesseract-ocr
# Mac: brew install tesseract

import cv2
import pytesseract
import os
from pathlib import Path

def extract_text_from_video():
    # Find the most recent mp4 file in downloads folder
    downloads_dir = Path("downloads")
    mp4_files = list(downloads_dir.glob("*.mp4"))
    
    if not mp4_files:
        print("No MP4 files found in downloads directory")
        return
    
    # Get the most recent file based on creation time
    video_path = max(mp4_files, key=lambda x: x.stat().st_ctime)
    
    # Open the video file
    cap = cv2.VideoCapture(str(video_path))
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"FPS: {fps}")
    frame_interval = int(fps / 6)
    extracted_texts = {}
    
    frame_number = 0
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break
            
        if frame_number % frame_interval == 0:
            # Calculate timestamp
            timestamp = frame_number / fps
            timestamp_str = f"{int(timestamp // 60):02d}:{int(timestamp % 60):02d}"
            
            # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold to get better OCR results
            _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            
            # Extract text from the frame
            text = pytesseract.image_to_string(threshold)
            
            # Add non-empty lines to the dictionary with timestamps
            for line in text.split('\n'):
                line = line.strip()
                if line:
                    extracted_texts[f"[{timestamp_str}] {line}"] = timestamp
        
        frame_number += 1
    
    # Release video capture
    cap.release()
    
    # Write extracted text to file with timestamps
    output_path = video_path.with_suffix('.ocr.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        # Sort by timestamp and write to file
        for text in sorted(extracted_texts.keys(), key=lambda x: extracted_texts[x]):
            f.write(text + '\n')
    
    print(f"OCR results saved to: {output_path}")

if __name__ == "__main__":
    extract_text_from_video()
