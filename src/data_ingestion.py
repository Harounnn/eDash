# Imports
import glob



class DataIngestion():
    def __init__(self):
        pass

    def get_csv_files_names(self):
        csv_files_names = []

        csv_files_path = glob.glob("Notebook\dataset\*.csv")

        for csv_file_path in csv_files_path:
            csv_files_names.append(csv_file_path.split("\\")[2])
        
        return csv_files_names