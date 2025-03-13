"""
Main script for running adaptive filtering experiments.
"""
import numpy as np
import matplotlib.pyplot as plt
from adaptive_filters import arls_n
from python.ANC.generate_synthetic_data import simulate_data
from python.ANC.hmm_viterbi import viterbi_for_ANC
from evaluation import generate_roc_curve,anc_filter


def run_experiment(h=0.03, f0=60, ampr0=1, ampr=10, H=1, Q=2, gamma_a=1e-1):
    """
    Run an experiment with the specified parameters.
    
    Parameters:
    -----------
    h : float, optional
        Amplitude of injected signal, default is 0.03
    f0 : float, optional
        Power line frequency, default is 60
    ampr0 : float, optional
        Amplitude of reference signal, default is 1
    ampr : float, optional
        Amplitude factor for reference, default is 10
    H : float, optional
        Noise level of primary signal, default is 1
    Q : float, optional
        Noise level of reference signal, default is 2
    gamma_a : float, optional
        Phase fluctuation parameter, default is 1e-1
        
    Returns:
    --------
    roc : ndarray
        ROC curve data
    """

    score, score_RLS = anc_filter(h, f0, ampr0, ampr, H, Q, gamma_a)
    #roc = generate_roc_curve(h, f0, ampr0, ampr, H, Q, gamma_a)
    return score, score_RLS


def plot_roc_curve(roc):
    """
    Plot ROC curve.
    
    Parameters:
    -----------
    roc : ndarray
        ROC curve data [pd_nofilter, pf_nofilter, pd_RLS, pf_RLS]
    """
    plt.figure(figsize=(10, 6))
    plt.semilogx(roc[:, 1], roc[:, 0], 'b-', linewidth=2, label='Without filtering')
    plt.semilogx(roc[:, 3], roc[:, 2], 'r-', linewidth=2, label='RLS')
    plt.grid(True)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve for Adaptive Noise Cancellation')
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Run experiment with default parameters
    roc = run_experiment()
    
    # Plot ROC curve
    #plot_roc_curve(roc)
