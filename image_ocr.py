from pathlib import Path
import json
from anthropic_processor import AnthropicProcessor

def process_images():
    # Initialize the AnthropicProcessor
    processor = AnthropicProcessor()
    
    # Create images directory if it doesn't exist
    images_dir = Path("./images")
    images_dir.mkdir(exist_ok=True)
    
    # Load existing results if available
    output_file = Path("ocr_results.json")
    if output_file.exists():
        with output_file.open('r', encoding='utf-8') as f:
            all_results = json.load(f)
    else:
        all_results = {}
    
    # Process each video directory in the images folder
    for video_dir in sorted(images_dir.glob("*")):
        
        if video_dir.is_dir():
            video_name = video_dir.name
            
            # Skip if video already processed
            if video_name in all_results:
                print(f"\nSkipping {video_name} - already processed")
                continue
                
            print(f"\nProcessing images from video: {video_name}")
            
            # Dictionary to store results for this video
            video_results = {}
            
            # Process each image in the video directory
            for image_path in sorted(video_dir.glob("*.png")):
                print(f"Processing image: {image_path.name}")
                
                try:
                    # Extract text from image
                    extracted_text = processor.extract_text_from_image(str(image_path))
                    
                    # Store result using frame timestamp as key
                    # Frame filename format is "frame_HH:MM:SS.png"
                    timestamp = image_path.stem.replace("frame_", "")
                    video_results[timestamp] = extracted_text
                    
                except Exception as e:
                    print(f"Error processing {image_path.name}: {str(e)}")
            
            # Store results for this video
            all_results[video_name] = video_results
            
            # Save results after each video is processed
            with output_file.open('w', encoding='utf-8') as f:
                json.dump(all_results, f, indent=4, ensure_ascii=False)
            print(f"Results saved for: {video_name}")
    
    print(f"\nAll OCR results saved to: {output_file}")

if __name__ == "__main__":
    process_images()
