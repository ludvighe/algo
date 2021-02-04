import numpy as np
import pandas as pd
import datetime
import json
import statistics
from datetime import datetime, timedelta
import time
from colorama import Fore, Back, Style 

import shrimpy_api.shrimpy_api as shrimpy

# Load settings
with open('crypto/crypto_settings.json', 'r', encoding='utf8') as f:
    global settings
    settings = json.load(f)


def fetch_market_data():
    print('\nFetching market data from Shrimpy...')
    response = shrimpy.fetch_market_data()
    data = response.json()

    if response.ok:  # response == 200
        print('Success!')
        return data
    else:
        print(f'\nFailed to fetch market data from Shrimpy. \nResponse: {data}\nExiting.')
        exit()


def fetch_mock_market_data():
    print(f'\nFetching mock market data...')
    return shrimpy.fetch_mock_market_data()


# Fetch market data
data = {}
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
    for i, symbol in enumerate(df.index): # remove [:5] to include all
        print(
            f'Fetching candles for {symbol} since {candleStartTime} and calculating mean...\t({i+1} / {len(df)})')
        try:
            if settings['test']:
                candle = shrimpy.fetch_mock_candles(symbol=symbol)
            else:
                while True:
                    candle = shrimpy.fetch_candles(
                        symbol=symbol, startTime=candleStartTime).json()
    
                    if 'error' in candle:
                        print(Fore.RED + f'Candle data for {symbol} contains an error. This might be because shrimpy\'s rate limit is reached.' + Fore.RESET)
                        print('Sleeping for 30 seconds and retrying...')
                        for x in range(30):
                            s = 'Sleeping' + '.' * (x % 4) + f'\tRetrying in {30 - x} seconds.'
                            print (s, end='\r')
                            time.sleep(1)
                    else:
                        break
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
        except:
            print(Fore.RED + f'Failed to parse candle for {symbol}. This might be because shrimpy\'s rate limit is reached.' + Fore.RESET)
            print(f'Response: {candle}')
            exit()

        try:
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
        except:
            print(Fore.RED + f'Failed to calculate mean of candle for {symbol}.' + Fore.RESET)
            print(f'Response: {means}')
            exit()
    mean_df.set_index('symbol', inplace=True)
    return mean_df

# Appending mean column to df
df['mean7Day'] = calculate_mean()['mean7Day']


# TODO: Decision making

print(df)
