# import td-ameritrade-python-api as td
from .config.config import CLIENT_ID, ACCOUNT, PASSWORD, REDIRECT_URI, CREDENTIALS_PATH
import td
from td.client import TDClient

def api_login():
    # Create a new session, credentials path is required.
    TDSession = TDClient(
        client_id=CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        credentials_path=CREDENTIALS_PATH
    )

    # Login to the session
    TDSession.login()

    return TDSession

