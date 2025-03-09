import folium
from folium.plugins import HeatMap
import geopandas as gpd
import numpy as np

# Load Fire Perimeter Data
fire_gdf = gpd.read_file('fire_perimeters.geojson')

# Ensure CRS is lat/lon (EPSG:4326) for Folium compatibility
if fire_gdf.crs is not None and fire_gdf.crs.to_epsg() != 4326:
    fire_gdf = fire_gdf.to_crs(epsg=4326)

# Aggregate Data: Group fires by approximate location (rounding lat/lon)
fire_gdf["lat"] = fire_gdf.geometry.centroid.y.round(1)  # Round to 1 decimal
fire_gdf["lon"] = fire_gdf.geometry.centroid.x.round(1)
grouped = fire_gdf.groupby(["lat", "lon"]).agg(
    total_fires=("year", "count"),
    avg_size=("gis_acres", np.mean),
    avg_intensity=("rescaled_intensity", np.mean)
).reset_index()

# Create Folium Map
center = [fire_gdf.geometry.centroid.y.mean(), fire_gdf.geometry.centroid.x.mean()]
m = folium.Map(location=center, zoom_start=6, tiles="CartoDB Positron")

# Add Summary Markers
for _, row in grouped.iterrows():
    popup_text = f"""
    <b>Total Fires:</b> {row['total_fires']}<br>
    <b>Avg. Size (Acres):</b> {round(row['avg_size'], 1)}<br>
    <b>Avg. Intensity:</b> {round(row['avg_intensity'], 2)}
    """
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

# Scaled-up Heatmap (More visible)
heat_data = grouped[['lat', 'lon']].values.tolist()
HeatMap(heat_data, radius=25, blur=15, min_opacity=0.5).add_to(m)

# Save and Display
m.save("optimized_fire_map.html")

