import pickle
import pandas as pd
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
    
    def write_file(self, filename):
        '''
            writes to ./data
        '''
        fname = './data/' + filename + '.pkl'
        self.chain.to_pickle(fname)
    
    def read_file(self, filename):
        '''
            reads from ./data
            doesn't require active session
        '''
        fname = './data/' + filename + '.pkl'
        self.chain = pd.read_pickle(fname)