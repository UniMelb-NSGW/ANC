import pytest
import numpy as np
from ANC.adaptive_filters import arls_n

def test_arls_n_basic_functionality():
    """Test basic functionality of arls_n with simple inputs."""
    # Create simple test signals
    n_samples = 100
    primary = np.sin(np.linspace(0, 10*np.pi, n_samples))  # Clean signal
    noise = 0.5 * np.sin(np.linspace(0, 20*np.pi, n_samples))  # Noise
    primary_noisy = primary + noise  # Primary signal with noise
    reference = noise  # Reference signal (noise only)
    
    # Run arls_n
    order = 4
    lambd = 0.99
    cancelled, adap, fit, P = arls_n(primary_noisy, reference, order, lambd)
    
    # Basic checks
    assert cancelled.shape == (n_samples,)
    assert fit.shape == (n_samples,)
    assert P.shape == (order, order)
    
    # After convergence, the cancelled signal should be closer to the original signal
    # than the noisy signal was (in terms of mean squared error)
    original_mse = np.mean((primary_noisy - primary) ** 2)
    cancelled_mse = np.mean((cancelled - primary) ** 2)
    
    # Only check the second half to allow for convergence
    half_idx = n_samples // 2
    cancelled_mse_half = np.mean((cancelled[half_idx:] - primary[half_idx:]) ** 2)
    
    # The algorithm should improve the signal after convergence
    assert cancelled_mse_half < original_mse

def test_arls_n_multichannel():
    """Test arls_n with multichannel reference signals."""
    n_samples = 100
    n_channels = 2
    
    # Create test signals
    primary = np.sin(np.linspace(0, 10*np.pi, n_samples))
    noise1 = 0.3 * np.sin(np.linspace(0, 20*np.pi, n_samples))
    noise2 = 0.2 * np.cos(np.linspace(0, 15*np.pi, n_samples))
    
    primary_noisy = primary + noise1 + noise2
    reference = np.column_stack((noise1, noise2))
    
    # Run arls_n
    order = 4
    lambd = 0.99
    cancelled, adap, fit, P = arls_n(primary_noisy, reference, order, lambd)
    
    # Check shapes
    assert cancelled.shape == (n_samples,)
    assert adap.shape == (order, n_channels)
    assert fit.shape == (n_samples,)
    assert P.shape == (order * n_channels, order * n_channels)
    
    # Check performance after convergence
    half_idx = n_samples // 2
    original_mse = np.mean((primary_noisy - primary) ** 2)
    cancelled_mse_half = np.mean((cancelled[half_idx:] - primary[half_idx:]) ** 2)
    
    assert cancelled_mse_half < original_mse

def test_arls_n_parameter_validation():
    """Test arls_n with different parameter values."""
    n_samples = 50
    primary = np.random.randn(n_samples)
    reference = np.random.randn(n_samples)
    
    # Test with different orders
    for order in [1, 5, 10]:
        cancelled, adap, fit, P = arls_n(primary, reference, order, 0.99)
        assert adap.shape == (order, 1)
        assert P.shape == (order, order)
    
    # Test with different lambda values
    for lambd in [0.9, 0.95, 0.99, 1.0]:
        cancelled, adap, fit, P = arls_n(primary, reference, 3, lambd)
        assert cancelled.shape == (n_samples,)

def test_arls_n_noise_cancellation():
    """Test arls_n's ability to cancel periodic noise."""
    n_samples = 200
    t = np.linspace(0, 1, n_samples)
    
    # Create a signal with multiple frequency components
    signal = np.sin(2 * np.pi * 5 * t)  # 5 Hz signal
    
    # Create line noise at 50 Hz
    line_noise = 0.5 * np.sin(2 * np.pi * 50 * t)
    
    # Primary signal is signal + noise
    primary = signal + line_noise
    
    # Reference is just the noise (in practice this would be measured)
    reference = line_noise
    
    # Run arls_n
    order = 5
    lambd = 0.99
    cancelled, adap, fit, P = arls_n(primary, reference, order, lambd)
    
    # After convergence, the cancelled signal should be closer to the original
    # signal than the primary signal was
    convergence_idx = 100  # Allow 100 samples for convergence
    
    # Calculate mean squared errors
    original_mse = np.mean((primary[convergence_idx:] - signal[convergence_idx:]) ** 2)
    cancelled_mse = np.mean((cancelled[convergence_idx:] - signal[convergence_idx:]) ** 2)
    
    # The cancelled signal should have lower MSE
    assert cancelled_mse < original_mse
    # The improvement should be significant (at least 50% reduction in MSE)
    assert cancelled_mse < 0.5 * original_mse

def test_arls_n_different_length_signals():
    """Test arls_n with primary and reference signals of different lengths."""
    primary = np.random.randn(100)
    reference = np.random.randn(80)  # Shorter than primary
    
    # Function should use the minimum length
    cancelled, adap, fit, P = arls_n(primary, reference, 3, 0.99)
    assert len(cancelled) == len(reference)
    
    # Test with reference longer than primary
    primary = np.random.randn(80)
    reference = np.random.randn(100)
    
    cancelled, adap, fit, P = arls_n(primary, reference, 3, 0.99)
    assert len(cancelled) == len(primary) 