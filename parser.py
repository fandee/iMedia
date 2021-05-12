import requests
from bs4 import BeautifulSoup
from time import sleep

class Parser:
    """
    Parse websites for key-words
    As start point uses google search <https://www.google.com/search> page where collecting links
    """

    def __init__(self, sites, key):
        """
        Constructor of Parser class - init object vars, creates basic search query
        :site - website for parsing
        :key - word for parsing
        """
        self.sites = sites
        self.key = key
        self.links = []
        for site in self.sites:
            self.search_query = 'https://www.google.com/search?q=site:{site}+{key}&tbs=qdr:d&num=100&start='.format(site=site, key=self.key)
            self.switch_pages()

    def __repr__(self):
        """
        :return - string representation of the object
        """
        return 'I am searching for "{key}" on <{site}> for 12 past hours'.format(key=self.key, site=self.site)


    def switch_pages(self):
        """
        Switch pages of google search and add links to object's var self.links
        """
        i = 0
        while True:
            temp_links = self.collect_links(str(i))
            length = len(temp_links)
            if not length:
                print('break')
                break
            self.links += temp_links
            print('Collected ' + str(length) + ' links')
            i += 100

    def collect_links(self, start_link):
        """
        Collect links of google search page
        :return - links
        """
        my_headers = { 'User-agent' : 'Mozilla/10.0' }
        search_page = requests.get(self.search_query + start_link, headers=my_headers).content
        print(self.search_query + start_link)
        soup = BeautifulSoup(search_page, 'html.parser')
        temp_links = []
        if soup.find('div', class_='g-recaptcha'):
            with open("page.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            print("CAPTCHA")
            return temp_links

        for div in soup.find_all('div', class_='kCrYT'):
            link = div.find('a')
            if not link:
                continue
            try:
                temp_links.append(link['href'].split('?q=')[1].split('&sa')[0])
            except IndexError as error:
                print(error)
        return temp_links

    def show(self):
        """
        list collected links
        """
        for link in self.links:
            print(link)


websites = ['www.google.com']
key = 'зе'

sam = Parser(websites, key)
# sam.switch_pages()
sam.show()