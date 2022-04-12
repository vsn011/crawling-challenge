import argparse
import json
import logging
import os
import requests
import time

from assignment import config
from assignment.auth import ImmoweltAccessToken

parser = argparse.ArgumentParser(description="Scrape Immowelt API")
parser.add_argument("--verbose", "-v", action=argparse.BooleanOptionalAction, help="Enable debug logs")
parser.add_argument("--schedule", "-s", type=int, help="Scrape schedule in seconds")
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

if args.schedule:
    while True:
        start_time = time.time()

        logging.info("doing something that takes 3 seconds")
        time.sleep(3)

        time.sleep(args.schedule - ((time.time() - start_time) % args.schedule))

else:
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
        time.sleep(5)

    with open("result.json", "w") as fp:
        json.dump(items, fp, indent=4)
