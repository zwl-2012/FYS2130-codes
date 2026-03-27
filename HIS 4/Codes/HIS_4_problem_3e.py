import numpy as np
import matplotlib.pyplot as plt

#------------------------------------------------------------------------#
                        ########## Problem 3 ##########
#------------------------------------------------------------------------#

########## Global values ##########
g = 9.81                    # gravitational acceleration
k0 = 2*np.pi                # Gaussian center
sigma = 0.2                 # surface tension
rho = 0.2                   # density


##### Amplitude #####
def A(k): return np.e**(-(k-k0)**2/(2*sigma**2))


##### #1 Non-dispersive #####
def w_non(k, v=1): return v*k


##### #2 Normal dispersion #####
def w_normal(k): return np.sqrt(g*abs(k))


##### #3 Anomalous dispersion #####
def w_anomalous(k): return np.sqrt(sigma/rho) * abs(k)**(3/2)


##### Create x-interval #####
def create_interval(X, dx):
    N = int(2*X/dx)
    x_interval = np.linspace(-X, X, N+1)
    return x_interval


##### Create time series elements #####
def create_time_jumps(T, periods):
    '''create time jumps "uniformly" '''
    t_jumps = np.linspace(0, T, periods)
    return t_jumps


########## Main action ##########
def plot_wave_packet(X, dx, T, w_type, periods=4, dk=0.1):
    '''X --- the x-interval range
    dx --- x step
    T --- end time
    w_type --- a list with 2 elements: [w_function, dispersion_type (int)]
    periods --- number of time series
    K --- the sum of different wavenumbers, discretization of integral
    '''
    
    x_interval = create_interval(X, dx)
    t_jumps = create_time_jumps(T, periods)
    
    k_lst = np.arange(k0-10*np.pi, k0 + 10*np.pi + dk, dk)
    
    if w_type[1] == 1: title = "Non-dispersive"
    elif w_type[1] == 2: title = "Normal dispersion"
    else: title = "Anomalous dispersion"
    
    w_func = w_type[0]
    
    
    for t in t_jumps:
        count = 0
        psi_interval = np.zeros(len(x_interval))
        for x in x_interval:
            psi = A(k_lst) * np.cos(k_lst * x - w_func(k_lst)*t) * dk
            psi_interval[count] = sum(psi)
            count += 1
            
        plt.plot(x_interval, psi_interval, label=f"t={t:.2f}s")
    plt.xlabel("x [m]"); plt.ylabel("Psi(x,t)"); plt.legend()
    plt.title(title + f" | dk={dk} | dx={dx}"); plt.show()
    

#---------------------------------------------------------#
                ########## ACTION ##########
#---------------------------------------------------------#
if __name__ == "__main__":
    print("Problem 3 e)")
    
    ########## Initial conditions ##########
    X, dx = 10, 0.01
    T = 2
    dk = 0.01
    periods = 3
    
    
    ########## Non-dispersive plot ##########
    w_nondisp = [w_non, 1]
    plot_wave_packet(X, dx, T, w_nondisp, periods=periods, dk=dk)
    
    
    ########## Normal dispersion plot ##########
    w_norm = [w_normal, 2]
    plot_wave_packet(X, dx, T, w_norm, periods=periods, dk=dk)
    
    
    ########## Anonmalous dispersion plot ##########
    w_anom = [w_anomalous, 3]
    plot_wave_packet(X, dx, T, w_anom, periods=periods, dk=dk)
    