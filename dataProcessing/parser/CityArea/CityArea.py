import pandas as pd
import dataProcessing.parser.Logger as log
import requests
import json

from dataProcessing.parser.geocoder import prefix


def getArea():
    flats = pd.read_csv(prefix + 'flats.csv')

    # filteredFlats = flats[flats.postalCode.isnull()]

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
                admin = data['features'][0]['properties']['geocoding']['admin']
                for i in range(9, 3, -1):
                    try:
                        area = admin['level' + str(i)]
                        if "район" in str(area):
                            flats.loc[flats['adress'] == address, 'area'] = area
                            break
                    except Exception:
                        pass

            except Exception:
                log.error('Area not exist for: %s' % str(lat) + " " + str(lon))

            try:
                postalCode = data['features'][0]['properties']['geocoding']['postcode']
                flats.loc[(flats['adress'] == address) & (flats['postalCode'].isnull()),
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