"""Statistical methods used in the simulation."""

import numpy as np


def validate_p_values(p_values):
    """Check that p-values form a nonempty, valid array."""
    p_values = np.asarray(p_values, dtype=float)

    if p_values.ndim != 1 or p_values.size == 0:
        raise ValueError("p_values must be a nonempty 1D array.")
    if not np.all(np.isfinite(p_values)):
        raise ValueError("p_values must be finite.")
    if np.any((p_values < 0) | (p_values > 1)):
        raise ValueError("p_values must be between 0 and 1.")

    return p_values


def storey_fixed(p_values, gamma, tuning=0.5):
    """Reject at gamma and estimate pi0 and FDR."""
    p_values = validate_p_values(p_values)

    if not 0 < gamma < 1:
        raise ValueError("gamma must be between 0 and 1.")
    if not 0 < tuning < 1:
        raise ValueError("tuning must be between 0 and 1.")

    m = p_values.size
    rejected = p_values <= gamma
    r = int(rejected.sum())

    pi0_hat = np.count_nonzero(p_values > tuning) / (
        m * (1 - tuning)
    )
    fdr_hat = pi0_hat * m * gamma / max(r, 1)

    return rejected, float(pi0_hat), float(fdr_hat)


def benjamini_hochberg(p_values, alpha):
    """Return BH rejection decisions and the largest rejected p-value."""
    p_values = validate_p_values(p_values)

    if not np.isfinite(alpha) or not 0 <= alpha <= 1:
        raise ValueError("alpha must be between 0 and 1.")

    m = p_values.size
    order = np.argsort(p_values)
    sorted_p = p_values[order]
    ranks = np.arange(1, m + 1)

    eligible = sorted_p <= alpha * ranks / m
    rejected = np.zeros(m, dtype=bool)

    if not np.any(eligible):
        return rejected, 0.0

    k = int(np.flatnonzero(eligible)[-1]) + 1
    rejected[order[:k]] = True
    threshold = float(sorted_p[k - 1])

    return rejected, threshold