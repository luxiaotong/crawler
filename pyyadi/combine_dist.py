import pandas as pd
import numpy as np

# Read From CSV
store_df = pd.read_csv('yadi.csv')
dist_df = pd.read_csv('dist.csv')

# Drop Duplicated
store_df = store_df.drop_duplicates('code')

# Replace C/D
to_replace = {
    'ccode': {
        150122: 150100,
        150802: 150800,
        340181: 340100,
        341881: 341800,
        653101: 653100,
        653201: 653200,
        652901: 652900,
        652801: 652800,
        652201: 652200,
        422801: 422800,
        222403: 222400,
        360403: 360400,
        360681: 360600,
        441702: 441700,
        500116: 500100,
        410482: 410400,
        542600: 540400,
    },
    'dcode': {
        110228: 110118,
        110229: 110119,
        120221: 120117,
        120223: 120118,
        130323: 130306,
        130621: 130607,
        130622: 130608,
        130625: 130609,
        210282: 210214,
        360400: 360403,
        360600: 360681,
        542621: 540400,
    }
}
store_df = store_df.replace(to_replace)

# P/C/D DataFrame
p_df = dist_df.drop_duplicates('p').set_index('pcode')['p']
c_df = dist_df.drop_duplicates('c').set_index('ccode')['c']
d_df = dist_df.drop_duplicates('d').set_index('dcode')['d']

# Append C/D DataFrame
extra = [
    [419001, '济源市'],
    [429004, '仙桃市'],
    [429005, '潜江市'],
    [429006, '天门市'],
    [469001, '五指山市'],
    [469002, '琼海市'],
    [469003, '儋州市'],
    [469005, '文昌市'],
    [469006, '万宁市'],
    [469007, '东方市'],
    [469022, '屯昌县'],
    [469023, '澄迈县'],
    [469024, '临高县'],
    [469026, '昌江黎族自治县'],
    [469027, '乐东黎族自治县'],
    [469028, '陵水黎族自治县'],
    [469029, '保亭黎族苗族自治县'],
    [469030, '琼中黎族苗族自治县'],
    [540400, '林芝市'],
]
for i in range(len(extra)):
    l = extra[i][0]
    v = extra[i][1]
    c_df.loc[l] = v
    d_df.loc[l] = v


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
