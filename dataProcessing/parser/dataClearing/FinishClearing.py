import pandas as pd
import time
import datetime
import re

def clear():
    flats = pd.read_csv('flats.csv')
    flats = flats.drop(['href', 'adress'], axis=1)
    flats.agency = flats.agency.fillna('Нет')
    print(flats.agency.unique())
    flats.commissionPercent = flats.commissionPercent.str.replace(' %', '').replace('без комиссии', '0').astype('int64')
    print(flats.commissionPercent.unique())
    flats.metroDistance = flats.metroDistance.transform(lambda x: metroDistanceTransform(x))
    print(flats.metroDistance.unique())
    print(flats.metroStation.unique())
    print(flats.apartmentType.unique())
    flats.relativeTime = flats.relativeTime.fillna('более месяца назад')
    print(flats.relativeTime.unique())
    flats.postalCode = flats.postalCode.astype('int64')
    print(flats.area.unique())
    flats.absoluteTime = flats.absoluteTime.str.replace('Вчера', '28 сентября').replace('Сегодня', '29 сентября')
    flats.rename(columns={'price': 'y'}, inplace=True)
    flats.y = flats.y.transform(lambda x: getY(x))
    print(flats['absoluteTime'].apply(lambda x: re.findall(r'[а-яА-Я]+', x)[0]).unique())
    flats['absoluteTime'] = \
                flats['absoluteTime'].apply(lambda x: 
                                ('2019 '+str(x)).strip().replace('\xa0',' ').replace('сентября','9').replace('Сегодня', '28 9').replace('августа', '8'))
    flats['absoluteTime'] = \
                flats['absoluteTime'].apply(lambda x: 
                                int(time.mktime(datetime.datetime.strptime(x, "%Y %d %m %H:%M").timetuple())))    
    flats.to_csv('flats_data.csv', index=False)

def getY(x):
    if x <= 10000:
        return 1
    if x > 10000 and x <= 15000:
        return 2
    if x > 15000 and x <= 20000:
        return 3
    return 4

def metroDistanceTransform(x):
    if ' м' in x:
        return int(x.replace(' м', ''))
    if ' км' in x:
        return int(float(x.replace(' км', ''))*1000)