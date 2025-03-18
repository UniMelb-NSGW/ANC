import pytest
import numpy as np
from ANC.hmm_viterbi import viterbi_colFLT, viterbi_for_ANC


class TestViterbiColFLT:
    def test_basic_functionality(self):
        """Test basic functionality of viterbi_colFLT with a simple example."""
        # Create a simple observation likelihood matrix
        # 3 states, 4 time steps
        obslik = np.array([
            [0.1, 0.4, 0.1, 0.1],  # State 0
            [0.2, 0.3, 0.5, 0.2],  # State 1
            [0.7, 0.3, 0.4, 0.7]   # State 2
        ])
        
        # Window size of 3 (consider all states in this small example)
        M = 5
        
        # Run the algorithm
        path, delta, score, psi = viterbi_colFLT(M, np.log(obslik))
        
        # Expected path for this simple example
        # At each time step, the algorithm should choose the state with highest probability
        expected_path = np.array([2, 0, 1, 2])
        
        # Check results
        assert isinstance(path, np.ndarray), "Path should be a numpy array"
        assert path.shape == (4,), "Path should have length 4"
        assert np.array_equal(path, expected_path), f"Expected path {expected_path}, got {path}"
        assert delta.shape == (3, 4), "Delta should have shape (3, 4)"
        assert isinstance(score, float), "Score should be a float"
    
    def test_window_size(self):
        """Test that the window size is properly enforced."""
        # Create a larger observation likelihood matrix
        # 5 states, 3 time steps
        obslik = np.array([
            [0.1, 0.2, 0.3],  # State 0
            [0.2, 0.3, 0.1],  # State 1
            [0.3, 0.1, 0.2],  # State 2
            [0.2, 0.3, 0.3],  # State 3
            [0.2, 0.1, 0.1]   # State 4
        ])
        
        # Window size of 3 (should only consider adjacent states)
        M = 3
        
        # Run the algorithm
        path, delta, score, psi = viterbi_colFLT(M, obslik)
        
        # Check that psi values are within the window constraints
        for t in range(1, obslik.shape[1]):
            for i in range(obslik.shape[0]):
                start = max(0, i - (M-1)//2)
                end = min(obslik.shape[0], i + (M-1)//2 + 1)
                assert start <= psi[i, t] < end, f"State transition at t={t}, i={i} violates window constraint"
    
    def test_even_window_size(self):
        """Test that even window sizes are properly handled (should be incremented to odd)."""
        obslik = np.random.rand(4, 5)  # 4 states, 5 time steps
        
        # Even window size (should be incremented to 5)
        M = 4
        
        # Run the algorithm
        path, delta, score, psi = viterbi_colFLT(M, obslik)
        
        # The effective window size should be M+1 (5)
        effective_M = M + 1
        
        # Check that the window constraint is respected
        for t in range(1, obslik.shape[1]):
            for i in range(obslik.shape[0]):
                start = max(0, i - (effective_M-1)//2)
                end = min(obslik.shape[0], i + (effective_M-1)//2 + 1)
                assert start <= psi[i, t] < end, f"State transition at t={t}, i={i} violates window constraint"


class TestViterbiForANC:
    def test_basic_functionality(self):
        """Test basic functionality of viterbi_for_ANC with synthetic data."""
        # Parameters
        gamma = 0.5  # Standard deviation of frequency
        N = 128      # Number of samples per block
        Nblocks = 10  # Number of blocks
        T = 1.0      # Time period
        W = 1000.0   # Sampling frequency
        
        # Create synthetic signal with 60Hz component
        t = np.arange(0, N*Nblocks) / W
        Y1 = np.sin(2*np.pi*60*t) + 0.1*np.random.randn(len(t))
        
        # Run the algorithm
        score, fhat, y0 = viterbi_for_ANC(gamma, Y1, N, Nblocks, T, W)
        # Check results
        assert isinstance(score, float), "Score should be a float"
        assert isinstance(fhat, np.ndarray), "fhat should be a numpy array"
        assert fhat.shape == (Nblocks,), "fhat should have length equal to Nblocks"
        assert isinstance(y0, np.ndarray), "y0 should be a numpy array"
        
        # Check that estimated frequencies are close to 60Hz
        assert np.all(np.abs(fhat - 60) < 10), "Estimated frequencies should be close to 60Hz"
    
    def test_no_signal(self):
        """Test behavior with random noise (no clear signal)."""
        # Parameters
        gamma = 0.5
        N = 128
        Nblocks = 10
        T = 1.0
        W = 1000.0
        
        # Create random noise signal
        Y1 = np.random.randn(N*Nblocks)
        
        # Run the algorithm
        score, fhat, y0 = viterbi_for_ANC(gamma, Y1, N, Nblocks, T, W)
        
        # Check results
        assert isinstance(score, float), "Score should be a float"
        assert isinstance(fhat, np.ndarray), "fhat should be a numpy array"
        assert fhat.shape == (Nblocks,), "fhat should have length equal to Nblocks"
        
        # Score should be lower for random noise compared to a clear signal
        # This is a relative test, so we just check that the score is not too high
        assert score < 100, "Score should be relatively low for random noise"


if __name__ == "__main__":
    pytest.main() 