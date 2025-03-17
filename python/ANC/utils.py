"""
Signal processing utilities for adaptive filtering.
"""
import numpy as np


def delay_sig(s0, dt, d):
    """
    Delay a signal by a specified amount using frequency domain processing.
    
    Parameters:
    -----------
    s0 : ndarray
        Input signal
    dt : float
        Time step
    d : float
        Delay amount in seconds
        
    Returns:
    --------
    s : ndarray
        Delayed signal
    """
    slen = len(s0)
    W = 1/dt
    
    # Use next power of 2 for efficient FFT
    nfft = int(2**np.ceil(np.log2(2*slen)))
    
    # Create frequency axis
    fax = W * np.arange(-nfft/2, nfft/2) / nfft
    
    # Frequency domain function for delay
    shft = np.exp(-1j * d * 2 * np.pi * fax)
    shft = np.fft.ifftshift(shft)
    
    # Apply delay in frequency domain
    fsd = np.fft.fft(s0, nfft)
    fsd = fsd * shft
    
    # Return to time domain
    dum = np.fft.ifft(fsd)
    
    # Return real part of the delayed signal
    s = np.real(dum[:slen])
    
    return s


def point_phase(f, t, T):
    """
    Calculate phase points for signal generation.
    
    Parameters:
    -----------
    f : ndarray
        Frequency array
    t : ndarray
        Time array
    T : float
        Time period
        
    Returns:
    --------
    p : ndarray
        Phase array
    """
    df = np.diff(f) / T
    df = np.append(df, 0)
    
    p = np.array([])
    pn = 0
    
    for n in range(len(f)):
        p = np.append(p, pn + f[n] * t + df[n] * t**2 / 2)
        pn = pn + f[n] * T + df[n] * T**2 / 2 #quadratic phase term
    
    return p 