import argparse
import json
import logging
import os
import pymongo
import requests
import signal
import time

from assignment.search import search_listings

keep_runing = True

def exit_gracefully():
    logging.info("exitting gracefully")
    keep_running = False

signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)
signal.signal(signal.SIGHUP, exit_gracefully)

parser = argparse.ArgumentParser(description="Scrape Immowelt API")
parser.add_argument("--output", "-o", help="Location to save the result JSON")
parser.add_argument("--verbose", "-v", action=argparse.BooleanOptionalAction, help="Enable debug logs")
parser.add_argument("--schedule", "-s", type=int, help="Scrape schedule in seconds")
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

if args.schedule:
    client = pymongo.MongoClient("mongodb://root:example@mongo:27017/")
    db = client["crawling"]
    collection = db["EstateSearch"]

    while True:
        start_time = time.time()

        items = search_listings()

        # Write to Mongo
        collection.insert_one(items)

        time.sleep(args.schedule - ((time.time() - start_time) % args.schedule))

else:
    # Call search part
    items = search_listings()

    with open(args.output, "w") as fp:
        json.dump(items, fp, indent=4)
