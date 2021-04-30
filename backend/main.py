import time
from datetime import datetime
import pickle
import pprint as pp
import pandas as pd
import json
import math
from pathlib import Path

from config.config import NEWSAPI_KEY
pd.set_option('display.max_columns', None)

from login import login
from Fin import Fin
from Search import Search


def main_test():
    session = login()

    params = {
        'symbol': 'GME',
        'opt_range': 'all'
    }

    gme = Fin(session, params)

    # set from session object
    # data = nio.get_data()
    # nio.get_thirty_day_chart()

    #get news
    # gme_news = gme.get_news(NEWSAPI_KEY)

   

    
    return

def pickle_data():
    session = login()

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


# if __name__ == '__main__':
#     # read_pickle()
#     # pickle_data()
#     set_fin_object()
    