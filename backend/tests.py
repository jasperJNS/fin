import time
from datetime import datetime, timedelta
import pickle
import pprint as pp
import pandas as pd
import json
import math
from pathlib import Path

from backend.config import config
NEWSAPI_KEY = config.NEWSAPI_KEY
pd.set_option('display.max_columns', None)

from backend.login import api_login
from backend.Fin import Fin
from backend.Search import Search
from backend.historical import get_history


def get_fin(ticker):
    session = api_login()

    params = {
        'symbol': ticker,
        'opt_range': 'all'
    }

    fin = Fin(session, params)

    data = fin.get_json()

    
    return data

def pickle_data():
    session = api_login()

    symbol = 'QQQ'
    params = {
        'symbol': symbol,
        'opt_range': 'all'
    }

    qqq = Fin(session, params)
    data = qqq.get_data()

    date = datetime.today().timestamp()
    fdate = time.strftime('%Y_%m_%d_%H:%M', time.gmtime(date))
    fdate = symbol + "_" + fdate
    fdir = Path.cwd() / 'backend/data' 
    with open('%s/%s'%(fdir, fdate), 'wb') as f:
        pickle.dump(data, f)

def read_pickle():
    fdir = Path.cwd() / 'backend/data/' 
    with open('%s/QQQ_2021_04_16_17:35'%fdir, 'rb') as f:
        data = pickle.load(f)
    

    # print('for date: ', d)
    # # getting calls within 30 delta
    # for calls in new_opt:
    #     delt = calls.delta
    #     if delt >= minDeltaCalls and delt <= maxDeltaCalls:
    #         print(calls)

    # minDeltaPuts = -minDeltaCalls
    # maxDeltaPuts = -maxDeltaCalls

    # # getting puts within -30 delta
    # for puts in new_opt:
    #     delt = puts.delta
    #     if delt <= minDeltaPuts and delt >= maxDeltaPuts:
    #         print(puts)




def set_fin_object():

    fname = 'QQQ_2021_04_15_18:02'
    ticker = Fin()
    ticker.read_data(fname)

    
    ticker.get_options_by_delta(1, 0.4)

    callGamma, putGamma = ticker.calculate_net_gamma()
    print(callGamma/putGamma)


def get_hist(ticker, num_days, shift_date: int=0):
    session = api_login()

    params = {
        'symbol': ticker,
        'opt_range': 'all'
    }

    fin = Fin(session, params)
    vol_params = {
        'periodCount': num_days, # 3-month period
        'periodType': 'month',
        'candleSize': 'daily',
        'candleTick': 1,
        'endDate': datetime.now() - timedelta(days=shift_date),
        'scale': 252 # trading days in year
    }

    return fin.get_historical_volatility(vol_params=vol_params)



# data = get_fin('QQQ')

# x = json.loads(data)
# print()