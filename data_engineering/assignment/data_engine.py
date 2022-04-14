from file_reader import Duplicate_finder #read_jsonl, _get_df_with_duplicates, _get_key_column, df_to_list
import logging
import json
import argparse
import os
from assignment import config

parser = argparse.ArgumentParser(description="Find duplicate listings")
parser.add_argument("--input", "-i", default="files\\", help="Location to read JSONL files from")
parser.add_argument("--output", "-o", default="output\\result.json", help="Location to save the result JSON")
parser.add_argument("--verbose", "-v", action=argparse.BooleanOptionalAction, help="Enable debug logs")
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)



duplicate_finder = Duplicate_finder(args.input, config.key_columns)


final_list= duplicate_finder.df_to_list()

logging.info('storing duplicate list')
with open(args.output, "w") as fp:
        json.dump(final_list, fp, indent=4)









