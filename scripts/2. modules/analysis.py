import branca
import pandas as pd
import geopandas as gpd
import folium
from folium import GeoJson

def filter_range(input_df, start_year, start_quarter, end_year, end_quarter, house_type=None, bedrooms=None):
        
    if (house_type and not bedrooms) or (bedrooms and not house_type):
        raise ValueError(f"Either both or neither of house_type or bedrooms must be None")
    
    house_filter = (input_df['housing: type'] == house_type) if house_type else (input_df['housing: type'] == 'all')
    room_filter = (input_df['housing: beds'] == bedrooms) if bedrooms else (input_df['housing: beds'] == 'all')

    if start_year == end_year:
        return input_df[
            (input_df['year'] == start_year) & (input_df['quarter'] >= start_quarter) 
            & (input_df['quarter'] <= end_quarter) & 
            house_filter & room_filter
        ].copy()
    else:
        return input_df[
            (((input_df['year'] > start_year) & (input_df['year'] < end_year)) | 
            ((input_df['year'] == start_year) & (input_df['quarter'] >= start_quarter)) | 
            ((input_df['year'] == end_year) & (input_df['quarter'] <= end_quarter))) & 
            house_filter & room_filter
        ].copy()

def standardize(column):
    return (column - column.mean()) / column.std()

def visualize_on_map(input_df, regions_df, display_col, year, quarter, house_type=None, bedrooms=None, transform=None, map_location=[-37.8136, 144.9631], zoom_start=10,
                     min_val=None, max_val=None, color_scale_label=""):
    """
    Convert a DataFrame to a GeoDataFrame based on the specified geometry column,
    and display it on a Folium map with the specified column as popups.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    geometry_col (str): The name of the geometry column.
    display_col (str): The name of the column to display in popups.
    map_location (list): Latitude and longitude for centering the map [lat, lon].
    zoom_start (int): Initial zoom level for the map.

    Returns:
    folium.Map: The Folium map with the GeoDataFrame visualized.
    """

    if (house_type and not bedrooms) or (bedrooms and not house_type):
        raise ValueError(f"Either both or neither of house_type or bedrooms must be None")
    
    house_filter = (input_df['housing: type'] == house_type) if house_type else (input_df['housing: type'] == 'all')
    room_filter = (input_df['housing: beds'] == bedrooms) if bedrooms else (input_df['housing: beds'] == 'all')

    input_df_filtered = input_df[(input_df['year'] == year) & (input_df['quarter'] == quarter)
                                 & house_filter & room_filter]

    df = pd.merge(regions_df, input_df_filtered, on='suburbs').dropna(subset=[display_col])

    # if max_val:
    #     df[display_col] = df[display_col].clip(upper=max_val)

    if transform:
        if transform == 'std':
            mean_value = df['housing: median'].mean()
            std_dev_value = df['housing: median'].std()

            df[display_col] = df[display_col].apply(lambda x : (x - mean_value) / std_dev_value)
        else:
            df[display_col] = df[display_col].apply(transform)
    
    # Create a GeoDataFrame using the geometry column
    gdf = gpd.GeoDataFrame(df, geometry=df['geometry'])
    
    # Check if the display column exists
    if display_col not in gdf.columns:
        raise ValueError(f"Column '{display_col}' not found in the GeoDataFrame.")
    
    # Create a color scale
    if not min_val:
        min_val = gdf[display_col].min()
    
    if not max_val:
        max_val = gdf[display_col].max()
    colormap = branca.colormap.LinearColormap(colors=['#440154', '#482878', '#3E4A89', '#2D708E', '#21918C', '#5CDB8A', '#FDE724'], 
                                                    vmin=min_val, vmax=max_val, caption=color_scale_label)

    # Convert GeoDataFrame to GeoJSON format
    geojson_data = gdf.to_json()

    # Create a Folium map centered at the specified location
    m = folium.Map(location=map_location, zoom_start=zoom_start)

    # Function to create a style for the GeoJSON
    def style_function(feature):
        value = feature['properties'][display_col]
        return {
            'fillColor': colormap(value),  # Use the color scale
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.5
        }

    # Add GeoJSON to the map with popups
    GeoJson(
        geojson_data,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=[display_col], aliases=[display_col.capitalize()])
    ).add_to(m)

    # Add color scale to the map
    colormap.add_to(m)

    return m