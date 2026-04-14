import unittest
from utils import clean_address, extract_price

class TestAgentTools(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(clean_address("123 Main St, WA!"), "123-Main-St-WA")

    def test_extraction(self):
        html = '{"price": 450000}'
        self.assertEqual(extract_price(html), "450000")

if __name__ == "__main__":
    unittest.main()