# UDFs imported by other files:
# api_to_json_extended_parameters.ipynb -> api_to_json, fetch_data_from_api


import http.client
import json
import pandas as pd

from typing import Optional

def fetch_data_from_api(endpoint: str = 'status') -> str:
    """
    Fetches data from the API based on the specified endpoint.

    Args:
        endpoint (str): The API endpoint to query (default is 'status').

    Returns:
        str: The raw JSON response data as a Unicode string.
    """
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "9c8eed52c73c854fa92b9ef6bd4a2498"  # Replace key with data from secrets.txt file
    }

    try:
        conn.request("GET", f"/{endpoint}", headers=headers)
        res = conn.getresponse()

        if res.status == 200:
            data = res.read().decode("utf-8")
            conn.close()
            return data
        else:
            print(f"Error: {res.status} - {res.reason}")
    except http.client.HTTPException as e:
        print(f"HTTP Exception occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    conn.close()
    return ""


def save_data_as_json(data: dict, file_path: str) -> None:
    """
    Saves data as JSON in a specified file.

    Args:
        data (dict): The JSON-serializable data to be saved.
        file_path (str): The file path (including the filename and .json extension) where the JSON data will be saved.
    """
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file)
    except (IOError, OSError) as e:
        raise Exception(f"Error writing to file: {e}")


def api_to_json(endpoint: str, file_name:str = None, return_json = False) -> Optional[dict]:
    """
    Fetches data from the API and saves it as a JSON file.

    Args:
        endpoint (str): The API endpoint to query.
    """
    try:
        endpoint_data = fetch_data_from_api(endpoint)

        if return_json:
            return_value = json.loads(endpoint_data)
        else:
            return_value = None

        if file_name is None:
            file_name = endpoint
        file_path = f"./data/raw_data/json_files/{file_name}.json"
        save_data_as_json(data=endpoint_data, file_path=file_path)
    except Exception as e:
        print(f"An error occurred: {e}")

    return return_value
