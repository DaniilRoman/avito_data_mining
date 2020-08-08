import datetime
import re

import numpy as np
import pandas as pd

def remove_duplicates(flats):
    flats.drop_duplicates(subset ="href", keep = "first", inplace = True) 
def clear_apartment_type(flats):
    flats.apartment_type = flats.apartment_type.apply(lambda x: x.replace("\n ", ""))
def cast_postal_code(flats):
    flats.postal_code = flats.postal_code.astype('Int32')
def rename_floor_column(flats):
    flats.rename(columns={'flat_floor':'apartment_floor'}, inplace=True)
def add_apartment_type_order_column(flats):
    flats['apartment_type_order'] = flats.apartment_type.map({'Студия': 0, '1-к квартира': 1, '2-к квартира': 2, '3-к квартира': 3, '4-к квартира': 4, '5-к квартира': 5})
def sort_by_apartment_type(flats):
    flats = flats.sort_values('apartment_type_order')
    
def _distance_convert(distance):    
    if distance is not np.nan:
        first_part = re.findall(r'\d+',distance)[0]
        if 'км' in distance:
            result = re.findall(r',\d+',distance)
            if len(result) != 0:
                result = result[0].replace(',','')
                first_part = int(float(first_part+result)*100)
            else:
                first_part = int(first_part)*1000
        return int(first_part)
    return distance
def compute_converted_distance(flats):
    flats['converted_distance'] = flats.metro_distance.apply(_distance_convert)


def _apartment_floor_to_group(apartment_floor, building_floor):
    if apartment_floor < 2:
        return 'button'
    if building_floor - apartment_floor < 1:
        return 'up'
    return 'middle'
def compute_apartment_floor_group(flats):
    flats['apartment_floor_group'] = flats.apply(
        lambda row: _apartment_floor_to_group(row['apartment_floor'], row['building_floor']), 
        axis=1)

def _area_to_city_side(area):
    if area in ['Приокский район', 'Советский район', 'Нижегородский район']:
        return 'Нагорная часть'
    if area in ['Автозаводский район', 'Канавинский район', 'Ленинский район', 'Московский район', 'Сормовский район']:
        return 'Заречная часть'
    return 'область'
def compute_city_side(flats):
    flats['side'] = flats.area.apply(_area_to_city_side)
    

def _clear_countryside_area(area):
    if area in ['Приокский район', 'Советский район', 'Нижегородский район','Автозаводский район', 'Канавинский район', 'Ленинский район', 'Московский район', 'Сормовский район']:
        return area
    return 'область'
def clear_countryside_area(flats):
    flats['area'] = flats.area.apply(_clear_countryside_area)

def _building_floor_to_floor_group(floor):
    if floor < 6:
        return 1
    if floor < 12:
        return 2
    return 3
def compute_floor_group(flats):
    flats['floor_group'] = flats.building_floor.apply(_building_floor_to_floor_group)