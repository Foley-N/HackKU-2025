import os
import base64
import json
from dotenv import load_dotenv
from requests import post, get

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
authorization_code = os.getenv('ACCESS_TOKEN')  # Store code in .env

##############################################################################
#     This is what a gen AI spat out after prompting it to try               #
#     and fix the issues with the new token funciton                         #
##############################################################################


def new_token():
    # Prepare data for POST request
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': authorization_code,
        'grant_type': 'authorization_code'
    }
    
    # Make the POST request
    response = post("https://www.strava.com/api/v3/oauth/token", data=data)
    
    # Check for HTTP errors
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    try:
        json_result = response.json()
        print("Token Response:", json_result)
        return json_result
    except json.JSONDecodeError:
        print("Error parsing JSON response")
        return None

def get_activity(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    test_url = "https://www.strava.com/api/v3/athlete/activities"
    response = get(test_url, headers=headers)
    json_result = response.json()
    print("kActivities:", json_result)
    return json_result

new_token()