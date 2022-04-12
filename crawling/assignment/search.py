import json
import logging
import requests
import time

from assignment.auth import ImmoweltAccessToken
from assignment import config

def search_listings():
    access_token = ImmoweltAccessToken()

    offset = 0
    count = float("inf")
    page_size = 1000
    url = "https://api.immowelt.com/estatesearch/EstateSearch/v1/Search"

    items = []

    while offset < count:
        logging.info(f"{offset}/{count}")

        payload = json.dumps(
            {
                "construction": {},
                "general": {
                    "category": [],
                    "distributionType": config.distribution_type,
                    "equipment": [],
                    "estateType": config.estate_types,
                },
                "location": {"geo": {"locationId": config.location_ids}},
                "offset": offset,
                "pagesize": page_size,
                "pricing": {},
                "sort": "SortByCreateDate",
            }
        )

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {access_token.token}",
        }

        response = requests.request(
            "POST", url, headers=headers, data=payload
        ).json()

        count = int(response["count"])
        offset = int(response["offset"]) + page_size
        items += response["items"]
        #time.sleep(5)

    return items
