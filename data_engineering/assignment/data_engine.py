from file_reader import read_jsonl, _get_df_with_duplicates, _get_key_column, df_to_list
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


df = read_jsonl(args.input)


logging.info('finding duplicate listings')
df_d = _get_df_with_duplicates(df, config.key_columns)


logging.info('creating list of duplicates')
final_list=df_to_list(df_d, config.key_columns)


logging.info('storing duplicate list')
with open(args.output, "w") as fp:
        json.dump(final_list, fp, indent=4)









