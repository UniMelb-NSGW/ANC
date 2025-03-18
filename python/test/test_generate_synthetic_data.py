"""
Unit tests for signal generation utilities.
"""
import pytest
import numpy as np
from ANC.generate_synthetic_data import simulate_data


def test_simulate_data_shapes():
    """Test that the shapes of returned arrays are correct."""
    # Test parameters
    f0 = 60.0  # Center frequency in Hz
    fq = np.array([60.0, 120.0, 180.0])  # Array of frequencies
    h = 0.5  # Injected signal amplitude
    H = 0.1  # Noise level of primary signal
    W = 1000.0  # Sampling frequency
    N = 1000  # Number of samples per block
    Q = 0.05  # Noise level of reference signal
    ampr0 = 1.0    # Amplitude of reference signal
    ampr = 0.8     # Amplitude factor for reference
    gamma_a = 0.1  # Phase fluctuation parameter
    
    # Call the function
    s, R, q, t = simulate_data(f0, fq, h, H, W, N, Q, ampr0, ampr, gamma_a)
    
    # Check shapes
    NT = len(fq)
    expected_length = N * NT
    
    assert len(s) == expected_length, f"Primary signal length should be {expected_length}"
    assert R.shape == (expected_length, 1), f"Reference signals shape should be ({expected_length}, 1)"
    assert len(q) == expected_length, f"Injected signal length should be {expected_length}"
    assert len(t) == expected_length, f"Time vector length should be {expected_length}"


def test_simulate_data_types():
    """Test that the returned arrays have the correct types."""
    # Test parameters
    f0 = 60.0
    fq = np.array([60.0])
    h = 0.5
    H = 0.1
    W = 1000.0
    N = 1000
    Q = 0.05
    ampr0 = 1.0
    ampr = 0.8
    gamma_a = 0.1
    
    # Call the function
    s, R, q, t  = simulate_data(f0, fq, h, H, W, N, Q, ampr0, ampr, gamma_a)
    
    # Check types
    assert isinstance(s, np.ndarray), "Primary signal should be a numpy array"
    assert isinstance(R, np.ndarray), "Reference signals should be a numpy array"
    assert isinstance(q, np.ndarray), "Injected signal should be a numpy array"
    assert isinstance(t, np.ndarray), "Time vector should be a numpy array"
    
    # Check data types
    assert s.dtype == np.float64, "Primary signal should be float64"
    assert R.dtype == np.float64, "Reference signals should be float64"
    assert q.dtype == np.float64, "Injected signal should be float64"
    assert t.dtype == np.float64, "Time vector should be float64"


def test_simulate_data_time_vector():
    """Test that the time vector is correctly generated."""
    # Test parameters
    f0 = 60.0
    fq = np.array([60.0])
    h = 0.5
    H = 0.1
    W = 1000.0  # 1000 Hz sampling rate
    N = 1000    # 1000 samples per block
    Q = 0.05
    ampr0 = 1.0
    ampr = 0.8
    gamma_a = 0.1
    
    # Call the function
    _, _, _, t  = simulate_data(f0, fq, h, H, W, N, Q, ampr0, ampr, gamma_a)
    
    # Check time vector properties
    dt = 1/W
    assert np.isclose(t[1] - t[0], dt), f"Time step should be {dt}"
    assert np.isclose(t[-1] - t[0], (len(t) - 1) * dt), "Time span should match expected duration"


def test_simulate_data_reproducibility():
    """Test that the function produces reproducible results with the same random seed."""
    # Test parameters
    f0 = 60.0
    fq = np.array([60.0])
    h = 0.5
    H = 0.1
    W = 1000.0
    N = 1000
    Q = 0.05
    ampr0 = 1.0
    ampr = 0.8
    gamma_a = 0.1
    
    # Set random seed
    np.random.seed(42)
    s1, R1, q1, t1 = simulate_data(f0, fq, h, H, W, N, Q, ampr0, ampr, gamma_a)
    
    # Reset seed and call again
    np.random.seed(42)
    s2, R2, q2, t2 = simulate_data(f0, fq, h, H, W, N, Q, ampr0, ampr, gamma_a)
    
    # Results should be identical
    assert np.allclose(s1, s2), "Results should be reproducible with the same random seed"
    assert np.allclose(R1, R2), "Results should be reproducible with the same random seed"