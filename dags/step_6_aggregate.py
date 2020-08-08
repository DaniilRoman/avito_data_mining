import pandas as pd

import context
from utils import get_all_filenames
from avito_data import CatchError, SaveExceptions

class Aggregator():
    @SaveExceptions(msg="Aggregation.")
    def execute(self):
        print("\n/////////\n/// Aggregator part\n/////////")

        folder_path = context.store.get_csv_folder()
        all_filenames = get_all_filenames(folder_path)
        self.__aggregate(all_filenames)


    @CatchError(msg="Aggregate csv files.")
    def __aggregate(self, filenames):
        print(filenames)
        aggregated_csv = pd.concat([pd.read_csv(f) for f in filenames])
        context.store.to_csv(aggregated_csv)