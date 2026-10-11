"""Tests for data generation, methods, and simulation results."""

import numpy as np
import pandas as pd
import pytest
from scipy.stats import norm

from src.dgps import generate_data, theoretical_power
from src.methods import storey_fixed, benjamini_hochberg
from src.metrics import calculate_metrics
from src.simulation import CONFIG, run_simulation


def test_dgp_properties():
    p, labels = generate_data(
        100000, 0.5, np.random.default_rng(123)
    )

    assert p.shape == labels.shape == (100000,)
    assert labels.sum() == 50000
    assert np.all((p >= 0) & (p <= 1))

    # Null p-values should be uniform; alternative Z values have mean 2.
    assert abs(p[labels].mean() - 0.5) < 0.01
    assert abs(norm.isf(p[~labels]).mean() - 2.0) < 0.02


def test_theoretical_power():
    assert theoretical_power(0.01) == pytest.approx(
        0.372, abs=0.001
    )
    assert theoretical_power(0.001) == pytest.approx(
        0.138, abs=0.001
    )


def test_bh_known_example():
    # Unsorted input also checks that decisions retain the original order.
    p = [0.2, 0.001, 0.8, 0.03, 0.01]
    rejected, threshold = benjamini_hochberg(p, 0.05)

    assert rejected.tolist() == [False, True, False, True, True]
    assert threshold == pytest.approx(0.03)


def test_bh_no_rejections():
    rejected, threshold = benjamini_hochberg(
        [0.2, 0.5, 0.9], 0.05
    )

    assert not rejected.any()
    assert threshold == 0.0


def test_storey_known_example():
    rejected, pi0_hat, fdr_hat = storey_fixed(
        [0.001, 0.01, 0.03, 0.2, 0.8], 0.01
    )

    assert rejected.tolist() == [True, True, False, False, False]
    assert pi0_hat == pytest.approx(0.4)
    assert fdr_hat == pytest.approx(0.01)


def test_storey_zero_rejections():
    rejected, pi0_hat, fdr_hat = storey_fixed(
        [0.6, 0.8], 0.01
    )

    assert not rejected.any()
    assert pi0_hat == pytest.approx(2.0)
    assert fdr_hat == pytest.approx(0.04)


def test_metrics_known_example():
    result = calculate_metrics(
        [True, False, True, False],
        [True, True, False, False],
    )

    assert result["false_rejections"] == 1
    assert result["true_rejections"] == 1
    assert result["total_rejections"] == 2
    assert result["fdp"] == 0.5
    assert result["power"] == 0.5


def test_metrics_no_rejections():
    result = calculate_metrics(
        [False, False], [True, False]
    )

    assert result["fdp"] == 0.0
    assert result["power"] == 0.0


def test_simulation_reproducibility_and_ranges():
    config = {
        **CONFIG,
        "m": 100,
        "pi0_values": [0.5],
        "gamma_values": [0.01, 0.001],
        "replicates": 10,
    }

    first = run_simulation(config)
    second = run_simulation(config)

    pd.testing.assert_frame_equal(first, second)
    assert len(first) == 20
    assert not first.isna().any().any()

    for method in ["fixed", "bh"]:
        assert first[f"{method}_fdp"].between(0, 1).all()
        assert first[f"{method}_power"].between(0, 1).all()

        assert (
            first[f"{method}_false_rejections"]
            + first[f"{method}_true_rejections"]
            == first[f"{method}_total_rejections"]
        ).all()