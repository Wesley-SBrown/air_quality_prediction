import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

# Load Fire Perimeter Data (Ensure it's in a GeoDataFrame)
fire_gdf = gpd.read_file('fire_perimeters.geojson')  # Adjust filename

# Convert to Web Mercator projection (needed for accurate buffers & basemap)
fire_gdf = fire_gdf.to_crs(epsg=3857)

# Create a buffer (10km around each fire perimeter)
fire_gdf['buffer'] = fire_gdf.geometry.buffer(50_000)  # 10,000 meters = 10km

# Plot
fig, ax = plt.subplots(figsize=(12, 9))

# Plot Buffers (semi-transparent)
fire_gdf['buffer'].plot(ax=ax, alpha=0.3, color='blue', edgecolor='black', linewidth=0.5, label="10km Buffer")

# Plot Fire Perimeters (outlines)
fire_gdf.plot(ax=ax, alpha=0.5, edgecolor='red', facecolor='none', linewidth=1, label="Fire Perimeter")

# Add Topographic Basemap
ctx.add_basemap(ax, source=ctx.providers.OpenTopoMap)

# Labels & Formatting
ax.set_title('Fire Perimeters with 10km Buffers on a Topographical Map', fontsize=14)
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.legend()
ax.set_axis_off()  # Hide axis labels for a cleaner map

plt.show()

