import cv2
from pathlib import Path

def process_videos():
    # Create videos and images directories if they don't exist
    videos_dir = Path("videos")
    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    
    # Get all video files (supporting common video formats)
    video_extensions = [".mp4", ".avi", ".mov", ".mkv", ".webm"]
    video_files = []
    for ext in video_extensions:
        video_files.extend(videos_dir.glob(f"*{ext}"))
    
    if not video_files:
        print("No video files found in videos directory")
        return
    
    # Process each video file
    for video_path in video_files:
        print(f"\nProcessing {video_path.name}...")
        
        # Create video-specific output directory
        video_name = video_path.stem
        video_output_dir = images_dir / video_name
        video_output_dir.mkdir(exist_ok=True)
        
        # Open the video file
        cap = cv2.VideoCapture(str(video_path))
        
        frame_number = 0
        last_saved_second = -1
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Calculate timestamp in seconds
            timestamp = frame_number / fps
            current_second = int(timestamp)
            timestamp_str = f"{int(timestamp // 3600):02}:{int((timestamp % 3600) // 60):02}:{int(timestamp % 60):02}"
            
            # Save frame every second
            if current_second != last_saved_second:
                image_filename = video_output_dir / f"frame_{timestamp_str}.png"
                cv2.imwrite(str(image_filename), frame)
                last_saved_second = current_second
            
            frame_number += 1
        
        # Cleanup
        cap.release()
        print(f"Saved frames from {video_path.name}")
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_videos()
