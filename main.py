from _db import DB
import datetime

# Create DB object and connect
db = DB()

def get_articles(date):
    """
    Parse articles for defined date and put in database

    """
    # get list of all sites in database
    sites = db.get_sites()
    articles = []
    # iterate through sites and append articles to full list
    for site in sites:
        print(site.site_link)
        articles += site.parse(date)
    # insert articles into database
    db.put_articles(articles, date)

# get date of today
today = datetime.date.today()
get_articles(today)