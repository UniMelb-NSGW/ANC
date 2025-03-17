# ANC: Adaptive Noise Cancellation for LIGO Instrumental Lines

[![arXiv](https://img.shields.io/badge/arXiv-2402.xxxxx-b31b1b.svg)](https://arxiv.org/abs/2402.xxxxx)
[![PRD](https://img.shields.io/badge/PRD-110.122004-blue.svg)](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.110.122004)

This repository contains the implementation of an Adaptive Recursive Least Squares (ARLS) algorithm for noise cancellation in LIGO instrumental lines, as described in the paper "Adaptive cancellation of mains power interference in continuous gravitational wave searches with a hidden Markov model" (Kimpson et al., 2024).

## Overview

The ANC package implements an adaptive filtering algorithm designed to cancel out instrumental line noise in gravitational wave data. The algorithm uses reference signals to estimate and remove power line interference while preserving the underlying gravitational wave signal.

## Installation

You can install the package using either of the following methods:

### Method 1: Using conda environment file (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ANC.git
cd ANC
```

2. Create and activate the conda environment using the provided environment file:
```bash
conda env create -f conda_environment.yml
conda activate anc
```

3. Install the package:
```bash
pip install -e .
```

### Method 2: Manual conda environment setup

If you prefer to create the environment manually:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ANC.git
cd ANC
```

2. Create and activate a conda environment:
```bash
conda create -n anc python=3.8
conda activate anc
```

3. Install the package:
```bash
pip install -e .
```

## Project Structure

```
ANC/
├── python/
│   └── ANC/
│       ├── adaptive_filters.py    # Core ARLS implementation
│       ├── generate_synthetic_data.py  # Data generation utilities
│       ├── hmm_viterbi.py        # Hidden Markov Model implementation
│       ├── evaluation.py         # Performance evaluation metrics
│       └── utils.py              # Helper functions
├── notebooks/
│   └── examples/                 # Example notebooks
└── tests/                        # Unit tests
```

## Usage

### Basic Example

```python
from ANC.adaptive_filters import arls_n
from ANC.generate_synthetic_data import simulate_data
import numpy as np

# Generate synthetic data
x, R, h, t = simulate_data(
    f_ac=60.0,      # Power line frequency
    fq=np.array([60.0]),  # GW signal frequency
    h0=1e-24,       # GW signal amplitude
    sigma_n=1e-23,  # Noise level
    W=4096,         # Sampling frequency
    N=4096,         # Samples per block
    sigma_r=1e-6,   # Reference noise
    A_c=1e-22,      # Clutter amplitude
    A_r=1.0,        # Reference amplitude
    gamma_a=0.1     # Phase fluctuation parameter
)

# Apply adaptive filter
cancelled, adap, fit, P = arls_n(
    primary=x,
    reference=R,
    order=10,       # Filter order
    lambd=0.99,     # Forgetting factor
    Delta=100.0     # Regularization parameter
)
```

### Jupyter Notebooks

Example notebooks demonstrating the usage of the package can be found in the `notebooks/examples/` directory. These notebooks cover:

- Basic usage of the adaptive filter
- Synthetic data generation
- Performance evaluation
- Real-world data analysis

## Documentation

Detailed documentation for each module can be found in the docstrings of the respective Python files. The main components are:

- `adaptive_filters.py`: Implements the core ARLS algorithm
- `generate_synthetic_data.py`: Utilities for generating test data
- `hmm_viterbi.py`: Hidden Markov Model implementation for state estimation
- `evaluation.py`: Metrics for evaluating filter performance
- `utils.py`: Helper functions and utilities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Citation

If you use this software in your research, please cite:

```bibtex
@article{kimpson2024adaptive,
  title={Adaptive cancellation of mains power interference in continuous gravitational wave searches with a hidden Markov model},
  author={Kimpson, Thomas and others},
  journal={Physical Review D},
  volume={110},
  number={12},
  pages={122004},
  year={2024},
  publisher={APS}
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
