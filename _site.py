from os import error
import requests
from bs4 import BeautifulSoup
from _article import Article
import sys


class Site:

    def __init__(self, site_id, 
                site_link, search_link, article, article_link, 
                start, next,
                article_main, article_title, article_meta, article_text,
                one_page):
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
        self.site_id = site_id
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
        self.one_page = one_page


    def __repr__(self):
        """
        Object's representation
        """
        return '''
site_id = {}\n
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
                '''.format(self.site_id, self.site_link, self.search_link, self.article, self.article_link, self.start, self.next, 
                        self.article_main, self.article_title, self.article_meta, self.article_text)

    def scrape(self, date):
        """
        Scrape list of links of articles for determined day on site
        :date - date(year, month, day) for scraping
        """
        links = []
        # while list of articles is not empty
        if self.one_page == True:
            url = self.search_link.format(y=date.year, m=date.month, d=date.day)
            # try to request url
            try:
                response = requests.get(url)
                bs = BeautifulSoup(response.content, 'html.parser')
                # get links of all articles on the page
                list_articles = bs.select(self.article)
                # element is not on the page
                try:
                    list_articles[0].select_one(self.article_link)['href']
                    for article in list_articles:
                        links.append(article.select_one(self.article_link)['href'])
                # except TypeError as e:
                except:
                    print('###')
                    print('_site.py: scrape(77-80)')
                    print('URL: ' + url)
                    print('###')
            # except requests.exceptions.ConnectionError as e:
            except:
                print('###')
                print('_site.py: scrape(71-86)')
                print('URL: ' + url)
                print('###')
            print('Links:' + str(len(links)))
            return links
        # set start page or row
        i = self.start
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
                # except TypeError as e:
                except:
                    print('###')
                    print('_site.py: scrape(111-114)')
                    print('URL: ' + url)
                    print('###')
            # except requests.exceptions.ConnectionError as e:
            except:
                print('###')
                print('_site.py: scrape(100-120)')
                print('URL: ' + url)
                print('###')
        print("Links: " + str(len(links)))
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
            # bug fix
            url = ''
            if link[0] == '/':
                url = self.site_link
            url += link
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
                        # except IndexError:
                        except:
                            print('###')
                            print('_site.py: parse(163-164)')
                            print('URL: ' + url)
                            print('###')
                            raise AttributeError
                    # new article
                    article = Article(self.site_id, url, 
                                    article_meta.replace('\n', ' ').replace('\'', '\'\'').strip(),
                                    article_title.replace('\'', '\'\''), 
                                    article_text.replace('\n', ' ').replace('\'', '\'\'')[:8000])
                    articles.append(article)
                    # status line
                    sys.stdout.write(str(int(n / len(links) * 100)) + '%\r')
                    n += 1
                # except AttributeError as e:
                except:
                    print('###')
                    print('_site.py: parse(154-180)')
                    print('URL: ' + url)
                    print('###')
                    # break
            # except requests.exceptions.ConnectionError as e:
            except:
                print('###')
                print('_site.py: parse(149-186)')
                print('URL: ' + url)
                print('###')
        return articles