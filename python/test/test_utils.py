"""
Unit tests for signal processing utilities.
"""
import pytest
import numpy as np
import sys
import os
from ANC.utils import delay_sig, point_phase




def test_delay_sig_shape():
    """Test that the delayed signal has the same shape as the input."""
    # Create a test signal
    dt = 0.001  # 1 kHz sampling rate
    t = np.arange(0, 1, dt)  # 1 second of data
    s0 = np.sin(2 * np.pi * 10 * t)  # 10 Hz sine wave
    
    # Apply delay
    d = 0.1  # 100 ms delay
    s = delay_sig(s0, dt, d)
    
    # Check shape
    assert len(s) == len(s0), "Delayed signal should have the same length as input"


def test_delay_sig_actual_delay():
    """Test that the signal is actually delayed by the specified amount."""
    # Create a test signal - use a pulse for easy delay detection
    dt = 0.001  # 1 kHz sampling rate
    t = np.arange(0, 1, dt)  # 1 second of data
    s0 = np.zeros_like(t)
    pulse_idx = 100  # Pulse at 100ms
    s0[pulse_idx] = 1.0
    
    # Apply delay
    d = 0.05  # 50 ms delay
    s = delay_sig(s0, dt, d)
    
    # Expected delay in samples
    delay_samples = int(d / dt)
    
    # Find the peak in the delayed signal
    delayed_peak_idx = np.argmax(s)
    
    # Allow for small numerical errors (±2 samples)
    assert abs(delayed_peak_idx - (pulse_idx + delay_samples)) <= 2, \
        f"Peak should be delayed by approximately {delay_samples} samples"


def test_delay_sig_zero_delay():
    """Test that zero delay returns approximately the original signal."""
    # Create a test signal
    dt = 0.001
    t = np.arange(0, 1, dt)
    s0 = np.sin(2 * np.pi * 10 * t)
    
    # Apply zero delay
    d = 0.0
    s = delay_sig(s0, dt, d)
    
    # Check that the signals are approximately equal
    assert np.allclose(s, s0, atol=1e-10), "Zero delay should return the original signal"


def test_delay_sig_negative_delay():
    """Test that negative delay works correctly (advance the signal)."""
    # Create a test signal - use a pulse for easy delay detection
    dt = 0.001
    t = np.arange(0, 1, dt)
    s0 = np.zeros_like(t)
    pulse_idx = 500  # Pulse in the middle
    s0[pulse_idx] = 1.0
    
    # Apply negative delay (advance)
    d = -0.05  # -50 ms delay (advance)
    s = delay_sig(s0, dt, d)
    
    # Expected advance in samples
    advance_samples = int(abs(d) / dt)
    
    # Find the peak in the advanced signal
    advanced_peak_idx = np.argmax(s)
    
    # Allow for small numerical errors (±2 samples)
    assert abs(advanced_peak_idx - (pulse_idx - advance_samples)) <= 2, \
        f"Peak should be advanced by approximately {advance_samples} samples"


def test_point_phase_shape():
    """Test that the point_phase function returns the correct shape."""
    # Test parameters
    f = np.array([10.0, 20.0, 30.0])  # Three frequency segments
    T = 1.0  # 1 second per segment
    t = np.linspace(0, 0.5, 100)  # Time points within a segment
    
    # Calculate phase
    p = point_phase(f, t, T)
    
    # Check shape
    assert len(p) == len(f) * len(t), "Phase array should have length = len(f) * len(t)"


def test_point_phase_constant_frequency():
    """Test point_phase with constant frequency."""
    # Test with constant frequency
    f = np.array([10.0])  # Single frequency
    T = 1.0
    t = np.linspace(0, 0.5, 100)
    
    # Calculate phase
    p = point_phase(f, t, T)
    
    # For constant frequency, phase should be linear with slope 2π*f
    expected_phase = 2 * np.pi * f[0] * t  # Convert to radians for comparison
    
    # Since point_phase doesn't multiply by 2π, we divide expected_phase by 2π
    expected_phase = expected_phase / (2 * np.pi)
    
    assert np.allclose(p, f[0] * t), "Phase should increase linearly with constant frequency"


def test_point_phase_multiple_segments():
    """Test point_phase with multiple frequency segments."""
    # Test parameters
    f = np.array([10.0, 20.0])  # Two frequency segments
    T = 1.0  # 1 second per segment
    t = np.linspace(0, 0.5, 10)  # Time points within a segment
    
    # Calculate phase
    p = point_phase(f, t, T)
    
    # Calculate df (rate of change of frequency)
    df = np.diff(f) / T
    df = np.append(df, 0)

    # First segment should match f[0]*t
    first_segment = p[:len(t)]
    expected_first = f[0] * t + df[0] * t**2 / 2
    assert np.allclose(first_segment, expected_first), "First segment phase calculation is incorrect"
    
    # Second segment should start where first segment left off
    second_segment = p[len(t):]
    first_segment_end = f[0] * T + df[0] * T**2 / 2
    expected_second = first_segment_end + f[1] * t + df[1] * t**2 / 2
    assert np.isclose(second_segment[0], expected_second[0]), "Second segment should start at the correct phase"


def test_point_phase_frequency_transition():
    """Test that point_phase handles frequency transitions correctly."""
    # Test with changing frequency
    f = np.array([10.0, 20.0])
    T = 1.0
    t = np.linspace(0, T, 100)
    
    # Calculate phase
    p = point_phase(f, t, T)
    
    # Check that phase is continuous at the transition
    first_segment_end = p[len(t)-1]
    second_segment_start = p[len(t)]
    
    # The difference should be approximately f[1]*t[0]
    expected_diff = f[1] * t[0]
    actual_diff = second_segment_start - first_segment_end
    
    assert np.isclose(actual_diff, expected_diff), \
        "Phase should be continuous at frequency transitions" 