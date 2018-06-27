import pandas as pd

import tagnews

df = tagnews.load_data()

# Filter to only include subset of news outlets
news_source_mappings = {
    113: 'trib',
    112: 'suntimes',
    100: 'cbs2',
    110: 'nbc5',
    98: 'abc7',
    115: 'wgntv',
    109: 'fox32',
}

assert -1e9 not in df['news_source_id'].unique()
flt = df['news_source_id'] == -1e9
for news_id in news_source_mappings:
    flt |= df['news_source_id'] == news_id

df = df.loc[flt]

# Filter to only include articles from 2017
df['last_modified'] = pd.to_datetime(df['last_modified'])
df = df.loc[('2017' < df['last_modified']) & (df['last_modified'] < '2018')]

# Filter to only include sexual assault/domestic violence
thresh = 0.5
df = df.loc[(df['DOMV_model'] > thresh) | (df['SEXA_model'] > thresh)]

# Save to CSV
df.to_csv('vaw-machine-discovered-2017.csv')
