import requests

from Backend.App.Utils.session_helper import Statuses, log_and_message_response

ANYPOINT_URL = 'http://localhost:8081/singularity'
weather_api_key = 'ddaeb0832cd3342dcdb78c9eab711418'
news_api_key = '9faef6573bb046a6b5da9cd04cfcc0b4'

def get_weather_and_news_data(city, country, country_code):

    if not city or not country:
        return log_and_message_response("Missing City or Country", Statuses.BAD_REQUEST)

    payload = {
        "q": f'{city},{country_code}',
        "weatherapikey": weather_api_key,
        "units": "metric",
        "q2": country,
        "newsapikey": news_api_key
    }

    try:
        response = requests.post(ANYPOINT_URL, json=payload, timeout=5)
        response.raise_for_status()
        return response.json(), Statuses.OK
    except requests.exceptions.HTTPError as e:
        return log_and_message_response("Anypoint returned an error", Statuses.BAD_REQUEST, "error", e)
    except requests.exceptions.RequestException as e:
        return log_and_message_response("Failed to connect to Anypoint endpoint", Statuses.BAD_REQUEST, "error", e)