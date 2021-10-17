from numba.pycc import CC
from numba import njit
import numpy as np

# name of compiled module to create:
cc = CC('rho_loop')

@cc.export('loop_lifetimes', 'f8[:,:](i2, i2, f4, f4, f4, f8[:,:], f8[:,:])')
@njit
def loop_lifetimes(S, T, z_0, rho, mu, eps_mat, z_mat):
    for s_ind in range(S):
      z_tm1 = z_0
      for t_ind in range(T):
        e_t = eps_mat[t_ind, s_ind]
        z_t = rho * z_tm1 + (1 - rho) * mu + e_t
        z_mat[t_ind, s_ind] = z_t
        z_tm1 = z_t
    return z_mat

# name of function in module, with explicit data types required (4byte=32bit ints and floats)
@cc.export('loop_rho_vals', 'f8[:,:](i2, i2, f4, f8[:], f4, f8[:,:], f8[:,:], f8[:,:])')
def loop_rho_vals(S, T, z_0, rho_rank, mu, eps_mat, z_mat, rho_mat):
  for rho_idx, rho in enumerate(rho_rank):
    #print('considering rho',rho)
    z_mat = loop_lifetimes(S, T, z_0, rho, mu, eps_mat, z_mat)
      
    # create array to store min time period when hit zero for each life
    # default to 50 if never hit zero
    
    min_life_0_period = np.full((S,2), T, dtype=np.int16)
    min_life_0_period[:,0] = np.arange(S)

    print('z_mat.shape[1]',z_mat.shape[1])
    for person in range(z_mat.shape[1]):
      col = z_mat[person,:]
      #print('considering person',person)
      for col_idx, z in enumerate(col):
        if z <= 0:
          min_life_0_period[person,1] = col_idx
          #print('found first subzero health',z,'at time',col_idx)
          break
        else:
          pass

    rho_mat[rho_idx,0] = rho
    rho_mat[rho_idx,1:] = min_life_0_period[:,1].ravel()
    #print('current row of rho mat:',rho_mat[rho_idx,:])

  return rho_mat


cc.compile()