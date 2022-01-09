from bs4 import BeautifulSoup
import json
import requests

class NewsScraper:
    __tickers = ''

    def __init__(self, ticker):
        self.ticker = ticker

    def __int__(self, tickers={}):
        self.__tickers = tickers

    def set_tickers(self, tickers):
        self.__tickers = tickers

    def get_tickers(self):
        return self.__tickers


    #TODO: [here]
    def filter_json(self):
        '''
        A function that filters a given json file by stock symbol. Only articles with given ticker/symbol remain.
        :return: json/txt
        '''
        pass

    def save_to_json(self,articles):
        '''
        Save the scraped output to text file in json format.
        :param articles: list of articles, can be taken as result from scraper method
        :return: json/txt
        '''
        with open('articles.json', 'w') as file:
            json.dump(articles, file, sort_keys = True, indent = 4)

    def scraper(self):
        '''
        :return: List of dictionaries, each with keys - title, link, published, symbol.
        Can be turned into json with method save_to_json.
        '''
        #Try more urls here: https://blog.feedspot.com/stock_rss_feeds/
        url = 'https://seekingalpha.com/feed.xml'
        print('Starting scraping...')
        try:
            r = requests.get(url)
            sp = BeautifulSoup(r.content,features='xml')
            #print(sp)
            a_lst = []
            articles = sp.findAll('item')
            for a in articles:
                title = a.find('title').text
                link = a.find('link').text
                published = a.find('pubDate').text
                #symbol = a.find('category',{'link':f'https://seekingalpha.com/symbol/{self.ticker}', 'type':'symbol'})
                symbol = a.find('category',{'type': 'symbol'})
                if symbol is None:
                    symbol = 'None'
                else:
                    symbol = symbol.text
                article = {
                    'title': title,
                    'link': link,
                    'published': published,
                    'symbol' : symbol
                }
                a_lst.append(article)
            print('Scraping finished!')
            return a_lst
        except Exception as e:
            print('Scraping failed with exception: ')
            print(e)