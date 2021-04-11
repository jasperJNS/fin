import FinanceDatabase as fd
import matplotlib.pyplot as plt
from yfinance.utils import get_json
from yfinance import download
import pprint as pp


# class Search:
#     def __init__(self, sector=None, equity=None, session=None):
#         '''
#             Handler for searching for assets by sector or other parameters;
#             Includes products, companies, derivatives from:
#                 Equities, ETFs, Funds, Indices, Crypt, Options, Futures, Money Markets
#
#             Aids in finding cross-section of related sectors for an equity or currency
#         '''

#     pass

airlines_us = fd.select_equities(country='United States', industry='Airlines')

pp.pprint(airlines_us, indent=2)