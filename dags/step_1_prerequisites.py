import re 
import requests

from typing import List
from bs4 import BeautifulSoup
from bs4 import NavigableString

from store import Store 
from avito_page_parser import PageParser

from avito_data import SaveExceptions

import context

class Prerequisites:
    @SaveExceptions(msg="Prerequisites part.")
    def execute(self):
        print("\n/////////\n/// Prerequisites part\n/////////")

        parser = context.parser

        response = requests.get(context.BASE_URL.format(1))
        tree = BeautifulSoup(response.content, 'html.parser')
        flats = parser.get_all_flats(tree)

        for flat in flats:
            parser.get_href(flat)

            parser.get_price(flat)

            parser.get_commission_percent(flat)

            parser.get_agency(flat)

            parser.get_commission_percent(flat)

            parser.get_metro_distance(flat)

            parser.get_address(flat)

            parser.get_metro_station(flat)

            parser.get_apartment_type(flat)

            parser.get_apartment_square(flat)

            parser.get_floors(flat)

            parser.get_time_of_creation(flat)

        print("Prerequisites for flats extracted.")