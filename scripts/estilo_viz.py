"""
Sistema visual del informe: paleta validada, estilo de matplotlib y utilidades
de figura (titulo + subtitulo + nota al pie con la lectura de la figura).

Decisiones de diseno:
  * Superficie clara #fcfcfb con tinta casi negra; rejilla de un solo tono por
    encima de la superficie (hairline) y sin bordes de caja.
  * Paleta categorica de orden fijo (azul, naranja, aqua, amarillo...). Los tres
    primeros cupos pasan las pruebas de separacion para daltonismo en todos los
    pares, por eso las figuras con 3 series usan solo esos.
  * Rampa secuencial de un solo tono (azul claro -> oscuro) para magnitudes y
    paleta divergente azul-rojo con gris en el centro para valores con signo.
"""
from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# --- superficies y tinta -----------------------------------------------------
SUPERFICIE = "#fcfcfb"
PLANO = "#f9f9f7"
TINTA = "#0b0b0b"
TINTA_2 = "#52514e"
TINTA_3 = "#898781"
REJILLA = "#e1e0d9"
EJE = "#c3c2b7"

# --- paleta categorica (orden fijo, nunca ciclado) ---------------------------
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
          "#e87ba4", "#008300", "#6250d6", "#e34948"]
AZUL, NARANJA, AQUA, AMARILLO = SERIES[0], SERIES[1], SERIES[2], SERIES[3]

# --- rampas ------------------------------------------------------------------
AZULES = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec",
          "#5598e7", "#3987e5", "#2a78d6", "#256abf", "#1c5cab",
          "#184f95", "#104281", "#0d366b"]
SECUENCIAL = LinearSegmentedColormap.from_list("azul_seq", AZULES)
DIVERGENTE = LinearSegmentedColormap.from_list(
    "azul_rojo", ["#0d366b", "#2a78d6", "#9ec5f4", "#f0efec",
                  "#f2a3a2", "#e34948", "#8f1f1e"])

FUENTES = ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"]


def aplicar_estilo() -> None:
    """Fija el estilo global de matplotlib/seaborn para todo el informe."""
    mpl.rcParams.update({
        "figure.facecolor": SUPERFICIE,
        "figure.dpi": 130,
        "savefig.dpi": 200,
        "savefig.facecolor": SUPERFICIE,
        "savefig.bbox": "tight",
        "axes.facecolor": SUPERFICIE,
        "axes.edgecolor": EJE,
        "axes.linewidth": 0.8,
        "axes.labelcolor": TINTA_2,
        "axes.labelsize": 10.5,
        "axes.titlesize": 12,
        "axes.titleweight": "semibold",
        "axes.titlecolor": TINTA,
        "axes.titlelocation": "left",
        "axes.titlepad": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": REJILLA,
        "grid.linewidth": 0.7,
        "grid.linestyle": "-",
        "xtick.color": TINTA_3,
        "ytick.color": TINTA_3,
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "xtick.labelcolor": TINTA_2,
        "ytick.labelcolor": TINTA_2,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "legend.frameon": False,
        "legend.fontsize": 9.5,
        "legend.labelcolor": TINTA_2,
        "lines.linewidth": 2.0,
        "lines.markersize": 5,
        "font.family": "sans-serif",
        "font.sans-serif": FUENTES,
        "text.color": TINTA,
        "axes.prop_cycle": mpl.cycler(color=SERIES),
        "figure.autolayout": False,
    })


def rotular(fig, titulo: str, subtitulo: str = "", nota: str = "",
            top: float = 0.93, bottom: float = 0.13) -> None:
    """Titulo, subtitulo (unidades/alcance) y lectura al pie, con margenes.

    El texto de la nota se ajusta al ancho de la figura para que nunca se salga
    del lienzo (bbox_inches='tight' incluye todo lo que quede fuera de los ejes).
    """
    import textwrap
    fig.subplots_adjust(top=top, bottom=bottom)
    fig.text(0.0, 1.10, titulo, ha="left", va="top",
             fontsize=14.5, fontweight="semibold", color=TINTA)
    if subtitulo:
        fig.text(0.0, 1.035, subtitulo, ha="left", va="top",
                 fontsize=10.5, color=TINTA_2)
    if nota:
        ancho = int(fig.get_figwidth() * 17.5)
        lineas = textwrap.wrap("Lectura: " + nota, ancho)
        alto = 0.042 * (6.0 / fig.get_figheight())
        for i, ln in enumerate(lineas):
            fig.text(0.0, -0.045 - i * alto, ln, ha="left", va="top",
                     fontsize=9.6, color=TINTA_2)


def guardar(fig, ruta) -> None:
    fig.savefig(ruta, dpi=200, bbox_inches="tight", facecolor=SUPERFICIE,
                pad_inches=0.35)


def miles(x, _=None) -> str:
    """Formateador de miles con punto (convencion colombiana)."""
    return f"{x:,.0f}".replace(",", ".")


def num(x, dec: int = 1) -> str:
    """Numero con coma decimal y punto de miles (convencion colombiana)."""
    s = f"{x:,.{dec}f}"
    return s.replace(",", "@").replace(".", ",").replace("@", ".")
