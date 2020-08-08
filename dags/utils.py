import os
import context

def get_all_filenames(folder_path):
    return [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)]


def get_all_csv_filenames():
    folder_path = context.store.get_csv_folder()
    return [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)]
