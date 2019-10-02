import re

import parser.Logger as log
from parser.Writer import writeErrorTree, writeToFile


def handleOnePage(flats, dates, pageNumber):
    flatList = []
    for flat, date in zip(flats, dates):
        try:
            flatDict = {}

            # PART 1
            href = flat.find('h3', {'class': 'title'}).find('a')['href']
            flatDict['href'] = href

            price = flat.find('span', {'class': 'price'})['content']
            flatDict['price'] = price

            agency = getAgency(flat)
            flatDict['agency'] = agency

            commissionPercent = getCommissionPercent(flat)
            flatDict['commissionPercent'] = commissionPercent

            # PART 2
            geo = flat.find('p', {'class': 'address'})

            metroDistance = getMetroDistance(geo)
            flatDict['metroDistance'] = metroDistance

            metroStation, adress = getMetroStationAndAdress(geo.contents)
            flatDict['metroStation'] = metroStation
            flatDict['adress'] = adress

            metroLine = getMetroLine(geo)
            flatDict['metroLine'] = metroLine

            # PART 3
            commonInfo = flat.find('h3', {'class': 'title'}).find('a').find('span').text

            apartmentType, apartmentSquare, floor = commonInfo.split(',')
            flatDict['apartmentType'] = apartmentType

            apartmentSquare = getClearApartmentSquare(apartmentSquare)
            flatDict['apartmentSquare'] = apartmentSquare

            apartmentFloor, buildingFloor = re.findall(r'\d+', floor)
            flatDict['apartmentFloor'] = apartmentFloor
            flatDict['buildingFloor'] = buildingFloor

            # PART 4
            flatDict['absoluteTime'] = date['data-absolute-date']
            try:
                flatDict['relativeTime'] = date['data-relative-date']
            except Exception:
                flatDict['relativeTime'] = None

            flatList.append(flatDict)

            log.info("Handling page `%s`: SUCCESS" % pageNumber)
        except Exception:
            href = flat.find('h3', {'class': 'title'}).find('a')['href']
            writeErrorTree(href + "\n\n" + str(flatDict) + "\n\n" + str(flat) + "\n\n" + str(date))
            log.error("Handling page `%s`: ERROR" % pageNumber)
    writeToFile(flatList, pageNumber)



def getClearApartmentSquare(dirtyApartmentSquare):
    match = re.search(r'\d+.\d+', dirtyApartmentSquare)
    if match:
        clearApartmentSquare = match.group()
    else:
        match = re.search(r'\d+', dirtyApartmentSquare)
        if match:
            clearApartmentSquare = match.group()
        else:
            clearApartmentSquare = 'ERROR'
    return clearApartmentSquare


def getMetroStationAndAdress(data):
    results = list(
        filter(lambda x: x != '' and '</i>' not in x and '</span>' not in x,
               map(lambda x: clearData(x).replace('\xa0', ' '),
                   map(lambda x: str(x).replace('<nobr>', ' ').replace('</nobr>', ' '),
                       data)
                   )
               )
    )
    metroStation = results[0]
    adress = ' '.join(results[1:])
    return metroStation, adress


def clearData(data):
    return re.sub('^\s+|\n|\r|\s+$', '', data)


def getCommissionPercent(flat):
    commissionPercent = flat.find('span', {'class': 'about__commission'})
    if commissionPercent == None:
        commissionPercent = '0 %'
    else:
        commissionPercent = clearData(commissionPercent.text)
    return commissionPercent


def getAgency(flat):
    agency = flat.find('div', {'class': 'data'})
    if agency == None:
        agency = 'None'
    else:
        agency = clearData(agency.text)
    return agency


def getMetroDistance(geo):
    metroDistance = geo.find('span')
    if metroDistance == None:
        metroDistance = 'None'
    else:
        metroDistance = metroDistance.text
    return metroDistance


def getMetroLine(geo):
    metroLine = geo.find('i')
    if metroLine == None:
        metroLine = 'None'
    else:
        metroLine = metroLine['title']
    return metroLine
