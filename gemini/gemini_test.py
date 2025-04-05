from google import genai
from strava2JG import get_activity, new_tokenJSON

# load_dotenv()
# local_api_key = os.getenv('') 

client = genai.Client(api_key= "")


def prompt_builder():
    json = get_activity(new_tokenJSON())

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
