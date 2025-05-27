import json

import requests

from Backend.App.Utils.session_helper import Statuses, log_and_message_response

CAMUNDA_URL = 'http://localhost:8080/engine-rest/process-definition/key/Process_14g9x09/start?withVariablesInReturn=true'
WEATHER_API_KEY = 'ddaeb0832cd3342dcdb78c9eab711418'
NEWS_API_KEY = '9faef6573bb046a6b5da9cd04cfcc0b4'

def start_camunda(city, country, country_code):

    if not city or not country:
        return log_and_message_response("Missing City or Country", Statuses.BAD_REQUEST)

    payload_data = {
        "q": f"{city},{country_code}",
        "weatherapikey": WEATHER_API_KEY,
        "units": "metric",
        "q2": country,
        "newsapikey": NEWS_API_KEY
    }

    camunda_payload = {
        "variables": {
            "payload": {
                "value": json.dumps(payload_data),
                "type": "String"
            }
        }
    }

    try:
        response = requests.post(CAMUNDA_URL, json=camunda_payload, timeout=5)
        response.raise_for_status()
        return response.json(), Statuses.OK
    except requests.exceptions.HTTPError as e:
        return log_and_message_response("Anypoint returned an error", Statuses.BAD_REQUEST, "error", e)
    except requests.exceptions.RequestException as e:
        return log_and_message_response("Failed to connect to Anypoint endpoint", Statuses.BAD_REQUEST, "error", e)