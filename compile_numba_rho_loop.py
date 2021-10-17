from numba.pycc import CC
import numpy as np

# name of compiled module to create:
cc = CC('rho_loop')

# name of function in module, with explicit data types required (4byte=32bit ints and floats)
@cc.export('loop_rho_vals', 'f8[:,:](i2, i2, f4, f8[:], f4, f8[:,:], f8[:,:], f8[:,:])')
def loop_rho_vals(S, T, z_0, rho_rank, mu, eps_mat, z_mat, rho_mat):
  for rho_idx, rho in enumerate(rho_rank):
    #print('considering rho',rho)
    for s_ind in range(S):
      z_tm1 = z_0
      for t_ind in range(T):
        e_t = eps_mat[t_ind, s_ind]
        z_t = rho * z_tm1 + (1 - rho) * mu + e_t
        z_mat[t_ind, s_ind] = z_t
        z_tm1 = z_t
      
    # create array to store min time period when hit zero for each life
    # default to 50 if never hit zero
    min_life_0_period = np.full((S,2), T, dtype=np.int16)
    min_life_0_period[:,0] = np.arange(S)

    for person in range(z_mat.shape[0]):
      col = z_mat[person,:]
      #print('considering person',person)
      for col_idx, z in enumerate(col):
        if z <= 0:
          min_life_0_period[person,1] = col_idx
          #print('found first subzero health',z,'at time',col_idx)
          break

    rho_mat[rho_idx,0] = rho
    rho_mat[rho_idx,1] = np.mean(min_life_0_period[:,1])
    #print('current row of rho mat:',rho_mat[rho_idx,:])

  return rho_mat

cc.compile()
