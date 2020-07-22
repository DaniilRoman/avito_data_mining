import os

def get_all_filenames(folder_path):
    return [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)]
