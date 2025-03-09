import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
import contextily as ctx

# Load fire data (make sure it contains lat/lon or geometry)
fire_df = pd.read_csv('data/cleaned_fire.csv')

# Check if we have perimeter data (or just lat/lon points)
if 'latitude' in fire_df.columns and 'longitude' in fire_df.columns:
    # Create Point geometries
    fire_df['geometry'] = fire_df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
    fire_gdf = gpd.GeoDataFrame(fire_df, geometry='geometry', crs="EPSG:4326")  # WGS84 projection

elif 'geometry' in fire_df.columns:
    # If already in WKT format, convert it
    fire_gdf = gpd.GeoDataFrame(fire_df, geometry=gpd.GeoSeries.from_wkt(fire_df['geometry']), crs="EPSG:4326")

else:
    raise ValueError("No valid latitude/longitude or geometry column found!")

# Convert to Web Mercator for basemap compatibility
fire_gdf = fire_gdf.to_crs(epsg=3857)

# Create a circular buffer (10km radius around each fire point)
fire_gdf['buffer'] = fire_gdf.geometry.buffer(50_000)  # 10,000 meters = 10km

# Plot fire points with buffers
fig, ax = plt.subplots(figsize=(12, 8))

# Plot buffers (transparent circles)
fire_gdf['buffer'].plot(ax=ax, alpha=0.3, color='red', edgecolor='black')

# Plot fire points
fire_gdf.plot(ax=ax, markersize=10, color='black', label='Fire Locations')

# Add basemap
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, alpha=0.8)

# Formatting
ax.set_title("Fire Locations with 50km Buffers")
ax.legend()
ax.set_axis_off()

plt.show()