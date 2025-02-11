import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from shapely.geometry import Point, LineString
import geopandas as gpd
from geopandas import GeoDataFrame
from backend.config import country_codes, BASE_URL_V3

def country_code_to_name(df):
    def get_country_name(code):
        try:
            return country_codes[code.lower()]
        except Exception as e:
            print(e)
            return None
    df['Country'] = df['Country'].apply(lambda x:get_country_name(x))
    return df


def points_histogram(stats):

    buckets = [0, 1000, 2000, 3000, 4000, 5000]
    x_tick_labels = ['0-1000', '1000-2000', '2000-3000', '3000-4000', '4000-5000']

    # Count the points falling into each bucket
    counts, _ = np.histogram(stats['round_wise_points'], bins=buckets)

    # Plot the histogram
    fig, ax = plt.subplots()
    ax.bar(buckets[:-1], counts, width=1000)

    # Customize the plot (optional)
    ax.set_xlabel('Points Range')
    ax.set_ylabel('Count')
    ax.set_title('Points Distribution')
    ax.set_xticks(ticks=buckets[:-1], labels=x_tick_labels)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, axis='y')
    
    return fig

def plot_countries_bar_chart(stats):

    top_n = 10 if len(stats['countries']) > 10 else len(stats['countries'])

    new_stats = {country_codes[key.lower()]: value for key, value in stats['countries'].items() if key}
    
    sorted_data = dict(sorted(new_stats.items(), key=lambda item: item[1], reverse=True)[:top_n])

    fig, ax = plt.subplots()
    
    ax.bar(sorted_data.keys(), sorted_data.values())
    ax.set_xlabel('Country')
    ax.set_ylabel('Count')
    ax.set_title('Most frequently occurring countries')
    ax.set_xticks(ax.get_xticks(), labels=ax.get_xticklabels(), rotation=45, fontsize='x-small')
    
    return fig

def plot_guessed_locations(guessed_locations):
    guessed_lat = []
    guessed_lng = []
    round_scores = []
    
    for guessed_loc in guessed_locations:
        guessed_lat.append(guessed_loc['lat'])
        guessed_lng.append(guessed_loc['lng'])
        round_scores.append(guessed_loc['score'])
        
    guessed_df = pd.DataFrame({'lat': guessed_lat,
                               'lng': guessed_lng,
                               'score': round_scores})
    
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    guessed_geometry = [Point(xy) for xy in zip(guessed_df['lng'], guessed_df['lat'])]
    guessed_gdf = GeoDataFrame(guessed_df, geometry=guessed_geometry)
    ax = guessed_gdf.plot(ax=world.plot(figsize=(10,10), color='lightblue'), marker='o', markersize=3,
                    cax='score', cmap='YlOrRd', vmin=0, vmax=5000)
    
    ax.set_title('Guessed Locations')
    ax.set_axis_off()
    fig = ax.get_figure()
    cax = fig.add_axes([0.1, 0.26, 0.8, 0.03])
    sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=0, vmax=5000))
    sm._A = []
    fig.colorbar(sm, cax=cax, orientation='horizontal', label='Score')
    return fig

def plot_round_locations(guessed_locations):
    round_lat = []
    round_lng = []

    for guessed_loc in guessed_locations:
        round_lat.append(guessed_loc['lat'])
        round_lng.append(guessed_loc['lng'])

    round_df = pd.DataFrame({'lat': round_lat,
                               'lng': round_lng})

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    round_geometry = [Point(xy) for xy in zip(round_df['lng'], round_df['lat'])]
    round_gdf = GeoDataFrame(round_df, geometry=round_geometry)

    ax = round_gdf.plot(ax=world.plot(figsize=(10,10), color='lightblue'), marker='o', markersize=3, color='red')

    ax.set_title('Round Locations')
    ax.set_axis_off()

    return ax.get_figure()

def plot_guessed_locations_2(guessed_locations):
    guessed_lat = []
    guessed_lng = []
    round_scores = []
    
    for guessed_loc in guessed_locations:
        guessed_lat.append(guessed_loc['lat'])
        guessed_lng.append(guessed_loc['lng'])
        round_scores.append(guessed_loc['score'])
        
    guessed_df = pd.DataFrame({'lat': guessed_lat,
                               'lng': guessed_lng,
                               'score': round_scores})
    
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    guessed_geometry = [Point(xy) for xy in zip(guessed_df['lng'], guessed_df['lat'])]
    guessed_gdf = GeoDataFrame(guessed_df, geometry=guessed_geometry)


    ax = guessed_gdf.plot(ax=world.plot(figsize=(10,10), color='lightblue'), marker='o', markersize=3,
                    cax='score', cmap='YlOrRd', vmin=0, vmax=5000)
    
    # Variation 1: Different Colormap and Marker
    fig, ax = plt.subplots(figsize=(10, 10))  # Create figure and axes explicitly
    world.plot(ax=ax, color='lightgray', edgecolor='black')  # Add world map first
    guessed_gdf.plot(ax=ax, marker='*', markersize=5, cax='score', cmap='viridis', vmin=0, vmax=5000, label="Guessed Locations") #label added
    ax.set_title('Guessed Locations (Variation 1)')
    ax.set_axis_off()
    # Colorbar (improved placement)
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=0, vmax=5000))
    sm._A = []
    cbar = fig.colorbar(sm, ax=ax, shrink=0.6, label='Score') # shrink added
    ax.legend() #legend added
    return fig

def plot_round_and_guessed_locations(round_locations, guessed_locations):
    round_lat = [] 
    round_lng = []
    guessed_lat = []
    guessed_lng = []
    round_scores =  [] # If you still want scores for guessed locations

    # Extract data
    for round_loc in round_locations:
        round_lat.append(round_loc['lat'])
        round_lng.append(round_loc['lng'])

    for guessed_loc in guessed_locations:
        guessed_lat.append(guessed_loc['lat'])
        guessed_lng.append(guessed_loc['lng'])
        if 'score' in guessed_loc:  # only add the score if it exists
            round_scores.append(guessed_loc['score'])

    # Create DataFrames
    round_df = pd.DataFrame({'lat': round_lat, 'lng': round_lng})
    guessed_df = pd.DataFrame({'lat': guessed_lat, 'lng': guessed_lng})
    if round_scores:  # only add score column if it exists
        guessed_df['score'] = round_scores

    # Create GeoDataFrames
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    round_geometry = [Point(xy) for xy in zip(round_df['lng'], round_df['lat'])]
    round_gdf = GeoDataFrame(round_df, geometry=round_geometry, crs=world.crs)  # Added CRS

    guessed_geometry = [Point(xy) for xy in zip(guessed_df['lng'], guessed_df['lat'])]
    guessed_gdf = GeoDataFrame(guessed_df, geometry=guessed_geometry, crs=world.crs)  # Added CRS

   # Create lines (connecting round and guessed locations) with dotted style
    lines = []
    for i in range(min(len(round_gdf), len(guessed_gdf))):
        line = LineString([round_gdf.geometry[i], guessed_gdf.geometry[i]])
        lines.append(line)
    lines_gdf = GeoDataFrame({'geometry': lines}, crs=world.crs)

    # Plotting
    ax = world.plot(figsize=(10, 10), color='lightblue')  # Plot world map first

    # Plot dotted lines
    lines_gdf.plot(ax=ax, color='gray', linestyle='dotted', linewidth=1)  # <--- Dotted lines

    # Plot round locations in black
    round_gdf.plot(ax=ax, color='black', marker='o', markersize=3, label='Round Locations')  # <--- Black color

    # Plot guessed locations with color gradient based on score
    guessed_gdf.plot(ax=ax, column='score', cmap='YlOrRd', marker='x', markersize=3,
                     legend=True, legend_kwds={'label': "Score", 'orientation': "horizontal"},
                     vmin=0, vmax=5000, label='Guessed Locations')  # <--- Color gradient

    ax.set_title('Round and Guessed Locations')
    ax.set_axis_off()
    ax.legend()  # Show legend

    return ax.get_figure()




# Printing the game function
def print_game_json(session, game_tokens, number_of_games):
    """Prints the raw JSON response for each game."""

    for i, token in enumerate(game_tokens[:number_of_games]):
        try:
            game = session.get(f"{BASE_URL_V3}/games/{token}").json()
            print(json.dumps(game, indent=4))  # Print the JSON with indentation
            print("-" * 50)  # Separator between games

        except Exception as e:
            print(f"Error fetching game {token}: {e}")
            continue  # Continue to the next game even if one fails

