'''Exploration script for input data.'''

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt


def main():
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

if __name__ == "__main__":
    main()