import unittest
from geocoder import DBConnector, Address, AddressNotMatched


class TestDBConnecter(unittest.TestCase):
    def setUp(self):
        self.c = DBConnector()

#    def test_search_townlands_sql_two_cases


class TestAddressCleaner(unittest.TestCase):
    def test_removes_deadspace(self):
        addr = Address("Cullionmore, , Mullingar, westmeath")
        self.assertEqual(addr.clean_string, "CULLIONMORE, MULLINGAR, WESTMEATH")

    def test_removes_dangerous_quotes(self):
        addr = Address('"Gavarnie", Ballinluska, Myrtleville, cork')
        self.assertEqual(addr.clean_string, "GAVARNIE, BALLINLUSKA, MYRTLEVILLE, CORK")


class TestAddressMatching(unittest.TestCase):

    def test_no_county_match(self):
        with self.assertRaises(AddressNotMatched):
            addr = Address("IMAGINARY ROAD, Imagination towm, bork")
            addr.geocode()

    def test_county_only_match(self):
        """
            test case: County Match: IMAGINARY ROAD, Imagination towm, Cork
        """
        addr = Address("IMAGINARY ROAD, Imagination towm, Cork")
        addr.geocode()
        self.assertEqual(addr.county, "CORK")
        self.assertEqual(addr.coords, "51.9884703543651,-8.76435435924216")

    def test_single_townland_match(self):
        addr = Address('Athlone Road, Ballymahon, longford')
        addr.geocode()
        self.assertEqual(addr.county, "LONGFORD")
        self.assertEqual(addr.townland, "BALLYMAHON")
        self.assertEqual(addr.coords, "53.5676604590877,-7.76816605599285")

    def test_two_townland_match(self):
        addr = Address('"Gavarnie", Ballinluska, Myrtleville, cork')
        addr.geocode()
        self.assertEqual(addr.county, "CORK")
        self.assertEqual(addr.townland, "BALLINLUSKA")
        self.assertEqual(addr.coords, "51.7862120962233,-8.3020631444478")
    
    def test_single_townland_multiple_results_match(self):
        """
            test case: Townland Match: Ocean Drive, Annagh, kerry 
        """
        addr = Address("Ocean Drive, Annagh, kerry")
        addr.geocode()
        self.assertEqual(addr.county, "KERRY")
        self.assertEqual(addr.townland, None)
        # County centroid
        self.assertEqual(addr.coords, "52.1678959322447,-9.52598126090479")

    def test_multiple_townland_multiple_results_match_for_one(self):
        """
            test case: Townland Match: Ocean Drive, Annagh, kerry 
        """
        addr = Address("Castlemaine, Annagh, kerry")
        addr.geocode()
        self.assertEqual(addr.county, "KERRY")
        self.assertEqual(addr.townland, "CASTLEMAINE")
        # County centroid
        self.assertEqual(addr.coords, "52.167712772052,-9.70351356052294")


# test case: locality match: Ocean Drive, Annagh, kerry

# test case: Missing Comma:  BALLINGOWAN KILLARNEY ROAD, Tralee, kerry


if __name__ == "__main__":
    unittest.main()
