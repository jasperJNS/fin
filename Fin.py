import pickle
import time
from datetime import datetime
import pandas as pd

class Fin:
    def __init__(self, session=None, opt_params=None):
        '''
            sets chain on init with session and params objects
        '''
        self.session = session
        self.opt_params = opt_params

        if session is not None:
            self.chain = session.get_options_chain(option_chain=opt_params)
    
    def get_chain(self):
        return self.chain
    
    def set_opt_params(self, opt_params):
        self.opt_params = opt_params
    

    def write_json(self, filename):
        '''
            writes to ./data
        '''
        fname = './data/' + filename + '.json'
        self.chain.to_json(fname, orient='records', indent=2)
    
    def read_json(self, filename):
        '''
            reads json into pandas dataframe
        '''
        fname = './data/' + filename + '.json'
        self.chain = pd.read_json(fname, orient='records')