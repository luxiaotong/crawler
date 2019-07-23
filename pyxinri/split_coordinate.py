import pandas as pd

xinri_df = pd.read_csv('xinri.csv')
xinri_df.columns=['id', 'title', 'address', 'coordinate', 'tel', 'p', 'c', 'd']

coord_df = xinri_df['coordinate'].str.split(',', expand=True)
coord_df.columns = ['longitude', 'latitude']

xinri_df = pd.concat([xinri_df, coord_df], axis=1)
xinri_df.to_csv('xinri_split_coord.csv')
print('Done')
