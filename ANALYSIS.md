# Analysis

## Main results

This project reproduces the simulation in Section 5 of Storey (2002), focusing on Table 2 and the power comparison in Figure 1. It uses 1,000 replications for each of 18 conditions, with 1,000 hypotheses per replication.

The main pattern agrees with the paper. The fixed-threshold procedure has higher average power than BH under the comparison used here. Its power stays close to 0.372 when gamma = 0.01 and 0.138 when gamma = 0.001. These values also agree with the theoretical power under the specified normal alternative.

BH power increases as the proportion of true null hypotheses increases. The fixed-threshold procedure's power stays nearly constant because each alternative hypothesis is tested against the same cutoff. Its false discovery rate increases with the null proportion.

Most reproduced values are close to the published results. However, at gamma = 0.001 and pi0 = 0.8, the average BH power is 0.11379, compared with 0.129 in Table 2. The Monte Carlo standard error is 0.000883, giving an approximate 95% interval of [0.11206, 0.11552]. The published value is outside this interval, so the difference should not be explained only as ordinary Monte Carlo variation in this run. The cause remains unresolved. The interval describes uncertainty in this simulation, not uncertainty in the published result.

## What the figures show

The power comparison figure shows the power advantage of the fixed-threshold procedure across the simulated conditions. The advantage becomes smaller as pi0 increases. The confidence intervals are narrow, so the overall pattern is stable across replications.

The FDR diagnostic compares the estimated FDR with the observed false discovery proportion averaged across replications. The estimates are generally higher than the empirical FDR. The lower panels show the paired difference between these quantities, with Monte Carlo uncertainty. Pairing is useful because both quantities come from the same simulated data. Some intervals include zero, so the figure does not establish a strictly positive gap in every condition.

## Fairness and limitations

Both procedures use the same p-values in each replication. Following the paper's comparison, BH is run at the FDR level estimated by the fixed-threshold procedure. This level depends on the data. Therefore, this study compares power under that specific rule; it does not compare both methods at a common, preselected nominal FDR level.

The design includes BH as an established comparison method, but does not compare other adaptive multiple-testing methods. It also uses independent tests and the same normal effect size for every alternative. These assumptions make the simulation easy to interpret, but real applications may involve correlated tests, weaker signals, or different effect sizes. Conditions with almost all hypotheses null are also not included.

I interpret pi0 as fixing the number of true null hypotheses in each replication. The original random seed and simulated data are not available for this reproduction, so exact numerical agreement is not expected. This project also excludes the bootstrap tuning procedure discussed later in the paper.

## Confidence and possible improvements

Nine tests pass, covering data generation, theoretical power, BH rejection decisions, FDR estimation, performance metrics, and reproducibility. Agreement with theoretical power provides an additional check, although these checks do not explain the remaining discrepancy with Table 2.

A useful extension would vary effect sizes and introduce dependence between tests. Another comparison could run both procedures at a preselected target FDR and examine power together with achieved FDR. More replications would reduce Monte Carlo uncertainty, but would not by themselves resolve a difference caused by an implementation or design choice.