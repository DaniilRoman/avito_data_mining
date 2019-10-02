import pandas as pd
import parser.Logger as log
import requests
import json

from parser.Writer import writeEncoderError

prefix = '../../'

def setCoordinates():
    flats = pd.read_csv(prefix + 'flats_after_clear_adress.csv')

    addNewColumns(flats)

    for address in flats.adress:
        try:
            restCallAndUpdateData(address, flats)
        except Exception:
            log.error('Rest call for %s was failed !!!' % address)

    print('OK')

def prepareAddress(address):
    return address.replace(' ', '+')

def restCallAndUpdateData(address, flats):
    try:
        data = None
        address = str(address)
        preparedAddress = prepareAddress(address)
        geoCoderUrl = 'https://geocode-maps.yandex.ru/1.x/?format=json&apikey=c90067e4-8c6e-4738-8b70-0a0386fa3fdc' \
                      '&geocode=%s' % preparedAddress
        responseGeoCoder = requests.get(geoCoderUrl)
        data = json.loads(responseGeoCoder.text)

        commonPart = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        longitude, latitude = str(commonPart['Point']['pos']).split()

        try:
            postalCode = commonPart['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
        except Exception:
            postalCode = ''

        flats.loc[flats['adress'] == address, 'latitude'] = latitude
        flats.loc[flats['adress'] == address, 'longitude'] = longitude
        flats.loc[flats['adress'] == address, 'postalCode'] = postalCode

        flats.to_csv(prefix + 'updated_flats.csv', index=False)
        log.info('Info for address: %s successful writen' % address)
    except Exception:
        if data != None:
            writeEncoderError(address + "\n\n" + str(data))
        else:
            writeEncoderError(address + "\n\n" 'response dont exist')

def addNewColumns(flats):
    flats['latitude'] = ''
    flats['longitude'] = ''
    flats['postalCode'] = ''
