import datetime
import locale
import re
from typing import List, Optional, Tuple

from avito_data import CatchError

class PageParser:
    def __init__(self):
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        self.year = datetime.datetime.today().year

    def get_all_flats(self, tree):
        flats = tree.find_all('div', {'class' : 'description item_table-description'})
        return flats

    @CatchError(msg="Cannot parse commission percent.")
    def get_commission_percent(self, flat) -> Optional[int]:
        commission_percent = flat.find('span', {'class' : 'snippet-price-commission'})
        if commission_percent == None or ("без комиссии" in str(commission_percent)):
            commission_percent = 0
        else:
            percent =re.search(r'\d+', self.clear_data(commission_percent.text))
            if percent is not None:
                commission_percent = int(percent.group())
            else:
                raise Exception("Cannot parse commission percent.")
        return commission_percent

    @CatchError(msg="Cannot parse time of creation.")
    def get_time_of_creation(self, flat) -> str:
        time_of_creation = flat.find('div', {"data-marker": "item-date"}).get("data-tooltip")
        if time_of_creation == "":
            time_of_creation = flat.find('div', {"data-marker": "item-date"}).text
            time_of_creation = self.clear_data(time_of_creation)
        time_of_creation = str(self.year)+ " " + time_of_creation
        try:
            result_date = datetime.datetime.strptime(time_of_creation, u'%Y %d %B %H:%M')
        except Exception:
            result_date = datetime.datetime.strptime(time_of_creation, u'%Y %d %b %H:%M')
    
        return str(result_date)

    @CatchError(msg="Cannot parse agency.")
    def get_agency(self, flat) -> Optional[str]:
        agency = flat.find('div', {'class' : 'data'}).find('p')
        if agency is not None:
            agency = self.clear_data(agency.text)
        return agency 

    @CatchError(msg="Cannot parse href.")
    def get_href(self, flat) -> str:
        return flat.find('h3', {'data-marker' : 'item-title'}).find('a')['href']

    @CatchError(msg="Cannot parse price.")
    def get_price(self, flat) -> int:
        price = flat.find('span', {'data-marker' : 'item-price'}).text
        price = list(filter(str.isdigit, price))
        price = int("".join(price))
        return price

    @CatchError(msg="Cannot parse apartment type.")
    def get_apartment_type(self, flat) -> str:
        apartment_type, apartment_square_str, floor_info = self.__get_common_info(flat)
        return self.clear_data(apartment_type)

    @CatchError(msg="Cannot parse apartment square.")
    def get_apartment_square(self, flat) -> float:
        apartment_type, apartment_square_str, floor_info = self.__get_common_info(flat)
        apartment_square_tmp = re.search(r'\d+(.\d+)?', apartment_square_str)
        if apartment_square_tmp is not None:
            apartment_square = apartment_square_tmp.group()
        else: 
            raise Exception("Cannot parse apartment square.")
        return apartment_square

    @CatchError(msg="Cannot parse apartment floor.")
    def get_floors(self, flat) -> Tuple[int, int]:
        apartment_type, apartment_square_str, floor_info = self.__get_common_info(flat)
        flat_floor, building_floor = re.findall(r'\d+', floor_info)
        return flat_floor, building_floor 

    @CatchError(msg="Cannot parse metro distance.")
    def get_metro_distance(self, flat) -> Optional[str]:
        metro_distance = flat.find('span', {'class':'item-address-georeferences-item__after'})
        if metro_distance != None:
            metro_distance = self.clear_data(metro_distance.text)
        return metro_distance

    @CatchError(msg="Cannot parse metro station.")
    def get_metro_station(self, flat) -> str:
        if (self.get_metro_distance(flat) is None):
            return "без метро"
        return flat.find('span', {'class':'item-address-georeferences-item__content'}).text


    @CatchError(msg="Cannot parse address.")
    def get_address(self, flat) -> str:
        return self.clear_data(flat.find('span', {'class' : 'item-address__string'}).text)


    def clear_data(self, data) -> str:
        return re.sub('^\s+|\n|\r|\s+$', '', data).replace('\xa0', ' ')

    @CatchError(msg="Cannot parse common info.")
    def __get_common_info(self, flat):
        apartment_type, apartment_square_str, floor_info = flat.find('h3', {'data-marker' : 'item-title'}).find('a').text.split(',')
        return apartment_type, apartment_square_str, floor_info
