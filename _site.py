from os import error
import requests
from bs4 import BeautifulSoup
from _article import Article
import sys


class Site:

    def __init__(self, 
                site_link, search_link, article, article_link, 
                start, next,
                article_main, article_title, article_meta, article_text):
        """
        Constructor - init vars for querying websites and searching elements
        :site_link - base website link
        :search_link - website's link for searching news
        :article - CSS selector for article's preview
        :article_link - CSS selector for article's link in preview
        :start - start row or page for URL. e.g google.com/page=0
        :next - depending on site, we will skip 1 page or 10/20... articles
        :article_main - CSS selector for article's content
        :article_title - CSS selector for article's title
        :article_meta - CSS selector for article's metadata
        :article_text - CSS selector for article's text
        """
        self.site_link = site_link
        self.search_link=search_link
        self.article = article
        self.article_link = article_link
        self.start = start
        self.next = next
        self.article_main = article_main
        self.article_title = article_title
        self.article_meta = article_meta
        self.article_text = article_text


    def __repr__(self):
        """
        Object's representation
        """
        return '''
site_link = {}\n
search_link = {}\n
article = {}\n
article_link = {}\n
start = {}\n
next = {}\n
article_main = {}\n
article_title = {}\n
article_meta = {}\n
article_text = {}\n
                '''.format(self.site_link, self.search_link, self.article, self.article_link, self.start, self.next, 
                        self.article_main, self.article_title, self.article_meta, self.article_text)

    def scrape(self, date):
        """
        Scrape list of links of articles for determined day on site
        :date - date(year, month, day) for scraping
        """
        links = []
        # set start page or row
        i = self.start
        # while list of articles is not empty
        while True:
            url = self.search_link.format(y=date.year, m=date.month, d=date.day, n=i)
            # try to request url
            try:
                response = requests.get(url)
                # switch articles page
                i += self.next
                bs = BeautifulSoup(response.content, 'html.parser')
                # get links of all articles on the page
                list_articles = bs.select(self.article)
                # no more articles or ElementAccessError
                if not len(list_articles):
                    break
                # element is not on the page
                try:
                    list_articles[0].select_one(self.article_link)['href']
                    for article in list_articles:
                        links.append(article.select_one(self.article_link)['href'])
                except TypeError as e:
                    print('ELEMENT ERROR: ' + self.article_link)
                    print(url)
                    print('#')
            except requests.exceptions.ConnectionError as e:
                print('CONNECTION ERROR')
                print(url)
                print('#')
        return links


    def parse(self, date):
        """
        Parse articles and return list of article objects
        :date - date's object (y, m, d)
        :return - list of articles
        """
        # scraping links
        links = self.scrape(date)
        articles = []
        # link counter
        n = 0
        for link in links:
            url = self.site_link + link
            # try to request url
            try:
                response = requests.get(url)
                bs = BeautifulSoup(response.content, 'html.parser')
                # select main content of article
                article_main = bs.select_one(self.article_main)
                try:
                    # title and metadata
                    article_title = article_main.select_one(self.article_title).text
                    article_meta = article_main.select_one(self.article_meta).text
                    # different CSS classes for text
                    try:
                        article_text = article_main.select_one(self.article_text.split('|')[0]).text
                    except AttributeError:
                        # try to access 2-nd class
                        try:
                            article_text = article_main.select_one(self.article_text.split('|')[1]).text
                        except IndexError:
                            raise AttributeError
                    # new article
                    article = Article(self.site_link+link, article_meta, article_title, article_text)
                    articles.append(article)
                    # status line
                    sys.stdout.write(str(int(n / len(links) * 100)) + '%\r')
                    n += 1
                except AttributeError as e:
                    print('ELEMENT ERROR')
                    print(url)
                    print('#')
                    break
            except requests.exceptions.ConnectionError as e:
                print('CONNECTION ERROR')
                print(url)
                print('#')
        return articles


# site_24 = Site(
#     site_link='https://24tv.ua/',
#     search_link='https://24tv.ua/search/search.do?searchValue=&mode=all&relevance=false&startDateFilter={y}-{m}-{d}&endDateFilter={y}-{m}-{d}&startRow={n}',
#     list_articles='.news-list > .list > li',
#     article_link='.news_title',
#     start=0,
#     next=10,
#     article_main='.article',
#     article_title='h1',
#     article_meta='time',
#     article_text='.news-content|.article_text'
# )

# site_strana = Site(
#     site_link='https://strana.ua/',
#     search_link='https://strana.ua/news/day={y}-{m}-{d}/page-{n}.html',
#     list_articles='article.lenta-news',
#     article_link='.article',
#     start=1,
#     next=1,
#     article_main= 'div.article',
#     article_title='.article',
#     article_meta = '.article-meta',
#     article_text = '.article-text'
# )
