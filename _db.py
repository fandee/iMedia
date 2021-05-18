from os import error
import pyodbc
from _site import Site

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
                site_link = row[0],
                search_link = row[1],
                article = row[2],
                article_link = row[3],
                start = row[4],
                next = row[5],
                article_main = row[6],
                article_title = row[7],
                article_meta = row[8],
                article_text = row[9]
            ))
        return sites

    def put_articles(self, articles, day):
        """
        Insert articles into database
        """
        for article in articles:
            try:
                self.cursor.execute("INSERT INTO Articles VALUES ({site_id}, '{link}', '{meta}', '{title}', '{text}', '{published_date}')".format(
                        site_id=2, 
                        link=article.link, 
                        meta=article.meta, 
                        title=article.title, 
                        text=article.text,
                        published_date=day))
                self.cursor.commit()
            except error as e:
                print(e)
                