import os
from dotenv import load_dotenv
import requests

from api.service.helper_functions import extract_json_list, json_list_to_csv
from api.service.image import load_image
from api.service.llm_client import send_request_to_openai
from api.service.template_generator import predictive_template

# Load environment variables from .env file
load_dotenv()

# Get API key and app ID from environment variables
NUTRITION_API_KEY = os.getenv('NUTRITION_API_KEY')
NUTRITION_API_ID = os.getenv('NUTRITION_API_ID')


# example images
image_burger_path = "./images/burger.jpeg"
image_curry_path = "./images/curry_one.jpeg"
image_pasta_path = "./images/pasta_one.jpeg"



def get_nutrition_info(query):
    """Send a POST request to Nutritionix API to get nutrition information for a query."""

    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': NUTRITION_API_ID,
        'x-app-key': NUTRITION_API_KEY
    }
    body = {
        'query': query
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return response.text



def get_ingredients_from_image(base64_image):
    prompt = predictive_template
    response = send_request_to_openai(base64_image, prompt)
    ingredients_text = extract_json_list(response)
    ingredients = get_nutrition_info(json_list_to_csv(ingredients_text))
    return ingredients


# Example usage
if __name__ == "__main__":
    image_path_or_url = image_burger_path
    base64_image = load_image(image_path_or_url)
    ingredients = get_ingredients_from_image(base64_image)
    print(ingredients)
