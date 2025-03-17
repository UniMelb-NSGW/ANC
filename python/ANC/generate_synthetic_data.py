"""
Signal generation utilities for testing adaptive filters. 
The notation matches the paper 'Adaptive cancellation of mains power interference in continuous gravitational 
wave searches with a hidden Markov model' (Physical Review D 110, 122004, 2024).
"""
import numpy as np
from ANC.utils import delay_sig, point_phase


def simulate_data(f0, fq, h0, sigma_n, W, N, sigma_r, A_ac, A_r, gamma_a, D_fac=1, sigma_theta=0.01):
    """
    Generate simulated data for testing adaptive filters.
    
    The notation matches Equations (1)-(4) from the paper:
        x(t) = h(t) + c(t) + n(t)
    
    where x(t) is the strain channel output, h(t) is the GW signal, 
    c(t) is the non-Gaussian interference, and n(t) is Gaussian noise.
    
    Parameters:
    -----------
    f0 : float
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
    D_fac : float, optional
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
    t0 = np.random.rand() * dt * 10  # Random time delay for reference
    t_delay = np.random.rand() * dt * 100  # Time delay between reference and clutter (τdelay in paper)
    
    t = np.arange(0, N*NT) / W
    taug = np.arange(0, N*NT+101) / W  # Longer time vector for noise generation
    T = N/W  # Time within one block
    
    # Generate magnitude with small random variations for reference
    Ar_t = np.random.rand(len(t)) / 1000 + A_ac
    
    # Generate phase with modulation and noise (Equation 3)
    # Θ(t) = 2πΔfac cos(2πt/P) + nΘ(t)
    theta_t = 2*np.pi*D_fac*np.cos(2*np.pi*gamma_a*t)
    n_theta = np.random.randn(len(taug)) * sigma_theta
    
    # Generate original reference signal (Equation 2)
    # r(t) = Ar(t) cos[2πfact + Θ(t)] + nr(t)
    r0 = Ar_t * np.cos(2*np.pi*f0*t + theta_t + n_theta[:len(t)]) + np.random.randn(len(t)) * sigma_r
    
    # Generate clutter signal (Equation 4)
    # c(t) = Ac(tn - τdelay) cos[2πfac(tn - τdelay) + Θ(tn - τdelay)]

    A_c = A_ac * 1.2  # Different amplitude for interference
    
    # Calculate delayed time points for clutter
    t_c = np.maximum(t - t_delay, 0)  # Ensure non-negative time
    
    # Delayed phase components for clutter
    theta_t_delayed = 2*np.pi*D_fac*np.cos(2*np.pi*gamma_a*t_c)
    n_theta_delayed = delay_sig(n_theta, dt, t_delay)[:len(t)]
    
    # Generate clutter signal
    A_c_t = np.random.rand(len(t)) / 1000 + A_c  # Small variations in clutter amplitude
    c = A_c_t * np.cos(2*np.pi*f0*t_c + theta_t_delayed + n_theta_delayed)
    
    # Generate reference signals with phase shifts
    NumRef = 1  # NOTE: Variable suggests multiple references, but only one is used currently
                # The paper discusses benefits of multiple PEM channels
    tdelta = np.array([0, 1/3/f0, 2/3/f0])  # NOTE: Array has 3 values but only the first is used
    R = np.zeros((len(t), NumRef))
    
    for n in range(NumRef):
        # Generate magnitude with small random variations
        Ar_prime = np.random.rand(len(t)) / 100 + A_r
        
        # Time-shifted signal (related to τdelay in Equation 4)
        tt = t + t0 + tdelta[n]
        phase_delayed = 2*np.pi*f0*tt + 2*np.pi*D_fac*np.cos(2*np.pi*gamma_a*tt)
        
        # Delay the noise
        n_theta_delayed = delay_sig(n_theta, dt, t0 + tdelta[n])
        phase_delayed = phase_delayed + n_theta_delayed[:len(t)]
        
        # Generate reference signal with noise
        r = Ar_prime * np.cos(phase_delayed) + np.random.randn(len(t)) * sigma_r  # Changed to cosine
        R[:, n] = r
    
    # Generate injected GW signal (Equation 18)
    # h(t) = h0 sin[2πϕgw(t)]
    p = point_phase(fq, t[:N], T)  
    h = h0 * np.sin(2*np.pi*p)  # Paper uses sine for GW signal, so keeping as is
    
    # Generate primary signal (Equation 1)
    # x(t) = h(t) + c(t) + n(t)
    x = h + c + np.random.randn(len(t)) * sigma_n
    
    return x, R, h, t, r0, c  