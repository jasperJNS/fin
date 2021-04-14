import FinanceDatabase as fd
import matplotlib.pyplot as plt
from yfinance.utils import get_json
from yfinance import download


class Search:
    def __init__(self):
        '''
            Handler for searching for assets by sector or other parameters;
            Includes products, companies, derivatives from:
                Equities, ETFs, Funds, Indices, Crypt, Options, Futures, Money Markets

            Aids in finding cross-section of related sectors for an equity or currency

            @param product: must be in:
                Options, Crypto, ETFs, Funds, Indices, Equities
                or other=(Futures, MoneyMarkets)
        '''
        self.data = {}

    def show_options(self, product):
        '''
            Can use this for initial tree of display options
        '''
        return fd.show_options(product)

    def search_products(self, product):

        return fd.search_products()