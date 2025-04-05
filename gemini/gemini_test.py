from google import genai
from strava2JG import get_activity, new_tokenJSON
from dotenv import load_dotenv
import os

load_dotenv()
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
authorization_code = os.getenv('refresh_token')  # Store code in .env


client = genai.Client(api_key= "")


def prompt_builder():
    # new_tokenJSON()
    # json = get_activity()

    prompt = f"use this json file {json} to build a prompt for building a recovery plan based on the activity type, distance ran, elapsed time, and average heart rate. along with this also suggest any healthy snacks or meals to better help the user recover."
    response = client.models.generate_content(
        model = "gemini-2.0-flash-thinking-exp", 
        contents=prompt
    )

    print(response)
    return(response)

def post_run_suggestion():

    prompt = prompt_builder()

    suggestion = client.models.generate_content(
        model="gemini-2.0-flash-thinking-exp",
        contents=prompt
    )
    print(suggestion.text)

post_run_suggestion()
