"""Script to load the data into Docker Postgres database"""
import pandas as pd
#import psycopg2
import warnings
import shutil
warnings.filterwarnings('ignore')

credentials = "postgresql://postgres:1234@172.17.0.2/test"

#Starting the data loading and cleaning. 
print('Unpacking archive')
shutil.unpack_archive('archive.zip')

honey_pot_data = pd.read_csv('AWS_Honeypot_marx-geo.csv')
print('read complete and df created')
null_filled_data = honey_pot_data.copy()
#filling the null values with unknown 
for col in ['type','country','cc','locale','localeabbr','postalcode']:
    null_filled_data[col].fillna('unknown',axis=0,inplace=True)
#filling the null values in case of floats with 0
for col_name in ['spt','dpt']:
    #null_filled_data.fillna(0,inplace=True,axis=0)
    null_filled_data[col_name].fillna(0,inplace=True,axis=0)
#dropping the column 
null_filled_data.drop('Unnamed: 15',inplace=True,axis=1)
#removing the rows that have any null values
null_filled_data.dropna(axis=0,inplace=True)
print('Cleaning complete. Ready to write into db')
#writing out the dataframe to postgres database
try:
    null_filled_data.to_sql(name='hacker_data',con=credentials,
                        if_exists='replace',index=True)
    print('Connect to postgres db and check the table hacker_data by select command')
except Exception as e:
    print(e)


