# Vanguard — A/B Test Analysis

Evaluation of the A/B test Vanguard ran between 15 March and 20 June 2017 on its online process, to decide whether the redesigned interface should replace the current one.

Deliverables: a documented Jupyter notebook, a Tableau dashboard and a business presentation.

## Who we are working for

Vanguard is not structured like its competitors, and that shapes what our recommendation should optimise for.

Founded in 1975 by John Bogle, the company is **owned by its own funds, which are owned by their investors**. There are no outside shareholders. It operates *at cost*: surpluses come back to clients as lower fees rather than going out as dividends. It now manages around $10.4 trillion.

The consequence for this project is that **reducing operating cost is not a saving for the company — it is a return for the client**. A client who cannot finish the process online and has to call generates a cost that ultimately comes out of the client-owners' pockets. An improvement in the online experience is therefore aligned with the company's founding purpose, not just with a conversion metric.

Its client base reflects that purpose. Vanguard's core retail clients are in the 45–75 range, concentrated in retirement accounts and 401(k) rollovers, and balances rise steeply with age: an average of roughly $299,000 for clients aged 65 and over, against $6,900 for the under-25s. Median age at account opening has recently fallen to 33, so the company is attracting younger clients — but its assets still sit with older ones.

Sources: [Vanguard's business model](https://www.latterly.org/vanguard-business-model/), [company profile](https://www.ebsco.com/research-starters/business-and-management/vanguard-group), [client demographics](https://businessmodelcanvastemplate.com/blogs/target-market/vanguard-target-market).

## Visual identity

The dashboard and the presentation should look like Vanguard documents, which the day 5 checklist asks for explicitly and the rubric rewards.

The brand's primary colour is a **maroon**, chosen to convey reliability and long standing. The logo has been wordmark-only since the ship was dropped in 2020. The overall register is institutional and restrained: no gradients, no startup styling.

Vanguard does not publish official hex codes. The values in circulation (`#A21918`, `#800000`) are sampled from the logo and are close enough to work with, but should not be presented as official.

## The questions we are answering

The analysis is built around five questions, asked in this order. Each one depends on the previous being settled, which is why the work is sequenced rather than split by topic.

| # | Question | What it means in practice |
|---|---|---|
| 1 | Can we trust our data? | Understand the datasets, find the quality issues, and decide how to handle each one |
| 2 | Can we trust our experiment? | Check that Control and Test are comparable before comparing any outcome |
| 3 | How should customer behaviour be measured? | Reconstruct journeys from raw events and define the KPIs |
| 4 | What evidence supports our conclusions? | Test whether the differences are real, and whether they matter |
| 5 | What should Vanguard do? | Turn the evidence into a recommendation a stakeholder can act on |

The notebook, the dashboard and the presentation should tell the same story from different angles.

## Team

| Who | Role |
|---|---|
| Aroa | Project Manager — coordinates the work, reviews and merges pull requests, and analyses alongside everyone else |
| Angélica | Data Analyst |

The Project Manager role is about keeping the repository and the plan in order, not about deciding the analysis. Methodological choices are agreed between us, and both of us should be able to explain any part of the work.

## Getting started

You need [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

```bash
git clone https://github.com/aroaxinping/vanguard-ab-test.git
cd vanguard-ab-test
uv sync
```

`uv sync` creates the `.venv` environment and installs every library listed in `pyproject.toml`. You do not need to run `uv venv` or install anything by hand.

The datasets are versioned in `data/raw/`, so cloning is all you need — there is nothing to download.

They are also available from Ironhack's public repo, and `uv run python -m project_template.download` re-fetches them if a file is ever lost or modified. It skips files that are already there.

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
from project_template.paths import RAW_DIR
from project_template.config import CONFIG

files = CONFIG["files"]

demo = pd.read_csv(RAW_DIR / files["demo"])
exp = pd.read_csv(RAW_DIR / files["experiment"])
web = pd.concat(
    [pd.read_csv(RAW_DIR / f) for f in files["web"]],
    ignore_index=True,
)
```

That gives you 70,609 clients, 70,609 assignments and 755,405 web events.

`RAW_DIR` is resolved from the repository root, so it works the same from `notebooks/`, from the root or from the terminal, and points to the right place on everyone's machine. Filenames come from `config.yaml`, so they are written down once rather than repeated across notebooks.

The same file holds the analysis parameters:

```python
CONFIG["funnel"]                  # ['start', 'step_1', 'step_2', 'step_3', 'confirm']
CONFIG["statistics"]["alpha"]     # 0.05
CONFIG["experiment"]["start"]     # 2017-03-15
```

Paths belong in `paths.py`, everything else in `config.yaml`. When you introduce a new analysis parameter, add it to the YAML rather than hardcoding it in a notebook.

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
data/raw/         original data, versioned and never modified
data/processed/   clean data produced by the analysis (git-ignored)
notebooks/        one notebook per person
figures/          exported charts
sql_scripts/      SQL queries
tableau/          Tableau workbooks (.twbx)
slides/           presentation
src/project_template/
    paths.py      project paths
    config.py     config.yaml loader
    download.py   dataset download
```

## Naming notebooks

Notebooks follow the [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/) convention, which is the usual standard for this kind of project:

```
<phase>.<iteration>-<author>-<short-description>.ipynb

1.0-aroa-data-quality.ipynb
│ │   │    └── what the notebook does, in kebab-case
│ │   └─────── who wrote it, so two people never edit the same file
│ └─────────── iteration within that phase
└───────────── phase of the analysis
```

**The phase number** orders the work, so the folder sorts into the sequence the notebooks should be read in — one phase per question above.

**The iteration number** exists so a phase can be split without renaming anything. If reconstructing journeys and computing KPIs get too big for one file, they become `3.0-` and `3.1-`. It is not a version number: `3.1` comes after `3.0`, it is not a better version of it.

Plain `1-`, `2-`, `3-` would order things just as well, but inserting a notebook between two of them means renumbering everything after it. The decimal leaves room to insert.

**The author suffix** is what keeps us out of each other's way. Notebooks are JSON with outputs embedded, so two people editing one file produce conflicts that are painful to resolve.

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
