"""Carga de config.yaml.

Uso desde un notebook:

    from project_template.config import CONFIG
    CONFIG["embudo"]          # ['start', 'step_1', ...]
    CONFIG["estadistica"]["alpha"]
"""

import yaml

from project_template.paths import PROJECT_ROOT

CONFIG_PATH = PROJECT_ROOT / "config.yaml"


def load_config(path=CONFIG_PATH) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


CONFIG = load_config()
