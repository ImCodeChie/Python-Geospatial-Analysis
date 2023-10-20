import rasterio
from rasterio.mask import mask
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from rasterio import Affine
import numpy as np
import os
import glob
import psutil
import warnings

# Get memory usage information
mem = psutil.virtual_memory()

# Extract required memory statistics
total_memory = mem.total
available_memory = mem.available
used_memory = mem.used
memory_percentage = mem.percent

# Load the shapefile
shapefile = gpd.read_file(r"C:....\\Boundary.shp")

# Specify the folder path containing the TIFF files
folder_path = r"C:....\\Folder"

# Search for TIFF files in the folder
tiff_files = glob.glob(os.path.join(folder_path, "*.tif"))

print("Start...\n")

# Print memory statistics
print("Total Memory:", total_memory)
print("Available Memory:", available_memory)
print("Used Memory:", used_memory)
print("Memory Usage Percentage:", memory_percentage, "\n")

# Iterate over each TIFF file
for tiff_file in tiff_files:
    print(f"Processing file: {tiff_file}")

    # Open the raster tile
    with rasterio.open(tiff_file) as src:
        # Extract the raster values within the shapefile geometry
        out_image, out_transform = mask(src, shapefile.geometry, crop=True)

        # No data values of the original raster
        no_data = src.nodata
        print(no_data)  # -9999.0

        print("Please wait...\n")

        # Iterate over blocks of the raster data
        block_size = 1000
        for i in range(0, out_image.shape[1], block_size):
            for j in range(0, out_image.shape[2], block_size):
                # Extract the block of data
                block = out_image[:, i:i+block_size, j:j+block_size]

                # Transformation function
                T1 = out_transform * Affine.translation(0.5, 0.5)  # reference the pixel center
                rc2xy = lambda r, c: T1 * (c, r)

                # Create lists to store the coordinates and pixel values
                x_coords = []
                y_coords = []
                pixel_values = []

                # Iterate over each pixel in the block
                for band in range(block.shape[0]):
                    for row in range(block.shape[1]):
                        for col in range(block.shape[2]):
                            # Calculate the coordinates of the pixel center
                            x, y = rc2xy(row+i, col+j)

                            # Get the pixel value
                            pixel_value = block[band, row, col]

                            # Add the coordinates and pixel value to the lists
                            x_coords.append(x)
                            y_coords.append(y)
                            pixel_values.append(pixel_value)

                # Create a DataFrame for the block
                d = pd.DataFrame({'x': x_coords, 'y': y_coords, 'pixel_value': pixel_values})

                # Create a spatial index for the shapefile
                shapefile_spatial_index = shapefile.sindex

                # Create a list to store the name attribute
                name_attribute = []

                # Iterate over each point in the block and find its corresponding name attribute
                for idx, row in d.iterrows():
                    point = Point(row['x'], row['y'])
                    intersected_indices = list(shapefile_spatial_index.intersection(point.bounds))
                    for intersected_idx in intersected_indices:
                        if shapefile.geometry[intersected_idx].contains(point):
                            name_attribute.append(shapefile.loc[intersected_idx, 'Name'])
                            break
                    else:
                        name_attribute.append(None)

                # Add the name attribute to the DataFrame
                d['Name'] = name_attribute

                # Specify the folder path for saving results
                output_folder = r"C:.....\\Result"

                # Create the full file path
                file_name = os.path.splitext(os.path.basename(tiff_file))[0]
                file_path = os.path.join(output_folder, f"{file_name}_block_{i}_{j}.csv")

                # Export the DataFrame to a CSV file
                print("Exporting CSV file to the directory, please wait...\n")

                # Save the DataFrame to a CSV file
                d.to_csv(file_path, index=False)

    # Print completion message for the current file
    print(f"Processing complete for {tiff_file}")

# Print completion message after processing all files
print("All files processed successfully!")
