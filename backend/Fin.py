import pickle
from pathlib import Path
import time
import pprint as pp
from datetime import datetime, timedelta
import math

import pandas as pd
import numpy as np
import requests
from newsapi import NewsApiClient


from CallPut import CallPut

class Fin:
    def __init__(self, session=None, opt_params: dict = {}):
        '''
            Primary object for handling stock queries for historical and options data
        '''
        self.session = session
        self.opt_params = opt_params
        self.data = {} #holds everything, for pickling

        self.symbol = None

        self.newsQueryArticles = []
        self.sector = []
        self.category = None #growth or value

        self.underlying = None
        self.nope = None
        self.nopeMAD = None
        
        self.vol = None # needs to be computed as aggregate of IV of all option strikes
        self.totalNumContracts = None
        self.totalVolume = None
        
        self.deltas = np.arange(-0.001, 0.999, 0.001)


        if session is not None and opt_params is not None:
            self._optchain = session.get_options_chain(option_chain=opt_params)
            self.set_data()
        
    def get_news(self, key, q: list = []):
        '''
            Handles news feed for any searchable topic

            @param q: Option to query for anything, not just stock tickers

            @return:
                q: list = [
                    'source': {
                        'id': id, sometimes null, usually matching name,
                        'name': name of news source, ie Business Insider, etc
                    }
                    'author': author,
                    'title': title,
                    'description': description,
                    'url': url,
                    'urlToImage': url image (icon),
                    'publishedAt': time/date published,
                    'content': first couple sentences, then truncated with number of following chars
                ]
                    
                }
        '''
        
        newsApi = NewsApiClient(api_key=key)
        query = newsApi.get_everything(q=self.symbol, sort_by='popularity')

        if query['status'] == 'ok':
            self.newsQueryArticles = query['articles']
            return self.newsQueryArticles
        else:
            raise FailedNewsException("No news found")

    
    def calculate_nope(self):
        '''
            Net Options Pricing Effect
        '''
        calls = self.data['calls']
        puts = self.data['puts']
        totalVolume = self.totalVolume

        netCallDelta = 0
        netPutDelta = 0

        for call in calls:
            netCallDelta += call.get_net_delta()
        
        for put in puts:
            netPutData += put.get_net_delta()

        #for now using open interest as a proxy for shares traded, but def not accurate
        return (netCallDelta - netPutData) / totalVolume
    
    def calculate_net_gamma(self):
        '''
            Calculate total gamma. Relates to put/call parity.
        '''
        calls = self.data['calls']
        puts = self.data['puts']

        netCallGamma = 0
        netPutGamma = 0

        for call in calls:
            netCallGamma += call.get_net_gamma()
        
        for put in puts:
            netPutGamma += put.get_net_gamma()

        return netCallGamma, netPutGamma

    def get_options_by_delta(self, date: int, deltaRange: float):
        '''
            Get options at date with strikes ranging from ATM(d = 0.5) outward to the delta provided
            @params 
            delta: float range from 0.001 to 0.999 inclusive
            date: int index from nearest to furthest date

            @return:
                list of strikes
        '''
        if deltaRange not in self.deltas:
            raise InvalidDeltaException("Invalid Delta")

        expDate = self.data['dates'][date]

        minDelta = 0.5 - deltaRange
        maxDelta = 0.5 + deltaRange
        
        for callput in self.data['options'][expDate]:
            delt = abs(callput.delta)
            if delt >= minDelta and delt <= maxDelta:
                print("in range: ", callput)
     
    def interpolate_deltas(self):
        '''
            Handles NaN or -999 that occasionally pop up from TDA's API

        '''
    def _get_quote(self):
        instruments = [self.symbol]
        quote = self.session.get_quotes(instruments=instruments)

        return quote[self.symbol]
        

    def set_data(self):
        '''
            Separates pulled option chain into calls, puts, and dates

        '''
        chain = self._get_chain()


        self.symbol = chain['symbol']
        self.underlying = chain['underlyingPrice']
        self.totalNumContracts = chain['numberOfContracts']

        callsMap = chain['callExpDateMap']
        putsMap = chain['putExpDateMap']

        #using the first strike of each expiry date chain to get the date of the chain
        expirationDates = {}
        dates = []
        calls = []
        puts = []

        for days, strikes in callsMap.items():
            for strike, value in strikes.items():
                call = CallPut(dict(value[0].items()))
                calls.append(call)
            
            # date as key
            d = call.get('expirationDate')[:10]
            expirationDates[d] = []

            # maintain list of dates
            dates.append(d)
        
        for days, strikes in putsMap.items():
            for strike, value in strikes.items():
                put = CallPut(dict(value[0].items()))
                puts.append(put)

        for c in calls:
            callDate = c.get('expirationDate')
            if callDate in expirationDates.keys():
                expirationDates[callDate].append(c)

        for p in puts:
            putDate = p.get('expirationDate')
            if putDate in expirationDates.keys():
                expirationDates[putDate].append(p)

        #storing in a dict for general use
        self.data['options'] = expirationDates
        self.data['dates'] = dates

        #separated for NOPE calculations, among others
        self.data['calls'] = calls
        self.data['puts'] = puts

        #retrieve underlying quote as well
        self.data['quote'] = self._get_quote()

        #set underlying data
        self.totalVolume = self.data['quote']['totalVolume']

        self.data['finData'] = {
            'symbol': self.symbol,
            'underlying': self.underlying,
            'totalNumContracts': self.totalNumContracts
        }
 
    def get_data(self):
        return self.data

    def _get_chain(self):
        return self._optchain
    
    def set_session(self, session):
        self.session = session
    
    def set_opt_params(self, opt_params):
        self.opt_params = opt_params
    
    def write_data(self, filename):
        '''
            writes to ./data
        '''
        fname = './data/' + filename + '.pkl'
        with open(fname, 'wb') as f:
            pickle.dump(self.data, f)
    
    def read_data(self, filename):
        '''
            sets calls and puts from pickle file
        '''
        fdir = Path.cwd() / 'backend/data/'

        with open('%s/%s'%(fdir, filename), 'rb') as f:
            self.data = pickle.load(f)

        #set underlying data
        self.totalVolume = self.data['quote']['totalVolume']

        finData = self.data['finData']
        self.symbol = finData['symbol']
        self.underlying = finData['underlying']
        self.totalNumContracts = finData['totalNumContracts']

        
        print('findata: ', finData)




    

class FailedNewsException(Exception):
    pass

class InvalidDeltaException(Exception):
    pass