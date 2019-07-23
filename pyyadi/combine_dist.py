import pandas as pd

# Read From CSV
store_df = pd.read_csv('yadi.csv')
dist_df = pd.read_csv('dist.csv')

# P/C/D DataFrame
p_df = dist_df.drop_duplicates('p').set_index('pcode')['p']
c_df = dist_df.drop_duplicates('c').set_index('ccode')['c']
d_df = dist_df.drop_duplicates('d').set_index('dcode')['d']

# Combine
store_df = store_df.join(p_df, 'pcode')
store_df = store_df.join(c_df, 'ccode')
store_df = store_df.join(d_df, 'dcode')

# Split
coord_df = store_df['gps'].str.split(',', expand=True).drop(columns=[2])
coord_df.columns = ['longitude', 'latitude']

# Concat
store_df = pd.concat([store_df, coord_df], axis=1)

store_df.to_csv('yadi_with_dist.csv')
print('Done')
