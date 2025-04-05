import os
import base64
import json
from datetime import datetime, timezone, timedelta
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
        #Get time from 30 minutes ago and now
        nowUTC = datetime.now(timezone.utc)
        thirtyMinutesAgo = nowUTC - timedelta(minutes=1)

        # convert to unix epoch timestamp
        afterTimeStamp = int(thirtyMinutesAgo.timestamp())
        beforeTimeStamp = int(nowUTC.timestamp())

        activites = get_activity(json_result["access_token"], afterTimeStamp, beforeTimeStamp)
        return 0
    except json.JSONDecodeError:
        print("Error parsing JSON response")
        return None
    
    

def get_activity(access_token, afterTime, beforeTime):
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
    "after": afterTime,
    "before": beforeTime
    }
    test_url = "https://www.strava.com/api/v3/athlete/activities"
    response = get(test_url, headers=headers, params=params)
    json_result = response.json()
    print("jsonResponse:", json_result)
    return json_result

new_token()
