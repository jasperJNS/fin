import requests
from newsapi import NewsApiClient

class NewsFeed:
    '''
        Handles news feed for any searchable topic
        Accepts string combinations for articles containing both references such as: 
            tsla AND bitcoin
            jerome powell AND yield

    '''
    def __init__(self, apikey):
        self.api = NewsApiClient(api_key=apikey)

    def get_top_headlines(self, ticker):
        return self.api.get_top_headlines(q=ticker)
    
    def get_everything(self, ticker):
        return self.api.get_everything(q=ticker, sort_by='popularity')
    
    def get_related_sector(self, ticker, sector):
        query = ticker + ' and ' + sector
        return self.api.get_everything(q=query, sort_by='popularity')