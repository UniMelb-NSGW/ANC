"""
Adaptive Recursive Least Squares (ARLS) implementation for noise cancellation.
Based on the algorithm described in "Adaptive cancellation of mains power interference
in continuous gravitational wave searches with a hidden Markov model" (Kimpson et al., 2024)
"""
import numpy as np
from tqdm import tqdm


def arls_n(primary, reference, order, lambd,Delta):
    """
    Adaptive RLS algorithm for noise cancellation as described in Section III of the paper.
    
    Parameters:
    -----------
    primary : ndarray
        Primary signal x(t) (signal + line noise) - Eq. (1)
    reference : ndarray
        Reference signal r(t) (line noise only) - Eq. (2)
    order : int
        Filter order M - controls complexity of the model (Sec. III.B)
    lambd : float
        Forgetting factor λ (0 < lambd <= 1) - gives exponentially less weight to older samples
    Delta : float
        Regularization parameter δ - used in initialization of covariance matrix P
        
    Returns:
    --------
    cancelled : ndarray
        Signal with line noise cancelled e(t) = x(t) - ĉ(t) - Eq. (9)
    adap : ndarray
        Adaptive filter coefficients w - Eq. (12)
    fit : ndarray
        Estimated line noise ĉ(t) - Eq. (10)
    P : ndarray
        Covariance matrix P = <ww^T> - used in ARLS algorithm
    """

    print("Applying ARLS filter")
    print("Filter order: ", order)

    # Ensure reference is always a 2D array
    if len(reference.shape) == 1:
        reference = reference.reshape(-1, 1)
    
    N = reference.shape[1]
    print("Number of reference channels: ", N)
    n = min(len(primary), len(reference))
    
    # Initialize tap-input vector (Eq. 11) as buffer for reference samples
    delayed = np.zeros((order, N))
    
    # Initialize tap weights w = 0 (Step 1 in Sec. III.B)
    adap = np.zeros((order, N))
    
    # Arrays to store estimated noise and cancelled signal
    fit = np.zeros(n)
    cancelled = np.zeros(n)
    
    # Initialize covariance matrix P = δ^-1*I (Step 1 in Sec. III.B)
    # δ is the regularization parameter. 
    I = np.eye(order * N)
    P = I * Delta
    
    # Main ARLS loop (Step 2 in Sec. III.B)
    for k in tqdm(range(n), desc="Processing samples"):
        # Update tap-input vector u_k with new reference sample
        delayed[0, :] = reference[k, :]
            
        # Estimate clutter ĉ_k (Eq. 10 and Step 2a in Sec. III.B)
        fit[k] = np.trace(np.dot(delayed.T, adap))

        # Calculate residual e_k (Eq. 9 and Step 2b in Sec. III.B)
        cancelled[k] = primary[k] - fit[k]
        
        # Flatten delayed for matrix operations
        delayed_flat = delayed.flatten()
        
        # Calculate gain vector g_k (Eq. 14 and Step 2c in Sec. III.B)
        K = np.dot(P, delayed_flat) / (lambd + np.dot(np.dot(delayed_flat.T, P), delayed_flat))
        
        # Update covariance matrix P_k (Eq. 16 and Step 2e in Sec. III.B)
        P = np.dot((I - np.outer(K, delayed_flat.T)), P) / lambd
        
        # Update tap weights w_k (Eq. 15 and Step 2d in Sec. III.B)
        adap = adap + cancelled[k] * np.reshape(K, (order, N))
        
        # Shift the delayed samples for next iteration
        delayed[1:order, :] = delayed[0:order-1, :]
    
    return cancelled, adap, fit, P