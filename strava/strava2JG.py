import os
import base64
import json
from datetime import datetime
import time
from dotenv import load_dotenv
from requests import post, get
from datetime import date, timedelta


load_dotenv()
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
authorization_code = os.getenv('refresh_token')  # Store code in .env

##############################################################################
#     This is what a gen AI spat out after prompting it to try               #
#     and fix the issues with the new token funciton                         #
##############################################################################


def new_token():
    # Prepare data for POST request
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': authorization_code,
        'grant_type': 'refresh_token'
    }
    
    # Make the POST request
    response = post("https://www.strava.com/api/v3/oauth/token", data=data)
    
    # Check for HTTP errors
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    try:
        json_result = response.json()
        print("Token Response:", json_result)
        # get twoDays ago and dayAgo datetime variables
        year = int(datetime.now().year)
        month = int(datetime.now().month)
        day = int(datetime.now().day)
        twoDaysAgo = datetime(year, month, day-2, 0, 0, 0)
        oneDayAgo = datetime(year, month, day-1, 0, 0, 0)

        # convert to unix epoch timestamp
        twoDaysAgoTS = twoDaysAgo.timestamp()
        oneDayAgoTS = oneDayAgo.timestamp()

        activites = get_activity(json_result["access_token"], twoDaysAgoTS, oneDayAgoTS)
        return 0
    except json.JSONDecodeError:
        print("Error parsing JSON response")
        return None
    
    

def get_activity(access_token, twoDaysAgo, oneDayAgo):
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
    "before": "{oneDayAgo}",
    "after": "{twoDaysAgo}"
    }
    test_url = "https://www.strava.com/api/v3/athlete/activities"
    response = get(test_url, headers=headers, params=params)
    json_result = response.json()
    print("jsonResponse:", json_result)
    return json_result

#new_token()

def json_parse():
    with open("strava/runResponse.json", "r") as file:
        data = json.load(file)
        #print(data)
        print(data["name"])

json_parse()