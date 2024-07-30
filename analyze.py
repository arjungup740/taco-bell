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

locations_count_by_city = full_df.groupby(['state', 'city'])['location_url'].nunique().reset_index().rename(columns = {'location_url':'count'})
locations_count_by_city[locations_count_by_city['count'] != 1]
comparison_df = full_df.groupby(['state', 'city', 'item_name'])['value']\
                       .agg(mean='mean', median = 'median', num_obs='size', nunique = 'nunique', max = 'max', min = 'min')\
                       .reset_index() # https://stackoverflow.com/questions/12589481/multiple-aggregations-of-the-same-column-using-pandas-groupby-agg

state_comparison_df = full_df.groupby(['state', 'item_name'])['value']\
                       .agg(mean='mean', median = 'median', num_obs='size', nunique = 'nunique', max = 'max', min = 'min')\
                       .reset_index()

metric = 'median'
# metric = 'mean'
easy_compare = pd.pivot_table(comparison_df, columns = ['city', 'state'], index = 'item_name', values= metric).reset_index()
easy_compare_states = pd.pivot_table(state_comparison_df, columns = ['state'], index = 'item_name', values = metric).reset_index()
 
# city1 = ('charlotte', 'nc')
# city1 = ('hollywood', 'fl')
# city1 = ('huntsville', 'al')
city1 =('alamo', 'ca')
easy_compare[city1]
city2 = ('adel', 'ga')
# city2 = ('brooklyn', 'ny')
two_city_compare = easy_compare[[('item_name',''), city1, city2]].dropna().copy()
two_city_compare['delta'] = two_city_compare[city1] - two_city_compare[city2]
two_city_compare['pct_delta'] = (two_city_compare[city1] - two_city_compare[city2]) / two_city_compare[city2] 
two_city_compare
two_city_compare.select_dtypes(include='number').mean()
two_city_compare.select_dtypes(include='number').median()


two_city_compare[ (two_city_compare['pct_delta'] <= -.2) | (two_city_compare['pct_delta'] >= .2)].sort_values(by = 'pct_delta', ascending = True)
two_city_compare[two_city_compare['item_name'].str.contains('taco', case=False)].sort_values(by = 'pct_delta', ascending = True)

full_df[(full_df['item_name'] == 'Watermelon Berry Lemonade Freeze') & (full_df['store_id'] == '038899')]
############################################################################### data qa

## check if dupe menu items per store
count_table = full_df.groupby(['item_name', 'store_id']).size().reset_index().rename(columns={0:'count'})
count_table[count_table['count']>1]

############################################################################### In development

##### get all states in the union

soup = get_soup(url)

directory_links = soup.findAll('a', class_='Directory-listLink', limit = None)
desired_keys = ['href', 'data-count']
list_of_city_urls = [{key: link[key] for key in desired_keys} for link in directory_links]

city_urls_df = pd.DataFrame(list_of_city_urls).rename(columns = {'data-count':'data_count', 'href':'url'})
city_urls_df['data_count'] = city_urls_df['data_count'].str.replace('(', '').str.replace(')', '').apply(int)
city_urls_df['url'] = 'https://locations.tacobell.com/' + city_urls_df['url']
 