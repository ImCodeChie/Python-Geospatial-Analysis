import geopandas as gpd
import pandas as pd
import random

print("\nStarting...\n")
print("Wait, task is ongoing...\n")

# Input shapefile
input_shapefile = r"C:\Users\lyi\Desktop\Brazil_Crop_ID\Selection_CropID\AllCrop.shp"
gdf = gpd.read_file(input_shapefile)

# Exclude parcels with QC = 0
gdf = gdf[gdf['QC'] != 0]

# Set the 'geometry' column
gdf = gdf.set_geometry('geometry')

# Define crop types (Activate only target crop)
#crop_type = 'SUGARCANE'
#crop_type = 'SOYBEANS'
#crop_type = 'CORN'
#crop_type = 'COTTON'
crop_type = 'RICE'

# Max nuumber of fields for the crop type
num_fields_per_crp_type = 600

# Specify the desired number of parcels for each year
num_fields_per_year = {
    '2021': 129,
    '2020': 0,
    '2019': 471,
    # '2018': 150,  #if needed
}

# Create an empty GeoDataFrame to store the selected parcels for training
selected_gdf_train = gpd.GeoDataFrame()

# Track selected indices to avoid repetition
selected_indices_train = set()

# Track selected parcels for the crop type and year
selected_parcels = {'train': set()}

# Function to check if the total number of selected parcels is reached for the crop type
def check_total_selected(year):
    return len(selected_parcels[year]) == num_fields_per_crp_type

# Filter parcels for the current crop type
crp_type_gdf = gdf[(gdf['crp_code'] == crop_type)]

# Randomly select parcels for the current crop type and sowing year for training
for year, num_fields in num_fields_per_year.items():
    sowing_years_gdf_train = crp_type_gdf[crp_type_gdf['sowing'] == year]
    num_selected_parcels_train = min(num_fields, len(sowing_years_gdf_train))

    available_indices_train = list(set(sowing_years_gdf_train.index) - selected_indices_train - selected_parcels['train'])
    num_selected_parcels_train = min(num_selected_parcels_train, len(available_indices_train))

    if num_selected_parcels_train > 0:
        selected_parcels_train = random.sample(available_indices_train, num_selected_parcels_train)
        selected_indices_train.update(selected_parcels_train)
        selected_parcels['train'].update(list(selected_parcels_train))

# Include parcels from the remaining years for training, if needed
while len(selected_parcels['train']) < num_fields_per_crp_type:
    # Sort remaining_years_gdf_train by the sowing year in descending order
    remaining_years_gdf_train = crp_type_gdf[~crp_type_gdf.index.isin(selected_indices_train)].sort_values(by='sowing', ascending=False)
    num_selected_parcels_train = min(num_fields_per_crp_type - len(selected_parcels['train']), len(remaining_years_gdf_train))

    if num_selected_parcels_train > 0:
        selected_parcels_train = random.sample(list(remaining_years_gdf_train.index), num_selected_parcels_train)
        selected_indices_train.update(selected_parcels_train)
        selected_parcels['train'].update(selected_parcels_train)

# Create the final GeoDataFrame with selected parcels
selected_gdf_train = crp_type_gdf.loc[list(selected_parcels['train'])]

# Save the output shapefile for training
shapefile_train = r"C:\Users\lyi\Desktop\Brazil_Crop_ID\Selection_CropID\Output\shapefile_train.shp"
selected_gdf_train.to_file(shapefile_train)

print("Training GeoDataFrame saved.\n")
print("Task completed.\n")
