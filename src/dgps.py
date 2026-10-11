"""Generate data for the simulation study."""

import numpy as np
from scipy.stats import norm


def generate_data(m, pi0, rng, effect=2.0):
    """Return one-sided p-values and true null labels."""
    if not isinstance(m, (int, np.integer)) or m <= 0:
        raise ValueError("m must be a positive integer.")
    if not 0 <= pi0 <= 1:
        raise ValueError("pi0 must be between 0 and 1.")

    null_count = m * pi0
    m0 = int(round(null_count))

    if not np.isclose(null_count, m0, rtol=0, atol=1e-8):
        raise ValueError("m * pi0 must be an integer.")

    # True means the test comes from the null distribution.
    is_null = np.arange(m) < m0
    means = np.where(is_null, 0.0, effect)

    z = rng.normal(loc=means, scale=1.0)

    # Survival function calculates 1 - Phi(z) accurately.
    p_values = norm.sf(z)

    return p_values, is_null


def theoretical_power(gamma, effect=2.0):
    """Calculate power for a fixed rejection threshold."""
    if not 0 < gamma < 1:
        raise ValueError("gamma must be between 0 and 1.")

    return float(norm.sf(norm.isf(gamma) - effect))