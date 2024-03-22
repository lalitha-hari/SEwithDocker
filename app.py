from flask import Flask, request, jsonify, render_template
from threading import Thread
from webcrawler import WebCrawler
from indexer import Indexer
from ranker import Ranker

app = Flask(__name__)
crawler =      None
indexer =      None
indexing_complete = False


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/search", methods=["GET"])
def search():
    global crawler, indexer, indexing_complete
    keyword = request.args.get("keyword")
    url = request.args.get("url")
    if not (keyword and url):
        return jsonify({"error": "Both keyword and URL parameters are required"}), 400

    if not crawler:
        crawler = WebCrawler()
    crawler_thread = Thread(target=crawler.crawl, args=(url,))
    crawler_thread.start()
    crawler_thread.join()

    if not indexer:
        indexer = Indexer()
        indexer.index = crawler.index

    results = indexer.search(keyword)
    if results:
        ranker = Ranker()
        ranked_results = ranker.rank_results(results, indexer.index, keyword)
        indexing_complete = True
        return jsonify(ranked_results)
    else:
        return jsonify({"error": "Result not found for the given keyword and URL"}), 404


@app.route("/indexing/status", methods=["GET"])
def indexing_status():
    global indexing_complete
    return jsonify({"indexing_complete": indexing_complete})


if __name__ == "__main__":
    app.run(debug=True)
