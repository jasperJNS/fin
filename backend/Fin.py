import pickle
import time
import pprint as pp
from datetime import datetime, timedelta

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
        
        self.vol = None # not sure which volatility this is (realized, historical? neither fit)
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
        self.nope = (netCallDelta - netPutData) / totalVolume
        
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
        self.vol = chain['volatility']
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
            'vol': self.vol,
            'totalNumContracts': self.totalNumContracts
        }

    def get_options_by_delta(self, date: int, deltaRange: float):
        '''
            Get options at date with strikes ranging from ATM(d = 0.5) outward to the delta provided
            @params 
            delta: float range from 0.001 to 0.999 inclusive
            date: int index from nearest to furthest date

            @return:
                list of strikes
        '''
        if delta not in self.deltas:
            raise InvalidDeltaException("Invalid Delta")
        
        minDelta = 0.5 - deltaRange
        maxDelta = 0.5 + deltaRange
        expDate = self.data['dates'][date]


        for callput in self.data['options'][expDate]:
            delt = callput.delta
            if delt >= minDelta and delt <= maxDelta:
                print(callput)
    
    def get_historical_data(self):
        # Define a list of all valid periods
        periodValues = {
            'minute': {
                'day': [1, 2, 3, 4, 5, 10]
            },
            'daily': {
                'month': [1, 2, 3, 6],
                'year': [1, 2, 3, 5, 10, 15, 20],
                'ytd': [1]
            },
            'weekly': {
                'month': [1, 2, 3, 6],
                'year': [1, 2, 3, 5, 10, 15, 20],
                'ytd': [1]
            },
            'monthly': {
                'year': [1, 2, 3, 5, 10, 15, 20]
            }
        }

        minuteFrequencies = [1, 5, 10, 15, 30]

        hist_symbol = self.symbol
        hist_needExtendedHoursData = True

        hist_data = []

        for freqType in periodValues.keys():
            freqPeriods = periodValues[freqType]

            for freqPeriod in freqPeriods.keys():
                possibleValues = freqPeriods[freqPeriod]

                for val in possibleValues:

                    hist_periodType = freqPeriod
                    hist_period = val
                    hist_frequencyType = freqType
                    hist_frequency = 1

                    historical_1_minute = self.session.get_price_history(
                        symbol=hist_symbol,
                        period_type=hist_periodType,
                        period=hist_period,
                        frequency_type=hist_frequencyType,
                        frequency=hist_frequency,
                        extended_hours=hist_needExtendedHoursData
                    )

                    hist_data.append(historical_1_minute)
        
        self.hist_data = hist_data
    
    def get_thirty_day_chart(self):
        # The max look back period for minute data is 31 Days.
        lookback_period = 31

        # Define today.
        today_00 = datetime.now()

        # Define 300 days ago.
        today_ago = datetime.now() - timedelta(days=lookback_period)

        # The TD API expects a timestamp in milliseconds. However, the timestamp() 
        # method only returns to seconds so multiply it by 1000.
        today_00 = str(int(round(today_00.timestamp() * 1000)))
        today_ago = str(int(round(today_ago.timestamp() * 1000)))

        # These values will now be our startDate and endDate parameters.
        hist_startDate = today_ago
        hist_endDate = today_00

        # Define the dynamic arguments, PERIOD IS NOT NEEDED!!!!
        hist_symbol = self.symbol
        hist_needExtendedHoursData = True
        hist_periodType = 'day'

        #make sure frequency type is correct, else its read as a malformed header -> 400
        hist_frequencyType = 'minute'
        hist_frequency = 1

        # Make the request
        historical_custom = self.session.get_price_history(
            symbol=hist_symbol,
            period_type=hist_periodType,
            frequency_type=hist_frequencyType,
            start_date=hist_startDate,
            end_date=hist_endDate,
            frequency=hist_frequency,
            extended_hours=hist_needExtendedHoursData
        )

        # Grab the candle count.
        candle_count = len(historical_custom['candles'])
        print('For PERIOD TYPE {} with CUSTOM PERIOD {} you got {} candles.'.format(
            hist_periodType, lookback_period, candle_count)
        )

        

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
        fname = './data/' + filename + '.pkl'
        with open(fname, 'rb') as f:
            self.data = pickle.load(f)

        finData = self.data['finData']
        print('findata: ', finData)

        self.symbol = finData[0]
        self.underlying = finData[1]
        self.vol = finData[2]
        self.totalNumContracts = finData[3]


        # self.symbol = finData['symbol']
        # self.underlying = finData['underlying']
        # self.vol = finData['vol']
        # self.totalNumContracts = finData['totalNumContracts']
    

class FailedNewsException(Exception):
    pass

class InvalidDeltaException(Exception):
    pass