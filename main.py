import pprint as pp
import pandas as pd
pd.set_option('display.max_columns', None)

from login import login
from Fin import Fin


# session = login()

# nio_params = {
#     'symbol': 'NIO',
#     'opt_range': 'all',
#     'exp_month': 'may'
# }

# nio = Fin(session, nio_params)

# # set from session object
# nio.set_chain()
# nio.write_file('nio_chain')


# temp just for reading file
nio = Fin(None, None)
nio.read_file('nio_chain')



chain_df = nio.get_chain()

calls = chain_df['callExpDateMap']



strike = '20.0'
pp.pprint(calls.iloc[0][strike], indent=4)

