import os
from typing import List, Optional

from bs4 import BeautifulSoup

from avito_data import AvitoFlat, SaveExceptions
from avito_page_parser import PageParser
from store import Store

import context
from utils import get_all_filenames

class MainFeatureExtracter:

    def __init__(self):
        self.parser: PageParser = context.parser
        self.store: Store = context.store

    @SaveExceptions(msg="Main feature extraction part.")
    def execute(self):
        print("\n/////////\n/// MainFeatureExtracter part\n/////////")

        folder_path = self.store.get_html_folder()
        all_filenames = get_all_filenames(folder_path)

        for filename in all_filenames:
            flat_list = self.extract(filename)
            self.store.save_to_csv(flat_list, filename)   
            print("Filename {} converted to csv.".format(filename))        

    def extract(self, filename) -> List[AvitoFlat]:
        flat_list = []

        with open(filename) as f:
            page_content = f.read()

            tree = BeautifulSoup(page_content, 'html.parser')
            flats = self.parser.get_all_flats(tree)

            for flat_html in flats:
                flat = self.__flat_from(flat_html)
                flat_list.append(flat)

        return flat_list


    def __flat_from(self, flat_html) -> AvitoFlat:
        flat_floor, building_floor, =self.parser.get_floors(flat_html)
        
        flat = AvitoFlat(
            href=self.parser.get_href(flat_html),
            price=self.parser.get_price(flat_html),
            agency=self.parser.get_agency(flat_html),
            commission_percent=self.parser.get_commission_percent(flat_html),
            metro_distance=self.parser.get_metro_distance(flat_html),
            metro_station=self.parser.get_metro_station(flat_html),
            address=self.parser.get_address(flat_html),
            time_of_creation=self.parser.get_time_of_creation(flat_html),
            apartment_type=self.parser.get_apartment_type(flat_html),
            square=self.parser.get_apartment_square(flat_html),
            building_floor=building_floor,
            flat_floor=flat_floor
        )

        return flat

if __name__ == "__main__":
    MainFeatureExtracter().execute()

