import unittest
from utils import clean_address, extract_property_data

class TestZillowAgentIntelligence(unittest.TestCase):

    def test_address_slugification(self):
        """Ensure messy user input is converted to Zillow-compatible slugs."""
        self.assertEqual(clean_address("123 Main St, Vancouver!"), "123-Main-St-Vancouver")
        self.assertEqual(clean_address("  Apt 4, 500 Broadway  "), "Apt-4-500-Broadway")

    def test_rental_detection(self):
        """Verify the agent identifies rentals and prioritizes rentZestimate."""
        mock_rental_html = """
            <html>
                <body>
                    <span>This property is "ForRent"</span>
                    <script>
                        var data = {
                            "rentZestimate": 2500,
                            "zestimate": 450000,
                            "price": null
                        };
                    </script>
                </body>
            </html>
        """
        result = extract_property_data(mock_rental_html)
        self.assertEqual(result["label"], "Monthly Rent")
        self.assertEqual(result["price"], "2500")

    def test_sale_detection(self):
        """Verify the agent identifies listings for sale and prioritizes price."""
        mock_sale_html = """
            <html>
                <body>
                    <script>
                        var data = {
                            "price": 525000,
                            "zestimate": 510000
                        };
                    </script>
                </body>
            </html>
        """
        result = extract_property_data(mock_sale_html)
        self.assertEqual(result["label"], "Listing Price")
        self.assertEqual(result["price"], "525000")

    def test_off_market_fallback(self):
        """Verify fallback to Zestimate when no active listing price exists."""
        mock_off_market_html = """
            <html>
                <body>
                    <script>
                        var data = {
                            "price": null,
                            "zestimate": 485000
                        };
                    </script>
                </body>
            </html>
        """
        result = extract_property_data(mock_off_market_html)
        self.assertEqual(result["label"], "Sales Zestimate")
        self.assertEqual(result["price"], "485000")

if __name__ == "__main__":
    unittest.main()