import os

import dotenv
import requests
from PIL import Image
import io
import base64
import requests
import json

dotenv.load_dotenv()

# example images
image_burger_path = "./images/burger.jpeg"
image_curry_path = "./images/curry_one.jpeg"
image_pasta_path = "./images/pasta_one.jpeg"



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
        "Accept": "application/json",
      "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return (response.json()["choices"][0]["message"]["content"])

