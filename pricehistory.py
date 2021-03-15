import requests
import json
import pandas as pd
from epochdate import epoch_to_date

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

def get_price_history(ticker, apikey):
    '''
        @params: stock ticker
        @return: historical equity price

        frame keys:
                'candles',
                'symbol',
                'empty'
    '''
    #top movers
    url = f"https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory"
    params = {
        'apikey': apikey
    }
    r = requests.get(url=url, params=params)
    resp = r.json()

    resp_df = pd.DataFrame.from_dict(resp)

    df = resp_df['candles'].apply(pd.Series)
    df['datetime'] = df.apply(lambda row: epoch_to_date(row['datetime']), axis=1)
    return df

