import pickle
import time
import pprint as pp
from datetime import datetime, timedelta

import pandas as pd

from CallPut import CallPut

class Fin:
    def __init__(self, session=None, opt_params=None):
        '''
            sets chain on init with session and params objects
        '''
        self.session = session
        self.opt_params = opt_params
        
        self.symbol = None
        self.underlying = None
        self.vol = None
        self.totalNumContracts = None
        self.nope = None
        self.nopeMAD = None
        self.data = {}

        if session is not None:
            self._optchain = session.get_options_chain(option_chain=opt_params)
            self.set_calls_puts()
        
        
    
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

                    historical_1_minute = session.get_price_history(
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
        hist_frequencyType = 'day'
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

        
    
    def calculate_nope(self):
        calls = self.data['calls']
        puts = self.data['puts']

        netCallDelta = 0
        netPutDelta = 0
        totalVolume = 0
        totalOpenInterest = 0

        for call in calls:
            netCallDelta += call.get_net_delta()
            totalOpenInterest += call.get_open_interest()
            totalVolume += call.get_volume()
        
        for put in puts:
            netPutData += put.get_net_delta()
            totalOpenInterest += put.get_open_interest()
            totalVolume += put.get_volume()

        self.totalOpenInterest = totalOpenInterest

        #for now using open interest as a proxy for shares traded, but def not accurate
        self.nope = (netCallDelta - netPutData) / (totalOpenInterest * 100)
        


    def set_calls_puts(self):
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
        dates = []
        calls = []
        puts = []

        for days, strikes in callsMap.items():
            for strike, value in strikes.items():
                call = CallPut(dict(value[0].items()))
                calls.append(call)
            
            #use last call in chain to get date
            d = call.get('expirationDate')
            dates.append(d)
        
        for days, strikes in putsMap.items():
            for strike, value in strikes.items():
                put = CallPut(dict(value[0].items()))
                puts.append(put)

        self.data['dates'] = dates
        self.data['calls'] = calls
        self.data['puts'] = puts
        self.data['finData'] = [self.symbol, self.underlying, self.vol, self.totalNumContracts]


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
        
    
