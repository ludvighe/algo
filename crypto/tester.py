import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json

import shrimpy_api.shrimpy_api as shrimpy
import consts.secrets as secrets

# Load settings
with open('crypto/crypto_settings.json', 'r', encoding='utf8') as f:
    global settings
    settings = json.load(f)


# SHRIMPY

def test_shrimpy():
    days_ago_7 = (datetime.now() - timedelta(days=7)).isoformat().split('.')[0]
    response = shrimpy.fetch_candles(symbol='BTC', interval='1D', startTime=days_ago_7)#'2021-02-02T00:00:00.000Z')
    print(pd.DataFrame.from_dict(response.json(), orient='columns'))

def test_shrimpy_mock():
    # shrimpy.write_to_mock_data()
    # print('If this fails check if destination json uses \" and not \'')
    # response = shrimpy.fetch_market_data()
    # df = pd.DataFrame.from_dict(response.json(), orient='columns')

    # shrimpy.write_mock_candles(settings['supported_tokens'])
    # data = shrimpy.fetch_mock_candles('BTC')
    # df = pd.DataFrame.from_dict(data, orient='columns')
    print(df)


test_shrimpy()
# test_shrimpy_mock()
