'''Exploration script for input data.'''

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt


def explore_input():
    path = "/home/lechartr/BIOME4/BIOME4_inputdata.nc"
    ds = nc.Dataset(path)
    for dim in ds.dimensions.values():
        print(dim)


     # Extract the dimensions and variables
    lat = ds.variables['lat'][:]
    lon = ds.variables['lon'][:]
    temp = ds.variables['sun'][:]

    print(temp.shape) # (12, 360, 720) for time, lon and lat
    temp_data = temp[0, :, :] # for the first time step

    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.contourf(lon, lat, temp_data, cmap='coolwarm')
    plt.colorbar(label='Sun')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Sunlight (exposure?) Distribution')

    # Save the plot as a PNG file
    plt.savefig('/home/lechartr/BIOME4/sun_distribution.png')

    # Display the plot
    plt.show()


def explore_output():
    path = "/Users/capucine/Documents/PhD/models/BIOME4/code/BIOME4/output.nc"
    ds = nc.Dataset(path)

    # Extract the dimensions and variables
    biome = ds.variables['biome'][:]
    print("Biome shape", biome.shape)

    # # Create latitude and longitude arrays based on the shape of the biome data
    lat = np.linspace(180, -180, biome.shape[0]) 
    lon = np.linspace(-360, 360, biome.shape[1])


    # Create a meshgrid for lat and lon
    lon, lat = np.meshgrid(lon, lat)

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.contourf(lon, lat, biome, cmap='viridis')
    plt.colorbar(label='Biome')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Biome Distribution')
    plt.savefig('/Users/capucine/Documents/PhD/models/BIOME4/code/BIOME4/biome_distribution.png')
    plt.show()


if __name__ == "__main__":
    explore_output()