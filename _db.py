from os import error
import pyodbc
from _site import Site
from _article import Article
from _search import Search

class DB:

    def __init__(self):
        conn = pyodbc.connect(
            'Driver={SQL Server};'
            'Server=hp;'
            'Database=iMediaDB;'
            'Trusted_Connection=yes;')
        self.cursor = conn.cursor()

    def get_sites(self):
        """
        Fetch list of sites from database
        """
        self.cursor.execute("SELECT * FROM vSites")
        sites = []
        for row in self.cursor:
            sites.append(Site(
                site_id = row[0],
                site_link = row[1],
                search_link = row[2],
                article = row[3],
                article_link = row[4],
                start = row[5],
                next = row[6],
                article_main = row[7],
                article_title = row[8],
                article_meta = row[9],
                article_text = row[10]
            ))
        return sites

    def insert_articles(self, articles, day):
        """
        Insert articles into database
        """
        for article in articles:
            try:
                self.cursor.execute("INSERT INTO Articles VALUES ({site_id}, '{link}', '{meta}', '{title}', '{text}', '{published_date}')".format(
                        site_id=article.site_id, 
                        link=article.link, 
                        meta=article.meta, 
                        title=article.title, 
                        text=article.text,
                        published_date=day))
                self.cursor.commit()
            except pyodbc.IntegrityError as e:
                print('UNIQUE Article link ERROR')
                
    def process_search(self, search):
        """
        Return articles with 
        """
        self.cursor.execute("SELECT * FROM Articles WHERE _Text LIKE '%{key}%'".format(key=key))
        articles = []
        for row in self.cursor:
            articles.append(Article(
                link=row[1],
                meta=row[-1],
                title=row[3],
                text=row[4]
            ))
        return articles