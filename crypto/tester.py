import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import time
import math
import statistics

import shrimpy_api.shrimpy_api as shrimpy


def general():
    for x in range(30):
        s = 'Sleeping' + '.' * (x % 4) + f'\tRetrying in {30 - x} seconds.'
        print(s, end='\r')
        time.sleep(1)


# Load settings
with open('crypto/crypto_settings.json', 'r', encoding='utf8') as f:
    global settings
    settings = json.load(f)


# SHRIMPY

def test_shrimpy():
    days_ago_7 = (datetime.now() - timedelta(days=7)).isoformat().split('.')[0]
    response = shrimpy.fetch_candles(
        symbol='BTC', interval='1D', startTime=days_ago_7)
    print(pd.DataFrame.from_dict(response.json(), orient='columns'))


def test_shrimpy_mock():
    # shrimpy.write_to_mock_data()
    # print('If this fails check if destination json uses \" and not \'')
    # response = shrimpy.fetch_market_data()
    # df = pd.DataFrame.from_dict(response.json(), orient='columns')

    # shrimpy.write_mock_candles(settings['supported_tokens'])
    # data = shrimpy.fetch_mock_candles('BTC')
    # df = pd.DataFrame.from_dict(data, orient='columns')
    # print(df)
    pass

# Sorry about the mess
def test_support_resistance():
    symbol = 'BTC'
    df = pd.DataFrame.from_dict(
        shrimpy.fetch_candles(symbol, interval='1H', startTime=datetime.now() - timedelta(days=7) * 2).json(), orient='columns')
    df = df.head(math.floor(len(df) / 2))
    print(df)

    total_mean = []  # mean totals of open, close, high and low
    highs = []  # all entries in column high
    lows = []  # all entries in column low

    for index, row in df.iterrows():
        total_mean.append(
            statistics.mean(
                [
                    float(row['open']),
                    float(row['close']),
                    float(row['high']),
                    float(row['low'])
                ]
            )
        )
        highs.append(float(row['high']))
        lows.append(float(row['low']))

    def confidence_interval(data):
        z = 1.96  # confidence_level
        x = statistics.mean(data)  # sample_mean
        n = len(data)  # sample_size
        standard_error = statistics.stdev(data) / statistics.sqrt(n)
        return [x + z * standard_error, x - z * standard_error]  # [high, low]

    def breakthrough(resistance, support):
        r = []  # Resistance breakthrough
        s = []  # Support breakthrough

        for index, row in df.iterrows():
            if float(row['high']) > resistance:
                r.append(row['time'])
            if float(row['low']) < support:
                s.append(row['time'])
        return {
            'resistance': r,
            'support': s
        }

    # Confidence Intervals
    resistance_ci = confidence_interval(highs)
    support_ci = confidence_interval(lows)
    total_ci = confidence_interval(total_mean)

    # Breakthroughs
    breakthroughs = breakthrough(resistance_ci[0], support_ci[1])

    print(
        f'{symbol} Resistance:\nHigh: {resistance_ci[0]}\tLow: {resistance_ci[1]}')
    print(f'{symbol} Support:\nHigh: {support_ci[0]}\tLow: {support_ci[1]}')
    print(
        f'{symbol} Total confidence interval:\nHigh: {total_ci[0]}\tLow: {total_ci[1]}')

    # r = breakthroughs['resistance']
    # s = breakthroughs['support']
    # print(f'{symbol} Breakthroughs:\nResistance: {r}\nSupport: {s}')

# general()
# test_shrimpy()
# test_shrimpy_mock()


test_support_resistance()
