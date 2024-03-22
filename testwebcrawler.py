import unittest
from unittest.mock import patch, MagicMock
from webcrawler import (
    WebCrawler,
)  # Assuming your webcrawler code is in a file named "webcrawler.py"


class TestWebCrawler(unittest.TestCase):
    @patch("webcrawler.requests.get")
    def test_crawl_single_page(self, mock_get):
        # Set up mock response for a single page with no links
        mock_response = MagicMock()
        mock_response.text = "<html><body>No links</body></html>"
        mock_get.return_value = mock_response

        # Initialize crawler and call crawl method
        crawler = WebCrawler()
        crawler.crawl("http://example.com")

        # Assertions
        self.assertTrue("http://example.com" in crawler.visited)
        self.assertTrue("http://example.com" in crawler.index)
        self.assertEqual(crawler.links_found, 0)

    @patch("webcrawler.requests.get")
    def test_crawl_multiple_pages(self, mock_get):
        # Set up mock response for a page with multiple links
        mock_response = MagicMock()
        mock_response.text = "<html><body><a href='http://example.com/page1'>Link 1</a><a href='http://example.com/page2'>Link 2</a></body></html>"
        mock_get.return_value = mock_response

        # Initialize crawler and call crawl method
        crawler = WebCrawler()
        crawler.crawl("http://example.com")

        # Assertions
        self.assertTrue("http://example.com" in crawler.visited)
        self.assertTrue("http://example.com" in crawler.index)
        self.assertTrue(
            "http://example.com/page1" in crawler.visited
        )  # Updated assertion
        self.assertTrue("http://example.com/page1" in crawler.index)
        self.assertTrue(
            "http://example.com/page2" in crawler.visited
        )  # Updated assertion
        self.assertTrue("http://example.com/page2" in crawler.index)
        self.assertEqual(crawler.links_found, 2)

    @patch("webcrawler.requests.get")
    def test_crawl_depth_limit(self, mock_get):
        # Set up mock response for a page with links to pages at different depths
        mock_response = MagicMock()
        mock_response.text = "<html><body><a href='http://example.com/page1'>Link 1</a><a href='http://example.com/page2'>Link 2</a></body></html>"
        mock_get.return_value = mock_response

        # Initialize crawler and call crawl method with depth limit
        crawler = WebCrawler()
        crawler.crawl("http://example.com", depth=1)

        # Assertions
        self.assertTrue("http://example.com" in crawler.visited)
        self.assertTrue("http://example.com" in crawler.index)
        self.assertTrue("http://example.com/page1" in crawler.visited)
        self.assertTrue("http://example.com/page1" in crawler.index)
        self.assertTrue("http://example.com/page2" in crawler.visited)
        self.assertTrue("http://example.com/page2" in crawler.index)
        self.assertEqual(crawler.links_found, 2)


if __name__ == "__main__":
    unittest.main()
