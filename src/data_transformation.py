# Imports
import pandas as pd
import numpy as np
import data_ingestion



class DataTransformation():
    def __init__(self):
        pass

    def add_epoch_column(self,year):
        first_epoch = [1990,2000]
        second_epoch = [2000,2010]
        third_epoch = [2010,2015]
        year = int(year)
        
        if year in range(first_epoch[0],first_epoch[1]+1):
            return f'{first_epoch[0]} - {first_epoch[1]}'
        elif year in range(second_epoch[0],second_epoch[1]+1):
            return f'{second_epoch[0]} - {second_epoch[1]}'
        else :
            return f'{third_epoch[0]} - {third_epoch[1]}'

    def data_transformation(self):
        data_ingestion_obj = data_ingestion.DataIngestion()

        # Read the dataset 
        main_df = pd.read_csv(data_ingestion_obj.get_csv_files_paths()[0])
        countries_df = pd.read_csv(data_ingestion_obj.get_csv_files_paths()[1])
        indicators_df = pd.read_csv(data_ingestion_obj.get_csv_files_paths()[2])

        #Transform Indicators dataframe
        education_indicators = []
        for i in indicators_df['Topic']:
            if 'Education' in i:
                education_indicators.append(i)
        education_indicators = np.array(education_indicators)
        education_indicators = list(np.unique(education_indicators))

        indicators_df_filter = ( (indicators_df['Topic'] == education_indicators[0]) | 
                                 (indicators_df['Topic'] == education_indicators[1]) | 
                                 (indicators_df['Topic'] == education_indicators[2]) | 
                                 (indicators_df['Topic'] == education_indicators[3]) )

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

        #Preparing dataframes for visualizatons

        ## 1st dataframe named q1 as question 1
        q1 = df.groupby(['Indicator Name','Region'])['Value'].mean()['DHS: Gross attendance rate. Post Secondary']
        q1 = q1.to_frame().reset_index()
        q1['Value'] = round(q1['Value'],1)

        ## 2nd dataframe named q2 as question 2
        for i,j in df.groupby('Indicator Name')[['Year','Value']]:
            if i == 'DHS: Proportion of out-of-school. Primary. Female':
                d1 = j
            elif i == 'DHS: Proportion of out-of-school. Primary. Male':
                d2 = j
                
        q21 = d1.groupby('Year').mean() #Female dataframe

        q22 = d2.groupby('Year').mean() #Male dataframe

        value_list_f = []
        value_list_m = []
        epoch_list = []

        for j in range(6,31,5):
            
            i = j-6
            
            value_list_f.append(q21.reset_index().iloc[i:j]['Value'].mean())
            value_list_m.append(q22.reset_index().iloc[i:j]['Value'].mean())
            
            epoch_list.append(str(i+1990)+'-'+str(j+1990-1))
            
        q2f = pd.DataFrame({'Value' : value_list_f,
                            'Years':epoch_list,
                            'Gender':'Female'})

        q2m = pd.DataFrame({'Value' : value_list_m,
                            'Years':epoch_list,
                            'Gender':'Male'})

        q2 = pd.concat([q2f,q2m])

        q2['Value'] = round(q2['Value'], 2)

        ## 3rd dataframe named q3 as question 3
        mask = df['Indicator Name'] == 'DHS: Gross attendance rate. Post Secondary'
        q3 = df[mask].groupby(['Country Code','Year']).mean(numeric_only=True).reset_index()
        q3 = q3.merge(countries_df, on='Country Code').drop(['Currency Unit'], axis=1).sort_values('Year')

        q3['Epoch'] = q3['Year'].apply(self.add_epoch_column)


        #Return these 3 dataframes
        return (q1,
                q2,
                q3)