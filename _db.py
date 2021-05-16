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