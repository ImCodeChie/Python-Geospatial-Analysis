import geopandas as gpd
import pandas as pd
import os

print("\nStarting...\n")

# Input shapefiles
shapefiles_directory = r"C:\Users\lyi\Desktop\Brazil_Crop_ID\Selection_CropID\Output\All_v2"

# List all shapefiles in the directory
shapefiles = [f for f in os.listdir(shapefiles_directory) if f.endswith('.shp')]

# Create an empty GeoDataFrame to store the merged data
merged_gdf = gpd.GeoDataFrame()

# Iterate through each shapefile
for shapefile in shapefiles:
    # Read the shapefile
    gdf = gpd.read_file(os.path.join(shapefiles_directory, shapefile))

    # Concatenate with the main GeoDataFrame
    merged_gdf = pd.concat([merged_gdf, gdf], ignore_index=True, sort=False)

# Save the merged shapefile with all crops
output_merged_shapefile = r"C:\Users\lyi\Desktop\Brazil_Crop_ID\Selection_CropID\Output\Final\merged_all_crops.shp"
merged_gdf.to_file(output_merged_shapefile)

# Extract 3 shapefiles by sowing year
output_directory = r"C:\Users\lyi\Desktop\Brazil_Crop_ID\Selection_CropID\Output\Final"
for sowing_year in merged_gdf['sowing'].unique():
    sowing_year_gdf = merged_gdf[merged_gdf['sowing'] == sowing_year].copy()
    
    # Include harvest year in the output shapefile name
    harvest_year = sowing_year_gdf['harvest'].iloc[0]  
    
    # Save the shapefile with both sowing and harvest years
    output_shapefile = os.path.join(output_directory, f"merged_{sowing_year}_{harvest_year}_all_crops.shp")
    sowing_year_gdf.to_file(output_shapefile)

print("Merge and save completed.\n")
