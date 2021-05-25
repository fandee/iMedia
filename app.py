from flask import Flask, render_template, url_for, request, redirect
from _db import DB
from _search import Search

app = Flask(__name__)
db = DB() # start connection with DB

@app.route('/')
def index():
    searches = db.get_searches()
    return render_template("index.html", searches=searches)

@app.route('/searches/<int:id>')
def search(id):
    search = db.get_search(id)
    articles = db.process_search(search)
    return render_template("search.html", search=search, articles=articles)

@app.route('/update/<int:id>', methods=['POST'])
def update_search(id):
    if request.method == 'POST':
        name = request.form['name']
        keys = request.form['keys'].split('&')
        print(keys)
        stops = request.form['stops']
        if stops:
            stops = stops.split('&')
        print(stops)
        search = Search(id, name, keys, stops)
        db.update_search(search)
        return redirect('/searches/'+str(id))

if __name__=="__main__":
    app.run(debug=True)