import unittest
from flask_testing import TestCase as FTestCase
from validator import validate_address
from webapp import create_app

class TestAddressValidator(unittest.TestCase):
    """
        Test that the validator validates addresses correctly
    """
    def test_string_is_empty(self):
        self.assertFalse(validate_address(" "))

    def test_special_chars(self):
        self.assertFalse(validate_address("@@@@@,lo!//,Cork"))

    def test_good_address_string(self):
        self.assertTrue(validate_address("Ludlow, charlesland, Greystones, Wicklow"))

class WebTestCase(FTestCase):

    def create_app(self):
        app = create_app()
        app.config["TESTING"] = True
        return app

    def setUp(self):
        self.app = create_app()

    def test_bad_address(self):
        response = self.client.get('/geocode?address=@@@@@..&&33,boots')
        self.assertEqual(response.status_code, 400)

    def test_no_match(self):
        response = self.client.get('/geocode?address=ballything, thingytown, bork')
        self.assertEqual(response.status_code, 404)

    def test_matching_address(self):
        response = self.client.get('/geocode?address=ludlow,charlesland,wicklow')



if __name__ == "__main__":
    unittest.main()
