from google import genai
from dotenv import load_dotenv
import os
import json
from requests import post, get
from datetime import datetime, timezone, timedelta

###############################################################################
# Enviroment variables

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


###############################################################################
# Gemini functions


client = genai.Client(api_key= "AIzaSyBpA0Ql3OrhSOYKi_xm4aKuypSMSJcdPoQ")


def prompt_builder():
    jsonResult = new_tokenJSON()
    #Get time from 3 days ago and now
    nowUTC = datetime.now(timezone.utc)
    threeDaysAgo = nowUTC - timedelta(days=3)

     # convert to unixj epoch timestamp
    afterTimeStamp = int(threeDaysAgo.timestamp())
    beforeTimeStamp = int(nowUTC.timestamp())

    json = get_activity(jsonResult["access_token"], afterTimeStamp, beforeTimeStamp)

    prompt = f"""Build a prompt for Google Gemini that uses the provided data {json} to generate a recovery plan for after a workout. The first section of the recovery
                plan will start with a short and encouraging message to the user congratulating them on their workout. After that please provide a short list of two to 
                three stretches to help prevent muscle cramps later on. The third section will be a short list of general tips to help the user continue to improve on their 
                workout journey (example: make sure to eat healthy, getting good sleep, tips to help improve their mental health)"""
    response = client.models.generate_content(
        model = "gemini-2.0-flash", 
        contents=prompt
    )

    #print(response.text)
    return(response.text)

def prompt_builder_goals():
    jsonResult = new_tokenJSON()
    #Get time from 3 days ago and now
    nowUTC = datetime.now(timezone.utc)
    threeDaysAgo = nowUTC - timedelta(days=3)

     # convert to unixj epoch timestamp
    afterTimeStamp = int(threeDaysAgo.timestamp())
    beforeTimeStamp = int(nowUTC.timestamp())

    json = get_activity(jsonResult["access_token"], afterTimeStamp, beforeTimeStamp)    
    
    prompt = f"""Build a prompt for Google Gemini that uses the provided data {json} to build realistic and achievable goals for future workouts. Look at specific things like improving t
                heir mile pace / average speed and time elapsed to better gauge these goals. Also look at any other data points that might be relevant in helping make new goals. please
                only provide a brief analysis and 2-3 goals. make sure the distance is in miles and the speed as mile pace (example the average american male can run 7 miniute mile)"""

    response = client.models.generate_content(
        model = "gemini-2.0-flash",
        contents=prompt
    )
    return(response.text)


def post_run_suggestion():
    prompt = prompt_builder()

    suggestion = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    print(suggestion.text)

def goal_setting():

    prompt = prompt_builder_goals()

    response = client.models.generate_content(
        model = "gemini-2.0-flash",
        contents=prompt
    )
    print(response.text)
    return(response.text)

###############################################################################
# Strava functions 

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

###############################################################################
# function calls

#post_run_suggestion()

goal_setting()
