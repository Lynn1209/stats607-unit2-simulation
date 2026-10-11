# ADEMP: Storey (2002) Simulation Study

## Paper and project scope

This project reproduces the simulation in Section 5 of:

Storey, J. D. (2002). A direct approach to false discovery rates. Journal of the Royal Statistical Society: Series B, 64(3), 479–498.

The main goal is to reproduce Table 2 and the power patterns in Figure 1. The bootstrap study in Section 7 is not included.

The paper found that the fixed-threshold approach had higher power than BH in this comparison. Its power was about 0.372 when gamma was 0.01 and about 0.138 when gamma was 0.001. The estimates of FDR and the null proportion were slightly conservative on average.

## Aims

- Compare the power of the fixed-threshold approach and BH.
- Check how close the estimated null proportion is to its true value.
- Compare the estimated FDR with the FDR observed in the simulation.
- Check whether the results are similar to Table 2 in the paper.

## Data-generating mechanisms

Each simulation replicate contains 1,000 independent test statistics.

- Null test statistics follow N(0, 1).
- Alternative test statistics follow N(2, 1).
- The number of null tests is fixed at 1,000 * pi0.
- One-sided p-values are calculated as p_i = 1 - Phi(Z_i).

The null proportion pi0 ranges from 0.1 to 0.9.
The rejection threshold gamma is either 0.01 or 0.001.
The tuning parameter lambda is fixed at 0.5.

Each condition is repeated 1,000 times.

### Design table

All conditions use 1,000 tests, an alternative mean of 2, a standard deviation of 1, and lambda = 0.5.

| Condition | pi0 | gamma | Null tests | Alternative tests |
|---|---|---|---|---|
| 1 | 0.1 | 0.01 | 100 | 900 |
| 2 | 0.2 | 0.01 | 200 | 800 |
| 3 | 0.3 | 0.01 | 300 | 700 |
| 4 | 0.4 | 0.01 | 400 | 600 |
| 5 | 0.5 | 0.01 | 500 | 500 |
| 6 | 0.6 | 0.01 | 600 | 400 |
| 7 | 0.7 | 0.01 | 700 | 300 |
| 8 | 0.8 | 0.01 | 800 | 200 |
| 9 | 0.9 | 0.01 | 900 | 100 |
| 10 | 0.1 | 0.001 | 100 | 900 |
| 11 | 0.2 | 0.001 | 200 | 800 |
| 12 | 0.3 | 0.001 | 300 | 700 |
| 13 | 0.4 | 0.001 | 400 | 600 |
| 14 | 0.5 | 0.001 | 500 | 500 |
| 15 | 0.6 | 0.001 | 600 | 400 |
| 16 | 0.7 | 0.001 | 700 | 300 |
| 17 | 0.8 | 0.001 | 800 | 200 |
| 18 | 0.9 | 0.001 | 900 | 100 |

## Estimands and targets

The main quantities of interest are:

- The true null proportion, pi0.
- FDR: the expected proportion of false rejections among all rejections.
- Power: the expected proportion of alternative tests rejected.
- The average rejection threshold used by BH.

For each replicate, the false discovery proportion is:

    FDP = V / max(R, 1)

Here, V is the number of false rejections and R is the total number of rejections. FDR is estimated by averaging FDP across replicates.

This project studies FDR, not positive FDR (pFDR).

The theoretical power of the fixed-threshold approach is:

    1 - Phi(Phi^{-1}(1 - gamma) - 2)

This provides a reference for checking the simulated power.

## Methods

### Fixed-threshold approach

Reject tests with p_i <= gamma.

Following Equation (6), estimate the null proportion as:

    pi0_hat = count(p_i > lambda) / (m * (1 - lambda))

Following Equation (10), estimate FDR as:

    fdr_hat = pi0_hat * m * gamma / max(R, 1)

Keep these estimates without truncating them for reporting.

### Benjamini-Hochberg (BH)

Use the same p-values and apply BH at:

    alpha = min(fdr_hat, 1)

Sort the p-values and find the largest k such that:

    p_(k) <= alpha * k / m

Reject the k smallest p-values. If no k satisfies this condition, reject nothing and record a threshold of zero.

The cap at 1 keeps alpha within its valid range. The simulation will record whether this cap is ever needed.

As in the paper, BH uses the estimated FDR from each replicate. Therefore, this is not a comparison at a fixed level such as 0.05.

## Performance measures

Save the following results for each replicate:

- Numbers of false, true, and total rejections for both methods.
- FDP and power for both methods.
- Estimated null proportion and estimated FDR.
- BH rejection threshold.
- Whether the BH level was capped at 1.

For each condition, report:

- Mean FDP, which estimates FDR.
- Mean power for both methods.
- Mean estimated null proportion and its bias.
- Mean estimated FDR and its difference from the fixed-threshold FDR.
- Mean BH rejection threshold.
- Differences from the published Table 2 results.

Monte Carlo standard errors are calculated as:

    MCSE = sample standard deviation / sqrt(number of replicates)

Approximate 95% Monte Carlo intervals use mean +/- 1.96 * MCSE. For comparisons using the same replicate, calculate the MCSE from the paired differences.

## Reproducibility and implementation

The master random seed is 20261011.

Use NumPy's default_rng and SeedSequence.spawn to create a separate random stream for each of the 18 conditions, in the table order. Both methods use the same data within each replicate.

Keep the simulation settings in one configuration dictionary. Save raw results before creating summaries, and print progress after each condition.

The Makefile will run the simulation, summarize results, and create:

1. A power plot comparing the two methods.
2. A diagnostic plot comparing estimated and simulated FDR.

Tests will check data generation, BH calculations, performance metrics, and reproducibility.

The results may differ slightly from the paper because its random seed is not reported. These differences will be considered alongside Monte Carlo uncertainty and the rounding in the published table.