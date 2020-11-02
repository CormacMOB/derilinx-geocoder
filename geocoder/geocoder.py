from psycopg2 import connect, sql
from psycopg2.extras import NamedTupleCursor
import os
import re

DB_URI = os.environ.get("DB_URI", "postgresql://geocode:geocode@localhost:5432/geocode")


class AddressNotMatched(Exception):
    """
        The address could not be matched to county or better
    """

class AddressInputException(Exception):
    """
        The address was invalid, contained inappropriate charachters or wasn't an address.
    """


class DBConnector:
    connection = connect(DB_URI)

    def search_county(self, county_string):
        """
            Search for a county

            county (str): Candidate string of a county name
        """
        query = sql.SQL(
            """SELECT 
                    english_name, 
                    ST_Y(centroid) as y,
                    ST_X(centroid) as x
                 FROM counties
                 WHERE english_name ilike %s"""
        )
        cur = self.connection.cursor()
        cur.execute(query, (county_string,))
        return cur.fetchall()

    def search_townlands(self, townland_strings, county=None):
        """
            Search for townlands

            townland_strings (list): Ordered list of candidate strings of 
                townland names.
        """
        townland_strings.reverse()
        searches = []
        string_sql = []
        if county:
            where_clause = "WHERE county = '%s' AND" % county
        else:
            where_clause = "WHERE"
        for idx, candidate in enumerate(townland_strings):
            select_clause = """
                SELECT
                   english_name as name,
                   ST_Y(centroid) as y,
                   ST_X(centroid) as x,
                   county,
                   {} as idx
                FROM townlands
                {}
                    english_name ilike %s
                """.format(
                idx, where_clause,
            )
            searches.append(select_clause)
        query = sql.SQL("{} ORDER BY idx".format("UNION ".join(searches)))
        cur = self.connection.cursor(cursor_factory=NamedTupleCursor)
        cur.execute(query, townland_strings)
        return cur.fetchall()


class Address:
    """
        Abstraction for the composition of address queries and the return of
        matched address
    """

    county = None
    townland = None
    x_coord = None
    y_coord = None

    def __init__(self, addr_string):
        self.string = addr_string
        self.clean_string = self.clean_addr_string()
        self.make_address_elements()

    def __repr__(self):
        return "Address object for {}".format(self.string)

    @property
    def coords(self):
        if self.x_coord and self.y_coord:
            return "{y_coord},{x_coord}".format(
                y_coord=self.y_coord, x_coord=self.x_coord
            )

    def make_address_elements(self):
        """
            Split the address into sub elements
        """
        self.comma_split_elements = [x.strip() for x in self.clean_string.split(",")]

    def clean_addr_string(self):
        """
        Remove unsafe and unnecessary characters and space from strings.

        This will remove empty comma delimited fragments before we divide up the string
        for matching.
        """
        addr_string = self.string[:]
        blacklist = ['"', ";", ":"]
        for pattern in blacklist:
            addr_string = addr_string.replace(pattern, "")

        # Clear off any unnecessary blank spots
        addr_string = re.sub(r",\s+,", ",", addr_string)
        return addr_string.upper()

    def pop_townland(self, result_set):
        """
            Extract townland data from result record.
            
            If there are multiple townlands at an index 
            and that index is the lowest index, reject that index
        """
        index_array = [x.idx for x in result_set]
        rv = None
        for item in result_set:
            if index_array.count(item.idx) > 1:
                continue
            else:
                rv = item
        return rv
            

    def geocode(self):
        """
            Query database for the components of the address
        """
        connection = DBConnector()

        # WHAT IF THERE IS NO ADDRESS???
        county_search = connection.search_county(self.comma_split_elements[-1])
        if len(county_search) > 0:
            self.county, self.y_coord, self.x_coord = county_search.pop()

        townland_search = connection.search_townlands(
            self.comma_split_elements[:-1], self.county
        )
        if not self.county and len(townland_search) == 0:
            raise AddressNotMatched

        townland = self.pop_townland(townland_search)
        if townland:
            self.townland = townland.name
            self.y_coord = townland.y
            self.x_coord = townland.x

