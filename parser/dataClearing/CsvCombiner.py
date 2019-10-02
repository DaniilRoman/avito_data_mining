import os
import glob
import pandas as pd

def combineCsv():
    os.chdir("data")
    all_filenames = [i for i in glob.glob('*.csv')]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    combined_csv.to_csv("flats.csv", index=False, encoding='utf-8-sig')