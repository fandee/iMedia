from _db import DB
import datetime

# Create DB object and connect
db = DB()

def save_articles(date):
    """
    Parse articles for defined date and save in database
    """
    # get list of all sites in database
    sites = db.get_sites()
    articles = []
    # iterate through sites and append articles to full list
    for site in sites:
        print(site.site_link)
        articles += site.parse(date)
    # insert articles into database
    db.insert_articles(articles, date)

# get date of today
if __name__=="__main__":
    today = datetime.date.today()
    save_articles(today)

