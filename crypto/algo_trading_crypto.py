import numpy as np
import pandas as pd
import datetime
import json
import statistics
from datetime import datetime, timedelta

import shrimpy_api.shrimpy_api as shrimpy

# Load settings
with open('crypto/crypto_settings.json', 'r', encoding='utf8') as f:
    global settings
    settings = json.load(f)


def fetch_market_data():
    print('\nFetching market data from Shrimpy...')
    response = shrimpy.fetch_market_data()
    global data
    data = response.json()

    if response.ok:  # response == 200
        print('Success')
    else:
        print('\nFailed to fetch market data from Shrimpy. Exiting.')
        exit()


def fetch_mock_market_data():
    print(f'\nFetching mock market data...')
    return shrimpy.fetch_mock_market_data()


# Fetch market data
global data
if settings['test']:
    data = fetch_mock_market_data()
else:
    data = fetch_market_data()


# Creation of DataFrame
df = pd.DataFrame.from_dict(data, orient='columns')
df.set_index('symbol', inplace=True)
df = df.loc[settings['supported_tokens']]


# Calculate mean
def calculate_mean():
    mean_df = pd.DataFrame(columns=['symbol', 'mean7Day'])

    candleStartTime = (datetime.now() - timedelta(days=7)
                       ).isoformat().split('.')[0]  # 7 days ago from now
    for i, symbol in enumerate(df.index[:5]):
        print(
            f'Fetching candles for {symbol} since {candleStartTime} and calculating mean... ({i+1} / {len(df)})')
        if settings['test']:
            candle = shrimpy.fetch_mock_candles(symbol=symbol)
        else:
            candle = shrimpy.fetch_candles(
                symbol=symbol, startTime=candleStartTime).json()
        means = []
        for entry in candle:
            means.append(statistics.mean(
                [
                    float(entry['open']),
                    float(entry['high']),
                    float(entry['low']),
                    float(entry['close'])
                ]
            ))
        mean_df = mean_df.append(
            pd.Series(
                [
                    symbol,
                    statistics.mean(means)
                ],
                index=['symbol', 'mean7Day']
            ),
            ignore_index=True
        )
    print(mean_df)


calculate_mean()
# print(df)
