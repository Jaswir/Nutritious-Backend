import os
from dotenv import load_dotenv
import requests

from api.service.llm_client import load_image, send_request_to_openai

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



def get_ingredients_from_image():
    pass

# Example usage
if __name__ == "__main__":
    image_path_or_url = image_burger_path
    base64_image = load_image(image_path_or_url)
    prompt = "This is a picture of the users meal. Given this photo, provide all of the ingredients of this food in csv format. Be careful to include all of the foods that are in the photo, include all individual ingredients you think were used to make the food: "
    response = send_request_to_openai(base64_image, prompt)
    print(response)

# Example usage
# if __name__ == "__main__":
#     query = "grape"
#     result = get_nutrition_info(query)
#     print(result)
