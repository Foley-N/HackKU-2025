import os
import base64
import pycurl
from dotenv import load_dotenv
from requests import post, get

def get_token():

    auth_string = CLIENT_ID + ":" + CLIENT_ID
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

