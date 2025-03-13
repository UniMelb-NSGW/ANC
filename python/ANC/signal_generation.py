"""
Signal generation utilities for testing adaptive filters.
"""
import numpy as np
from ANC.signal_processing import delay_sig, point_phase


def simulate_data(f0, fq, h, H, W, N, Q, ampr0, ampr, gamma_a, D_a=1, sigma_a=0.01):
    """
    Generate simulated data for testing adaptive filters.
    
    Parameters:
    -----------
    f0 : float
        Center frequency of reference
    fq : ndarray
        Array of frequencies
    h : float
        Injected signal amplitude
    H : float
        Noise level of primary signal
    W : float
        Sampling frequency
    N : int
        Number of samples per block
    Q : float
        Noise level of reference signal
    ampr0 : float
        Amplitude of reference signal
    ampr : float
        Amplitude factor for reference
    gamma_a : float
        Phase fluctuation parameter
    D_a : float, optional
        Amplitude of phase modulation, default is 1
    sigma_a : float, optional
        Standard deviation of phase noise, default is 0.01
        
    Returns:
    --------
    s : ndarray
        Primary signal (signal + line noise)
    R : ndarray
        Reference signals
    q : ndarray
        Injected signal
    t : ndarray
        Time vector
    r0 : ndarray
        Original reference signal
    """
    NT = len(fq)
    dt = 1/W
    t0 = np.random.rand() * dt * 10  # Random time delay
    
    t = np.arange(0, N*NT) / W
    taug = np.arange(0, N*NT+101) / W
    T = N/W  # Time within one block
    
    # Generate magnitude with small random variations
    mag0 = np.random.rand(len(t)) / 1000 + ampr0
    
    # Generate phase with modulation and noise
    phase = 2*np.pi*f0*t + 2*np.pi*D_a*np.cos(2*np.pi*gamma_a*t)
    noise = np.random.randn(len(taug)) * sigma_a
    
    # Generate original reference signal
    r0 = mag0 * np.sin(phase + noise[:len(t)])
    
    # Generate reference signals with phase shifts
    NumRef = 1
    tdelta = np.array([0, 1/3/f0, 2/3/f0])
    R = np.zeros((len(t), NumRef))
    
    for n in range(NumRef):
        # Generate magnitude with small random variations
        mag = np.random.rand(len(t)) / 100 + ampr
        
        # Time-shifted signal
        tt = t + t0 + tdelta[n]
        phase_delayed = 2*np.pi*f0*tt + 2*np.pi*D_a*np.cos(2*np.pi*gamma_a*tt)
        
        # Delay the noise
        noise_delayed = delay_sig(noise, dt, t0 + tdelta[n])
        phase_delayed = phase_delayed + noise_delayed[:len(t)]
        
        # Generate reference signal with noise
        r = mag * np.sin(phase_delayed) + np.random.randn(len(t)) * Q
        R[:, n] = r
    
    # Generate injected signal
    p = point_phase(fq, t[:N], T)
    q = h * np.sin(2*np.pi*p)
    
    # Generate primary signal
    s = r0 + q + np.random.randn(len(t)) * H
    
    return s, R, q, t, r0


