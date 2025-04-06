import os
import base64
import json
from datetime import datetime, timezone, timedelta
import time
from dotenv import load_dotenv
from requests import post, get
import mysql.connector
import threading


load_dotenv()
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
authorization_code = os.getenv('refresh_token')
host = os.getenv('host')
user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')




def load_env():
    load_dotenv()
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')
    authorization_code = os.getenv('refresh_token')  # Store code in .env


    return client_id, client_secret, authorization_code

# Function retrieves json with tokens
def new_tokenJSON():
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': authorization_code,
        'grant_type': 'refresh_token'
    }

    response = post("https://www.strava.com/api/v3/oauth/token", data=data)
    
    # Checking for HTTP errors
    #print(f"Status Code: {response.status_code}")
    #print(f"Response Text: {response.text}")
    
    try:
        json_result = response.json()
        #print("Token Response:", json_result)
        
        return json_result
    except json.JSONDecodeError:
        print("Error parsing JSON response")
        return None
    
# Function sets values for getRequest
def getRequest(json_result):
    #Get time from 7 days ago and now
    nowUTC = datetime.now(timezone.utc)
    sevenDaysAgo = nowUTC - timedelta(days=7)

     # convert to unix epoch timestamp
    afterTimeStamp = int(sevenDaysAgo.timestamp())
    beforeTimeStamp = int(nowUTC.timestamp())


    activites = get_activity(json_result["access_token"], afterTimeStamp, beforeTimeStamp)

    return activites 
    
# Function sends getRequest 
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

# Function goes through all new activities(json) and adds the entires that don't exist
def updateDatabase(jsonActivities):

    # Connecting to db
    mydb = mysql.connector.connect(
      host= host,
      user= user,
      password= password,
      database= database
    )

    cursor = mydb.cursor()

    # iterate through all activities in jsonActivities
    for activity in jsonActivities:
        # query Activity entires from database json_result["access_token"]
        newQuery = "SELECT * FROM dbhackku.Activities where id =" + str(activity["id"])
        insertQuery = ""
        cursor.execute(newQuery)
        result = cursor.fetchall()
        # if null then add entry
        if len(result) == 0:
            try:
                insertQuery = f"""
            INSERT INTO Activities (id, activityName, activityType, activityDistance, activityElapsedTime, activityElevationGain, activityStartTime, activityAverageSpeed, activityAverageHR)
            VALUES ({str(activity["id"])}, '{str(activity["name"])}', '{str(activity["sport_type"])}', '{str(activity["distance"])}', '{str(activity["elapsed_time"])}', '{str(activity["total_elevation_gain"])}', '{str(activity["start_date_local"])}', '{str(activity["average_speed"])}', '{str(activity["average_heartrate"])}')
            """
            # if can't access averageSpeed or averageHeartRate set as NULL
            except:
                 insertQuery = f"""
                INSERT INTO Activities (id, activityName, activityType, activityDistance, activityElapsedTime, activityElevationGain, activityStartTime, activityAverageSpeed, activityAverageHR)
                VALUES ({str(activity["id"])}, '{str(activity["name"])}', '{str(activity["sport_type"])}', '{str(activity["distance"])}', '{str(activity["elapsed_time"])}', '{str(activity["total_elevation_gain"])}', '{str(activity["start_date_local"])}', NULL, NULL)
                """                
            cursor.execute(insertQuery)
            mydb.commit()
            print(cursor.rowcount, "record inserted.")
        # otherwise skip
        else:
            continue
    mydb.close()

            # if not null then skip entry
    return "New entries: "


# Function runs python file
def checkDatabase():
    now = datetime.now()
    print("Executing Code at: " + str(now))
    jsonResult = new_tokenJSON()
    jsonActivities = getRequest(jsonResult)
    #print(f"Activities in the last 5 mins: {jsonActivities}")
    updateDatabase(jsonActivities)
    print("Executed Code!")

# Function runs every 15 seconds
def repeatedFunction():
      checkDatabase()
      threading.Timer(15, repeatedFunction).start()

repeatedFunction()
