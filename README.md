# 1
## (a)

The original version of the code simulated 1000 lifetimes on a single core in 3.431394 seconds (run using health_sim_orig.sbatch and reported in health_sim_orig.out).  
  
The version of the code which used numba to pre-compile the nested for loops simulated 1000 lifetimes on a single core in 0.463110 seconds (run using health_sim_numbacc.sbatch and reported in health_sim_numbacc.out).  
  
By pre-compiling with numba, we saw a speedup from 3.43 seconds to 0.46 seconds, which is a time savings of 2.97 seconds, or equivalently 626% faster than the original script.  
  
## (b)
  
![Time to Simulate against Number of Cores](simtime_cores.png)

## (c)

The speedup isn't linear because it is limited by the serial components of the process, namely the need to create our initial objects (eps_mat and empty z_mat), as predicted by Amdahl's Law. We're also not increasing the size of the data, which would allow us to see closer to linear speed-up according to Gustafson-Barsis's Law. 


# 2
## (a)
  
The mean time for each core to process its 20 values of $\rho$ over 1000 lifetimes was 1.638 seconds.  
  
## (b)
  
![Time to Reach Negative Health by Persistence](rho_tests.png)  

## (c)
  
The optimal persistence, $\rho$ is 0: with a 0 persistence, it takes approximately 1450 periods to reach a point where health drops below 0. 
  

# 3
## (a)

Running on a single CPU core on Midway, the serial code took 1.1387 seconds to complete.  
  
By contrast, the GPU version on Midway took 4.668 seconds to complete.   

## (b)
  
This is far slower than the original CPU implementation, and it is likely due in part to needing to send our raster arrays to the GPU for processing, then receive them back to the CPU. Transferring data to and from GPUs is a known limitation on speed, so in this case it seems not worth the increased parallelizability the GPU offers.  
  
## (c)








# Sources:

https://thispointer.com/find-max-value-its-index-in-numpy-array-numpy-amax/
