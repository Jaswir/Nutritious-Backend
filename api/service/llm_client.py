import os

import dotenv
import requests
from PIL import Image
import io
import base64

dotenv.load_dotenv()


def load_image(image_source):
    """
    Loads an image from a local path or URL and returns a base64-encoded string.

    :param image_source: A string, either a path to a local file or a URL to an image.
    :return: A base64-encoded string of the image.
    """
    if image_source.startswith('http://') or image_source.startswith('https://'):
        response = requests.get(image_source)
        image = Image.open(io.BytesIO(response.content))
    else:
        image = Image.open(image_source)

    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


import requests

def send_request_to_openai(base64_image, prompt):
    """
    Sends an API request to OpenAI's GPT model including an image.

    :param base64_image: A base64-encoded string of the image.
    :param api_key: Your OpenAI API key.
    :param prompt: A text prompt to accompany the image.
    :return: The response from the API as a JSON object.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }

    payload = {
      "model": "gpt-4-vision-preview",
      "prompt": prompt,
      "temperature": 0.5,
      "max_tokens": 100,
      "attachments": [
        {
          "images": f"images:image/jpeg;base64,{base64_image}",
          "type": "image"
        }
      ]
    }

    response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=payload)
    return response.json()

# Example usage
if __name__ == "__main__":
    image_path_or_url = "path_or_url_to_your_image"
    base64_image = load_image(image_path_or_url)
    response = send_request_to_openai(base64_image)
    print(response)
