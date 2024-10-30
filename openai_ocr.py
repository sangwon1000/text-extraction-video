# Install required packages:
# pip install openai
# pip install Pillow

import openai
import base64
from PIL import Image
from pathlib import Path
import io
import dotenv
import os

dotenv.load_dotenv()

def extract_text_from_image(image_path="./downloads/test.png"):
    # Initialize OpenAI client
    client = openai.OpenAI(
        api_key=os.getenv("OPEN_AI_API_KEY")
    )
    
    # Load and encode the image
    image = Image.open(image_path)
    
    # Convert image to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    base64_image = base64.b64encode(img_bytes).decode('utf-8')
    
    # Create message with the image
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "hi."
                    },
                    # {
                    #     "type": "image_url",
                    #     "image_url": {
                    #         "url": f"data:image/png;base64,{base64_image}"
                    #     }
                    # }
                ]
            }
        ],
        max_tokens=1000
    )
    
    # Extract text from response
    text = response.choices[0].message.content
    
    # Create output file path
    output_path = Path(image_path).with_suffix('.ocr.txt')
    
    # Write extracted text to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"OCR results saved to: {output_path}")
    
    # Also print the text to console
    print("\nExtracted text:")
    print("-" * 40)
    print(text)
    print("-" * 40)

if __name__ == "__main__":
    extract_text_from_image() 