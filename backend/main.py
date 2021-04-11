import time
from datetime import datetime
import pprint as pp
import pandas as pd
pd.set_option('display.max_columns', None)

from login import login
from Fin import Fin


def main_test():
    session = login()

    nio_params = {
        'symbol': 'NIO',
        'opt_range': 'all'
    }

    nio = Fin(session, nio_params)

    # set from session object
    data = nio.get_data()
    nio.get_thirty_day_chart()
    
    return


def set_fin_object():
    session = login()
    nio = Fin()
    nio.read_data('nio_all_dates_3_22')
    nio.set_session(session)

    nio.get_thirty_day_chart()



if __name__ == '__main__':
    # set_fin_object()
    main_test()