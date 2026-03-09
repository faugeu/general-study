# GeneralStudy

Project created with MLOps-Template cookiecutter. For more info: https://mlopsstudygroup.github.io/mlops-guide/


## 📋 Initialization
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


## 🏃🏻 Running Project

### 🔑 Setup IBM Bucket Credentials for IBM COS

#### MacOS and Linux
Setup your credentials on ```~/.aws/credentials``` and ```~/.aws/config```. DVC works perfectly with IBM Obejct Storage, although it uses S3 protocol, you can also see this in other portions of the repository.


~/.aws/credentials

```credentials
[default]
aws_access_key_id = {Key ID}
aws_secret_access_key = {Access Key}
```


### ✅ Pre-commit Testings

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


### ⚗️ Using DVC

Download data from the DVC repository(analog to ```git pull```)
```
dvc pull
```

Reproduces the pipeline using DVC
```
dvc repro
```

### AHP-TOPSIS Pipeline (Fuzzy AHP + TOPSIS)

The pipeline requires a JSON file with your criteria and subcriteria comparisons. Run from the project root:

```bash
python src/scripts/run_ahp_pipeline.py --payload-file data/ahp_payload_example.json
```

Optional: `--results-dir` (default `results`).

Outputs are written to `results/` (default):

- `ahp_topsis_ranking.csv` – Investment alternatives ranking (TOPSIS closeness)
- `ahp_topsis_consistency.csv` – AHP consistency report (CR) per node
- `ahp_topsis_global_weights.csv` – Global weights by sub-criterion
- `ahp_topsis_summary.json` – Summary (top alternative, closeness score)

Create your JSON with pair keys in the form `"A | B"` (e.g. `"Financial security | Profitability": 3`). See the example in `data/ahp_payload_example.json`. Criterion and subcriterion names must match those in `src/scripts/ahp_topsis/constants.py`.