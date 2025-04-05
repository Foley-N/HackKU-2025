from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
local_api_key = os.getenv('api_key') 

client = genai.Client(api_key=local_api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works",
)

print(response.text)

