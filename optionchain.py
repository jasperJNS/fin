import requests
import json
import pandas as pd
from epochdate import epoch_to_date

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

def get_option_chain(ticker, apikey):
    '''
        @params: stock ticker
        @return: option chain

        
    '''
    #top movers
    url = "https://api.tdameritrade.com/v1/marketdata/chains"

    contractType = 'ALL'
    includeQuotes = 'TRUE'
    strategy = 'SINGLE'
    interval = '1'
    strikeRange = 'ALL'
    expiryMonth = 'ALL'
    optionType = 'ALL'

    params = {
        'apikey': apikey,
        'symbol': ticker,
        'contractType': contractType,
        'includeQuotes': includeQuotes,
        'strategy': strategy,
        'interval': interval,
        'range': strikeRange,
        'expMonth': expiryMonth,
        'optionType': optionType
    }
    r = requests.get(url=url, params=params)
    resp = r.json()

    resp_df = pd.DataFrame.from_dict(resp)

    return resp_df

