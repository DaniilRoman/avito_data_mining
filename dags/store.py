import csv
import datetime
import pickle
from pathlib import Path
from typing import List

from utils import get_all_filenames
from avito_data import AvitoFlat, ParseException

from context import FOLDER_CITY_PREFIX


class Store:

    _EXCEPTIONS_FOLDER: str = "./exceptions/" + FOLDER_CITY_PREFIX
    _EXCEPTIONS_FILE_PATH = _EXCEPTIONS_FOLDER + "/{}__{}.txt"
    _exceptions_count = 1

    _HTML_PAGES_FOLDER: str = "./avito_html_pages/" + FOLDER_CITY_PREFIX
    _CSV_PAGES_FOLDER: str = "./avito_csv_pages/" + FOLDER_CITY_PREFIX
    _RESULT_FOLDER: str = "./avito"

    _RESULT_FILE_PATH = _RESULT_FOLDER + "/" + FOLDER_CITY_PREFIX + "_flats_{}.csv"

    def __init__(self):
        # create folders if not exists
        for folder in [self._EXCEPTIONS_FOLDER, self._HTML_PAGES_FOLDER, self._CSV_PAGES_FOLDER, self._RESULT_FOLDER]:
            Path(folder).mkdir(parents=True, exist_ok=True)

        for folder in [self._HTML_PAGES_FOLDER, self._CSV_PAGES_FOLDER]:
            folder = folder+"/"+self._get_current_date()
            Path(folder).mkdir(parents=True, exist_ok=True)

    def get_html_folder(self):
        return self._get_current_folder(self._HTML_PAGES_FOLDER)
    def get_csv_folder(self):
        return self._get_current_folder(self._CSV_PAGES_FOLDER)
    def get_exception_file_name(self):
        return self._EXCEPTIONS_FILE_PATH.format(self._get_current_date(), self._exceptions_count)

    def save_exceptions(self, exceptions: List[ParseException]):
        new_file_name = self.get_exception_file_name()
        self._exceptions_count+=1

        with open(new_file_name, 'wb') as f:
            pickle.dump(exceptions, f)
        print('Exceptions have been saved to {}'.format(new_file_name))

    def get_exceptions(self) -> List[ParseException]:
        filenames = get_all_filenames(self._EXCEPTIONS_FOLDER)
        exceptions = []
        
        for filename in filenames:
            with open(filename, 'rb') as f:
                exceptions += pickle.load(f)
        return exceptions
        
    def save_html_page(self, page_number, response):
        file_name = self.get_html_folder()+"/"+str(page_number)+".txt"

        with open(file_name, 'w') as f:
            f.write(str(response))
        print('Page `{}` have been saved.'.format(page_number))

    def save_to_csv(self, flat_list: List[AvitoFlat], html_fileame: str):
        csv_file_name = html_fileame.replace("html", "csv").replace("txt", "csv")
        with open(csv_file_name, 'w') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            wr.writerow(AvitoFlat.get_fields())
            for flat in flat_list:
                wr.writerow(flat.as_tuple())

    def to_csv(self, pandas_file):
        pandas_file.to_csv(self._RESULT_FILE_PATH.format(self._get_current_date()), index=False, encoding='utf-8-sig')
        print('Flats have been saved.')

    def _get_current_folder(self, folder) -> str:
        return folder+"/"+self._get_current_date()

    def _get_current_date(self) -> str:
        return str(datetime.date.today())
    
# if __name__ == "__main__":
    # Store().save_prerequisites_exceptions(["test1", "test2", "test3"])
