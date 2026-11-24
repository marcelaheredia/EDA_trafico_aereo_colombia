# Datos

Esta carpeta está vacía a propósito: el archivo crudo pesa 61 MB y no se versiona
en el repositorio. Se descarga en un solo comando desde el portal de datos abiertos
del Estado colombiano:

```bash
python scripts/01_descargar_datos.py
```

- `crudos/trafico_aereo_od_raw.csv` — archivo tal como lo publica la Aeronáutica
  Civil (501.819 filas × 16 columnas). Lo crea el comando de arriba.
- `procesados/trafico_aereo_limpio.parquet` — conjunto depurado (501.738 × 23).
  Lo crea el cuaderno al ejecutarse.

**Fuente:** Aeronáutica Civil de Colombia, *Transporte Aéreo Comercial – Tráfico
Origen‑Destino*, conjunto `gb6w-ynu4` de [datos.gov.co](https://www.datos.gov.co/d/gb6w-ynu4).
Licencia Creative Commons Attribution Share-Alike 4.0 International.
