import time
from datetime import datetime

def epoch_to_date(epoch):
    '''
        @param: date in epoch milliseconds
        @return: human-readable date

    '''
    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(epoch/1000.0))
