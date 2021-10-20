import numpy as np
import rasterio
import time
import sys
import pyopencl as cl
import pyopencl.array as cl_array
import pyopencl.clrandom as clrand
import pyopencl.tools as cltools
from pyopencl.elementwise import ElementwiseKernel
import matplotlib.pyplot as plt


tile = int(sys.argv[1])

def landsat_gpu(tiles):

    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

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

    red_dev = cl_array.to_device(queue, red)
    nir_dev = cl_array.to_device(queue, nir)

    ndvi_dev = cl_array.empty_like(red_dev)

    # NDVI calculation
    ndvi_knl = ElementwiseKernel(ctx,
            "double *N, double *R, double *V",
            "V[i] = (N[i] - R[i]) / (N[i] + R[i])"
            )

    ndvi_knl(nir_dev, red_dev, ndvi_dev)

    ndvi = ndvi_dev.get()
    print(ndvi.shape)
    print(ndvi)

    print("Time Elapsed (Elementwise Map) with increase of", tiles,"x size: ", time.time() - t0)


def main():
    serial_processing(tiles=tile)

if __name__ == '__main__':
    main()
