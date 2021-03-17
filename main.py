import td

import pprint as pp
import pandas as pd
pd.set_option('display.max_columns', 500)

from login import login
from options_chain import get_options_chain


# Get session object
session = login()

nio = session.get_quotes(instruments=['NIO'])
pp.pprint(nio, width=1)
opt_params = {
    'symbol': 'NIO',
    'opt_range': 'all',
    'exp_month': 'may'
}

chain = get_options_chain(session, opt_params)


chain_df = pd.DataFrame(chain)

print(chain_df.head())