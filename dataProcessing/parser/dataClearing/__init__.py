flats.loc[flats['agency']=='None', 'agency'] = 'No'
flats.loc[flats['agency']!='No', 'agency'] = 'Yes'