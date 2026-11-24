# -*- coding: utf-8 -*-
"""
Descarga el conjunto de datos del analisis desde el portal de datos abiertos
de Colombia y lo guarda sin modificar en datos/crudos/.

Fuente : Aeronautica Civil de Colombia, "Transporte Aereo Comercial -
         Trafico Origen-Destino (Colombia)".
Portal : https://www.datos.gov.co/d/gb6w-ynu4
Licencia: Creative Commons Attribution Share-Alike 4.0 International.

Nota sobre el API: el endpoint /resource/{id}.csv devuelve solo 1.000 filas por
defecto (ese fue el primer tropiezo del trabajo). Para traer el conjunto
completo hay que usar el endpoint de exportacion /api/views/{id}/rows.csv.

Uso:
    python scripts/01_descargar_datos.py
"""
from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

ID_CONJUNTO = "gb6w-ynu4"
URL = f"https://www.datos.gov.co/api/views/{ID_CONJUNTO}/rows.csv?accessType=DOWNLOAD"
BASE = Path(__file__).resolve().parents[1]
DESTINO = BASE / "datos" / "crudos" / "trafico_aereo_od_raw.csv"


def descargar(forzar: bool = False) -> Path:
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    if DESTINO.exists() and not forzar:
        mb = DESTINO.stat().st_size / 1e6
        print(f"El archivo ya existe ({mb:.1f} MB): {DESTINO}")
        print("Use --forzar para descargarlo de nuevo.")
        return DESTINO

    print(f"Descargando {URL} ...")
    peticion = urllib.request.Request(URL, headers={"Accept-Encoding": "gzip, deflate"})
    with urllib.request.urlopen(peticion, timeout=900) as respuesta, open(DESTINO, "wb") as salida:
        datos = respuesta.read()
        salida.write(datos)
    mb = DESTINO.stat().st_size / 1e6
    with open(DESTINO, encoding="utf-8", errors="replace") as f:
        filas = sum(1 for _ in f) - 1
    print(f"Listo: {DESTINO} ({mb:.1f} MB, {filas:,} filas)".replace(",", "."))
    return DESTINO


if __name__ == "__main__":
    descargar(forzar="--forzar" in sys.argv)
