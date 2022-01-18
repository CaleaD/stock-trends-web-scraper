# stock-trends-web-scraper
A scraper with API and web interface.

On the client side, the user will be met with a search field for input and will be able to opt either for trends on a specific stock or for multiple. On the server side, the request will be sent to the API will act as a bridge in the communication between the user and scraper. The main service featured by the application is the scraper tool which will gather data from other web services in order to then get structured data to the client on his queried stocks. There are two scrapers which have different properties. One which will get news from an RSS Feed on the requested stocks, and another which will collect a batch of stock market data from Yahoo Finance. The batch will includes stocks from chosen dates and queries specific stock tickers provided by Google Finance and Yahoo Finance. Data collected will include high, low in that day/year, close and open price, volume, market cap and market status. They will also be displayed to the user on site as time series or tables and the requested information will be available to download as CSV. For current trends, to parse the RSS type document we will scrape the xml from SeekingAlpha and
put the data into a json file. Scraping will be done using BeautifulSoup. The main functionalities for the site will be done in Python with libraries and frameworks to aid the creation of the API (Flask, jinja2), the scrapers (BeautifulSoup, pandas) and the plots (matplotlib, chart.js).

### Financial Data Scraper

The financial scraper() method first searches on Google Finance the fields necessary for price, market status, name and symbol. The ticker attribute of this class functions as a search parameter for the urls. The variable data stores additional data that can be taken at once from the class attributes of divs, mainly it will
return a list containing the following data: symbol, market status, price, open, close, market cap, volume, name, day min, day max, year min, year max.

### RSS Data Scraper

The NewsScraper class includes all of the necessary methods for scraping RSS news data or parsing the information into jsons. The scraper() method in this class makes a get request to the url and then acquires its content. It then fills an empty lists with dictionaries that have keys pertaining to an article’s title, link, published date and symbol (ticker for the stock) by searching each tag using BeautifulSoup.

### Quick Guide

On the main page, the search field awaits user input of no more than 200 characters. You can therefore opt either for trends on a specific stock or for multiple. For one stock, the name or ticker of the stock should be inserted in the field. For more than one stocks, a list separated by commas can be written into the field. The input will not be recognized if one of the specified stocks is not provided by Yahoo Finance or Google Finance or if the spelling is wrong. 

Once the search parameters have been set, by clicking the "Enter" button, the request will be sent to the API which will load in either a table or formatted data. It may take a while to update the page, since matplotlib is quite slow in plotting the data (Chart.js may be used in future updates). The data displayed will include high, low, close and open price, volume and other specifics. In the case of requesting one stock, the historical data of that day can be available to download as CSV by pressing the "Download CSV" button. To search again just input another value/values into the search field.

(!) If the plot is missing data it might be because the market hour has just started and the data got cleared for new input on the requested servers.
