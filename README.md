# easy-data-scripts
A few Python scripts to easily get data from the BitMEX API.


### Get Started

[Generate an API Key](https://www.bitmex.com/app/apiKeys). This is required for all scripted
interaction with BitMEX.

```bash
git clone git@github.com:BitMEX/easy-data-scripts.git
cd easy-data-scripts
python setup.py install
#
# Important! Edit settings.py to add your API_KEY and API_SECRET.
#

# Using the script:

# View help
python fetchTradeHistory.py -h
# Print CSV results to stdout
python fetchTradeHistory.py
# Generate CSV file
python fetchTradeHistory.py > records.csv
# Generate JSON file
python fetchTradeHistory.py --fileType json > records.json
# Filter results to a single contract
python fetchTradeHistory.py --filter='{"symbol": "XBTUSD"}' > records.csv
```
