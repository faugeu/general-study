# GeneralStudy

Project created with MLOps-Template cookiecutter. For more info: https://mlopsstudygroup.github.io/mlops-guide/

## Project Structure

```
general-study/
├── data/
│   └── ahp_payload_example.json          # Example JSON input for AHP comparisons
├── github_actions/                       # Scripts for github actions
├── notebooks/                            # Jupyter notebooks for exploration
├── src/
│   ├── scripts/
│   │   ├── ahp_topsis/                   # AHP + TOPSIS pipeline package
│   │   │   ├── __init__.py
│   │   │   ├── ahp.py                    # Pairwise matrix, eigenvector weights, CR, CR suggestions
│   │   │   ├── constants.py              # Alternatives, criteria, decision matrix
│   │   │   ├── default_payload.py        # JSON payload loader
│   │   │   ├── recommend.py              # End-to-end pipeline orchestration
│   │   │   ├── topsis.py                 # TOPSIS ranking logic
│   │   │   └── weights.py                # Global sub-criteria weight computation
│   │   ├── monte_carlo_sim/              # Monte Carlo simulation package
│   │   │   ├── __init__.py
│   │   │   ├── config.py                 # Simulation parameters and defaults
│   │   │   ├── utils.py                  # Shared utility functions
│   │   │   ├── processes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── expenses.py           # Stochastic expense process
│   │   │   │   ├── income.py             # Stochastic income process
│   │   │   │   └── returns.py            # Asset return distributions
│   │   │   └── simulation/
│   │   │       ├── __init__.py
│   │   │       ├── monte_carlo.py        # Monte Carlo engine (run simulations)
│   │   │       └── wealth_path.py        # Wealth accumulation path logic
│   │   ├── results/                      # Results display page
│   │   │   ├── _init_.py
│   │   │   ├── ahp.py                    # AHP results components
│   │   │   ├── charts.py                 # Visualization charts
│   │   │   ├── constants.py              # UI constants
│   │   │   ├── monte_carlo.py            # Monte Carlo results components
│   │   │   ├── page.py                   # Results Streamlit page
│   │   │   └── ui.py                     # Shared UI helpers
│   │   ├── savings_profile/              # User financial profile input page
│   │   │   ├── _init_.py
│   │   │   ├── constants.py              # Field definitions and defaults
│   │   │   ├── inputs.py                 # Input form components
│   │   │   ├── page.py                   # Savings profile Streamlit page
│   │   │   └── validation.py             # Input validation logic
│   │   ├── survey/                       # AHP pairwise comparison input page
│   │   │   ├── _init_.py
│   │   │   ├── builder.py                # Survey form builder
│   │   │   ├── constants.py              # Saaty scale and labels
│   │   │   ├── matrix_widget.py          # Pairwise matrix UI widget
│   │   │   ├── page.py                   # Survey Streamlit page
│   │   │   └── tooltip.py                # Tooltip helpers
│   │   ├── app.py                        # Streamlit multi-page entry point
│   │   └── run_ahp_pipeline.py           # CLI entry point for AHP-TOPSIS pipeline
│   └── tests/
│       └── test_generalstudy.py
├── .github/workflows/                    # Github action workflows
├── .pre-commit-config.yaml
├── pyproject.toml
├── requirements.txt
└── main.py
```


##  Initialization
```
cookiecutter https://github.com/mlops-guide/mlops-template.git
uv init
python3 -m venv .venv
```

##  Running Project
```
uv sync
source .venv/bin/activate
streamlit run src/scripts/app.py
```
