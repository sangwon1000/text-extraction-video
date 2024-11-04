# Install required packages:
# pip install anthropic
# pip install Pillow

import anthropic
import base64
from PIL import Image
from pathlib import Path
import io
import dotenv
import os

dotenv.load_dotenv()

class AnthropicProcessor:
    def __init__(self, api_key=None):
        self.client = anthropic.Anthropic(
            api_key=api_key or os.getenv("ANTHROPIC_API_KEY")
        )
    
    def extract_text_from_image(self, image_path="./downloads/test.png"):
        # Load and encode the image
        image = Image.open(image_path)
        
        # Convert image to bytes
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()
        base64_image = base64.b64encode(img_bytes).decode('utf-8')
        
        # Create message with the image
        message = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please extract all text from this image. Output only the extracted text, nothing else. If there is no text in the image, output '-'"
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": base64_image
                        }
                    }
                ]
            }]
        )
        
        text = message.content[0].text
        
        # Create output file path
        output_path = Path(image_path).with_suffix('.ocr.txt')
        
        # Write extracted text to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"OCR results saved to: {output_path}")
        print("\nExtracted text:")
        print("-" * 40)
        print(text)
        print("-" * 40)
        
        return text

    def process_text(self, text, system_prompt=None):
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
            
        messages.append({
            "role": "user",
            "content": text
        })
        
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=messages
        )
        
        return response.content[0].text

if __name__ == "__main__":
    processor = AnthropicProcessor()
    # Example usage:
    # processor.extract_text_from_image()
    # response = processor.process_text("What is the meaning of life?")
    # print(response) 