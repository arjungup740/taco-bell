
What we are seeking to understand
* how much spread is there 
    * for supreme party packs, not much
* how much spread is there when removing hawwaii and alaska?
    * for supreme party packs, not much
* how much does cost of living in a place explain that spread 
    * state level analysis
    * city level analysis
        * for both of these, not a ton. States it's a little better
    * if we look at % deviation from mean vs. % deviation from mean for both values and regress those? Would this change anything?
* how many people are overpaying, and by how much?
    * can look at you vs. the regression line -- given model not very good, maybe not very relevant
    * Similarly look at % deviation from mean for each and see what's happening
    * histogram the % deviations

* can we set this up to do over every menu item to find the ones that vary a lot/a little -- are there any that do have more of connection

* do for 2024
* Quality, rescrape questions



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