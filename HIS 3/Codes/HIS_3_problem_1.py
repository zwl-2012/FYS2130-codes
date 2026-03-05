import numpy as np
import matplotlib.pyplot as plt

#---------------------------------------------------------#
                ########## a) ##########
#---------------------------------------------------------#

#### Decaying signal ####
def x_signal(t, f0, tau): return np.cos(2*np.pi*f0*t)*np.e**(-abs(t)/tau)



#### Compute signal over time interval ####
def compute_x_signal(f0, tau, interval, dt):
    ts = np.arange(interval[0], interval[1]+dt, dt)
    xs = x_signal(ts, f0, tau)
    return xs, ts



#### Compute FFT (DFT) of x, using built-in libraries ####
def FFT(x): return np.fft.fft(x)



#### Compute frequency bin of FFT ####
def FFT_freq(x, dt): return np.fft.fftfreq(len(x), d=dt)



#### Plot time domain ####
def plot_domain_time(ts, xs, Xs, f_s):
    plt.plot(ts, xs, color="black", label="x(t)")
    #plt.plot(ts, abs(Xs))
    plt.xlabel("t [s]"); plt.ylabel("x(t)"); plt.legend()
    plt.title(f"Time domain  f_s={f_s} Hz"); plt.show()



#### Plot frequency domain ####
def plot_domain_frequency(freqs, Xs, f_s, f_nyq, state=None):
    # Only need the first half of freqs (only the positives matter)
    half = 0; n = len(freqs)
    if n % 2 == 0: half = int(n/2-1)
    else: half = int((n-1)/2)
    
    # state determines whether plot is semilog or not
    if state == "log": # Semilog scale
        plt.plot(freqs[:half+1], np.abs(Xs[:half+1]), label="FFT magnitude")
        plt.xlabel("Frequency [Hz]"); plt.ylabel("|X(f)| (log scale)")
        plt.title(f"Frequency domain (semilog) f_s={f_s}, f_Nyq={f_nyq} Hz")
        plt.yscale("log"); plt.legend(); plt.show()
        
    else: # Ordinary scale
        plt.plot(freqs[:half+1], np.abs(Xs[:half+1]), label="FFT magnitude")
        plt.xlabel("Frequency [Hz]"); plt.ylabel("|X(f)| (log scale)"); plt.legend()
        plt.title(f"Frequency domain  f_s={f_s}, f_Nyq={f_nyq} Hz"); plt.show()




#---------------------------------------------------------#
                ########## b) ##########
#---------------------------------------------------------#


#### Plot frequency domain with main peak frequency ####
def plot_domain_frequency_peak(freqs, Xs, f_s, f_nyq, f0, state=None):
    half = 0; n = len(freqs)
    if n % 2 == 0: half = int(n/2-1)
    else: half = int((n-1)/2)
    
    # state determines whether plot is semilog or not
    if state == "log": # Semilog scale
        plt.plot(freqs[:half+1], np.abs(Xs[:half+1]), label="FFT magnitude")
        plt.axvline(f0, color="red", linestyle="dashed", label="FFT Peak / f0")
        plt.xlabel("Frequency [Hz]"); plt.ylabel("|X(f)| (log scale)")
        plt.title(f"Frequency domain (semilog) f_s={f_s}, f_Nyq={f_nyq} Hz")
        plt.yscale("log"); plt.legend(); plt.show()
        
    else: # Ordinary scale
        plt.plot(freqs[:half+1], np.abs(Xs[:half+1]), label="FFT magnitude")
        plt.axvline(f0, color="red", linestyle="dashed", label="FFT Peak / f0")
        plt.xlabel("Frequency [Hz]"); plt.ylabel("|X(f)| (log scale)"); plt.legend()
        plt.title(f"Frequency domain  f_s={f_s}, f_Nyq={f_nyq} Hz"); plt.show()




#---------------------------------------------------------#
                ########## ACTION ##########
#---------------------------------------------------------#
if __name__ == "__main__":
    
    print("a) Sampling and FFT")
    
    ##### Initial conditions #####
    f0 = 10                     # Carrier frequency (Hz)
    f_s = 200                   # Sampling frequency (Hz)
    f_nyq = f_s/2               # Nyquist frequency (Hz)
    tau = 0.3                   # Signal decay (s)
    T = 3                       # Time T (s)
    interval = [-T/2, T/2]      # Total time interval
    dt = 1/f_s                  # timestep (s)
    
    
    
    ##### Make computations #####
    xs, ts = compute_x_signal(f0, tau, interval, dt)
    Xs = FFT(xs); #Xs = np.real(Xs)
    freqs = FFT_freq(xs, dt)

    
    ##### Plot time and frequency domains #####
    plot_domain_time(ts, xs, Xs, f_s)
    plot_domain_frequency(freqs, Xs, f_s, f_nyq, "log")
    
    
    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
    
    
    
    print("b) Dominant frequency")
    
    ##### Plot frequency domain with f0 peak #####
    plot_domain_frequency_peak(freqs, Xs, f_s, f_nyq, f0, "log")
    
    
    
    ########## Why does peak has finite width? ##########
    """The peak (f0) in frequency domain is finite because DFT is 
    a finite series which means that the sum is finite. 
    The sum is finite because the time interval is finite. """
    
    
    
    
    ########## What happens when decay scale is tau=0.6 ? ##########
    """x(t) will decay slower
    Peak remains the same in frequency domain
    FFT magnitude have oscillations further away from the peak frequency"""
    
    ##### New initial conditions #####
    new_tau = 0.6
    
    
    ##### Computations #####
    xs, ts = compute_x_signal(f0, new_tau, interval, dt)
    Xs = FFT(xs)
    freqs = FFT_freq(xs, dt)
    
    
    
    ##### Plot time and frequency domain with peak f0 and new tau #####
    plot_domain_time(ts, xs, Xs, f_s)
    plot_domain_frequency_peak(freqs, Xs, f_s, f_nyq, f0, "log")
    
    
    
    
    ########## How does varying T affect it? ##########
    """Smaller T: more oscillations further from peak frequency
    Bigger T: less osillations, more smooth"""
    
    ##### New initial conditions #####
    Ts = [T-2, T, T+2]
    
    
    ##### Computations #####
    
    for T in Ts:
        print(f"T={T}s")
        xs, ts = compute_x_signal(f0, tau, [-T/2, T/2], dt)
        Xs = FFT(xs); freqs = FFT_freq(xs, dt)
        
        #plot_domain_time(ts, xs, Xs, f_s)
        plot_domain_frequency_peak(freqs, Xs, f_s, f_nyq, f0, "log")
        
        print(len(ts))
        print(max(np.abs(Xs)))
    
    
    
    
    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
    
    
    
    print("c) Undersampling and aliasing")
    
    ########## Repeat a) with lower sampling frequency ##########
    
    ##### New initial conditions #####
    f0 = 10                     # Carrier frequency (Hz)
    f_s = 15                    # Sampling frequency (Hz)
    f_nyq = f_s/2               # Nyquist frequency (Hz)
    tau = 0.3                   # Signal decay (s)
    T = 3                       # Time T (s)
    interval = [-T/2, T/2]      # Total time interval
    dt = 1/f_s                  # timestep (s)
    
    
    ##### Make computations #####
    xs, ts = compute_x_signal(f0, tau, interval, dt)
    Xs = FFT(xs)
    freqs = FFT_freq(xs, dt)

    
    ##### Plot time and frequency domains #####
    plot_domain_time(ts, xs, Xs, f_s)
    plot_domain_frequency(freqs, Xs, f_s, f_nyq, "log")
    
    
    
    ##### Compare different f_s for time and frequency domains #####
    f_s_old = 200; dt_old = 1/f_s_old
    xs_old, ts_old = compute_x_signal(f0, tau, interval, dt_old)
    Xs_old = FFT(xs_old)
    freqs_old = FFT_freq(xs_old, dt_old)
    
    plt.plot(ts_old, xs_old)
    plt.plot(ts, xs, linestyle="dashed", color="red")
    plt.xlabel("t [s]"); plt.ylabel("x(t)"); plt.show()
    
    
    
    ########## What happens? ##########
    """Time domain: x(t) is unable to sample all values of signal
    In time domain the signal is misinterpreted as a new signal with lower frequency. 
    The frequency domain reaches a peak for an entirely different frequency 
    than the carrier frequency f0. """
    
