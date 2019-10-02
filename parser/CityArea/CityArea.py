import pandas as pd
import parser.Logger as log
import requests
import json

from parser.geocoder.Geocoder import prefix


def getArea():
    flats = pd.read_csv(prefix + 'updated_flats.csv')

    addNewColumns(flats)

    for index, row in flats.iterrows():
        address = row['adress']
        lat = row['latitude']
        lon = row['longitude']
        try:

            geoCoderUrl = 'https://nominatim.openstreetmap.org/reverse?format=geocodejson&lat=%s&lon=%s' % (lat, lon)
            responseGeoCoder = requests.get(geoCoderUrl)
            data = json.loads(responseGeoCoder.text)

            try:
                area = data['features'][0]['properties']['geocoding']['admin']['level9']
                flats.loc[flats['adress'] == address, 'area'] = area
            except Exception:
                log.error('Area not exist for: %s' % str(lat) + " " + str(lon))

            try:
                postalCode = data['features'][0]['properties']['geocoding']['postcode']
                flats.loc[flats['adress'] == address and (flats['postalCode'] == '' or flats['postalCode'] == None),
                          'postalCode'] = postalCode
            except Exception:
                log.error('Postal code not exist for: %s' % str(lat) + " " + str(lon))

            flats.to_csv(prefix + 'finish_flats.csv', index=False)
            log.info('Handling complete for: %s' % str(lat) + " " + str(lon))
        except Exception:
            log.error('Rest call for %s was failed !!!' % str(lat)+" "+str(lon))

def addNewColumns(flats):
    flats['area'] = ''


if __name__ == "__main__":
    getArea()