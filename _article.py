class Article:

    def __init__(self, site_id, link, meta, title, text):
        """
        Constructor - init Article's object vars
        :link - article's link
        :meta - article's metadata (date, time, author, views)
        :title - article's title
        :text - article's text
        """
        self.site_id = site_id
        self.link = link
        self.meta = meta
        self.title = title
        self.text = text

    def __repr__(self):
        return self.link