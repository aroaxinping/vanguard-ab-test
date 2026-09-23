"""Project paths, always resolved from the repository root.

Wherever the code runs from (notebooks/, the root, a terminal), these paths
stay absolute and correct on every machine that clones the repository.
"""

from pathlib import Path

# This file lives in src/project_template/, so the root is two levels up.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

FIGURES_DIR = PROJECT_ROOT / "figures"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
SQL_DIR = PROJECT_ROOT / "sql_scripts"
