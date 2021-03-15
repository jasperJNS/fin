# import td-ameritrade-python-api as td
from config.config import CLIENT_ID, ACCOUNT, PASSWORD, REDIRECT_URI, CREDENTIALS_PATH

import td
from td.client import TDClient
import pprint as pp


# Create a new session, credentials path is required.
TDSession = TDClient(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    credentials_path=CREDENTIALS_PATH
)

# Login to the session
TDSession.login()

# Grab real-time quotes for 'MSFT' (Microsoft)
nio = TDSession.get_quotes(instruments=['NIO'])

# Grab real-time quotes for 'AMZN' (Amazon) and 'SQ' (Square)
# multiple_quotes = TDSession.get_quotes(instruments=['AMZN','SQ'])

pp.pprint(nio, width=1)