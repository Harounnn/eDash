# Imports
import pandas as pd
import numpy as np
import data_ingestion



class DataTransformation():
    def __init__(self):
        pass

    def data_transformation(self):
        data_ingestion_obj = data_ingestion.DataIngestion()

        # Read the dataset 
        main_df = pd.read_csv(data_ingestion_obj.get_csv_files_paths()[0])
        indicators_df = pd.read_csv(data_ingestion_obj.get_csv_files_paths()[1])
        countries_df = pd.read_csv(data_ingestion_obj.get_csv_files_paths()[2])

        #Transform Indicators dataframe
        education_indicators = []
        for i in indicators_df['Topic']:
            if 'Education' in i:
                education_indicators.append(i)
        education_indicators = np.array(education_indicators)
        education_indicators = list(np.unique(education_indicators))

        indicators_df_filter = ( (indicators_df['Topic'] == ed_ind[0]) | (indicators_df['Topic'] == ed_ind[0]) | 
                                 (indicators_df['Topic'] == ed_ind[0]) | (indicators_df['Topic'] == ed_ind[0]) )
        indicators_df = indicators_df[indicators_df_filter][['Topic','Indicator Name']]

        #Transform countries dataframe
        countries_df = countries_df[['Country Code','Short Name','Currency Unit','Region']]
        countries_df.dropna(inplace=True)

        #Transform main dataframe
        main_df = main_df.loc[:,:'2020']
        main_df = main_df.merge(indicators_df,left_on='Indicator Name', right_on='Indicator Name', how='left')
        main_df = main_df.dropna(axis=0,subset=['Topic']).drop(['Country Name','Indicator Code'],axis=1)

        #Establish the principal dataframe
        df = main_df
        df_filter_1 = ( (df['Topic'] != 'Tertiary Education (SABER)') &
                        (df['Topic'] != 'Education Management Information Systems (SABER)') )
        df = df[df_filter_1]

        selected_indicators = ['DHS: Gross attendance rate. Post Secondary. Female',
                               'DHS: Gross attendance rate. Post Secondary. Male',
                               'DHS: Gross attendance rate. Post Secondary','DHS: Proportion of out-of-school. Primary. Female',
                               'DHS: Proportion of out-of-school. Primary. Male','DHS: Proportion of out-of-school. Primary.']
        
        df_filter_2 = ((df['Indicator Name'] == selected_indicators[0]) | (df['Indicator Name'] == selected_indicators[1])| 
                       (df['Indicator Name'] == selected_indicators[2]) | (df['Indicator Name'] == selected_indicators[3])| 
                       (df['Indicator Name'] == selected_indicators[4]) | (df['Indicator Name'] == selected_indicators[5]))
        
        df = df[df_filter_2]

        start_year = 1990
        last_year = 2015

        df = pd.melt(df,id_vars=['Indicator Name','Country Code'],
                    value_vars=[str(i) for i in range(start_year,last_year + 1)]
                    ,var_name='Year', value_name='Value')
        df = df.dropna()
        df = df.merge(countries_df,left_on='Country Code', right_on='Country Code', how='left')
        df = df[['Indicator Name','Short Name','Country Code','Currency Unit','Region','Year','Value']]

        #################################
                #IN PROGRESS#
        #################################
