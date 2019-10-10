import pandas as pd

def addVipStatus():
    flats = pd.read_csv('finish_flats.csv')
    filepath = 'vipHrefList/vipHrefList.txt'
    with open(filepath) as fp:
        txt = fp.read()
        txt = txt.replace('][', '\n').replace(', ', '\n').replace('[', '').replace(']', '').replace('\'', '')
    newFile = 'vipHrefList/vip.txt'
    with open(newFile, 'w') as f:
        f.write(txt)
    vips = []
    with open(newFile) as fp:
        line = fp.readline()
        while line:
            line = fp.readline()
            vips.append(str(line).replace(' ', '').replace('\n', '').replace('\'', ''))
    flats['vip'] = 'No'
    flats.loc[flats['href'].isin(vips), 'vip'] = 'Yes'
    flats.to_csv('flatsWithVip')

if __name__ == "__main__":
    addVipStatus()