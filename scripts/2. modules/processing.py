import pandas as pd
import geopandas as gpd
import os

REGION_DF_PATH = 'data/2. raw/location/sa2_to_rental_suburb_groups.csv'

def get_regions_df(path_depth: int):
    path = '../' * path_depth + REGION_DF_PATH

    regions_df = pd.read_csv(path).drop("Unnamed: 0", axis=1)
    regions_df['geometry'] = gpd.GeoSeries.from_wkt(regions_df['geometry'])

    regions_df = gpd.GeoDataFrame(
        regions_df,
        geometry='geometry'
    )

    return regions_df

def fix_col_names(df):
    df.columns = df.columns.str.lower().str.replace(' ', '_')

def to_csv(df, path, file_name):
    os.makedirs(os.path.dirname(os.path.join(path, file_name)), exist_ok=True)
    df.to_csv(os.path.join(path, file_name))

def to_shapefile(df, path, file_name):
    os.makedirs(os.path.dirname(os.path.join(path, file_name)), exist_ok=True)
    df.to_file(os.path.join(path, file_name))