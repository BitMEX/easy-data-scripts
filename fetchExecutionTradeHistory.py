import argparse
import json
import csv
import sys
from lib import bitmex
from settings import API_KEY, API_SECRET, API_BASE

parser = argparse.ArgumentParser(description='Fetch your full execution trade history from BitMEX.')
parser.add_argument('--apiKey', type=str, required=(not API_KEY), default=API_KEY,
                    help='API Key. Generate from https://www.bitmex.com/app/apiKeys')
parser.add_argument('--apiSecret', type=str, required=(not API_SECRET), default=API_SECRET,
                    help='API Secret.')
parser.add_argument('--fileType', type=str, default='csv',
                    help='Output file type. Must end be json or csv.')
parser.add_argument('--filter', type=str,
                    help='Query filter as JSON.')

args = parser.parse_args()

# Validate Args
fileType = args.fileType
if fileType != 'json' and fileType != 'csv':
    raise Exception('Output file type must be json or csv! Given: %s' % fileType)

if not args.apiKey or not args.apiSecret:
    print('Please fill in API_KEY and API_SECRET in settings.py!\n' +
          'You can create an API key from https://www.bitmex.com/app/apiKeys')
    sys.exit(1)

if(args.filter):
    # Verify if it's proper JSON
    try:
        json.loads(args.filter)
    except ValueError as e:
        raise ValueError("Filter is not valid JSON! Make sure to single-quote the string.")

# Create connector
connector = bitmex.BitMEX(base_url=API_BASE, apiKey=args.apiKey, apiSecret=args.apiSecret)

# Do trade history query
count = 500  # max API will allow
query = {
    'reverse': 'true',
    'start': 0,
    'count': count,
    'filter': args.filter
}

out = []
while True:
    data = connector._curl_bitmex(path="execution/tradeHistory", verb="GET", query=query, timeout=10)
    out.extend(data)
    query['start'] += count
    if len(data) < count:
        break

# Write to stdout
if fileType == 'csv':
    # csv requires dict keys
    keys = out[0].keys()
    keys.sort()
    csvwriter = csv.DictWriter(sys.stdout, fieldnames=keys)
    csvwriter.writeheader()
    csvwriter.writerows(out)
elif fileType == 'json':
    print(json.dumps(out, sort_keys=True, indent=4, separators=(',', ': ')))
else:
    # Shouldn't happen
    raise Exception('Unknown output file type.')
