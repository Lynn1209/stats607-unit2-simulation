PYTHON ?= python3

.PHONY: all simulate analyze figures clean test

all: figures

simulate:
	$(PYTHON) -m src.simulation

analyze: simulate
	$(PYTHON) -m src.analyze

figures: analyze
	$(PYTHON) -m src.figures

test:
	$(PYTHON) -m pytest -q

clean:
	rm -f results/raw/replicates.csv results/raw/run_info.json
	rm -f results/summary.csv results/paper_comparison.csv
	rm -f results/figures/power_comparison.png results/figures/power_comparison.pdf
	rm -f results/figures/fdr_diagnostic.png results/figures/fdr_diagnostic.pdf