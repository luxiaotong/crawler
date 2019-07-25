import pandas as pd

aima_df = pd.read_csv('aima.csv')

location_df = aima_df['location'].str.split(',', expand=True)
location_df.columns = ['longitude', 'latitude']

aima_df = pd.concat([aima_df, location_df], axis=1)
aima_df.to_csv('aima_split_location.csv')
print('Done')
