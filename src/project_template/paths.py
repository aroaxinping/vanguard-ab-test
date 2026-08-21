"""Rutas del proyecto, resueltas siempre desde la raíz.

Da igual desde dónde se ejecute el código (notebooks/, raíz, terminal):
las rutas son absolutas y correctas para cualquiera que clone el repo.
"""

from pathlib import Path

# paths.py está en src/project_template/, así que la raíz son dos niveles arriba.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

FIGURES_DIR = PROJECT_ROOT / "figures"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
SQL_DIR = PROJECT_ROOT / "sql_scripts"
