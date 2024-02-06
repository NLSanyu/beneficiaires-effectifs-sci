import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
PAPPERS_API_KEY = os.getenv("PAPPERS_API_KEY")
url = f"https://api.pappers.fr/v2/entreprise?api_token={PAPPERS_API_KEY}&siren=444979314"


response = requests.request("GET", url, timeout=10)

print(response.json())

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(response.json(), f)
