# Import required libraries
import rasterio
import numpy as np
import time
import sys

tile = sys.argv[1]
print('factor to increase data size',tile)

def serial_processing(tiles):

    t0 = time.time()

    # Import bands as separate images; in /project2/macs30123 on Midway2
    band4 = rasterio.open(
    '/project2/macs30123/landsat8/LC08_B4.tif') #red
    band5 = rasterio.open(
    '/project2/macs30123/landsat8/LC08_B5.tif') #nir

    # Convert nir and red objects to float64 arrays
    red = band4.read(1).astype('float64')
    nir = band5.read(1).astype('float64')

    red = np.tile(red, tiles)
    nir = np.tile(nir, tiles)

    # NDVI calculation
    ndvi = (nir - red) / (nir + red)

    print('time elapsed for serial NDVI calculation with ',tiles,'x increase:', time.time() - t0)


def main():
    serial_processing(tiles=tile)

if __name__ == '__main__':
    main()
