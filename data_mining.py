from pathlib import Path
import json
from anthropic_processor import AnthropicProcessor

def analyze_video_content():
    # Initialize AnthropicProcessor
    processor = AnthropicProcessor()
    
    # Load combined data
    combined_data_path = Path("combined_data.json")
    if not combined_data_path.exists():
        print("combined_data.json not found")
        return
    
    with combined_data_path.open('r', encoding='utf-8') as f:
        combined_data = json.load(f)
    
    analysis_results = {}


    from itertools import islice
    first_two = list(islice(combined_data.items(), 2))
    print(f"First timestamp: {first_two[0][0]}")
    print(f"First item data: {first_two[0][1]}")
    print(f"\nSecond timestamp: {first_two[1][0]}")
    print(f"Second item data: {first_two[1][1]}")
    
    
    # System prompt for content analysis
    system_prompt = """
    You will be given the OCR text extracted from video frames
    Provide the list of all the restaurants mentioned in the transcription.
    For the name of the restaurant, use the name from the OCR Text.
    Include description of the restaurant.
    You must give answer in json format with the following format:
    {
        "restaurants": [
            {
                "name": "restaurant name",
                "description": "restaurant description"
            }
        ]
    }     
    """
# , the audio transcription, and the Description.     
# You are an audio transcriber. You have already transcribed the audio, but unsure of the quality of the transcription.
#     You will be given the OCR text extracted from video frames, the audio transcription, and the Description. Correct any errors in the transcription. 
#     When you make a revision, replace text with the OCR Text extracted from video frames.

#     1. OCR Text
#     2. Transcription
#     3. Description
    
#     First give me the revised transcription with correct wordings.
#     then Provide all the restaurants mentioned in the transcription. Include description of the restaurant.

    # Process each video's content
    # for timestamp, content in first_two:
    for timestamp, content in combined_data.items():
        print(f"\nAnalyzing content from: {timestamp}")
        
        # Combine all available content
        content_parts = []
        
        if content.get("ocr"):
            content_parts.append("OCR Text:\n" + str(content["ocr"]))
        
        # if content.get("transcription"):
        #     content_parts.append("Transcription:\n" + str(content["transcription"]))
            
        # if content.get("description"):
        #     content_parts.append("Description:\n" + str(content["description"]))
        
        if not content_parts:
            print(f"No content available for {timestamp}")
            continue
        
        # Combine all content parts
        combined_text = "\n\n".join(content_parts)
        print(combined_text)

        try:
            # Process the combined content
            analysis = processor.process_text(combined_text, system_prompt)
            analysis_results[timestamp] = analysis
            print(f"Successfully analyzed content from {timestamp}")
            
        except Exception as e:
            print(f"Error analyzing content from {timestamp}: {str(e)}")
            analysis_results[timestamp] = f"Error: {str(e)}"
    
    # Save analysis results
    output_path = Path("content_analysis.json")
    with output_path.open('w', encoding='utf-8') as f:
        json.dump(analysis_results, f, indent=4, ensure_ascii=False)
    
    print(f"\nAnalysis complete. Results saved to {output_path}")
    
    
analyze_video_content()