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

    def add_search(self, search):
        """
        Insert search object into DataBase
        """
        try:
            self.cursor.execute("INSERT INTO Searches (SearchName) VALUES ('{search_name}')".format(search_name=search.name))
            self.cursor.commit()
            search_id = self.cursor.execute("SELECT IDENT_CURRENT('Searches')").fetchone()[0]
            for key in search.keys:
                self.cursor.execute("INSERT INTO KeyWords VALUES ({search_id}, '{key}')".format(search_id=search_id, key=key))
                self.cursor.commit()
            for stop in search.stops:
                self.cursor.execute("INSERT INTO StopWords VALUES ({search_id}, '{stop}')".format(search_id=search_id, stop=stop))
                self.cursor.commit()
        except error as e:
            print(e)


    def get_searches(self):
        searches = [Search(row[0], row[1], [], []) for row in self.cursor.execute("SELECT * FROM Searches")]
        for search in searches:
            search.keys = [row[0] for row in self.cursor.execute("SELECT KeyWord FROM KeyWords WHERE SearchID = {search_id}".format(search_id=search.id))]
            search.stops = [row[0] for row in self.cursor.execute("SELECT StopWord FROM StopWords WHERE SearchID = {search_id}".format(search_id=search.id))]
        return searches


    def process_search(self, search):
        """
        Creating SQL query and return list of id of articles for the search's object
        """
        query = "SELECT ID FROM Articles WHERE (_Text LIKE '%{key}%'".format(key=search.keys[0])
        for key in search.keys[1:]:
            query += " OR _Text LIKE '%{key}%'".format(key=key)
        query += ")"
        if len(search.stops):
            for stop in search.stops:
                query += " AND _Text NOT LIKE '%{stop}%'".format(stop=stop)
        id_list = [row[0] for row in self.cursor.execute(query)]
        print(query)
        return id_list