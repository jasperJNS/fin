from config.config import apikey
from pricehistory import get_price_history
from optionchain import get_option_chain

import requests
import json
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

ticker = 'EBON'

priceHistory_df = get_price_history(ticker, apikey)
print(priceHistory_df.head())
print(priceHistory_df.tail())
print(priceHistory_df.shape)

# options = get_option_chain(ticker, apikey)

# print(options.head())
# print(options.shape)
# print(options['numberOfContracts'])