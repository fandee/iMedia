from _db import DB
import datetime
from _site import Site

# Create DB object and connect
db = DB()
# get list of all sites in database
sites = db.get_sites()
# get date of today
today = datetime.date.today()
articles = []
# iterate through sites and append articles to full list
for site in sites:
    print(site.site_link)
    articles += site.parse(today)
# print articles
for article in articles:
    print(article)