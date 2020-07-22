import pandas as pd
import requests
import json
import os

import context
from utils import get_all_filenames
from avito_data import CatchError, SaveExceptions

class AreaGetter():

    def __init__(self):
        self.area = 'area'
        self.address = 'address'
        self.latitude = 'latitude'
        self.longitude = 'longitude'
        self.postal_code = 'postal_code'

    @SaveExceptions(msg="Getting area.")
    def execute(self):
        print("\n/////////\n/// AreaGetter part\n/////////")

        folder_path = context.store.get_csv_folder()
        all_filenames = get_all_filenames(folder_path)

        for filename in all_filenames:
            self.transform(filename)
            print("Filename {} was been transformed by openstreetmap.".format(filename))

    def transform(self, filename):
        flats = pd.read_csv(filename)

        flats[self.area] = ''

        for index, flat in flats.iterrows():
            address = flat[self.address]
            lat = flat[self.latitude]
            lon = flat[self.longitude]

            area = self.__rest_call(address, lat, lon)
            self.__update_file(address, flats, filename, area)

    @CatchError(msg="Rest call for getting area failled.")
    def __rest_call(self, address, lat, lon) -> str:
        url = 'https://nominatim.openstreetmap.org/reverse?format=geocodejson&lat=%s&lon=%s' % (lat, lon)
        response = requests.get(url)
        data = json.loads(response.text)

        admin = data['features'][0]['properties']['geocoding']['admin']
        try: 
            for i in range(9, 3, -1):
                    area = admin['level' + str(i)]
                    if "район" in str(area):
                        return area
        except Exception:
            print("Area not found for %s : %s" % (lat, lon))
        return "область"

    @CatchError(msg="Fail on update file with address on getting area")
    def __update_file(self, address, flats, filename, area):
        flats.loc[flats[self.address] == address, self.area] = area

        flats.to_csv(filename, index=False)

from store import Store 
if __name__ == "__main__":
    context.store = Store()
    AreaGetter().execute()