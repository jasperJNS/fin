import time
from datetime import datetime
import pickle
import pprint as pp
import pandas as pd
import json
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

    params = {
        'symbol': 'QQQ',
        'opt_range': 'all'
    }

    qqq = Fin(session, params)
    data = qqq.get_data()

    
    with open('qqq_options.pkl', 'wb') as f:
        pickle.dump(data, f)

def read_pickle():
    with open('qqq_options.pkl', 'rb') as f:
        data = pickle.load(f)
    options = data['options']
    dates = data['dates']

    finData = data['finData']
    underlying = finData['underlying']
    vol = finData['vol']
    totalContracts = finData['totalNumContracts']

    quote = data['quote']
    print('quote:')
    for k, v in quote.items():
        print(k, v)

    # print('underlying: ', underlying)
    # print('vol: ', vol)
    # print('totalContracts: ', totalContracts)



    deltas = set()
    d = dates[1]
    opt = options[d]

    deltaLimit = 0.1
    minDeltaCalls = 0.5 - deltaLimit
    maxDeltaCalls = 0.5 + deltaLimit

    # getting calls within 30 delta
    for calls in opt:
        delt = calls.delta
        if delt >= minDeltaCalls and delt <= maxDeltaCalls:
            print(calls)

    minDeltaPuts = -minDeltaCalls
    maxDeltaPuts = -maxDeltaCalls

    # getting puts within -30 delta
    for puts in opt:
        delt = puts.delta
        if delt <= minDeltaPuts and delt >= maxDeltaPuts:
            print(puts)




def set_fin_object():
    session = login()
    qqq = Fin()
    qqq.read_data('nio_all_dates_3_22')
    nio.set_session(session)

    nio.get_thirty_day_chart()



if __name__ == '__main__':
    read_pickle()
    
    # with open('baba_reg_news.json', 'w') as f:
    #     json.dump(headline, f, indent=4)

    # s = Search()

    # eq = s.show_options('equities') 
    # pp.pprint(eq, indent=4)