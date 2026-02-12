# Analysis Plan — Detecting Changes and Associating Causes on Brent Oil Prices

Objective
- Study how major political, economic, and policy events influence Brent oil prices over the past decade.

Planned Analysis Steps
1. Data ingestion and cleaning
   - Load `data/BrentOilPrices.csv` and standardize date and price formats.
   - Resample to business days if needed and interpolate small gaps.
2. Exploratory analysis
   - Plot raw series, log prices, and returns.
   - Visualize rolling mean and rolling volatility (30/90 day windows).
3. Time-series diagnostics
   - Test for stationarity (ADF, KPSS) on levels and returns.
   - Decompose trend/seasonality (STL) to inspect long-term trend.
   - Check heteroskedasticity (ARCH effects) and volatility clustering.
4. Event compilation
   - Compile structured `data/processed/events.csv` of 10–15 events (political, sanctions, OPEC decisions, pandemics, conflicts) with dates and categories.
5. Change point and structural break analysis
   - Apply change point detection (e.g., `ruptures` Pelt/Binseg) on prices and returns to identify break dates.
   - Fit piecewise linear models or segmented regressions to quantify parameter shifts.
6. Statistical association with events
   - Map detected change points to compiled events within a pre-specified window (e.g., ±14 days).
   - Use event study methodology: estimate abnormal returns relative to a baseline model and compute cumulative abnormal returns.
   - Run regression models with event dummies controlling for market/ macro variables where available.
7. Robustness and causality discussion
   - Use placebo tests, varying windows, and alternative break detection methods.
   - Discuss limitations and refrain from claiming causation without stronger identification strategies.
8. Reporting
   - Produce figures, a short executive report, and a notebook that stakeholders can run.

Assumptions and Limitations
- Data quality: We assume `data/BrentOilPrices.csv` contains daily, correctly recorded prices. Missingness will be handled conservatively.
- Correlation vs causation: Detected temporal associations between events and price changes do not by themselves prove causality. Confounders and contemporaneous global shocks may drive both events and prices.
- Event dating: Some events are gradual or have uncertain start dates; we use the earliest public date or announcement and test windows around the date.
- Model limitations: Change point methods identify structural breaks but can be sensitive to hyperparameters and pre-processing. Volatility clustering and nonstationarity complicate inference.

Communication Channels
- Technical report (PDF) summarizing methods and results.
- Jupyter notebook for reproducibility and interactive exploration.
- Dashboard prototype (`dashboard/app.py`) for stakeholders to view key plots (future work).
- Presentation deck for executives highlighting actionable takeaways.

Expected Outputs
- A reproducible notebook with diagnostics and change point analysis.
- `data/processed/events.csv` with compiled events.
- Figures showing detected change points, price trajectories, and event overlays.
- Short write-up of assumptions, limitations, and recommended next steps.
