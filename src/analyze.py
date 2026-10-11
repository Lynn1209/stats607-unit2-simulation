"""Summarize simulation results and compare with Table 2."""

import numpy as np
import pandas as pd

from src.dgps import theoretical_power
from src.simulation import ROOT


# Values transcribed from Storey (2002), Table 2.
# Within each list, pi0 increases from 0.1 to 0.9.
PAPER = {
    0.01: {
        "fixed_fdp": [
            .003, .007, .011, .018, .026,
            .039, .060, .097, .195
        ],
        "fixed_power": [
            .372, .372, .372, .372, .372,
            .372, .371, .372, .372
        ],
        "bh_power": [
            .074, .122, .164, .203, .235,
            .268, .295, .319, .344
        ],
        "fdr_hat": [
            .004, .008, .013, .019, .027,
            .040, .061, .099, .200
        ],
        "pi0_hat": [
            .141, .236, .331, .426, .523,
            .618, .714, .809, .905
        ],
        "bh_threshold": [
            .0003, .0008, .001, .002, .003,
            .004, .005, .007, .008
        ],
    },
    0.001: {
        "fixed_fdp": [
            .0008, .002, .003, .005, .007,
            .011, .017, .028, .061
        ],
        "fixed_power": [
            .138, .138, .137, .138, .138,
            .138, .138, .138, .137
        ],
        "bh_power": [
            .016, .031, .046, .060, .074,
            .088, .101, .129, .133
        ],
        "fdr_hat": [
            .001, .002, .003, .005, .008,
            .011, .017, .030, .066
        ],
        "pi0_hat": [
            .141, .236, .331, .426, .523,
            .618, .714, .809, .905
        ],
        "bh_threshold": [
            .00001, .00005, .0001, .0002, .0003,
            .0004, .0005, .0006, .0008
        ],
    },
}


def summarize_results(raw):
    """Calculate means, MCSEs, and paired differences."""
    rows = []
    measures = [
        "fixed_fdp", "bh_fdp",
        "fixed_power", "bh_power",
        "pi0_hat", "fdr_hat", "bh_threshold",
    ]

    for condition, group in raw.groupby("condition", sort=True):
        pi0 = float(group["pi0"].iloc[0])
        gamma = float(group["gamma"].iloc[0])
        n = len(group)

        row = {
            "condition": condition,
            "pi0": pi0,
            "gamma": gamma,
            "replicates": n,
            "alpha_capped_count": int(group["alpha_capped"].sum()),
            "theoretical_power": theoretical_power(
                gamma, float(group["effect"].iloc[0])
            ),
        }

        for measure in measures:
            values = group[measure]
            row[f"{measure}_mean"] = values.mean()
            row[f"{measure}_mcse"] = values.std(ddof=1) / np.sqrt(n)

        paired = {
            "power_gain": group["fixed_power"] - group["bh_power"],
            "fdr_estimation_gap": group["fdr_hat"] - group["fixed_fdp"],
        }

        for name, values in paired.items():
            row[f"{name}_mean"] = values.mean()
            row[f"{name}_mcse"] = values.std(ddof=1) / np.sqrt(n)

        row["pi0_bias"] = row["pi0_hat_mean"] - pi0
        rows.append(row)

    return pd.DataFrame(rows)


def compare_with_paper(summary):
    """Save simulated and published values side by side."""
    rows = []

    for _, condition in summary.iterrows():
        gamma = float(condition["gamma"])
        pi0 = float(condition["pi0"])
        index = int(round(pi0 * 10)) - 1

        for measure, published_values in PAPER[gamma].items():
            simulated = condition[f"{measure}_mean"]
            published = published_values[index]

            rows.append({
                "pi0": pi0,
                "gamma": gamma,
                "measure": measure,
                "simulated": simulated,
                "published": published,
                "difference": simulated - published,
                "simulation_mcse": condition[f"{measure}_mcse"],
            })

    return pd.DataFrame(rows)


def main():
    raw_path = ROOT / "results" / "raw" / "replicates.csv"
    raw = pd.read_csv(raw_path)

    summary = summarize_results(raw)
    comparison = compare_with_paper(summary)

    output_dir = ROOT / "results"
    summary.to_csv(output_dir / "summary.csv", index=False)
    comparison.to_csv(
        output_dir / "paper_comparison.csv", index=False
    )

    columns = [
        "pi0", "gamma",
        "fixed_power_mean", "bh_power_mean",
        "fixed_fdp_mean", "fdr_hat_mean", "pi0_hat_mean",
    ]
    print(summary[columns].round(4).to_string(index=False))
    print("\nSaved results/summary.csv")
    print("Saved results/paper_comparison.csv")
    print(
        "BH alpha capped:",
        int(summary["alpha_capped_count"].sum()),
        "times",
    )


if __name__ == "__main__":
    main()