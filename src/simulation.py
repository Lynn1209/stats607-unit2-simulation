"""Run the simulation and save replicate-level results."""

import json
import logging
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd

from src.dgps import generate_data
from src.methods import storey_fixed, benjamini_hochberg
from src.metrics import calculate_metrics


ROOT = Path(__file__).resolve().parents[1]

CONFIG = {
    "m": 1000,
    "effect": 2.0,
    "pi0_values": [i / 10 for i in range(1, 10)],
    "gamma_values": [0.01, 0.001],
    "tuning": 0.5,
    "replicates": 1000,
    "seed": 20261011,
}


def run_simulation(config):
    """Run every condition using separate random streams."""
    conditions = [
        (pi0, gamma)
        for gamma in config["gamma_values"]
        for pi0 in config["pi0_values"]
    ]

    streams = np.random.SeedSequence(config["seed"]).spawn(
        len(conditions)
    )
    rows = []

    for condition_id, ((pi0, gamma), stream) in enumerate(
        zip(conditions, streams), start=1
    ):
        rng = np.random.default_rng(stream)

        for replicate in range(1, config["replicates"] + 1):
            p_values, is_null = generate_data(
                m=config["m"],
                pi0=pi0,
                rng=rng,
                effect=config["effect"],
            )

            fixed, pi0_hat, fdr_hat = storey_fixed(
                p_values, gamma, tuning=config["tuning"]
            )

            alpha = min(fdr_hat, 1.0)
            bh, bh_threshold = benjamini_hochberg(
                p_values, alpha
            )

            row = {
                "condition": condition_id,
                "replicate": replicate,
                "m": config["m"],
                "effect": config["effect"],
                "pi0": pi0,
                "gamma": gamma,
                "tuning": config["tuning"],
                "pi0_hat": pi0_hat,
                "fdr_hat": fdr_hat,
                "bh_alpha": alpha,
                "alpha_capped": fdr_hat > 1.0,
                "bh_threshold": bh_threshold,
            }

            for name, decisions in [("fixed", fixed), ("bh", bh)]:
                metrics = calculate_metrics(decisions, is_null)
                row.update({
                    f"{name}_{key}": value
                    for key, value in metrics.items()
                })

            rows.append(row)

        logging.info(
            "Completed condition %d/%d: pi0=%.1f, gamma=%g",
            condition_id, len(conditions), pi0, gamma
        )

    return pd.DataFrame(rows)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    start = perf_counter()

    output_dir = ROOT / "results" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)

    results = run_simulation(CONFIG)
    output_path = output_dir / "replicates.csv"
    results.to_csv(output_path, index=False)

    elapsed = perf_counter() - start
    metadata = {
        "config": CONFIG,
        "elapsed_seconds": elapsed,
        "rows": len(results),
        "alpha_capped_count": int(results["alpha_capped"].sum()),
    }

    with (output_dir / "run_info.json").open("w") as file:
        json.dump(metadata, file, indent=2)

    logging.info("Saved %d rows to %s", len(results), output_path)
    logging.info("Simulation finished in %.2f seconds", elapsed)


if __name__ == "__main__":
    main()