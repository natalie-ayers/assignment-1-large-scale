from numba.pycc import CC

# name of compiled module to create:
cc = CC('life_loop')

# name of function in module, with explicit data types required (4byte=32bit ints and floats)
@cc.export('loop_lifetimes', 'f8[:,:](i2, i2, f4, f4, f4, f8[:,:], f8[:,:])')
def loop_lifetimes(S, T, z_0, rho, mu, eps_mat, z_mat):
    for s_ind in range(S):
      z_tm1 = z_0
      for t_ind in range(T):
        e_t = eps_mat[t_ind, s_ind]
        z_t = rho * z_tm1 + (1 - rho) * mu + e_t
        z_mat[t_ind, s_ind] = z_t
        z_tm1 = z_t
    return z_mat

cc.compile()

print('successfully compiled life_loop function')