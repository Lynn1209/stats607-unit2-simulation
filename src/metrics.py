"""Calculate performance measures for each replicate."""

import numpy as np


def calculate_metrics(rejected, is_null):
    """Count rejections and calculate FDP and power."""
    rejected = np.asarray(rejected, dtype=bool)
    is_null = np.asarray(is_null, dtype=bool)

    if rejected.ndim != 1 or rejected.size == 0:
        raise ValueError("rejected must be a nonempty 1D array.")
    if rejected.shape != is_null.shape:
        raise ValueError("Decisions and labels must have the same shape.")

    false_rejections = int(np.sum(rejected & is_null))
    true_rejections = int(np.sum(rejected & ~is_null))
    total_rejections = false_rejections + true_rejections
    alternative_count = int(np.sum(~is_null))

    fdp = false_rejections / max(total_rejections, 1)

    # Power is undefined when there are no alternative tests.
    power = (
        true_rejections / alternative_count
        if alternative_count > 0
        else float("nan")
    )

    return {
        "false_rejections": false_rejections,
        "true_rejections": true_rejections,
        "total_rejections": total_rejections,
        "fdp": fdp,
        "power": power,
    }