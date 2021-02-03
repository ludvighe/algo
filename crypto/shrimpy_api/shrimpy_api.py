import pandas as pd
import requests
import shrimpy
import json

default_exchange = 'coinbasepro'  # TODO: Make setting
mock_directory = 'crypto/data/mock/'


# Fetches market data of all tokens supported by given exchange
def fetch_market_data(exchange=default_exchange):
    return requests.get(f'https://dev-api.shrimpy.io/v1/exchanges/{exchange}/ticker')
    """ 
    EXAMPLE OUTPUT
    [
        {
            "name": "Ethereum",
            "symbol": "ETH",
            "priceUsd": "100.114205389399",
            "priceBtc": "0.027057825",
            "percentChange24hUsd": "5.432113558652999",
            "lastUpdated": "2018-12-19T22:51:13.000Z"
        },
    ]
    """


# Fetches candles (historical market data) of given symbol (token)
def fetch_candles(symbol, exchange=default_exchange, interval='1D', startTime='2021-01-26T00:00:00.000Z'):
    return requests.get(f'https://dev-api.shrimpy.io/v1/exchanges/{exchange}/candles?quoteTradingSymbol=USD&baseTradingSymbol={symbol}&interval={interval}&startTime={startTime}')
    # https://dev-api.shrimpy.io/v1/exchanges/coinbasepro/candles?quoteTradingSymbol=USD&baseTradingSymbol=BTC&interval=1D&startTime=2021-01-26T00:00:00.000Z

    """
    baseTradingSymbol:      string  = The base symbol of a pair on the exchange. (e.g. XLM for a XLM-BTC pair)
    quoteTradingSymbol:     string  = The quote symbol of a pair on the exchange. (e.g. BTC for a XLM-BTC pair)
    interval:               string  = The interval must be one of the following values: 1m, 5m, 15m, 1h, 6h, or 1d)
                                      These values correspond to intervals representing one minute, five minutes,
                                      fifteen minutes, one hour, six hours, and one day, respectively.
    startTime (optional):   Date    = Optionally only return data on or after the supplied startTime (inclusive).

    EXAMPLE OUTPUT
    [
        {
            "open": "32260.5200000000000000", 
            "high": "32960.3700000000000000", 
            "low": "30830.0000000000000000", 
            "close": "32510.8200000000000000", 
            "volume": "23535.8389168800000000", 
            "quoteVolume": 752630885.9925821, 
            "btcVolume": 23533.476195010626, 
            "usdVolume": 752630885.9925821, 
            "time": "2021-01-26T00:00:00.000Z"
        }, 
        ...
    ]
    """


# MOCK FUNCTIONS (for testing purposes)

def write_to_mock_data():  # .json
    # Note that JSON will use ' instead of " which python json doesn't like
    with open(f'{mock_directory}mock_market_data.json', 'w', encoding='utf8') as f:
        f.write(str(fetch_market_data().json()).replace('\'', '\"'))


def fetch_mock_market_data():
    with open(f'{mock_directory}mock_market_data.json', 'r', encoding='utf8') as f:
        return json.load(f)


def write_mock_candles(symbols):
    symbols = symbols[:5]
    mock_candles = dict().fromkeys(symbols)
    for i, symbol in enumerate(symbols):
        print(
            f'Fetching candles for {symbol} and calculating mean...\t({i+1} / {len(symbols)})')
        candle = fetch_candles(symbol=symbol).json()
        mock_candles[symbol] = candle
        with open(f'{mock_directory}mock_candles.json', 'w', encoding='utf8') as f:
            f.write(str(mock_candles).replace('\'', '\"'))


def fetch_mock_candles(symbol):
    with open(f'{mock_directory}mock_candles.json', 'r', encoding='utf8') as f:
        data = json.load(f)
        return data[symbol]
