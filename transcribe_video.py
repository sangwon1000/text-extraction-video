from moviepy.editor import VideoFileClip
import whisper
from pathlib import Path
import json
from datetime import timedelta

def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format"""
    return str(timedelta(seconds=int(seconds))).split('.')[0]

def transcribe_video(video_path):
    # Load the video file
    print("Loading video file...")
    video = VideoFileClip(str(video_path))
    
    # Extract audio from video
    print("Extracting audio...")
    audio_path = "temp_audio.mp3"
    video.audio.write_audiofile(audio_path)
    
    # Load Whisper model (options: tiny, base, small, medium, large)
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    
    # Transcribe audio
    print("Transcribing audio...")
    result = model.transcribe(audio_path)
    
    # Format transcriptions with timestamps
    transcriptions = {}
    for segment in result["segments"]:
        start_time = format_timestamp(segment["start"])
        text = segment["text"].strip()
        transcriptions[start_time] = text
    
    # Save transcriptions to JSON
    output_file = Path("transcription.json")
    with output_file.open('w', encoding='utf-8') as f:
        json.dump(transcriptions, f, indent=4, ensure_ascii=False)
    
    # Save as plain text with timestamps
    with Path("transcription.txt").open('w', encoding='utf-8') as f:
        for timestamp, text in transcriptions.items():
            f.write(f"[{timestamp}] {text}\n\n")
    
    # Cleanup
    Path(audio_path).unlink()
    video.close()
    
    print(f"Transcription completed. Results saved to {output_file}")

if __name__ == "__main__":
    # Path to your video file
    video_path = Path("downloads/2024-03-13_09-15-46_UTC.mp4")
    
    if not video_path.exists():
        print(f"Video file not found at {video_path}")
    else:
        transcribe_video(video_path) 