"""
Evaluation utilities for adaptive filtering.
"""
import numpy as np
from adaptive_filters import arls_n
from python.ANC.hmm_viterbi import viterbi_for_ANC


def anc_filter(h, f0, ampr0, ampr, H, Q, gamma_a):
    """
    Apply adaptive noise cancellation and evaluate performance.
    
    Parameters:
    -----------
    h : float
        Amplitude of injected signal
    f0 : float
        Power line frequency
    ampr0 : float
        Amplitude of reference signal
    ampr : float
        Amplitude factor for reference
    H : float
        Noise level of primary signal
    Q : float
        Noise level of reference signal
    gamma_a : float
        Phase fluctuation parameter
        
    Returns:
    --------
    score : float
        Score without filtering
    score_RLS : float
        Score with RLS filtering
    """
    from python.ANC.generate_synthetic_data import simulate_data
    
    W = 1000  # Sampling frequency
    N = 2**14
    T = N/W
    Nb = 50
    gamma = 1e-2  # Standard deviation of GW frequency
    
    # Generate random frequencies
    fq = np.cumsum(np.concatenate(([59.5], gamma * np.sqrt(T) * np.random.randn(Nb-1))))
    
    # Generate simulated data
    s, r, _, _, _ = simulate_data(f0, fq, h, H, W, N, Q, ampr0, ampr, gamma_a)
    
    # Apply RLS filter
    lambda_val = 1
    c_RLS, _, _,_= arls_n(s, r, 36, lambda_val) # cancelled, adap, fit, P 
    
    
    # Evaluate using Viterbi
    score, _,_ = viterbi_for_ANC(gamma, s, N, Nb, T, W) #score, fhat, y0 
    score_RLS, _,_= viterbi_for_ANC(gamma, c_RLS, N, Nb, T, W)
    
    return score, score_RLS


def generate_roc_curve(h, f0, ampr0, ampr, H, Q, gamma_a, num_trials=300):
    """
    Generate ROC curve data for adaptive filtering.
    
    Parameters:
    -----------
    h : float
        Amplitude of injected signal
    f0 : float
        Power line frequency
    ampr0 : float
        Amplitude of reference signal
    ampr : float
        Amplitude factor for reference
    H : float
        Noise level of primary signal
    Q : float
        Noise level of reference signal
    gamma_a : float
        Phase fluctuation parameter
    num_trials : int, optional
        Number of trials, default is 300
        
    Returns:
    --------
    roc : ndarray
        ROC curve data [pd_nofilter, pf_nofilter, pd_RLS, pf_RLS]
    """
    score_mat = []
    score_RLS_mat = []
    k_all = np.zeros(num_trials)
    
    for ind in range(num_trials):
        if np.random.rand() > 0.5:
            score, score_RLS = anc_filter(h, f0, ampr0, ampr, H, Q, gamma_a)
            k_all[ind] = 1
        else:
            score, score_RLS = anc_filter(0, f0, ampr0, ampr, H, Q, gamma_a)
            k_all[ind] = 0
            
        score_mat.append(score)
        score_RLS_mat.append(score_RLS)
    
    score_mat = np.array(score_mat)
    score_RLS_mat = np.array(score_RLS_mat)
    
    # Calculate ROC curve points
    th_nofilter = np.linspace(np.min(score_mat), np.max(score_mat), 1001)
    th_RLS = np.linspace(np.min(score_RLS_mat), np.max(score_RLS_mat), 1001)
    
    pd_nofilter = np.zeros(1001)
    pf_nofilter = np.zeros(1001)
    pd_RLS = np.zeros(1001)
    pf_RLS = np.zeros(1001)
    
    for i in range(1001):
        pd_nofilter[i] = np.sum(score_mat[k_all == 1] >= th_nofilter[i])
        pf_nofilter[i] = np.sum(score_mat[k_all == 0] >= th_nofilter[i])
        pd_RLS[i] = np.sum(score_RLS_mat[k_all == 1] >= th_RLS[i])
        pf_RLS[i] = np.sum(score_RLS_mat[k_all == 0] >= th_RLS[i])
    
    pd_nofilter = pd_nofilter / np.sum(k_all == 1)
    pf_nofilter = pf_nofilter / np.sum(k_all == 0)
    pd_RLS = pd_RLS / np.sum(k_all == 1)
    pf_RLS = pf_RLS / np.sum(k_all == 0)
    
    roc = np.vstack([pd_nofilter, pf_nofilter, pd_RLS, pf_RLS]).T
    
    return roc 