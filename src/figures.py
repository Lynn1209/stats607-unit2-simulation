"""Create the power plot and FDR diagnostic plot."""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from src.simulation import ROOT


COLORS = {
    "fixed": "#287D8E",
    "bh": "#D87542",
}


def style_axis(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)
    ax.set_xticks([i / 10 for i in range(1, 10)])
    ax.set_xlabel(r"Null proportion $\pi_0$")


def save_figure(fig, name):
    folder = ROOT / "results" / "figures"
    folder.mkdir(parents=True, exist_ok=True)

    for extension in ["png", "pdf"]:
        fig.savefig(
            folder / f"{name}.{extension}",
            dpi=300,
            bbox_inches="tight",
        )

    plt.close(fig)
    print(f"Saved {name}.png and {name}.pdf")


def plot_power(summary):
    fig, axes = plt.subplots(
        1, 2, figsize=(10, 4.8), sharey=True
    )

    for ax, gamma in zip(axes, [0.01, 0.001]):
        data = summary[summary["gamma"] == gamma].sort_values("pi0")

        for method, label, marker in [
            ("fixed", "Storey fixed threshold", "o"),
            ("bh", "BH at estimated FDR", "s"),
        ]:
            ax.errorbar(
                data["pi0"],
                data[f"{method}_power_mean"],
                yerr=1.96 * data[f"{method}_power_mcse"],
                color=COLORS[method],
                marker=marker,
                markersize=5,
                linewidth=2,
                capsize=3,
                label=label,
            )

        ax.axhline(
            data["theoretical_power"].iloc[0],
            color="#555555",
            linestyle=":",
            linewidth=1.3,
            label="Fixed-threshold theoretical power",
        )

        ax.set_title(rf"$\gamma = {gamma}$")
        ax.set_ylim(0, 0.42)
        style_axis(ax)

    axes[0].set_ylabel("Mean power")
    fig.suptitle("Power comparison: Storey (2002) simulation", fontsize=14)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles, labels,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.07),
        ncol=2,
        frameon=False,
        fontsize=9,
    )
    fig.text(
        0.5, 0.015,
        "1,000 independent tests per replicate; 1,000 replicates per condition.\n"
        "Error bars: approximate 95% Monte Carlo intervals. "
        "BH uses a replicate-specific estimated FDR.",
        ha="center",
        fontsize=8,
    )
    fig.tight_layout(rect=[0, 0.22, 1, 0.93])
    save_figure(fig, "power_comparison")


def plot_fdr_diagnostic(summary):
    fig, axes = plt.subplots(
        2, 2, figsize=(10, 7), sharex=True
    )

    for column, gamma in enumerate([0.01, 0.001]):
        data = summary[summary["gamma"] == gamma].sort_values("pi0")
        upper = axes[0, column]
        lower = axes[1, column]

        for measure, label, color, marker in [
            ("fixed_fdp", "Empirical fixed-threshold FDR", "#287D8E", "o"),
            ("fdr_hat", "Mean estimated FDR", "#D87542", "s"),
        ]:
            upper.errorbar(
                data["pi0"],
                data[f"{measure}_mean"],
                yerr=1.96 * data[f"{measure}_mcse"],
                color=color,
                marker=marker,
                linewidth=1.8,
                capsize=3,
                label=label,
            )

        lower.errorbar(
            data["pi0"],
            data["fdr_estimation_gap_mean"],
            yerr=1.96 * data["fdr_estimation_gap_mcse"],
            color="#6C5792",
            marker="o",
            linewidth=1.8,
            capsize=3,
        )
        lower.axhline(0, color="#555555", linestyle="--", linewidth=1)

        upper.set_title(rf"$\gamma = {gamma}$")
        upper.set_ylim(bottom=0)
        style_axis(upper)
        style_axis(lower)
        upper.set_xlabel("")

    axes[0, 0].set_ylabel("FDR")
    axes[1, 0].set_ylabel("Mean estimated FDR - empirical FDR")

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(
        handles, labels,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.055),
        ncol=2,
        frameon=False,
        fontsize=9,
    )
    fig.suptitle("Diagnostic: checking FDR estimation", fontsize=14)
    fig.text(
        0.5, 0.015,
        "Error bars: approximate 95% Monte Carlo intervals; "
        "bottom panels use paired replicate differences.\n"
        "Positive gaps indicate conservative estimation on average. "
        "Panel scales differ by threshold.",
        ha="center",
        fontsize=8,
    )
    fig.tight_layout(rect=[0, 0.13, 1, 0.95])
    save_figure(fig, "fdr_diagnostic")


def main():
    plt.rcParams.update({
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.labelsize": 10,
        "font.family": "DejaVu Sans",
    })

    summary = pd.read_csv(ROOT / "results" / "summary.csv")
    plot_power(summary)
    plot_fdr_diagnostic(summary)


if __name__ == "__main__":
    main()