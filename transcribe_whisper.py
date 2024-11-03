from moviepy.editor import VideoFileClip
import whisper
from pathlib import Path
import json
from datetime import timedelta

class VideoTranscriber:
    def __init__(self, video_path):
        self.video_path = Path(video_path)
        self.temp_audio = "temp_audio.mp3"
        self.model = None
        self.video = None
        self.transcriptions = {}

    @staticmethod
    def format_timestamp(seconds):
        """Convert seconds to HH:MM:SS format"""
        return str(timedelta(seconds=int(seconds))).split('.')[0]

    def transcribe(self, output_name):
        if not self.video_path.exists():
            print(f"Video file not found at {self.video_path}")
            return False

        try:
            self._load_video()
            self._extract_audio()
            self._load_model()
            self._perform_transcription()
            self._save_results(output_name)
            self._cleanup()
            return True
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            self._cleanup()
            return False

    def _load_video(self):
        print("Loading video file...")
        self.video = VideoFileClip(str(self.video_path))

    def _extract_audio(self):
        print("Extracting audio...")
        self.video.audio.write_audiofile(self.temp_audio)

    def _load_model(self):
        print("Loading Whisper model...")
        self.model = whisper.load_model("base")

    def _perform_transcription(self):
        print("Transcribing audio...")
        result = self.model.transcribe(self.temp_audio)
        
        for segment in result["segments"]:
            start_time = self.format_timestamp(segment["start"])
            text = segment["text"].strip()
            self.transcriptions[start_time] = text

    def _save_results(self, output_name):
        # Save transcriptions to JSON
        output_file = Path(f"{output_name}.json")
        with output_file.open('w', encoding='utf-8') as f:
            json.dump(self.transcriptions, f, indent=4, ensure_ascii=False)
        
        # Save as plain text with timestamps
        with Path("transcription.txt").open('w', encoding='utf-8') as f:
            for timestamp, text in self.transcriptions.items():
                f.write(f"[{timestamp}] {text}\n\n")
        
        print(f"Transcription completed. Results saved to {output_file}")

    def _cleanup(self):
        if self.video:
            self.video.close()
        if Path(self.temp_audio).exists():
            Path(self.temp_audio).unlink()