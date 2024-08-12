
What we are seeking to understand
* how much spread there 
* how much more expensive is taco bell in places that are expensive to live vs. places that are cheap to live -- cities/metro areas vs. everything else, and across states
* how have these changed since 2023?
* how does your locale compare to the national average



########### thoughts dump

Overall findings:
* prices are remarkably tight, and don't vary drastically on core menu items like crunchwrap supreme
* spread a big bigger on higher priced items
* less variation across taco bell vs. cost of living indices, e.g. taco bell 

BACKLOG
* debug why we only have a small amount of states
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

Note that 2024 is misisng DC, Wisconsin, and Wyoming behavior

There's various stores we're missing in the error dict and various stores probably missing betwene 23 and 24, can go back and do a comparison