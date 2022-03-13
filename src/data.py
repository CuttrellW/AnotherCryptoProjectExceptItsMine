import requests
import json
import yaml
import pandas as pd

from scaler import Scaler

CONFIG_PATH = 'config/default.yaml'


# Load YAML spec file
def load_config_file(filename):
    with open(filename, 'r') as stream:
        try:
            parsed_yaml = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return parsed_yaml


# Load api key (not included in public repository - create your free key at https://www.alphavantage.co/support/#api-key)
def load_apikey():
    with open('../key.json') as stream:
        data = json.load(stream)

    return data['apikey']


# Get price data from Alpha Vantage
def get_price_data():

    specs = load_config_file(CONFIG_PATH)

    price_data_params = specs['priceData']
    symbol = price_data_params['symbol']
    market = price_data_params['market']
    interval = price_data_params['interval']
    outputsize = price_data_params['outputsize']

    apikey = load_apikey()

    url = f'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol={symbol}&market={market}&interval={interval}&outputsize={outputsize}&apikey={apikey}'
    r = requests.get(url).json()
    data = r[f'Time Series Crypto ({interval})']

    return data


if __name__ == '__main__':
    price_data_list = []
    price_data = get_price_data()

    # Format raw data for data frame
    for interval in price_data:
        price = float(price_data[interval]['1. open'])
        price_data_list.append({"time": interval, "price": price})

    # Create dataframe
    df = pd.DataFrame(price_data_list)

    # Add column for scaled price data
    scaled_data = Scaler(df["price"]).min_max_scale()
    df['scale'] = scaled_data

    print(df)

