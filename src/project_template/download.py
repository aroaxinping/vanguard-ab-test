"""Descarga los datasets del proyecto Vanguard en data/raw/.

Los datos no se versionan en el repo (pesan ~68 MB). Este script los baja
del repo público de Ironhack para que todo el equipo trabaje con los mismos
archivos en la misma ruta.

Uso:
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
        destino = RAW_DIR / name

        if destino.exists() and not force:
            mb = destino.stat().st_size / 1024**2
            print(f"ya existe   {name}  ({mb:.1f} MB)")
            continue

        print(f"descargando {name} ...")
        urllib.request.urlretrieve(BASE_URL + name, destino)
        mb = destino.stat().st_size / 1024**2
        print(f"listo       {name}  ({mb:.1f} MB)")


if __name__ == "__main__":
    download()
