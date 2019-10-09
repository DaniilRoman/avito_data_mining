import pandas as pd

def clearDataAndSave():
    flats = pd.read_csv('flats.csv')
    clearAdress(flats)
    flats.to_csv('flats_after_clear_adress.csv', index=False)

def clearAdress(flats):
    flats.adress = flats.adress.apply(filterSpaceInStart)
    flats.loc[flats['adress'].str
             .contains('новгород', case=False) == False, 'adress'] \
        = 'Нижний Новгород, ' + flats['adress']

def filterSpaceInStart(string):
    string = str(string).strip()
    count = 0
    for c in string:
        if c != ' ' and c != ',':
            break
        count = count + 1
    return string[count:]