'''Exploration script for input data.'''

from matplotlib.colors import ListedColormap
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import os
import imageio


def explore_input():
    path = "/Users/capucine/Documents/PhD/models/BIOME4/code/BIOME4/BIOME4_inputdata.nc"
    output_dir = "/Users/capucine/Documents/PhD/models/BIOME4/code/BIOME4/plots/"
    gif_path = "/Users/capucine/Documents/PhD/models/BIOME4/code/BIOME4/variables_over_time.gif"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ds = nc.Dataset(path)

    lat = ds.variables['lat'][:]
    lon = ds.variables['lon'][:]
    times = ds.variables['time'][:]

    variables = ['temp', 'prec', 'sun']
    titles = ['Temperature (°C)',
            'Precipitation (mm)',
            'Sunshine (%)']
    cmap = 'coolwarm'

    for t in range(len(times)):
        fig, axs = plt.subplots(1, len(variables), figsize=(15, 5))
        fig.suptitle(f'Time Step {t+1}')
        
        for i, var in enumerate(variables):
            data = ds.variables[var][t, :, :]
            data = np.ma.masked_where(data == ds.variables[var].missing_value, data)

            c = axs[i].contourf(lon, lat, data, cmap=cmap)
            fig.colorbar(c, ax=axs[i], orientation='vertical')
            axs[i].set_title(titles[i])
            axs[i].set_xlabel('Longitude')
            axs[i].set_ylabel('Latitude')

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        file_path = os.path.join(output_dir, f'time_step_{t+1}.png')
        plt.savefig(file_path)
        plt.close(fig)

    # Create GIF
    with imageio.get_writer(gif_path, mode='I', duration=4) as writer:
        for t in range(len(times)):
            file_path = os.path.join(output_dir, f'time_step_{t+1}.png')
            image = imageio.imread(file_path)
            writer.append_data(image)

    print(f"GIF saved to {gif_path}")



def explore_output():
    path = "/Users/capucine/Documents/PhD/models/BIOME4/code/BIOME4/output.nc"
    ds = nc.Dataset(path)

    # Extract the dimensions and variables
    biome = ds.variables['biome'][:]
    print("Biome shape", biome.shape)

    # Create latitude and longitude arrays based on the shape of the biome data
    lat = np.linspace(90, -90, biome.shape[0]) 
    lon = np.linspace(-180, 180, biome.shape[1])

    # Create a meshgrid for lat and lon
    lon, lat = np.meshgrid(lon, lat)

    # Define discrete categories for biomes
    biome_categories = np.unique(biome)
    n_categories = len(biome_categories)

    # Define a colormap for the categories
    cmap = ListedColormap(plt.cm.viridis(np.linspace(0, 1, n_categories)))

    # Plotting
    plt.figure(figsize=(12, 6))
    contour = plt.contourf(lon, lat, biome, levels=biome_categories, cmap=cmap, extend='both')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Biome Distribution')

    # Create a custom legend
    handles = [plt.Rectangle((0, 0), 1, 1, color=cmap(i / (n_categories - 1))) for i in range(n_categories)]
    labels = [f'Biome {int(cat)}' for cat in biome_categories]
    plt.legend(handles, labels, title='Biomes', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.savefig('/Users/capucine/Documents/PhD/models/BIOME4/code/BIOME4/biome_distribution.png', bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    explore_output()