import requests
from flask import current_app


def get_latest_rates(app_id: str) -> dict:
    url = f'https://openexchangerates.org/api/latest.json'
    response = requests.get(url, params={
        'app_id': app_id,
    })
    response.raise_for_status()
    response_json = response.json()
    current_app.logger.info(f'Response body: {response_json}')
    return response_json
