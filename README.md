# GeneralStudy

Project created with MLOps-Template cookiecutter. For more info: https://mlopsstudygroup.github.io/mlops-guide/

## Project Structure

```
general-study/
├── data/
│   └── ahp_payload_example.json      # Example JSON input for AHP comparisons
├── models/                           # Saved model artifacts
├── notebooks/                        # Jupyter notebooks for exploration
├── results/                          # Pipeline output (CSV / JSON)
│   ├── ahp_topsis_consistency.csv
│   ├── ahp_topsis_global_weights.csv
│   ├── ahp_topsis_ranking.csv
│   └── ahp_topsis_summary.json
├── src/
│   ├── scripts/
│   │   ├── ahp_topsis/               # AHP + TOPSIS pipeline package
│   │   │   ├── __init__.py
│   │   │   ├── ahp.py                # Pairwise matrix, eigenvector weights, CR, CR suggestions
│   │   │   ├── constants.py          # Alternatives, criteria, decision matrix
│   │   │   ├── default_payload.py    # JSON payload loader
│   │   │   ├── recommend.py          # End-to-end pipeline orchestration
│   │   │   ├── topsis.py             # TOPSIS ranking logic
│   │   │   └── weights.py            # Global sub-criteria weight computation
│   │   ├── pages/
│   │   │   ├── dashboard.py          # Streamlit dashboard page
│   │   │   └── investment_criterias.py  # Streamlit AHP input page
│   │   ├── app.py                    # Streamlit multi-page entry point
│   │   └── run_ahp_pipeline.py       # CLI entry point for AHP-TOPSIS pipeline
│   └── tests/
│       └── test_generalstudy.py
├── .github/workflows/
│   └── test_on_push.yaml             # CI pipeline (Black + Pytest)
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

```
uv sync
source .venv/bin/activate
streamlit run src/scripts/app.py
uv add streamlit
```


##  Running Project

### Setup IBM Bucket Credentials for IBM COS

#### MacOS and Linux
Setup your credentials on ```~/.aws/credentials``` and ```~/.aws/config```. DVC works perfectly with IBM Obejct Storage, although it uses S3 protocol, you can also see this in other portions of the repository.


~/.aws/credentials

```credentials
[default]
aws_access_key_id = {Key ID}
aws_secret_access_key = {Access Key}
```


### Pre-commit Testings

In order to activate pre-commit testing you need ```pre-commit```

Installing pre-commit with pip
```
pip install pre-commit
```

Installing pre-commit on your local repository. Keep in mind this creates a Github Hook.
```
pre-commit install
```

Now everytime you make a commit, it will run some tests defined on ```.pre-commit-config.yaml``` before allowing your commit.

**Example**
```
$ git commit -m "Example commit"

black....................................................................Passed
pytest-check.............................................................Passed
```


### Using DVC

Download data from the DVC repository(analog to ```git pull```)
```
dvc pull
```

Reproduces the pipeline using DVC
```
dvc repro
```
