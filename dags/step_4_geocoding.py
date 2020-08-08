import pandas as pd
import requests
import json
import os

import context
from utils import get_all_csv_filenames
from avito_data import SaveExceptions, CatchError

class Geocoder():
    def __init__(self):
        self.address = 'address'
        self.latitude = 'latitude'
        self.longitude = 'longitude'
        self.postal_code = 'postal_code'

    @SaveExceptions(msg="Geocoder call.")
    def execute(self):
        print("\n/////////\n/// Geocoder part\n/////////")

        all_filenames = get_all_csv_filenames()
        
        for filename in all_filenames:
            self.transform(filename)
            print("Filename {} was been transformed by geocoder.".format(filename))

    def transform(self, filename):
        flats = pd.read_csv(filename)

        self.__add_new_columns(flats)

        for address in flats.address:
            latitude, longitude, postal_code = self.__rest_call(address, flats)
            self.__update_flats(address, flats, latitude, longitude, postal_code)
        
        flats.to_csv(filename, index=False)


    @CatchError(msg="Rest call was failed !!!")
    def __rest_call(self, address, flats):

        address = self.__geocoder_bug_fix(address)
        address = (context.CITY+" "+address).replace(' ', '+')
        geocoder_url = 'https://geocode-maps.yandex.ru/1.x/?format=json&apikey=%s' \
                    '&geocode=%s' % (context.GEOCODER_KEY, address)
        
        try: 
            response = requests.get(geocoder_url)
            data = json.loads(response.text)
        except Exception:
            print("\n///////\nRest call to `{}` was faiiled\n//////\n".format(address))
            raise

        try:
            common_part = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
            longitude, latitude = str(common_part['Point']['pos']).split()
        except:
            print("Cannot extract longitude, latitude from \n{}\nby address: `{}`".format(data, address))
            raise

        try:
            postal_code = int(common_part['metaDataProperty']['GeocoderMetaData']['Address']['postal_code'])
        except Exception:
            postal_code = ''

        return latitude, longitude, postal_code

    def __geocoder_bug_fix(self, address: str) -> str:
        area_str = "район"
        if address.count(area_str) > 1:
            address = address.replace(area_str,"")
        return address

    @CatchError(msg="Fail on update file with address on geocoder")
    def __update_flats(self, address, flats, latitude, longitude, postal_code):
        flats.loc[flats[self.address] == address, self.latitude] = latitude
        flats.loc[flats[self.address] == address, self.longitude] = longitude
        flats.loc[flats[self.address] == address, self.postal_code] = postal_code


    def __add_new_columns(self, flats):
        flats[self.latitude] = ''
        flats[self.longitude] = ''
        flats[self.postal_code] = ''
