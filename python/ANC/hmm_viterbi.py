"""
Detection algorithms for adaptive filtering - corrected Viterbi implementation.
"""
import numpy as np


def viterbi_colFLT(M, obslik):
    """
    Find the most-probable (Viterbi) path through the HMM state trellis.
    
    Parameters:
    -----------
    M : int
        Window size for column filtering
    obslik : ndarray
        Observation likelihood matrix (assumed to be log-likelihoods)
        
    Returns:
    --------
    path : ndarray
        Most likely state sequence
    delta : ndarray
        Log probability of the best sequence
    score : float
        Score of the best path
    psi : ndarray
        Best predecessor state at each time and state
    """
    # Ensure M is odd
    if M % 2 == 0:
        M += 1
    
 
    Q, T = obslik.shape
    
    delta = np.zeros((Q, T))
    psi = np.zeros((Q, T), dtype=int)
    
    # Initialize first time step with observation log-likelihoods
    t = 0
    #delta[:, t] = obslik[:, t]

    # Initialize with uniform prior
    delta[:, 0] = np.log(1.0 / Q) + obslik[:, 0]

    
    # Forward pass
    for t in range(1, T):
        for i in range(Q):
            # Define window boundaries
            start = max(0, i - (M-1)//2)
            end = min(Q, i + (M-1)//2 + 1)
            window_size = end - start
         
            
            # Transition log-probability (uniform within window)
            trans_logprob = np.log(1.0 / window_size)
            
            # Calculate log-probabilities for all possible previous states in window
            log_probs = np.zeros(window_size)
            for j in range(window_size):
                prev_state = start + j
                log_probs[j] = delta[prev_state, t-1] + trans_logprob
            
            # Find maximum log-probability
            j_max = np.argmax(log_probs)
            
            # Update delta and psi (working in log space)
            delta[i, t] = log_probs[j_max] + obslik[i, t]
            psi[i, t] = start + j_max
    
    # Find best ending state
    score = np.max(delta[:, T-1])
    ind = np.argmax(delta[:, T-1])
    
    # Backtrack
    path = np.zeros(T, dtype=int)
    path[T-1] = ind
    
    for t in range(T-2, -1, -1):
        path[t] = psi[path[t+1], t+1]
    
    return path, delta, score, psi


def viterbi_for_ANC(gamma, Y1, N, Nblocks, T, W):
    """
    Compute Viterbi path of frequencies given the data.
    
    Parameters:
    -----------
    gamma : float
        Standard deviation of frequency
    Y1 : ndarray
        Input signal
    N : int
        Number of samples per block
    Nblocks : int
        Number of blocks
    T : float
        Time period
    W : float
        Sampling frequency
        
    Returns:
    --------
    score : float
        Score of the best path
    fhat : ndarray
        Estimated frequency path
    y0 : ndarray
        Filtered spectrogram around 60 Hz
    """
    # Create frequency axis
    w = np.linspace(-W/2, W/2, 2*N)
    dw = w[1] - w[0]  # Frequency bin width
    
    # Compute FFT for each block
    y = np.abs(np.fft.fftshift(
        np.fft.fft(Y1.reshape(N, Nblocks), 2*N, axis=0), 
        axes=0))
    
    # Find frequency bins around 60 Hz
    n = np.where(np.abs(w - 60) < 10)[0]
    w0 = w[n]
    y0 = y[n, :]
    
    # Convert spectrogram to log-likelihoods
    # Higher amplitude means higher likelihood
    obslik = np.log(y0 + 1e-10)  # Add small constant to avoid log(0)
    
    # Calculate window size for Viterbi
    M = max(1, int(np.ceil(2 * np.sqrt(T) * gamma / dw)))
    
    # Compute Viterbi path
    path, delta, score, psi = viterbi_colFLT(2*M+1, obslik)
    
    # Calculate score (difference between max and average log-likelihood)
    score = np.max(delta[:, -1]) - np.mean(delta[:, -1])
    
    # Map path to frequencies
    fhat = w0[path]
    
    return score, fhat, y0