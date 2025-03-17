"""
Signal generation utilities for testing adaptive filters. 
The notation matches the paper 'Adaptive cancellation of mains power interference in continuous gravitational 
wave searches with a hidden Markov model' (Physical Review D 110, 122004, 2024).
"""
import numpy as np
from ANC.utils import delay_sig, point_phase


def simulate_data(f_ac, fq, h0, sigma_n, W, N, sigma_r, A_ac, A_r, gamma_a, Δfac=1, sigma_theta=0.01,NumRef=1):
    """
    Generate simulated data for testing adaptive filters.
    
    The notation matches Equations (1)-(4) from the paper:
        x(t) = h(t) + c(t) + n(t)
    
    where x(t) is the strain channel output, h(t) is the GW signal, 
    c(t) is the non-Gaussian interference, and n(t) is Gaussian noise.
    
    Parameters:
    -----------
    f_ac : float
        Center frequency of reference (mains power, fac in paper, typically 60 Hz)
    fq : ndarray
        Array of frequencies for GW signal
    h0 : float
        GW signal amplitude
    sigma_n : float
        Standard deviation of Gaussian noise (strain channel)
    W : float
        Sampling frequency
    N : int
        Number of samples per block
    sigma_r : float
        Standard deviation of reference signal measurement noise
    A_ac : float
        Amplitude of reference signal
    A_r : float
        Amplitude factor for reference
    gamma_a : float
        Phase fluctuation parameter (related to 1/P in the paper)
    Δfac : float, optional
        Amplitude of phase modulation (Δfac in paper), default is 1
    sigma_theta : float, optional
        Standard deviation of phase noise (σΘ in paper), default is 0.01
        
    Returns:
    --------
    x : ndarray
        Primary signal (signal + line noise + Gaussian noise)
    R : ndarray
        Reference signals
    h : ndarray
        Injected GW signal
    t : ndarray
        Time vector
    r0 : ndarray
        Original reference signal
    c : ndarray
        Clutter/interference signal
    """
    NT = len(fq)
    dt = 1/W
    t_delay = np.random.rand() * dt * 100  # Time delay between reference and clutter (τdelay in paper)
    
    t = np.arange(0, N*NT) / W
    
    #taug = np.arange(0, N*NT+101) / W  # Longer time vector for noise generation
    
    T = N/W  # Time within one block
    

    # Generate the clutter signal
    P = 1/gamma_a
    n_θ = np.random.randn(len(t)) * sigma_theta
    Θ = 2*np.pi * Δfac*np.cos(2*np.pi*t/P) + n_θ
    c = A_r * np.cos(2*np.pi*f_ac*t + Θ) 



    # Generate reference signals with phase shifts
    tdelta = np.array([0, 1/3/f_ac, 2/3/f_ac])  # 3 phase power

    R = np.zeros((len(t), NumRef))
    for n in range(NumRef):
        # Generate the reference, which occurs at some earlier time
        n_θ_delayed = delay_sig(n_θ, dt, -(t_delay + tdelta[n]))
        
        # Time-shifted signal (related to τdelay in Equation 4)
        tt = t  - (t_delay + tdelta[n])
        phase_delayed = 2*np.pi * Δfac*np.cos(2*np.pi*tt/P) + n_θ_delayed
        
        r = A_r * np.cos(2*np.pi*f_ac*tt + phase_delayed) + np.random.randn(len(t)) * sigma_r  # Changed to cosine
        R[:, n] = r
    
    # Generate injected GW signal (Equation 18)
    # h(t) = h0 sin[2πϕgw(t)]
    p = point_phase(fq, t[:N], T)  
    h = h0 * np.sin(2*np.pi*p)  # Paper uses sine for GW signal, so keeping as is
    
    # Generate primary signal (Equation 1)
    # x(t) = h(t) + c(t) + n(t)
    x = h + c + np.random.randn(len(t)) * sigma_n
    
    return x, R, h, t