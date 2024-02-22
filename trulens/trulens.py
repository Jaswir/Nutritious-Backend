import os
import json

os.environ["OPENAI_API_KEY"] = "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"

# Create openai client
from openai import OpenAI

client = OpenAI()

# Imports main tools:
from trulens_eval import Feedback, OpenAI as fOpenAI, Tru, Provider, Select
from trulens_eval import TruBasicApp

tru = Tru(database_redact_keys=True)
tru.reset_database()


def llm_standalone(prompt):
    return (
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        .choices[0]
        .message.content
    )


calories = """370.92"""
ingredients = """
• zucchini
• diced potatoes
• onions
• tomato sauce
• minced garlic
• vegetable oil
• salt
• ground black pepper
• crushed red pepper flakes
• dried herbs
• cumin
• turmeric
"""

micro_nutrients = """
• Cholesterol:
0.00 mg
• Total_fat:
16.09 g
• Saturated_fat:
1.49 g
• Dietary_fiber:
10.40 g
• Protein:
9.48 g
• Sugars:
14.07 g
• Carbs:
54.42 g
• Sodium:
1189.38 mg
• Potassium:
1892.47 mg"""

prompt_input = f"How healthy is this food? \n Calories: {calories} \n Ingredients: {ingredients} \n Micro Nutrients: {micro_nutrients}"
prompt_output = llm_standalone(prompt_input)


class NutritiousFeedback(Provider):
    def custom_feedback(self, output: str) -> float:

        evaluation_prompt = f"""You are a renowned dietitian based on the following information:
        Calories: {calories},
        Ingredients: {ingredients},
        Micro Nutrients: {micro_nutrients}, 

        Someone gave the following advice: {output}
Give a score between 1 on 10 to evaluate this advice for succintness. A good answer only contains 1 to 3 sentences mentioning some essential points. 
Ensure your evaluation is presented in JSON format: {{"score": X}}"""

        print("Evaluation prompt:" + evaluation_prompt)

        response = llm_standalone(evaluation_prompt)
        print("Response" + response)
        res = int(json.loads(response)["score"])

        print("Result", res)
        return res / 10


nutritiousFeedback = NutritiousFeedback()

# Custom relevance function
f_custom_function = Feedback(nutritiousFeedback.custom_feedback).on(
    output=Select.RecordOutput
)


tru_llm_standalone_recorder = TruBasicApp(
    llm_standalone, app_id="Happy Bot", feedbacks=[f_custom_function]
)

with tru_llm_standalone_recorder as recording:
    tru_llm_standalone_recorder.app(prompt_input)


tru.run_dashboard()
