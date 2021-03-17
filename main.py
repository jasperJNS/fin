import td

import pickle
import pprint as pp
import pandas as pd
pd.set_option('display.max_columns', None)

from login import login
from options_chain import get_options_chain

class Fin:
    def __init__(self, session, opt_params):
        self.session = session
        self.opt_params = opt_params

        self.chain = None

    def set_chain(self):
        self.chain = pd.DataFrame(get_options_chain(self.session, self.opt_params))

    def get_chain(self):
        return self.chain
    
    def set_opt_params(self, opt_params):
        self.opt_params = opt_params
    
    def write_chain(self, filename):
        '''
            writes to ./data
        '''
        fname = './data/' + filename + '.pkl'
        self.chain.to_pickle(fname)
    
    def read_chain(self, filename):
        '''
            reads from ./data
        '''
        fname = './data/' + filename + '.pkl'
        self.chain = pd.read_pickle(fname)

session = login()

opt_params = {
    'symbol': 'NIO',
    'opt_range': 'all',
    'exp_month': 'may'
}

nio = Fin(session, opt_params)

# set from session object
nio.set_chain()


chain_df = nio.get_chain()
nio.write_chain('nio_chain')


# write to file
# chain_df.to_pickle('./nio_chain.pkl')

# # read file
# chain_df = pd.read_pickle('./nio_chain.pkl')



calls = chain_df['callExpDateMap']
strike = '20.0'
pp.pprint(calls.iloc[0][strike], indent=4)

