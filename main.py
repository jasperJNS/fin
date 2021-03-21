import pprint as pp
import pandas as pd
pd.set_option('display.max_columns', None)

from login import login
from Fin import Fin
from CallPut import CallPut

def main_test():
    # session = login()

    # nio_params = {
    #     'symbol': 'NIO',
    #     'opt_range': 'all',
    #     'exp_month': 'may'  #months up to, but NOT including {exp_month}
    # }

    # nio = Fin(session, nio_params)

    # # set from session object
    # nio.set_chain()
    # nio.write_file('nio_2021319')


    # temp just for reading file
    nio = Fin()
    nio.read_file('nio_all_dates')

    print('\n'*5)


    chain = nio.get_chain()
    chain_df = pd.DataFrame(chain)
    print(chain_df.head())
    chain_df.to_json('nio_all_dates.json', orient='records', indent=2)


def json_test():
    nio = Fin()
    nio.read_json('nio_all_dates')
    chain = nio.get_chain()

    print("cols: ", chain.columns)

    #these are universal across all dates
    symbol = chain['symbol'].iloc[0]
    underlying = chain['underlyingPrice'].iloc[0]
    vol = chain['volatility'].iloc[0]
    totalNumContracts = chain['numberOfContracts'].iloc[0]

    '''
        so each row in callexdatemap or putexpdatemap is date indexed

        so let's unwrap, each row will be its own dataframe, records style

        then overall data is a list of dates, then a dictionary of dates to their respective dfs


    '''
    print(chain.columns, chain.shape)

    callsMap = chain['callExpDateMap']

    #using the first strike of each expiry date chain to get the date of the chain
    dates = []
    calls = []
    for idx, callMap in enumerate(callsMap):
        for strikes in list(callsMap[idx].keys()):
            strike = strikes
            call = CallPut(dict(callsMap[idx][strike][0].items()))
            
            calls.append(call)
            
        #use last call in chain to get date
        date = call.get('expirationDate')
        dates.append(date)

    puts = []
    putsMap = chain['putExpDateMap']
    for idx, putMap in enumerate(putsMap):
        for strikes in list(putsMap[idx].keys()):
            strike = strikes
            put = CallPut(dict(putsMap[idx][strike][0].items()))
            
            puts.append(put)

    for k, v in puts[0].items():
        print(k, v)
    for k, v in calls[0].items():
        print(k, v)





if __name__ == '__main__':
    json_test()