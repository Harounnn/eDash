# Imports
import glob



class DataIngestion():
    def __init__(self):
        pass

    def get_csv_files_paths(self):

        csv_files_paths = glob.glob("Notebook\dataset\*.csv")
        
        return csv_files_paths