from pathlib import Path
import json
from transcribe_whisper import VideoTranscriber

def process_videos():
    # Create videos directory if it doesn't exist
    videos_dir = Path("./videos")
    videos_dir.mkdir(exist_ok=True)
        
    # Get all video files (supporting common video formats)
    video_extensions = [".mp4", ".avi", ".mov", ".mkv", ".webm"]
    video_files = []
    for ext in video_extensions:
        video_files.extend(videos_dir.glob(f"*{ext}"))
    
    if not video_files:
        print("No video files found in ./videos directory")
        return

    # Process each video file
    for video_path in video_files:
        # Skip if transcription already exists
        json_path = video_path.with_suffix('.json')
        print(json_path)
        if json_path.exists():
            print(f"Skipping {video_path.name} - transcription already exists")
            continue
            
        print(f"\nProcessing {video_path.name}...")
        transcriber = VideoTranscriber(video_path)
        success = transcriber.transcribe(str(video_path))
        
        if success:
            print(f"Successfully transcribed {video_path.name}")
        else:
            print(f"Failed to transcribe {video_path.name}")

    # Print summary of all transcriptions
    print("\nTranscription Summary:")
    for json_file in videos_dir.glob("*.json"):
        try:
            with json_file.open('r', encoding='utf-8') as f:
                transcription = json.load(f)
                total_segments = len(transcription)
                print(f"\n{json_file.stem}:")
                print(f"Total segments: {total_segments}")
                
                # Print full transcription
                # print("\nFull Transcription:")
                # for time, text in transcription.items():
                #     print(f"[{time}] {text}")
                
                # Print first and last segments as preview
                if total_segments > 0:
                    times = list(transcription.keys())
                    print(f"First segment [{times[0]}]: {transcription[times[0]][:100]}...")
                    print(f"Last segment [{times[-1]}]: {transcription[times[-1]][:100]}...")
        except Exception as e:
            print(f"Error reading {json_file}: {str(e)}")

if __name__ == "__main__":
    process_videos()
