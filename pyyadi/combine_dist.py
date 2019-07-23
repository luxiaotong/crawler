import pandas as pd

store_df = pd.read_csv('yadi.csv')
print(store_df)

dist_df = pd.read_csv('dist.csv')

p_df = dist_df.drop_duplicates('p').set_index('pcode')['p']
c_df = dist_df.drop_duplicates('c').set_index('ccode')['c']
d_df = dist_df.drop_duplicates('d').set_index('dcode')['d']

store_df = store_df.join(p_df, 'pcode')
store_df = store_df.join(c_df, 'ccode')
store_df = store_df.join(d_df, 'dcode')
print(store_df)
store_df.to_csv('yadi_with_dist.csv')
