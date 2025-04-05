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

def get_activity():
    act_url = url + "/athlete/activities"
    ressult = get(act_url)
    json_result = json.loads(ressult.content)
    print(json_result)
    return json_result

get_activity()