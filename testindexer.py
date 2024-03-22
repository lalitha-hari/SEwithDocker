import unittest
from indexer import (
    Indexer,
)  # Assuming your indexer code is in a file named "indexer.py"


class TestIndexer(unittest.TestCase):
    def setUp(self):
        self.indexer = Indexer()

    def test_index_page(self):
        url = "http://example.com"
        text = "This is a sample text containing keyword"
        self.indexer.index_page(url, text)
        self.assertEqual(self.indexer.index[url], text)

    def test_search(self):
        self.indexer.index_page("http://example1.com", "Sample text with keyword")
        self.indexer.index_page(
            "http://example2.com", "Another sample text without keyword"
        )
        results = self.indexer.search("keyword")
        self.assertIn("http://example1.com", results)
        self.assertIn("http://example2.com", results)


if __name__ == "__main__":
    unittest.main()
