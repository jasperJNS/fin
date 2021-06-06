import yfinance as yf
import vaex as va
import pandas as pd
import datetime
from datetime import timedelta
from datetime import datetime
import pprint as pp

from .convert_dates import epoch_to_datetime




def get_history(
    fin, 
    periodCount: int=30, 
    periodType: str=None, 
    freqType: str=None, 
    frequency: int=1,
    day_0 = None, 
    day_n=None, 
    extHours=False) -> list:
    '''
        @fin: fin object, with session and ticker attached
        @period: number of days to look back
        @periodType: ['day', 'month', 'year', 'ytd']
        @freqType: candle size for each period type: 
                        day: 'minute',
                        month: 'daily', 'weekly'
                        year: 'daily', 'weekly', 'monthly'
                        ytd: 'daily', 'weekly'
        @frequency: ticks per candle: 
                        minute: [1, 5, 10, 15, 30],
                        all else: [1]
        @day_n: end date, default is current date
        @extHours: set True for extended hours data

        @return: list:
                    date = {
                        'close': closing price of day,
                        'date': date,
                        'high': highest price of day,
                        'low': lowest price of day,
                        'open': opening price of day,
                        'volume': shares traded
                    }
    '''
    session = fin.session
    symbol = fin.symbol

    
    # define start date
    day_0 = day_n - timedelta(days=periodCount)

    # td api expects time in ms
    day_0 = str(int(round(day_0.timestamp() * 1000)))
    day_n = str(int(round(day_n.timestamp() * 1000)))

    start = day_0
    end = day_n

    # define dynamic args for tda
    freqType = 'daily'
    freq = 1

    historical = session.get_price_history(
        symbol=symbol,
        period_type=periodType,
        frequency_type=freqType,
        start_date=start,
        end_date=end,
        frequency=freq,
        extended_hours=extHours
    )

    for candle in historical['candles']:        
        candle['date'] = epoch_to_datetime(candle['datetime'])
        del candle['datetime']

    return historical['candles']