import argparse
import json
import csv
import sys
import time
from lib import bitmex
from settings import API_BASE

parser = argparse.ArgumentParser(description='Fetch trade history from BitMEX.')
parser.add_argument('--path',    type=str, help='Path')
parser.add_argument('--symbol',  type=str, help='Symbol filter.')
parser.add_argument('--filter',  type=str, help='Query filter as JSON.')
parser.add_argument('--binSize', type=str, help='Bin Size.')
parser.add_argument('--sleep', type=float, help='Sleep time for big requests.')

args = parser.parse_args()

# Validate Args
if args.filter:
    # Verify if it's proper JSON
    try:
        json.loads(args.filter)
    except ValueError as e:
        raise ValueError("Filter is not valid JSON! Make sure to single-quote the string.")

# Create connector
connector = bitmex.BitMEX(base_url=API_BASE)

# Do trade history query
path = "trade"
if args.path:
    path = args.path
count = 500  # max API will allow
query = {
    'reverse': 'false',
    'start': 0,
    'count': count,
    'filter': args.filter
}
if args.symbol:
    query['symbol'] = args.symbol
if args.binSize:
    query['binSize'] = args.binSize

csvwriter = None

while True:
    data = connector._curl_bitmex(path=path, verb="GET", query=query, timeout=10)
    if args.sleep:
        time.sleep(args.sleep)
    if csvwriter is None:
        # csv requires dict keys
        if len(data) == 0:
            break
        keys = data[0].keys()
        keys.sort()
        # Write to stdout
        csvwriter = csv.DictWriter(sys.stdout, fieldnames=keys)
        csvwriter.writeheader()

    csvwriter.writerows(data)

    query['start'] += count
    if len(data) < count:
        break

