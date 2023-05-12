# Imports
import pandas as pd
import data_ingestion



class DataTransformation():
    def __init__(self):
        pass

    def data_transformation(self):
        data_ingestion_obj = data_ingestion.DataIngestion()

        main_df = pd.read_csv("Notebook\dataset\\" + data_ingestion_obj.get_csv_files_names()[0])
        indicators_df = pd.read_csv("Notebook\dataset\\" + data_ingestion_obj.get_csv_files_names()[1])
        countries_df = pd.read_csv("Notebook\dataset\\" + data_ingestion_obj.get_csv_files_names()[2])




# IN PROGRESS
