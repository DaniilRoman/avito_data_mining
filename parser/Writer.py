import os
import csv
from time import time

import parser.Logger as log

currentDir = lambda fileName: os.path.join(fileName)

def pathToFile(fileName, subDir='data'):
    return os.path.join(subDir, fileName)


def writeToFile(flats, pageNumber):
    csvColumns = ['href', 'price', 'agency', 'commissionPercent', 'metroDistance', 'metroStation', 'adress',
                  'metroLine', 'apartmentType', 'apartmentSquare', 'apartmentFloor', 'buildingFloor', 'absoluteTime',
                  'relativeTime']
    fileName = "flats_%s.csv" % pageNumber
    path = pathToFile(fileName)
    try:
        with open(path, 'w') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=csvColumns)
            writer.writeheader()
            for flat in flats:
                writer.writerow(flat)
    except IOError:
        log.error("Writing in csv file `%s`!" % fileName)


def writeErrorTree(tree):
    name = str(time())
    fileName = "%s.txt" % name
    path = pathToFile(fileName, 'errorTrees')
    try:
        with open(path, 'w') as file:
            file.write(tree)
            log.info("Error tree has been wrote for flat: %s." % name)
    except IOError:
        log.error("Writing in file `%s`! \nTree:\n%s " % (fileName, tree))

def writeEncoderError(response):
    fileName = str(time()).replace('.', '')+'.txt'
    path = pathToFile(fileName, '../../geocoderError')
    try:
        with open(path, 'w') as file:
            file.write(response)
            log.info("Error response has been wrote for file: %s." % fileName)
    except IOError:
        log.error("Writing in file `%s`! \nResponse:\n%s " % (fileName, response))

def writeVipHrefs(list):
    fileName = "vipHrefList.txt"
    path = pathToFile(fileName, 'vipHrefList')
    try:
        with open(path, 'a') as file:
            file.write(str(list))
            log.info("Href list has been wrote.")
    except IOError:
        log.error("Writing in file `%s`!" % fileName)
