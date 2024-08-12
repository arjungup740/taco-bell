import pandas as pd
import pickle as pkl
import matplotlib.pyplot as plt
import seaborn as sns
pd.options.display.float_format = '{:.2f}'.format

## some pkl read in
with open('full_df.pkl', 'rb') as file:
    full_df = pkl.load(file)

len(full_df)

## dedupe menu items
full_df = full_df.drop_duplicates(subset = ['item_name', 'store_id']) # need this because the same item might be listed under multiple categories
len(full_df)
full_df.columns
# Index(['menu_section_name', 'primary_section_name', 'calories', 'code', 'name',
#        'currencyIso', 'value', 'priceType', 'url', 'store_id', 'location_url'],
#       dtype='object')
# full_df['state'] = full_df['location_url'].str.split('/')[3]

full_df['state'], full_df['city'] = zip(*full_df['location_url'].str.split('/').str[3:5])

core_items = [
              'Supreme Taco Party Pack', 
            #   'Chicken Quesadilla', 
            #   'cinnabon delights 12 pack', 
              'Crunchwrap Supreme®', 
            #   'beefy 5 layer burrito', 
            #   'Nacho cheese doritos locos taco', 
            #   '3 doritos locos tacos combo'
              ]

working = full_df[full_df['item_name'].isin(core_items)]

############################################### Do some digging

agg_funcs = {
    'mean': 'mean',
    'median': 'median',
    'num_stores': 'size',
    'nunique_prices': 'nunique',
    'max': 'max',
    'min': 'min',
    'sd': 'std'
}

########## in aggregate

metric = 'median'
metric = 'mean'

working .groupby('state')['value'].agg(**agg_funcs)

working.groupby(['state', 'item_name'])['value'].agg(**agg_funcs).sort_values(by = ['item_name', metric], ascending = False)


########## breaking down by menu items

comparison_df = working.groupby(['state', 'city', 'item_name'])['value']\
                       .agg(**agg_funcs)\
                       .reset_index()\
                       .sort_values(by = ['item_name', metric, 'state', 'city'], ascending = False) # https://stackoverflow.com/questions/12589481/multiple-aggregations-of-the-same-column-using-pandas-groupby-agg

state_comparison_df = working .groupby(['state', 'item_name'])['value']\
                       .agg(**agg_funcs)\
                       .reset_index()\
                       .sort_values(by = ['item_name', metric, 'state'], ascending = False)

easy_compare = pd.pivot_table(comparison_df, columns = ['city', 'state'], index = 'item_name', values= metric).reset_index()
easy_compare_states = pd.pivot_table(state_comparison_df, columns = ['state'], index = 'item_name', values = metric).reset_index()

city_list = [tuple(x) for x in working [['city', 'state']].drop_duplicates().values] 

# city1 = ('charlotte', 'nc')
# city1 = ('hollywood', 'fl')
# city1 = ('huntsville', 'al')
city1 =('mountain-view', 'ca')
easy_compare[city1]
city2 = ('greenville', 'al')
# city2 = ('brooklyn', 'ny')
two_city_compare = easy_compare[[('item_name',''), city1, city2]].dropna().copy()
two_city_compare['delta'] = two_city_compare[city1] - two_city_compare[city2]
two_city_compare['pct_delta'] = (two_city_compare[city1] - two_city_compare[city2]) / two_city_compare[city2] 
two_city_compare
two_city_compare.select_dtypes(include='number').mean()
two_city_compare.select_dtypes(include='number').median()


two_city_compare[ (two_city_compare['pct_delta'] <= -.2) | (two_city_compare['pct_delta'] >= .2)].sort_values(by = 'pct_delta', ascending = True)
two_city_compare[two_city_compare['item_name'].str.contains('taco', case=False)].sort_values(by = 'pct_delta', ascending = True)

working [(working ['item_name'] == 'Watermelon Berry Lemonade Freeze') & (working ['store_id'] == '038899')]


###### distributions

percentiles = [0, 10, 25, 50, 75, 90, 100]

# Create a DataFrame to hold percentile values
percentile_df = full_df.groupby(['state', 'item_name'])['value'].quantile([p/100 for p in percentiles])\
                       .unstack()\
                       .reset_index()\
                       .sort_values(by = ['item_name', 1, 'state'], ascending = False)

#### can stick in some histograms
plt.figure(figsize=(12, 6))
sns.boxplot(x='group', y='value', data=percentile_df)
plt.xticks(rotation=90)
plt.xlabel('Group')
plt.ylabel('Value')
plt.title('Percentile Distributions by Group')
plt.show()

############################################################################### data qa

## check if dupe menu items per store
count_table = working .groupby(['item_name', 'store_id']).size().reset_index().rename(columns={0:'count'})
count_table[count_table['count']>1]

locations_count_by_city = working .groupby(['state', 'city'])['location_url'].nunique().reset_index().rename(columns = {'location_url':'count'})
locations_count_by_city[locations_count_by_city['count'] != 1]

