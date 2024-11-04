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
    
    # System prompt for content analysis
    system_prompt = """You are an expert content analyzer. Analyze the provided video content including:
    1. OCR text extracted from video frames
    2. Audio transcription
    3. Video description
    
    Provide a concise summary that includes:
    - Main topics/themes
    - Key points
    - Notable quotes or text
    - Overall content classification
    Keep the analysis focused and relevant."""
    
    # Process each video's content
    for timestamp, content in combined_data.items():
        print(f"\nAnalyzing content from: {timestamp}")
        
        # Combine all available content
        content_parts = []
        
        if content.get("ocr"):
            content_parts.append("OCR Text:\n" + str(content["ocr"]))
        
        if content.get("transcription"):
            content_parts.append("Transcription:\n" + str(content["transcription"]))
            
        if content.get("description"):
            content_parts.append("Description:\n" + str(content["description"]))
        
        if not content_parts:
            print(f"No content available for {timestamp}")
            continue
        
        # Combine all content parts
        combined_text = "\n\n".join(content_parts)
        
        # try:
        #     # Process the combined content
        #     analysis = processor.process_text(combined_text, system_prompt)
        #     analysis_results[timestamp] = analysis
        #     print(f"Successfully analyzed content from {timestamp}")
            
        # except Exception as e:
        #     print(f"Error analyzing content from {timestamp}: {str(e)}")
        #     analysis_results[timestamp] = f"Error: {str(e)}"
    
    # Save analysis results
    output_path = Path("content_analysis.json")
    with output_path.open('w', encoding='utf-8') as f:
        json.dump(analysis_results, f, indent=4, ensure_ascii=False)
    
    print(f"\nAnalysis complete. Results saved to {output_path}")
    
    
