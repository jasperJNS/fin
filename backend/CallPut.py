import time
from datetime import datetime
from collections.abc import MutableMapping

class CallPut(MutableMapping):
    def __init__(self, *args, **kwargs):
        self._values = {
            'putCall': '',
            'symbol': '',
            'description': '',
            'exchangeName': '',
            'bid': '',
            'ask': '',
            'last': '',
            'mark': '',
            'bidSize': '',
            'askSize': '',
            'bidAskSize': '',
            'lastSize': '',
            'highPrice': '',
            'lowPrice': '',
            'openPrice': '',
            'closePrice': '',
            'totalVolume': '',
            'tradeDate': '',
            'tradeTimeInLong': '',
            'quoteTimeInLong': '',
            'netChange': '',
            'volatility': '',
            'delta': '',
            'gamma': '',
            'theta': '',
            'vega': '',
            'rho': '',
            'openInterest': '',
            'timeValue': '',
            'theoreticalOptionValue': '',
            'theoreticalVolatility': '',
            'optionDeliverablesList': '',
            'strikePrice': '',
            'expirationDate': '',
            'daysToExpiration': '',
            'expirationType': '',
            'lastTradingDay': '',
            'multiplier': '',
            'settlementType': '',
            'deliverableNote': '',
            'isIndexOption': '',
            'percentChange': '',
            'markChange': '',
            'markPercentChange': '',
            'mini': '',
            'nonStandard': '',
            'inTheMoney': ''
        }
        self.update(dict(*args, **kwargs))

        #convert dates to readable
        dateKeys = ['tradeTimeInLong', 'quoteTimeInLong', 'expirationDate', 'lastTradingDay']
        for key in dateKeys:
            self._values[key] = self.convert_readable_dates(self._values[key])
    
    def get_net_delta(self):
        return self._values['totalVolume'] * self._values['delta']
    
    def get_volume(self):
        return self._values['totalVolume']
    
    def get_open_interest(self):
        return self._values['openInterest']

    def convert_readable_dates(self, epoch):
        '''
            @param: date in epoch milliseconds
            @return: human-readable date

        '''
        return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(epoch/1000.0))

    def __getitem__(self, key):
      return self._values[key]
  
    def __getattr__(self, attr):
        return self.get(attr)
    
    #for pickling
    def __getstate__(self): return self.__dict__
    def __setstate__(self, d): self.__dict__.update(d)

    def __setitem__(self, key, value):
        self._values[key] = value

    def __delitem__(self, key):
        del self._values[key]
    
    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)

    def __contains__(self, item):
        if item in self._values.keys():
            return True
        return False
    
    def pop(self, k):
        return self._values.pop(k)
    
    def keys(self):
        return self._values.keys()
    
    def items(self):
        return self._values.items()
    
    def values(self):
        return self._values.values()
    
    def _to_df(self):
        return pd.DataFrame.from_dict([self._values])

    