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



## Open Route API

Finally, you will need an open routes API key in order to run `distance_to_cbd_suburb`. The notebook has instructions as to where to put it.