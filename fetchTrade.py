import argparse
import json
import csv
import sys
from lib import bitmex
from settings import API_BASE

parser = argparse.ArgumentParser(description='Fetch trade history from BitMEX.')
parser.add_argument('--filter', type=str,
                    help='Query filter as JSON.')

args = parser.parse_args()

# Validate Args
if(args.filter):
    # Verify if it's proper JSON
    try:
        json.loads(args.filter)
    except ValueError as e:
        raise ValueError("Filter is not valid JSON! Make sure to single-quote the string.")

# Create connector
connector = bitmex.BitMEX(base_url=API_BASE)

# Do trade history query
count = 500  # max API will allow
query = {
    'reverse': 'false',
    'start': 0,
    'count': count,
    'filter': args.filter
}

header = False

while True:
    data = connector._curl_bitmex(path="trade", verb="GET", query=query, timeout=10)

    # Write to stdout
    # csv requires dict keys
    keys = data[0].keys()
    keys.sort()
    csvwriter = csv.DictWriter(sys.stdout, fieldnames=keys)
    if not header:
        csvwriter.writeheader()
        header = True
    csvwriter.writerows(data)

    query['start'] += count
    if len(data) < count:
        break

