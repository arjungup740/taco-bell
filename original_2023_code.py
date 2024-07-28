import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup
import pickle as pkl
pd.set_option('display.float_format', '{:.2f}'.format)
pd.set_option('display.max_rows', 100)
# one_resto = requests.get('https://www.tacobell.com/tacobellwebservices/v3/tacobell/products/menu/029867', headers=one_resto_headers)
# print(one_resto)
# data = one_resto.json()
# data.keys()

############################################################################### Utils

def flatten_list(list_to_flatten):

    return [item for sublist in list_to_flatten for item in sublist]

def get_soup(url):

    response = requests.get(url)
    # make a soup object
    soup = BeautifulSoup(response.content, "html.parser")

    return soup

def get_all_city_urls_in_state_or_all_states_in_country(url):
    soup = get_soup(url)

    directory_links = soup.findAll('a', class_='Directory-listLink', limit = None)
    desired_keys = ['href', 'data-count']
    list_of_city_urls = [{key: link[key] for key in desired_keys} for link in directory_links]

    city_urls_df = pd.DataFrame(list_of_city_urls).rename(columns = {'data-count':'data_count', 'href':'url'})
    city_urls_df['data_count'] = city_urls_df['data_count'].str.replace('(', '').str.replace(')', '').apply(int)
    city_urls_df['url'] = 'https://locations.tacobell.com/' + city_urls_df['url']
    # if there's data count of 1, add it to a location list, if there's a data count of >1, pass it to a city list handler

    return city_urls_df

def get_all_location_urls_from_city(url):
    soup = get_soup(url)
    teaser_links = soup.findAll('a', class_ = 'Teaser-viewPage', limit= None)
    teaser_links = soup.find_all(class_=['Teaser-titleLink'], limit = None) #['Teaser-titleLink', 'Teaser-viewPage']

    # Extract the href attribute from each element
    hrefs = ['https://locations.tacobell.com' + link['href'].replace('../', '/') for link in teaser_links]

    return hrefs

def get_store_id_from_location_url(url, soup, dict_of_store_ids): # get_store_id_from_location_url
    
    data_code_element = soup.find(attrs={'data-code': True})
    if data_code_element:
        data_code_value = data_code_element['data-code']
        # print("Found data-code element with value:", data_code_value)
        dict_of_store_ids[url] = data_code_value
    else:
        # print("No data-code element found")
        dict_of_store_ids[url] = 0

    return dict_of_store_ids

def get_indiv_store_raw_data(store_id, one_resto_headers):
    one_resto = requests.get(f'https://www.tacobell.com/tacobellwebservices/v3/tacobell/products/menu/{store_id}', headers=one_resto_headers)
    data = one_resto.json()

    return data

def get_one_store_df(data):
#### using number indexing, might be easier
    menu_data = data['menuProductCategories']
    one_store_data_list = []
    # cols_one_menu_item_dict = ['menu_section_name', 'calories', 'code', 'name', 'currency', 'price', 'string_price', 'price_type', 'item_stub_url']
    for i in range(len(data['menuProductCategories'])):
        menu_section_name = data['menuProductCategories'][i]['name']
        for j in range(len(data['menuProductCategories'][i]['products'])):
            one_menu_item_dict = {}
            one_menu_item_dict['menu_section_name'] = menu_section_name
            one_menu_item_dict['primary_section_name'] = menu_data[i]['products'][j]['primaryCategory']
            one_menu_item_dict['calories'] =  menu_data[i]['products'][j]['calories']
            one_menu_item_dict['item_code'] = menu_data[i]['products'][j]['code']
            one_menu_item_dict['item_name'] = menu_data[i]['products'][j]['name']
            one_menu_item_dict['currencyIso'] = menu_data[i]['products'][j]['price']['currencyIso']
            one_menu_item_dict['value'] = menu_data[i]['products'][j]['price']['value']
            one_menu_item_dict['priceType'] = menu_data[i]['products'][j]['price']['priceType']
            one_menu_item_dict['item_url'] = menu_data[i]['products'][j]['url']
            #  print(one_menu_item_dict)
            one_store_data_list.append(one_menu_item_dict)

            #  print()
            # product_list['value']
        # print(menu_section_name) 
    one_store_df = pd.DataFrame(one_store_data_list)
    one_store_df['store_id'] = store_id

    return one_store_df

############################################################################### Runner

one_resto_headers = \
{
    'Accept': '*/*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en-US,en;q=0.9',
'Connection': 'keep-alive',
'Host': 'www.tacobell.com',
# 'Referer': 'https://www.tacobell.com/food?store=005457',
'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Windows"',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'same-origin',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

##### get all city urls in a state
start = datetime.datetime.now()
url = 'https://locations.tacobell.com/'

state_urls_df = get_all_city_urls_in_state_or_all_states_in_country(url)

# state_urls = ['https://locations.tacobell.com/nc.html', 'https://locations.tacobell.com/oh.html']
# state_urls = state_urls_df['url'].tolist()[0:2]

# indiv_location_urls_nested = []
# city_urls_nested = []
full_city_urls_df = []
for url in state_urls_df['url']:
    print(f'state_url = {url}')
    city_urls_df = get_all_city_urls_in_state_or_all_states_in_country(url)
    full_city_urls_df.append(city_urls_df)
    # location_urls = city_urls_df[city_urls_df['data_count'] == 1]['url'].tolist()
    # indiv_location_urls_nested.append(location_urls)
    # actual_city_urls = city_urls_df[city_urls_df['data_count'] != 1]['url'].tolist()
    # city_urls_nested.append(actual_city_urls)
    # city_urls_df[city_urls_df['data_count'] == 0]
full_city_urls_df = pd.concat(full_city_urls_df)

with open('all_city_urls_df.pkl', 'wb') as file:
    pkl.dump(full_city_urls_df , file)

multi_url_cities_df = full_city_urls_df[full_city_urls_df['data_count'] != 1]
location_urls_df = full_city_urls_df[full_city_urls_df['data_count'] == 1]

# full_city_urls_df[full_city_urls_df['url'].str.contains('com/wy/')]

# city_urls_flat = flatten_list(city_urls_nested)
# indiv_location_urls_flat = flatten_list(indiv_location_urls_nested)
###### get all location urls in a city
# city_urls = ['https://locations.tacobell.com/nc/charlotte.html', 'https://locations.tacobell.com/oh/columbus.html']

from_cities_indiv_location_urls = []
for url in multi_url_cities_df['url']: # .iloc[:10]
        print(f'city_url = {url}')
        from_cities_indiv_location_urls.append(get_all_location_urls_from_city(url))

location_urls_df2 = pd.concat([pd.DataFrame(x) for x in from_cities_indiv_location_urls]).rename(columns = {0:'url'})
location_urls_df2['data_count'] = 1

all_location_urls_df = pd.concat([location_urls_df, location_urls_df2])

with open('all_location_urls_df.pkl', 'wb') as file:
    pkl.dump(all_location_urls_df, file)

# indiv_location_urls_flat = indiv_location_urls_flat + flatten_list(from_cities_indiv_location_urls)
# multi_url_cities_df[multi_url_cities_df['url'].str.contains('athens')]
# all_location_urls_df[all_location_urls_df['url'].str.contains('athens')]

###### get store ids from location urls
dict_of_store_ids = {}
# locations_error_list = {}
# url_list = ['https://locations.tacobell.com/nc/charlotte/13121-south-tryon-st-.html', 'https://locations.tacobell.com/nc/charlotte/1800-e-woodlawn-rd.html', ]

for url in all_location_urls_df['url']:
    print(f"indiv location url we're currently getting a store_id for = {url}")
    soup = get_soup(url)
    dict_of_store_ids = get_store_id_from_location_url(url, soup, dict_of_store_ids)

with open('all_store_ids_dict.pkl', 'wb') as file:
    pkl.dump(dict_of_store_ids, file)

# with open('all_store_ids_dict.pkl', 'rb') as file:
#     test = pkl.load(file)
# dict_of_store_ids == test
##### ping API with store ids to get menu data 


# list_of_store_ids = ['029867', '002863', '005500']
list_of_one_store_dfs = []
error_dict = {}
for location_url, store_id in dict_of_store_ids.items():
    print(f"indiv store_id we're pulling menu data for = {location_url}")
    try:
        raw_data = get_indiv_store_raw_data(store_id, one_resto_headers)
        ## add a step saving down raw data locally, then eventually to s3
        one_store_df = get_one_store_df(raw_data)
        one_store_df['location_url'] = location_url
        list_of_one_store_dfs.append(one_store_df)
    except Exception as e:
        print(f'hit error on store_id = {store_id}, error code = {e}')
        error_dict[store_id] = e
end = datetime.datetime.now()
print(f'took {end-start}')

with open('all_one_store_dfs_list.pkl', 'wb') as file:
    pkl.dump(list_of_one_store_dfs, file)

# with open('all_one_store_dfs_list.pkl', 'rb') as file:
#     test = pkl.load(file)
# list_of_one_store_dfs == test

full_df = pd.concat(list_of_one_store_dfs)

with open('full_df.pkl', 'wb') as file:
    pkl.dump(full_df, file)

# with open('full_df.pkl', 'rb') as file:
#     test = pkl.load(file)
# full_df.equals(test)

full_df.memory_usage(deep=True).sum()

len(full_df)
## dedupe menu items
full_df = full_df.drop_duplicates(subset = ['item_name', 'store_id'])
len(full_df)
full_df.columns
# Index(['menu_section_name', 'primary_section_name', 'calories', 'code', 'name',
#        'currencyIso', 'value', 'priceType', 'url', 'store_id', 'location_url'],
#       dtype='object')
# full_df['state'] = full_df['location_url'].str.split('/')[3]

full_df['state'], full_df['city'] = zip(*full_df['location_url'].str.split('/').str[3:5])

full_df.groupby(['state', 'city'])['location_url'].nunique()
comparison_df = full_df.groupby(['state', 'city', 'item_name'])['value']\
                       .agg(mean='mean', median = 'median', num_obs='size', nunique = 'nunique')\
                       .reset_index() # https://stackoverflow.com/questions/12589481/multiple-aggregations-of-the-same-column-using-pandas-groupby-agg

state_comparison_df = full_df.groupby(['state', 'item_name'])['value']\
                       .agg(mean='mean', median = 'median', num_obs='size', nunique = 'nunique')\
                       .reset_index()

metric = 'median'
easy_compare = pd.pivot_table(comparison_df, columns = ['city', 'state'], index = 'item_name', values= metric).reset_index()
easy_compare_states = pd.pivot_table(state_comparison_df, columns = ['state'], index = 'item_name', values = metric).reset_index()

easy_compare[('alabaster','al')] 
# city1 = ('charlotte', 'nc')
# city1 = ('hollywood', 'fl')
city1 = ('huntsville', 'al')
# city2 = ('brooklyn', 'ny')
city2 = ('brooklyn', 'ny')
two_city_compare = easy_compare[[('item_name',''), city1, city2]].dropna().copy()
two_city_compare['delta'] = two_city_compare[city1] - two_city_compare[city2]
two_city_compare['pct_delta'] = (two_city_compare[city1] - two_city_compare[city2]) / two_city_compare[city2] 
two_city_compare
two_city_compare.select_dtypes(include='number').mean()
two_city_compare.select_dtypes(include='number').median()


two_city_compare[ (two_city_compare['pct_delta'] < -.2) | (two_city_compare['pct_delta'] > .2)].sort_values(by = 'pct_delta', ascending = True)
two_city_compare[two_city_compare['item_name'].str.contains('taco', case=False)].sort_values(by = 'pct_delta', ascending = True)*

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
    

############################################################################### general notes

## some dead links, dig into finding those stores
# hit error on store_id = E320067, error code = 'menuProductCategories'
# hit error on store_id = E320066, error code = 'menuProductCategories'
# hit error on store_id = E320058, error code = 'menuProductCategories'


# Print the extracted hrefs
# for href in hrefs:
#     print(href)

### unclear why this didn't work
# link = soup.findAll("a", class_="Core-order Core-order-notAlone Core-orderOnline") # this doesn't have the store id in the href, those bastards
# link = soup.find("div", class_="Core Core--ace")

## don't think we need this but save down in case
# url = 'https://locations.tacobell.com/nc.html'

# city_urls_df = get_all_city_urls_in_state_or_all_states_in_country(url)

# location_urls = city_urls_df[city_urls_df['data_count'] == 1]['url'].tolist()
# actual_city_urls = city_urls_df[city_urls_df['data_count'] != 1]['url'].tolist()

# city_urls_df[city_urls_df['data_count'] == 0]
