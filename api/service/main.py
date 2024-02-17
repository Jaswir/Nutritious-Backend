import asyncio
import pprint

from api.service.helper_functions import extract_json_list
from api.service.llm_client import send_request_with_image_to_openai
from api.service.nutrition import get_nutrition_info, formalize_ingredients
from api.service.template_generator import predictive_template


async def get_ingredients_from_image(base64_image: str):
    # get ingredients from image
    prompt = predictive_template
    response = await send_request_with_image_to_openai(base64_image,
                                      prompt)
    ingredients = extract_json_list(response)


    # get nutrition info for each ingredient
    nutrition_info_tasks = [get_nutrition_info(ingredient) for ingredient in ingredients]
    nutrition_infos = await asyncio.gather(*nutrition_info_tasks)
    formatted_ingredients = await formalize_ingredients(nutrition_infos)

    pprint.pprint(formatted_ingredients)
    return formatted_ingredients

