import json
import logging
import os
import requests


class ImmoweltAccessToken:
    """Class for keeping track of the access token."""

    def __init__(self):
        url = "https://api.immowelt.com/auth/oauth/token"
        payload = {"grant_type": "client_credentials"}
        headers = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=utf-8",
            "authorization": f'Basic {os.getenv("IMMOWELT_KEY")}',
        }

        response_json = requests.request(
            "POST", url, headers=headers, data=payload
        ).json()

        try:
            self.token = response_json["access_token"]
            self.expires_in = response_json["expires_in"]
        except KeyError:
            logging.error(response_json)

        logging.info(f"access token expires in {self.expires_in}")
