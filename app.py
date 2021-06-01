from flask import Flask, render_template, url_for, request, redirect
from _db import DB
from _search import Search
import datetime

app = Flask(__name__)
db = DB() # start connection with DB

def save_articles(date):
    """
    Parse articles everyday and save in database
    """
    # date = datetime.date.today()
    # get list of all sites in database
    sites = db.get_sites()
    articles = []
    # iterate through sites and append articles to full list
    for site in sites:
        print(site.site_link)
        articles += site.parse(date)
    # insert articles into database
    db.insert_articles(articles, date)
    print('Collected ' + str(len(articles)) + ' articles')

@app.route('/')
def index():
    searches = db.get_searches()
    return render_template("index.html", searches=searches)

@app.route('/searches/<int:id>')
def search(id):
    search = db.get_search(id)
    articles = db.process_search(search)
    return render_template("search.html", search=search, articles=articles)

@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        keys = request.form['keys'].split('&')
        stops = request.form['stops']
        if stops:
            stops = stops.split('&')
        search = Search(id, name, keys, stops)
        db.add_search(search)
        return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update_search(id):
    if request.method == 'POST':
        name = request.form['name']
        keys = request.form['keys'].split('&')
        stops = request.form['stops']
        if stops:
            stops = stops.split('&')
        search = Search(id, name, keys, stops)
        db.update_search(search)
        return redirect('/searches/'+str(id))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_search(id):
    db.delete_search(id)
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)