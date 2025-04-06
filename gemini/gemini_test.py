from google import genai
from dotenv import load_dotenv
import os
import json
from requests import post, get
from datetime import datetime, timezone, timedelta


load_dotenv()
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
authorization_code = os.getenv('refresh_token')  # Store code in .env

def load_env():
    load_dotenv()
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')
    authorization_code = os.getenv('refresh_token')  # Store code in .env


    return client_id, client_secret, authorization_code


client = genai.Client(api_key= "AIzaSyBpA0Ql3OrhSOYKi_xm4aKuypSMSJcdPoQ")


def prompt_builder():
    jsonResult = new_tokenJSON()
    #Get time from 3 days ago and now
    nowUTC = datetime.now(timezone.utc)
    threeDaysAgo = nowUTC - timedelta(days=3)

     # convert to unix epoch timestamp
    afterTimeStamp = int(threeDaysAgo.timestamp())
    beforeTimeStamp = int(nowUTC.timestamp())

    json = get_activity(jsonResult["access_token"], afterTimeStamp, beforeTimeStamp)

    prompt = f"use this json file {json} to build a prompt for building a recovery plan based on the activity type, distance ran, elapsed time, and average heart rate. along with this also suggest any healthy snacks or meals to better help the user recover."
    response = client.models.generate_content(
        model = "gemini-2.0-flash", 
        contents=prompt
    )

    print(response.text)
    return(response.text)

def post_run_suggestion():
    prompt = prompt_builder()

    suggestion = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    print(suggestion.text)

def new_tokenJSON():
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
    #print(f"Status Code: {response.status_code}")
    #print(f"Response Text: {response.text}")
    
    try:
        json_result = response.json()
        #print("Token Response:", json_result)
        
        return json_result
    except json.JSONDecodeError:
        print("Error parsing JSON response")
        return None
    
def getRequest(json_result):
    #Get time from 30 minutes ago and now
    nowUTC = datetime.now(timezone.utc)
    thirtyMinutesAgo = nowUTC - timedelta(days=2)

     # convert to unix epoch timestamp
    afterTimeStamp = int(thirtyMinutesAgo.timestamp())
    beforeTimeStamp = int(nowUTC.timestamp())


    activites = get_activity(json_result["access_token"], afterTimeStamp, beforeTimeStamp)

    return activites 

def get_activity(access_token, afterTime, beforeTime):
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
    "after": afterTime,
    "before": beforeTime
    }
    test_url = "https://www.strava.com/api/v3/athlete/activities"
    response = get(test_url, headers=headers, params=params)
    json_result = response.json()
    #print("jsonResponse:", json_result)
    return json_result


post_run_suggestion()
