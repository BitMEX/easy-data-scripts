# easy-data-scripts
A few Python scripts to easily get data from the BitMEX API.

This is a work in progress and will grow to a more modular library.

### Get Started

```bash
git clone git@github.com:BitMEX/easy-data-scripts.git
cd easy-data-scripts
python setup.py install
# View help
python fetchTradeHistory.py -h
# Generate CSV
python fetchTradeHistory.py --user email@email.com --out records.csv
# Generate JSON
python fetchTradeHistory.py --user email@email.com --out records.json
# Filter results to a single contract
python fetchTradeHistory.py --user email@email.com --out records.csv --filter='{"symbol": "XBT24H"}'
```
