# Team 11 - Real Estate Consulting Project
Hi there! Welcome to the notebook of Team 11, please have a cup of coffee ☕ and enjoy your stay.

## Navigation

The repository has been split up into 4 main folders:
1. Data: where all data is stored
2. Notebooks: the bulk of the code is stored here, including the summary notebooks.
3. Plots: this contains some of the plots used, although most plots are embedded in each folder.
4. Scripts: this contains scraping files, along with 

All of the summary notebooks can be found at `notebooks/4. analysis`. In particular prioritise reading:
1. `a. EDA/exploratory`
2. `a. EDA/folium_visualisations` (which allows you to see how different features are distributed across Victoria)
3. `b. modelling/liveability`
As these provide the most detailed insights.

We recommend running through the scripts in the following order to obtain the data. Note that the domain data will take a long time to collect in the landing layer. Therefore we'd recommend skipping stage  which then requires excluding running any notebooks contained in a domain folder as it is dependent on that data.

#### 1. Scrape Domain Data
1. Run script: scripts/1. downloading/scrape_domain.py until fully complete
2. Run notebook: notebooks/1. landing/combine_domain_dfs.ipynb

#### 2. Landing Layer
1. Run all notebooks in `notebooks/1. landing` in their numbered order

#### 3. Raw Layer
2. Run all notebooks in `notebooks/2. raw` in their numbered order

#### 4. Curated Layer
3. Run all notebooks in `notebooks/3. curated` in their numbered order

#### 5. Analysis
4. Feel free to peruse these notebooks in whatever order you please.

## Summary of Challenges

Within the notebooks are some of the challenges we faced as a team. In particular some highlighted ones are:
1. Joins: data was of different granularity, or even different region types (e.g. SA2 vs postcode vs subrubs), so some complex geopandas operations had to be performed to combine and aggregate across different regions. This is explained in depth at `notebooks/2. raw/sa2_join` and is *highly recommended to read*.
2. Scraping: as Domain.com has limits to how many listings you can query at once, we had to first calculate search bins based on prices to make sure we get the right number of properties. This approach is explained in more detail in `scripts/1. downloading/scrape_domain.py`.
3. Visualisation: different datasets had different time periods and also frequencies (e.g. 2016-2020 vs 2017-2021). We made sure to source only data with enough of an overlapping period that would work for our analysis which was 4 years.
4. Extrapolation: at times we had to extrapolate or interpolate data to have more specific time series as data as missing. This is particularly evident in the future predictions of rental prices.
5. At times the data has had to be rotated (onehot encoded or reverse one hot encoded), which has proven to be challenging.

## Open Route API

Finally, you will need an open routes API key in order to run `distance_to_cbd_suburb`. The notebook has instructions as to where to put it.