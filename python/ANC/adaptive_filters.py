"""
Adaptive filtering algorithms for noise cancellation.
Contains Python implementations of ALMS and ARLS algorithms.
"""
import numpy as np


def alms_n(primary, reference, order=2):
    """
    Adaptive LMS algorithm for noise cancellation.
    
    Parameters:
    -----------
    primary : ndarray
        Primary signal (signal + line noise)
    reference : ndarray
        Reference signal (line noise only)
    order : int, optional
        Filter order, default is 2
        
    Returns:
    --------
    cancelled : ndarray
        Signal with line noise cancelled
    adap : ndarray
        Adaptive filter coefficients
    fit : ndarray
        Estimated line noise
    """
    mu = 1e-4
    N = reference.shape[1] if len(reference.shape) > 1 else 1
    n = min(len(primary), len(reference))
    
    delayed = np.zeros((N, order))
    adap = np.zeros((N, order))
    cancelled = np.zeros(n)
    fit = np.zeros(n)
    
    for k in range(n):
        if len(reference.shape) > 1:
            delayed[:, 0] = reference[k, :]
        else:
            delayed[0, 0] = reference[k]
            
        fit[k] = np.trace(np.dot(delayed, adap.T))
        cancelled[k] = primary[k] - fit[k]
        adap = adap + 2 * mu * cancelled[k] * delayed
        
        # Shift the delayed samples
        delayed[:, 1:order] = delayed[:, 0:order-1]
    
    return cancelled, adap, fit


def arls_n(primary, reference, order, lambd):
    """
    Adaptive RLS algorithm for noise cancellation.
    
    Parameters:
    -----------
    primary : ndarray
        Primary signal (signal + line noise)
    reference : ndarray
        Reference signal (line noise only)
    order : int
        Filter order
    lambd : float
        Forgetting factor (0 < lambd <= 1)
        
    Returns:
    --------
    cancelled : ndarray
        Signal with line noise cancelled
    adap : ndarray
        Adaptive filter coefficients
    fit : ndarray
        Estimated line noise
    P : ndarray
        Correlation matrix
    """
    N = reference.shape[1] if len(reference.shape) > 1 else 1
    n = min(len(primary), len(reference))
    
    delayed = np.zeros((order, N))
    adap = np.zeros((order, N))
    fit = np.zeros(n)
    cancelled = np.zeros(n)
    
    # Initialize correlation matrix
    Delta = 1e2
    I = np.eye(order * N)
    P = I * Delta
    
    for k in range(n):
        if len(reference.shape) > 1:
            delayed[0, :] = reference[k, :]
        else:
            delayed[0, 0] = reference[k]
            
        fit[k] = np.trace(np.dot(delayed.T, adap))
        cancelled[k] = primary[k] - fit[k]
        
        # Flatten delayed for matrix operations
        delayed_flat = delayed.flatten()
        
        # Calculate Kalman gain
        K = np.dot(P, delayed_flat) / (lambd + np.dot(np.dot(delayed_flat.T, P), delayed_flat))
        
        # Update correlation matrix
        P = np.dot((I - np.outer(K, delayed_flat.T)), P) / lambd
        
        # Update filter coefficients
        adap = adap + cancelled[k] * np.reshape(K, (order, N))
        
        # Shift the delayed samples
        delayed[1:order, :] = delayed[0:order-1, :]
    
    return cancelled, adap, fit, P 