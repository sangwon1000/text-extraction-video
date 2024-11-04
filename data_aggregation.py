from pathlib import Path
import json
from datetime import datetime

def parse_timestamp(filename):
    """Parse timestamp from filename format: 2024-03-13_03-31-14_UTC"""
    try:
        # Remove UTC and split into date and time
        date_time_str = filename.replace('_UTC', '')
        return datetime.strptime(date_time_str, '%Y-%m-%d_%H-%M-%S')
    except:
        return None

def group_files_by_timestamp():
    # Get all files
    ocr_results = load_ocr_results()
    transcriptions = load_video_transcriptions()
    text_docs = load_text_documents()
    
    # Dictionary to store grouped content
    grouped_content = {}
    
    # Helper function to add content to groups
    def add_to_group(timestamp_str, content_type, data):
        if timestamp_str not in grouped_content:
            grouped_content[timestamp_str] = {
                "timestamp": timestamp_str,
                "ocr": None,
                "transcription": None,
                "description": None
            }
        grouped_content[timestamp_str][content_type] = data

    # Process OCR results
    for video_name, ocr_data in ocr_results.items():
        timestamp = parse_timestamp(video_name)
        if timestamp:
            add_to_group(video_name, "ocr", ocr_data)

    # Process transcriptions
    for video_name, trans_data in transcriptions.items():
        timestamp = parse_timestamp(video_name)
        if timestamp:
            add_to_group(video_name, "transcription", trans_data)

    # Process text documents
    for doc_name, text_data in text_docs.items():
        timestamp = parse_timestamp(doc_name)
        if timestamp:
            add_to_group(doc_name, "description", text_data)

    return grouped_content

def load_ocr_results():
    ocr_file = Path("ocr_results.json")
    if ocr_file.exists():
        with ocr_file.open('r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def load_video_transcriptions():
    videos_dir = Path("./videos")
    transcriptions = {}
    
    for json_file in videos_dir.glob("*.json"):
        try:
            # Remove the .mp4 extension from the stem to match timestamp format
            clean_stem = json_file.stem.replace('.mp4', '')
            with json_file.open('r', encoding='utf-8') as f:
                data = json.load(f)
                transcriptions[clean_stem] = data
        except Exception as e:
            print(f"Error reading {json_file}: {str(e)}")
            transcriptions[clean_stem] = None
    return transcriptions

def load_text_documents():
    docs = {}
    for txt_file in Path("./videos").glob("*.txt"):
        try:
            # Use the raw stem as it already matches the timestamp format
            with txt_file.open('r', encoding='utf-8') as f:
                docs[txt_file.stem] = f.read()
        except Exception as e:
            print(f"Error reading {txt_file}: {str(e)}")
            docs[txt_file.stem] = None
    
    return docs

def combine_data():
    # Group all related files by timestamp
    grouped_content = group_files_by_timestamp()
    
    # Save combined data
    with open("combined_data.json", 'w', encoding='utf-8') as f:
        json.dump(grouped_content, f, indent=4, ensure_ascii=False)
    
    print("Data combined and saved to combined_data.json")
    
    # Print summary
    print("\nContent Summary:")
    for timestamp, content in grouped_content.items():
        print(f"\nTimestamp: {timestamp}")
        print("Contains:")
        for content_type, data in content.items():
            if data and content_type != "timestamp":
                print(f"- {content_type}")

if __name__ == "__main__":
    combine_data()
