actually do next
* check which states have low counts and how many left to grab. 
    Maybe 3 states worth focusing on. And then wisconsin west virgina and wyoming dc left out in the wind
* dig into which of their locations didn't get scraped
    * see which full_city_urls are not in full_df's urls. Then take that list and see how that matches up to the state counts and also the error codes. Focus on vermont and maine
    * honestly, I think they're unscrapeable. Let's move on, and drop vermont, and make a note
* dig into missingness

what we could do next

* check missingness for the menu item you zoomed in on
* run it for crunchwraps quickly? If you wanted to create a crunchwrap supreme index

* Quality -- 0s, and missing data for 2024 rescrape questions
* can we set this up to do over every menu item to find the ones that vary a lot/a little -- are there any that do have more of connection

########### thoughts dump

What we have shown so far
* For supreme taco party packs in 2023, there is perhaps a decent amount of spread. While 80% of prices fall within +/- 15% of the national mean price (assuming this is not that much), from 15% below to 15% above, it's $21 to $29...that is meaningful

Overall findings:
* prices are remarkably tight, and don't vary drastically on core menu items like crunchwrap supreme
* spread a big bigger on higher priced items
* less variation across taco bell vs. cost of living indices, e.g. taco bell 

BACKLOG
* debug why we only have a small amount of states
* cost of living by state: 
    https://www.statista.com/statistics/1240947/cost-of-living-index-usa-by-state/
    https://worldpopulationreview.com/state-rankings/cost-of-living-index-by-state # can scrape it
    https://taxfoundation.org/data/all/state/2023-sales-tax-rates-midyear/ # taxes
    https://catalog.data.gov/dataset/zip-code-data

* try MSA aggregations: https://github.com/chambliss/Major-Metro-Areas-And-Their-Cities
    * compare the micropolitan to the metropolitan
* matrix of pct differences
* compare the 5 boroughs to each other
* compare 5 boroughs vs. charlotte, other places
* compare top 20 MSAs vs. rest of the country
* compare how results track against general cost of living indices for the same places, or general population things
* think on ways for an app to display all the data


Considerations to add/think about after first pass together
* pct differences below a certain threshold don't matter
* if only 1 or two restos vs. many

Data issues to understand
* missing most states & cities
    * do a catalog of what's missing
* See how many times your num appearance on menus for common items differs from number of stores in the city
* $0 items

Note that 2024 is misisng DC, Wisconsin, and Wyoming behavior

There's various stores we're missing in the error dict and various stores probably missing betwene 23 and 24, can go back and do a comparison