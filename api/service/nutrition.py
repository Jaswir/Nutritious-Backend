import asyncio
import os
import aiohttp

from dotenv import load_dotenv

from api.data_models.Food import Ingredient
from api.service.helper_functions import extract_json_list, json_list_to_csv
from api.service.llm_client import send_request_with_image_to_openai
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



async def get_nutrition_info(query):
    """Send a POST request to Nutritionix API to get nutrition information for a query asynchronously."""
    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': NUTRITION_API_ID,
        'x-app-key': NUTRITION_API_KEY
    }
    body = {'query': query}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Error: {response.status}")
                return await response.text()


async def formalize_ingredients(ingredients):
    formatted_ingredients = []
    for ingredient in ingredients:
        ingredient_data = ingredient['foods'][0]
        formatted_ingredient = Ingredient(
            name=ingredient_data.get('food_name'),
            serving_quantity=ingredient_data.get('serving_qty'),
            serving_unit=ingredient_data.get('serving_unit'),
            serving_weight_grams=ingredient_data.get('serving_weight_grams'),
            calories=ingredient_data.get('nf_calories'),
            total_fat=ingredient_data.get('nf_total_fat'),
            saturated_fat=ingredient_data.get('nf_saturated_fat'),
            cholesterol=ingredient_data.get('nf_cholesterol'),
            sodium=ingredient_data.get('nf_sodium'),
            total_carbohydrate=ingredient_data.get('nf_total_carbohydrate'),
            dietary_fiber=ingredient_data.get('nf_dietary_fiber'),
            sugars=ingredient_data.get('nf_sugars'),
            protein=ingredient_data.get('nf_protein'),
            potassium=ingredient_data.get('nf_potassium'),
            phosphorus=ingredient_data.get('nf_phosphorus')
        )
        formatted_ingredients.append(formatted_ingredient)
    return formatted_ingredients

async def get_ingredients_nutrition(base64_image):
    prompt = predictive_template
    response = await send_request_with_image_to_openai(base64_image,
                                      prompt)
    response = """'```json
[
  "brioche bun",
  "mayonnaise",
  "beef patty",
  "grilled onions",
  "garlic powder",
  "salt",
  "black pepper",
  "butter",
  "avocado slices",
  "lettuce"
]
```'"""
    ingredients = extract_json_list(response)

    # Gather nutrition info for all ingredients concurrently
    nutrition_info_tasks = [get_nutrition_info(ingredient) for ingredient in ingredients]
    nutrition_infos = await asyncio.gather(*nutrition_info_tasks)
    formatted_ingredients = await formalize_ingredients(nutrition_infos)

    return formatted_ingredients

