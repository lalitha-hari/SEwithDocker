from flask import jsonify

# Import necessary modules from other files
from app import app, request, index_documents, crawler, indexer, ranker

@app.route('/api/search', methods=['GET'])
def api_search():
    keyword = request.args.get('keyword')
    if keyword:
        results = index_documents(keyword)
        if results:
            return jsonify(results)
        else:
            return jsonify({'message': 'No results found for the given keyword.'}), 404
    else:
        return jsonify({'error': 'Keyword parameter is required.'}), 400

@app.route('/api/crawled-data', methods=['GET'])
def api_crawled_data():
    url = request.args.get('url')
    if url:
        if url in crawler.index:
            return jsonify({'url': url, 'content': crawler.index[url]})
        else:
            return jsonify({'message': 'URL not found in crawled data.'}), 404
    else:
        return jsonify({'error': 'URL parameter is required.'}), 400

@app.route('/api/index-document', methods=['POST'])
def api_index_document():
    data = request.get_json()
    if data and 'url' in data and 'text' in data:
        url = data['url']
        text = data['text']
        indexer.index_page(url, text)
        return jsonify({'message': f'Document indexed successfully: {url}'}), 200
    else:
        return jsonify({'error': 'Invalid JSON data. URL and text are required.'}), 400

@app.route('/api/rank-results', methods=['POST'])
def api_rank_results():
    data = request.get_json()
    if data and 'results' in data and 'keyword' in data:
        results = data['results']
        keyword = data['keyword']
        ranked_results = ranker.rank_results(results, indexer.index, keyword)
        return jsonify(ranked_results)
    else:
        return jsonify({'error': 'Invalid JSON data. Results and keyword are required.'}), 400
