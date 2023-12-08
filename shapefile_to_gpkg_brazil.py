import os
import geopandas as gpd

def convert_shapefiles_to_geopackage(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".shp"):
                shapefile_path = os.path.join(root, filename)

                # Read the shapefile
                gdf = gpd.read_file(shapefile_path)

                # Drop the 'fid' column if it exists
                if 'fid' in gdf.columns:
                    gdf = gdf.drop('fid', axis=1)

                # Set the geometry column if not already set
                if gdf.geometry.name != 'geometry':
                    gdf = gdf.set_geometry('geometry')

                # Create a GeoPackage file for each shapefile
                output_geopackage_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.gpkg")

                # Use 'GPKG' as the driver, not '.gpkg'
                try:
                    gdf.to_file(output_geopackage_path, driver='GPKG')
                    print(f"Successfully converted {shapefile_path}")
                except Exception as e:
                    print(f"Error converting {shapefile_path}: {e}")

if __name__ == "__main__":
    # Replace 'input_folder' and 'output_folder' with your folder paths
    input_folder = r'C:\Users\lyi\Desktop\Clip_validation\Brazil_clip\result\clipped_tiles\Shapefile'
    output_folder = r'C:\Users\lyi\Desktop\Clip_validation\Brazil_clip\result\clipped_tiles\geopkg'

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    convert_shapefiles_to_geopackage(input_folder, output_folder)

print('task is finished')
