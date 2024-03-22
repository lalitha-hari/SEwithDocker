import unittest
from ranker import Ranker  # Assuming your ranker code is in a file named "ranker.py"

class TestRanker(unittest.TestCase):
    def setUp(self):
        self.ranker = Ranker()

    def test_rank_results_single_keyword(self):
        index = {
            "http://example1.com": "Sample text with keyword keyword",
            "http://example2.com": "Another sample text without keyword"
        }
        keyword = "keyword"
        results = ["http://example1.com", "http://example2.com"]
        ranked_results = self.ranker.rank_results(results, index, keyword)
        
        # Check if the ranking is done correctly
        expected_ranking = {"http://example1.com": 2, "http://example2.com": 1}
        self.assertEqual(ranked_results, expected_ranking)

    def test_rank_results_same_keyword_multiple_occurrences(self):
        index = {
            "http://example1.com": "Sample text with keyword keyword",
            "http://example2.com": "Another sample text with keyword keyword keyword"
        }
        keyword = "keyword"
        results = ["http://example1.com", "http://example2.com"]
        ranked_results = self.ranker.rank_results(results, index, keyword)
        
        # Check if the ranking is done correctly
        expected_ranking = {"http://example1.com": 2, "http://example2.com": 3}
        self.assertEqual(ranked_results, expected_ranking)

    def test_rank_results_no_keyword_occurrence(self):
        index = {
            "http://example1.com": "Sample text without keyword",
            "http://example2.com": "Another sample text without keyword"
        }
        keyword = "keyword"
        results = ["http://example1.com", "http://example2.com"]
        ranked_results = self.ranker.rank_results(results, index, keyword)
        
        # Check if the ranking is done correctly (all URLs should have rank 0)
        expected_ranking = {"http://example1.com": 1, "http://example2.com": 1}
        self.assertEqual(ranked_results, expected_ranking)


if __name__ == "__main__":
    unittest.main()
