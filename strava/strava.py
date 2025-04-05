import os
import base64
import pycurl
import json
from dotenv import load_dotenv
from requests import post, get


# some basic set up for using the api
load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

auth_string = client_id + ":" + client_secret 
auth_bytes = auth_string.encode("utf-8")
auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")


url = "https://www.strava.com/api/v3/athlete"

def new_token():
    token = post("https://www.strava.com/api/v3/oauth/token?client_id=154485&client_secret=9fc28f2ed9d740f9f0faa37a6d7a5ab4310ed0f5&refresh_token=e2827eda87745f267f96a2f5ae4391ef8ba22641&grant_type=refresh_token")
    json_result = token.json()
    #print(json_result)
    return(json_result)

#new_token()

def get_activity():
    token = new_token()
    #act_url = url + "/athlete/activities"
    test_url = "https://www.strava.com/api/v3/athlete/activities"
    result = get(test_url)
    json_result = json.loads(result.content)
    print(json_result)
    return json_result

get_activity()