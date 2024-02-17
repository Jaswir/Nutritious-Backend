import os

import dotenv
import requests
from PIL import Image
import io
import base64
import requests

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