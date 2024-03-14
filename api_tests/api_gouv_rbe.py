import os
import logging

from dotenv import load_dotenv
import requests

import pandas as pd

load_dotenv()

logging.basicConfig(
    filename="errors.log",
    format="%(asctime)s - %(message)s",
    level=logging.ERROR
)


def fetch_data():
    """Fetch data in from the EONET API"""
    RBE_API_BASE_URL = os.getenv("RBE_API_BASE_URL")

    api_endpoint = f"{RBE_API_BASE_URL}" # placeholder endpoint, base url

    response = requests.get(api_endpoint, timeout=10)

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return None

    data = response.json()["..."]
    return data


def prep_data():
    """Put data in a Pandas dataframe for analysis"""
    data = fetch_data()
    data_list = []
    for item in data:
        datapoint = {
            # Placeholder code
            "Title": item['title'],
            "Name": item['names'][0]['name']
        }

        data_list.append(datapoint)

    df = pd.DataFrame(data_list)

    return df
