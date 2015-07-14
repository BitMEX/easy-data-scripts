import argparse
import getpass
import json
import csv
from os import path
from lib import bitmex

parser = argparse.ArgumentParser(description='Fetch your full trade history from BitMEX.')
parser.add_argument('--user', type=str, required=True,
                    help='BitMEX account email address.')
parser.add_argument('--out', type=str, required=True,
                    help='Output file location. Must end with .json or .csv.')
parser.add_argument('--password', type=str,
                    help='Password. If not provided here, will be prompted.')
parser.add_argument('--otpToken', type=str,
                    help='OTP Token (Google Authenticator), if enabled.')

args = parser.parse_args()

extension = path.splitext(args.out)[1][1:].lower()
if extension != 'json' and extension != 'csv':
  print extension
  raise Exception('Output file extension must be json or csv!')

if not args.password:
  args.password = getpass.getpass()

# Create connector
connector = bitmex.BitMEX(base_url="https://www.bitmex.com/api/v1/", login=args.user,
                          password=args.password, otpToken=args.otpToken)

# Log in
connector.authenticate()

# Do trade history query
count = 500 # max API will allow
query = {
    'reverse': True,
    'start': 0,
    'count': count
}
out = []
outStr = ''
while True:
  data = connector._curl_bitmex(api="execution/tradeHistory", verb="GET", query=query, timeout=10)
  out.extend(data)
  query['start'] += count
  if len(data) < count:
    break

# Write to file
with open(args.out, 'w+') as outfile:

  if extension == 'csv':
    # csv requires dict keys
    keys = out[0].keys()
    keys.sort()
    csvwriter = csv.DictWriter(outfile, fieldnames=keys)
    csvwriter.writeheader()
    csvwriter.writerows(out)
  elif extension == 'json':
    outfile.write(json.dumps(out, sort_keys=True, indent=4, separators=(',', ': ')))
  else:
    raise Exception('Unknown output file type.')

print "Wrote %d results to %s." % (len(out), args.out)
