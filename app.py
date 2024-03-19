
from flask import Flask, request, render_template
import csv
from threading import Thread
from webcrawler import WebCrawler
from indexer import Indexer
from ranker import Ranker

app = Flask(__name__)
crawler = None

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    global crawler
    keyword = request.args.get('keyword')
    url = request.args.get('url')
    if keyword and url:
        if crawler is None:
            crawler = WebCrawler()
        # Threading for crawling
        crawler_thread = Thread(target=crawler.crawl, args=(url,))
        crawler_thread.start()
        
        # Wait for the crawling to finish and then index documents
        crawler_thread.join()
        results = index_documents(keyword)

        if results:
            return render_template('results.html', results=results)
        else:
            return render_template('results.html', message='Result not found for the given keyword and URL.')
    else:
        return render_template('results.html', error='Both keyword and URL parameters are required.'), 400

def index_documents(keyword):
    indexer = Indexer()
    indexer.index = crawler.index
    results = indexer.search(keyword)
    if results:
        ranker = Ranker()
        ranked_results = ranker.rank_results(results, indexer.index, keyword)
        return ranked_results
    else:
        return None

@app.route('/csvdata', methods=['GET'])
def csv_data():
    # Load data from CSV
    data = []
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return render_template('csvdata.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)