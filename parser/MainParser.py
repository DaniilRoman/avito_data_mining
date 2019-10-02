import requests
import numpy as np
from bs4 import BeautifulSoup
from time import sleep

from parser.OnePageData import handleOnePage
from parser.VipOrderHandler import handleVipOrder


def parse():
    startPage = 1
    endPage = 50
    for pageNumber in range(startPage, endPage):

        url = 'https://www.avito.ru/nizhniy_novgorod/kvartiry/sdam/na_dlitelnyy_srok?p=%s' % pageNumber
        response = requests.get(url)

        if response.status_code == 404:
            exit(1)

        tree = BeautifulSoup(response.content, 'html.parser')

        handleVipOrder(tree)

        dates = tree.find_all('div', {'class': 'js-item-date'})
        flats = tree.find_all('div', {'class': 'description item_table-description'})

        handleOnePage(flats, dates, pageNumber)

        randomSleep()


def randomSleep():
    r = np.random.normal(size=1, loc=5, scale=2)
    if r < 1:
        r = 1.2345
    if r > 8:
        r = 6.6666
    sleep(r)
