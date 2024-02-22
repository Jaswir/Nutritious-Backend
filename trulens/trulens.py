import os
from os import environ
import json

os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY_3p5")


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



def getNutrientsData():
    nutrients = []
    with open('trulens/nutrient-data.txt', 'r') as file:
        nutrients = file.read().split('好')

    return nutrients

nutrients = getNutrientsData()


class NutritiousFeedback(Provider):
    def succintness_feedback(self, output: str) -> float:
      
        print("Output: ", output)   
        minSucctintness = 500
        size = len(output)

        if size < minSucctintness:
            print("succinctness: " , 1.0)
            return 1.0
        
        else :
            overSize = size - minSucctintness
            succintness =  min(1.0, overSize / 500)
            print("succinctness: " , 1 - succintness)
            return 1 - succintness


nutritiousFeedback = NutritiousFeedback()

# Custom relevance function
f_custom_function = Feedback(nutritiousFeedback.succintness_feedback).on(
    output=Select.RecordOutput
)

tru_llm_standalone_recorder = TruBasicApp(
    llm_standalone, app_id="Happy Bot", feedbacks=[f_custom_function]
)




with tru_llm_standalone_recorder as recording:
    for i in range(len(nutrients)):
        n = nutrients[i]
        prompt_input = f"How healthy is this food? Answer in 1 to 3 sentences\n {n}"

        tru_llm_standalone_recorder.app(prompt_input)


tru.run_dashboard()
