"""Download the Vanguard project datasets into data/raw/.

The data is not tracked in the repository (~68 MB). This script fetches it
from Ironhack's public repo so the whole team works from the same files at
the same path.

Usage:
    uv run python -m project_template.download
"""

import urllib.request

from project_template.paths import RAW_DIR

BASE_URL = (
    "https://raw.githubusercontent.com/data-bootcamp-v4/lessons/main/"
    "5_6_eda_inf_stats_tableau/project/files_for_project/"
)

FILES = [
    "df_final_demo.txt",
    "df_final_experiment_clients.txt",
    "df_final_web_data_pt_1.txt",
    "df_final_web_data_pt_2.txt",
]


def download(force: bool = False) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    for name in FILES:
        target = RAW_DIR / name

        if target.exists() and not force:
            mb = target.stat().st_size / 1024**2
            print(f"already there  {name}  ({mb:.1f} MB)")
            continue

        print(f"downloading    {name} ...")
        urllib.request.urlretrieve(BASE_URL + name, target)
        mb = target.stat().st_size / 1024**2
        print(f"done           {name}  ({mb:.1f} MB)")


if __name__ == "__main__":
    download()
