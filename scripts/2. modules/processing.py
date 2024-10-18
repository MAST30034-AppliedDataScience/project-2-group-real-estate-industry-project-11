import pandas as pd
import geopandas as gpd

regions_df = pd.read_csv('../../data/raw/location/sa2_to_rental_suburb_groups.csv')
regions_df['geometry'] = gpd.GeoSeries.from_wkt(regions_df['geometry'])

regions_df = gpd.GeoDataFrame(
    regions_df,
    geometry='geometry'
)

regions_df