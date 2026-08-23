# Vanguard — A/B Test Analysis

Evaluation of the A/B test Vanguard ran between 15 March and 20 June 2017 on its online process, to decide whether the redesigned interface should replace the current one.

Deliverables: a documented Jupyter notebook, a Tableau dashboard and a business presentation.

## Getting started

You need [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

```bash
git clone https://github.com/aroaxinping/vanguard-ab-test.git
cd vanguard-ab-test
uv sync
```

`uv sync` creates the `.venv` environment and installs every library listed in `pyproject.toml`. You do not need to run `uv venv` or install anything by hand.

### Download the data

The datasets are around 68 MB and are not tracked in the repository. Download them with:

```bash
uv run python -m project_template.download
```

This drops the four files into `data/raw/`. If they are already there, it skips them.

### Register the Jupyter kernel

Once per machine, so that Jupyter can see the project environment:

```bash
uv run python -m ipykernel install --user --name vanguard --display-name "Python (Vanguard)"
```

In Jupyter, pick the **Python (Vanguard)** kernel. Alternatively, `uv run jupyter lab` opens Jupyter from inside the environment with no kernel registration at all.

## Reading the data

Do not hardcode paths. Import them:

```python
import pandas as pd
from project_template.paths import RAW_DIR, PROCESSED_DIR

demo = pd.read_csv(RAW_DIR / "df_final_demo.txt")
exp  = pd.read_csv(RAW_DIR / "df_final_experiment_clients.txt")
web1 = pd.read_csv(RAW_DIR / "df_final_web_data_pt_1.txt")
web2 = pd.read_csv(RAW_DIR / "df_final_web_data_pt_2.txt")
```

`RAW_DIR` is resolved from the repository root, so it works the same from `notebooks/`, from the root or from the terminal, and points to the right place on everyone's machine.

Analysis parameters live in `config.yaml`:

```python
from project_template.config import CONFIG

CONFIG["funnel"]                  # ['start', 'step_1', 'step_2', 'step_3', 'confirm']
CONFIG["statistics"]["alpha"]     # 0.05
CONFIG["experiment"]["start"]     # 2017-03-15
```

Paths belong in `paths.py`, parameters in `config.yaml`. When you introduce a new analysis parameter, add it to the YAML rather than hardcoding it in a notebook.

## The data

Four files, comma-separated despite the `.txt` extension.

| File | Rows | Contents |
|---|---|---|
| `df_final_demo.txt` | 70,609 | Age, gender, tenure, balance, calls and logons |
| `df_final_experiment_clients.txt` | 70,609 | Assignment to Control or Test |
| `df_final_web_data_pt_1.txt` | 343,141 | Web events, first part |
| `df_final_web_data_pt_2.txt` | 412,264 | Web events, second part |

The two event files must be concatenated before analysis.

**Two naming gotchas.** The funnel steps are `step_1`, `step_2` and `step_3` with an underscore, even though the brief writes them without one. And the assignment column is `Variation`, capitalised. Copying the names straight from the brief returns empty filters with no error.

The funnel has five events, in this order:

```
start → step_1 → step_2 → step_3 → confirm
```

The logs record **events, not completed journeys**: a client may repeat steps, navigate backwards, restart or abandon the process.

## Layout

```
data/raw/         original data, never modified (git-ignored)
data/processed/   clean data produced by the analysis
notebooks/        one notebook per person
figures/          exported charts
sql_scripts/      SQL queries
slides/           presentation
src/project_template/
    paths.py      project paths
    config.py     config.yaml loader
    download.py   dataset download
```

## Working agreements

- Everyone works on **their own branch**, never directly on `main`.
- **One notebook per person**, with your name in the filename. Notebooks are JSON with outputs embedded, so two people editing the same file produce unreadable conflicts.
- Shared code goes in `src/project_template/`, not duplicated across notebooks.
- Analysis parameters go in `config.yaml`, not hardcoded in notebooks.
- `main` is protected: changes are integrated through pull requests only.

## Daily routine

**Starting the day**, sync your branch with whatever was merged yesterday:

```bash
git switch main
git pull
git switch your_branch
git merge main
```

If there are conflicts, git marks the affected files with `<<<<<<<`, `=======` and `>>>>>>>`. Decide which content to keep, delete the markers, and commit.

Then open Jupyter and work on your notebook.

**Ending the day**, in this order:

1. In Jupyter: restart the kernel and clear all cell outputs. This keeps diffs readable and the repository light.
2. Save the notebook.
3. Stage only the files you touched — never `git add -A`:

   ```bash
   git add notebooks/your_notebook.ipynb
   git commit -m "A message explaining what you did"
   git push origin your_branch
   ```

4. Open a pull request against `main` so the work gets integrated.

## Adding a library

```bash
uv add library_name
```

This updates `pyproject.toml` and `uv.lock`. Commit both so the whole team ends up with the same versions. Do not use `pip install`.
