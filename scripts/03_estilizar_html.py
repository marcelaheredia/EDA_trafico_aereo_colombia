# -*- coding: utf-8 -*-
"""
Exporta el cuaderno a HTML y le aplica el sistema visual del informe: la misma
paleta, la misma tipografia y el mismo aire de las figuras, mas un indice
lateral. Solo cambia la presentacion; el contenido del cuaderno es el mismo.

Uso:
    python scripts/03_estilizar_html.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CUADERNO = BASE / "notebooks" / "analisis_exploratorio.ipynb"
SALIDA = BASE / "notebooks" / "analisis_exploratorio.html"


CSS = r"""
<style id="estilo-informe">
/* ===========================================================
   Sistema visual del informe · mismos tokens que estilo_viz.py
   =========================================================== */
:root, body[data-jp-theme-light="true"] {
  color-scheme: light;
  --superficie: #fcfcfb;
  --plano: #e9e7e1;
  --tinta: #0b0b0b;
  --tinta-2: #52514e;
  --tinta-3: #898781;
  --rejilla: #e1e0d9;
  --azul: #2a78d6;
  --azul-claro: #86b6ef;
  --azul-palido: #dbe8fa;
  --azul-tinte: #f2f7fe;
  --naranja: #eb6834;
  --aqua: #1baf7a;
  --codigo-fondo: #f6f6f2;
  --medida: 74ch;
  --sans: "Helvetica Neue", -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  --mono: ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas, monospace;

  --jp-content-font-family: var(--sans);
  --jp-code-font-family: var(--mono);
  --jp-content-font-color0: var(--tinta);
  --jp-content-font-color1: var(--tinta);
  --jp-layout-color0: var(--superficie);
  --jp-layout-color1: var(--superficie);
  --jp-cell-editor-background: var(--codigo-fondo);
  --jp-cell-editor-border-color: transparent;
  --jp-border-color1: var(--rejilla);
  --jp-content-link-color: var(--azul);
}

html { scroll-behavior: smooth; }
body.jp-Notebook {
  background: var(--plano);
  font-family: var(--sans);
  color: var(--tinta);
  font-size: 16.5px;
  line-height: 1.68;
  -webkit-font-smoothing: antialiased;
  margin: 0; padding: 0;
}

/* ---------- barra de progreso de lectura ---------- */
#progreso-pista {
  position: fixed; inset: 0 0 auto 0; height: 4px; z-index: 60;
  background: rgba(11,11,11,.08);
}
#progreso {
  height: 100%; width: 0;
  background: linear-gradient(90deg, var(--azul) 0%, var(--azul) 55%,
              var(--naranja) 80%, var(--aqua) 100%);
  transition: width .08s linear;
}

/* ---------- lienzo ---------- */
main {
  --aire: clamp(1.5rem, 4.2vw, 3.8rem);
  max-width: 1120px;
  margin: 2.6rem auto 3rem;
  padding: 0 var(--aire) 3.5rem;
  background: var(--superficie);
  border: 1px solid #ddd9d0;
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 1px 2px rgba(11,11,11,.04), 0 24px 60px -34px rgba(11,11,11,.3);
}

/* ---------- celdas ---------- */
.jp-InputPrompt, .jp-OutputPrompt, .jp-Collapser { display: none !important; }
.jp-Cell { padding: 0 !important; margin: 0 0 1.15rem !important; }
.jp-Cell-inputWrapper, .jp-Cell-outputWrapper { padding: 0 !important; }
.jp-InputArea, .jp-OutputArea { padding: 0 !important; }
.jp-InputArea { display: block !important; position: relative; }
.jp-InputArea-editor { display: block !important; width: 100% !important;
  border: none !important; border-radius: 14px !important; }
.jp-OutputArea-child, .jp-OutputArea-output { display: block !important; width: 100% !important; }
.anchor-link { display: none !important; }

/* ---------- tipografia y medida de lectura ---------- */
.jp-RenderedHTMLCommon { font-family: var(--sans); font-size: 16.5px; line-height: 1.68; color: var(--tinta); }
.jp-RenderedMarkdown > p,
.jp-RenderedMarkdown > ul,
.jp-RenderedMarkdown > ol,
.jp-RenderedMarkdown > h3,
.jp-RenderedMarkdown > h4,
.jp-RenderedMarkdown > blockquote { max-width: var(--medida); }
.jp-RenderedHTMLCommon p { margin: 0 0 1.05rem; }
.jp-RenderedHTMLCommon strong { font-weight: 650; }
.jp-RenderedHTMLCommon a { color: var(--azul); text-decoration: none;
  border-bottom: 1px solid rgba(42,120,214,.32); }
.jp-RenderedHTMLCommon a:hover { border-bottom-color: var(--azul); }
.jp-RenderedHTMLCommon code {
  font-family: var(--mono); font-size: .85em; background: #f0efe9;
  padding: .12em .4em; border-radius: 5px; color: #1c5cab;
}

.jp-RenderedHTMLCommon h1 {
  font-size: clamp(2.1rem, 4.6vw, 3.25rem); line-height: 1.06; font-weight: 700;
  letter-spacing: -0.028em; margin: 0 0 1.2rem;
}
.jp-RenderedHTMLCommon h2 {
  font-size: clamp(1.5rem, 2.6vw, 1.95rem); font-weight: 680; letter-spacing: -0.018em;
  line-height: 1.18; margin: 4rem 0 1.3rem; padding-top: 2.1rem;
  border-top: 1px solid var(--rejilla); scroll-margin-top: 1.5rem;
}
.jp-RenderedHTMLCommon h2 .num {
  display: block; font-size: 2.5rem; font-weight: 800; line-height: 1;
  color: var(--azul-palido); letter-spacing: -0.04em; margin-bottom: .35rem;
  font-variant-numeric: tabular-nums;
}
.jp-RenderedHTMLCommon h3 { font-size: 1.14rem; font-weight: 660; margin: 2.3rem 0 .7rem; }
.jp-RenderedHTMLCommon h4 { font-size: 1rem; font-weight: 650; margin: 1.5rem 0 .5rem; }
.jp-RenderedMarkdown > h3.pregunta {
  font-size: 1.42rem; font-weight: 700; letter-spacing: -0.015em; line-height: 1.26;
  margin: 3rem 0 1.2rem; max-width: 40ch;
}
.chip-pregunta {
  display: block; font-size: .7rem; font-weight: 700; letter-spacing: .16em;
  text-transform: uppercase; color: var(--azul); margin-bottom: .5rem;
}
.jp-RenderedHTMLCommon blockquote {
  margin: 1.5rem 0; padding: .95rem 1.25rem; border-left: 3px solid var(--azul);
  background: var(--azul-tinte); border-radius: 0 12px 12px 0; color: var(--tinta-2);
}
.jp-RenderedHTMLCommon ul, .jp-RenderedHTMLCommon ol { padding-left: 1.35rem; margin: 0 0 1.05rem; }
.jp-RenderedHTMLCommon li { margin: .38rem 0; }
.jp-RenderedMarkdown pre {
  background: var(--codigo-fondo); border: 1px solid #e7e6df; border-radius: 14px;
  padding: 16px 18px; font-family: var(--mono); font-size: 12.6px; line-height: 1.62;
  overflow-x: auto; margin: 1.2rem 0 1.5rem;
}
.jp-RenderedMarkdown pre code { background: none; padding: 0; color: inherit; font-size: inherit; }

/* ===========================================================
   Portada: la primera celda, clara y a sangre
   =========================================================== */
main > .jp-Cell:first-of-type .jp-RenderedMarkdown {
  position: relative;
  background:
    radial-gradient(125% 155% at 88% -25%, #d3e2f8 0%, rgba(211,226,248,0) 62%),
    radial-gradient(110% 130% at -8% 112%, #f6e8da 0%, rgba(246,232,218,0) 60%),
    linear-gradient(168deg, #f2f4f4 0%, var(--superficie) 72%);
  border-bottom: 1px solid #e3e1da;
  color: var(--tinta);
  margin: 0 calc(-1 * var(--aire)) 2.6rem;
  padding: clamp(2.6rem, 5vw, 4.2rem) var(--aire) clamp(2.2rem, 4vw, 3.2rem);
  max-width: none;
}
main > .jp-Cell:first-of-type .jp-RenderedMarkdown::before {
  content: ""; position: absolute; inset: 0 0 auto 0; height: 4px;
  background: linear-gradient(90deg, var(--azul) 0 46%, var(--naranja) 46% 78%, var(--aqua) 78% 100%);
}
main > .jp-Cell:first-of-type h1 { color: var(--tinta); max-width: 23ch; }
main > .jp-Cell:first-of-type p { color: var(--tinta-2); max-width: 78ch; }
main > .jp-Cell:first-of-type strong { color: var(--tinta); font-weight: 650; }
main > .jp-Cell:first-of-type code { background: rgba(255,255,255,.75); color: #1c5cab; }
main > .jp-Cell:first-of-type hr { display: none; }
main > .jp-Cell:first-of-type h3 {
  font-size: .74rem; text-transform: uppercase; letter-spacing: .16em; font-weight: 700;
  color: var(--azul); margin: 2.4rem 0 1.1rem; padding-top: 1.4rem;
  border-top: 1px solid #dedcd4; max-width: none;
}
main > .jp-Cell:first-of-type ol {
  counter-reset: hallazgo; list-style: none; padding: 0; max-width: none;
  display: grid; grid-template-columns: repeat(auto-fit, minmax(255px, 1fr)); gap: 1rem;
}
main > .jp-Cell:first-of-type ol > li {
  counter-increment: hallazgo; margin: 0; padding: 1.15rem 1.2rem 1.25rem;
  background: rgba(255,255,255,.72); border: 1px solid rgba(11,11,11,.07); border-radius: 14px;
  box-shadow: 0 1px 2px rgba(11,11,11,.03), 0 10px 26px -20px rgba(11,11,11,.22);
  backdrop-filter: blur(2px);
  font-size: .95rem; line-height: 1.55; color: var(--tinta-2);
}
main > .jp-Cell:first-of-type ol > li::before {
  content: counter(hallazgo); display: flex; align-items: center; justify-content: center;
  width: 1.75rem; height: 1.75rem; border-radius: 50%; margin-bottom: .7rem;
  background: var(--azul); color: #fff; font-size: .85rem; font-weight: 700;
}
main > .jp-Cell:first-of-type ol > li strong { color: var(--tinta); }
main > .jp-Cell:first-of-type > .jp-Cell-inputWrapper p:last-child {
  color: var(--tinta-3); font-size: .92rem;
}

/* ===========================================================
   Indice de contenido en la pagina
   =========================================================== */
#indice-pagina { margin: 0 0 3.2rem; }
#indice-pagina h2 {
  font-size: .74rem; text-transform: uppercase; letter-spacing: .16em; font-weight: 700;
  color: var(--tinta-3); margin: 0 0 .4rem; padding: 0; border: none;
}
#indice-pagina ol {
  list-style: none; margin: 0; padding: 0;
  display: grid; grid-template-columns: repeat(auto-fit, minmax(330px, 1fr));
  column-gap: 2.5rem;
}
#indice-pagina li { margin: 0; border-top: 1px solid var(--rejilla); }
#indice-pagina a {
  display: flex; gap: .9rem; align-items: baseline; padding: .62rem .2rem;
  color: var(--tinta); text-decoration: none; border: none; font-size: .96rem;
  transition: color .15s, padding .15s;
}
#indice-pagina a:hover { color: var(--azul); padding-left: .55rem; }
#indice-pagina .ip-num {
  font-size: .82rem; font-weight: 700; color: #5598e7;
  font-variant-numeric: tabular-nums; min-width: 1.6em;
}
#indice-pagina a:hover .ip-num { color: var(--azul); }

/* ===========================================================
   Llamados: justificaciones de diseño, problemas y hallazgos
   =========================================================== */
.nota-metodo, .nota-problema, .nota-hallazgo {
  max-width: var(--medida); border-radius: 0 14px 14px 0;
  padding: .95rem 1.25rem; margin: 1.3rem 0 1.5rem;
}
.nota-metodo   { background: #f1faf6; border-left: 3px solid var(--aqua); }
.nota-problema { background: #fdf4ef; border-left: 3px solid var(--naranja); }
.nota-hallazgo {
  background: var(--azul-tinte); border-left: 3px solid var(--azul);
  border-radius: 0 14px 14px 0;
}
.nota-hallazgo strong:first-child { color: #1c5cab; }

/* ---------- tablas ---------- */
.jp-RenderedHTMLCommon table, table.dataframe {
  border-collapse: collapse; width: 100%; margin: 1.4rem 0 1.8rem;
  font-size: .89rem; font-variant-numeric: tabular-nums; border: none;
}
.jp-RenderedHTMLCommon thead th, table.dataframe thead th {
  text-align: left; font-weight: 650; color: var(--tinta); background: transparent;
  border-bottom: 1.5px solid var(--tinta); padding: .55rem .75rem; font-size: .81rem;
  text-transform: uppercase; letter-spacing: .05em;
}
.jp-RenderedHTMLCommon tbody td, .jp-RenderedHTMLCommon tbody th,
table.dataframe tbody td, table.dataframe tbody th {
  border-top: 1px solid var(--rejilla); border-bottom: none;
  padding: .52rem .75rem; vertical-align: top; color: var(--tinta-2);
}
.jp-RenderedHTMLCommon tbody tr:hover, table.dataframe tbody tr:hover { background: #f4f8fd; }
table.dataframe tbody th { font-weight: 600; color: var(--tinta); }
table.dataframe tbody td { text-align: right; }
.jp-OutputArea-output:has(table.dataframe) { overflow-x: auto; }
table.dataframe { width: auto; min-width: 100%; font-size: .83rem; }
table.dataframe th, table.dataframe td { white-space: nowrap; }
table.dataframe thead th { text-transform: none; letter-spacing: 0; }

/* ---------- codigo ---------- */
.jp-CodeCell .highlight, .jp-CodeCell .jp-InputArea-editor {
  background: var(--codigo-fondo) !important;
  border: 1px solid #e7e6df !important; border-radius: 14px !important;
}
.jp-CodeCell .highlight pre, .jp-CodeCell pre {
  font-family: var(--mono) !important; font-size: 12.6px !important;
  line-height: 1.62 !important; padding: 16px 18px !important; margin: 0 !important;
  color: #26262a; overflow-x: auto;
}
.etiqueta-lenguaje {
  position: absolute; top: 9px; right: 14px; font-family: var(--mono); font-size: 10px;
  letter-spacing: .1em; text-transform: uppercase; color: var(--tinta-3); pointer-events: none;
}
.boton-copiar {
  position: absolute; top: 6px; right: 58px; border: 1px solid #e0dfd7; background: #fff;
  color: var(--tinta-2); font-family: var(--sans); font-size: 10.5px; letter-spacing: .06em;
  text-transform: uppercase; padding: .22rem .6rem; border-radius: 7px; cursor: pointer;
  opacity: 0; transition: opacity .15s;
}
.jp-CodeCell .jp-InputArea:hover .boton-copiar { opacity: 1; }
.boton-copiar:hover { border-color: var(--azul); color: var(--azul); }

/* coloreado de sintaxis con la paleta del informe */
.highlight .k, .highlight .kn, .highlight .kc, .highlight .ow { color: #6250d6; font-weight: 600; }
.highlight .nb, .highlight .nf { color: var(--azul); }
.highlight .s, .highlight .s1, .highlight .s2, .highlight .sa, .highlight .se { color: #15785a; }
.highlight .mi, .highlight .mf, .highlight .m { color: #b24a16; }
.highlight .c, .highlight .c1, .highlight .cm { color: var(--tinta-3); font-style: italic; }
.highlight .o, .highlight .p { color: #5a5955; }
.highlight .nn, .highlight .nc { color: var(--tinta); }

/* ---------- salidas de texto ---------- */
.jp-OutputArea-output pre {
  font-family: var(--mono) !important; font-size: 12.3px !important;
  line-height: 1.6 !important; color: var(--tinta-2) !important;
  background: transparent !important; border: none !important;
  border-left: 2px solid var(--rejilla) !important;
  padding: .4rem 0 .4rem 1.05rem !important; margin: .55rem 0 1.3rem !important;
  overflow-x: auto;
}
.jp-OutputArea-output { background: transparent !important; }

/* ---------- figuras ---------- */
.jp-OutputArea-output img, .jp-RenderedImage img {
  display: block; margin: 1.8rem auto 2.4rem; max-width: 100%; height: auto;
  border-radius: 8px; cursor: zoom-in; transition: transform .18s ease, filter .18s ease;
}
.jp-OutputArea-output img:hover { transform: scale(1.006); filter: saturate(1.03); }
#visor {
  position: fixed; inset: 0; z-index: 90; display: none;
  background: rgba(11,11,11,.93); cursor: zoom-out;
  align-items: center; justify-content: center; padding: 2.5vmin;
}
#visor.abierto { display: flex; }
#visor img { max-width: 96vw; max-height: 92vh; border-radius: 6px; background: #fcfcfb; }
#visor::after {
  content: "clic o Esc para cerrar"; position: absolute; bottom: 1.4rem; left: 50%;
  transform: translateX(-50%); color: #8d8b84; font-size: 12px; letter-spacing: .06em;
}

/* ---------- indice lateral ---------- */
#indice {
  position: fixed; top: 50%; transform: translateY(-50%);
  left: max(1rem, calc(50vw - 790px)); width: 196px;
  font-size: 12.2px; line-height: 1.38; z-index: 40; display: none;
}
#indice::before {
  content: "Contenido"; display: block; font-size: 10px; letter-spacing: .16em;
  text-transform: uppercase; color: var(--tinta-3); font-weight: 700; margin: 0 0 .7rem .8rem;
}
#indice ol { list-style: none; margin: 0; padding: 0; }
#indice li { margin: .3rem 0; }
#indice a {
  color: #8f8d86; text-decoration: none; display: block; padding: .18rem 0 .18rem .8rem;
  border-left: 2px solid #d6d4cc; transition: color .15s, border-color .15s, padding .15s;
}
#indice a:hover { color: var(--tinta); border-left-color: #a9a79f; }
#indice .toc-num {
  display: inline-block; width: 1.5em; color: #bcbab2; font-variant-numeric: tabular-nums;
  font-weight: 600;
}
#indice a.activo .toc-num { color: var(--azul); }
#indice a.activo {
  color: var(--azul); border-left-color: var(--azul); font-weight: 600; padding-left: 1rem;
}
@media (min-width: 1520px) { #indice { display: block; } }

/* ---------- pie ---------- */
#pie-informe {
  max-width: 1120px; margin: 0 auto 4rem; padding: 0 clamp(1.5rem, 4.2vw, 3.8rem);
  color: var(--tinta-3); font-size: 12.6px; line-height: 1.6;
  display: flex; justify-content: space-between; gap: 1.5rem; flex-wrap: wrap;
}
#pie-informe a { color: var(--tinta-3); }

@media print {
  body.jp-Notebook { background: #fff; }
  main { box-shadow: none; border: none; max-width: none; margin: 0; border-radius: 0; }
  #indice, #progreso-pista, .boton-copiar { display: none !important; }
  .jp-Cell { break-inside: avoid; }
  main > .jp-Cell:first-of-type .jp-RenderedMarkdown { background: #0b0b0b !important;
    -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
</style>
"""

JS = r"""
<script>
(function () {
  /* ---------- barra de progreso ---------- */
  const pista = document.createElement('div'); pista.id = 'progreso-pista';
  const barra = document.createElement('div'); barra.id = 'progreso';
  pista.appendChild(barra); document.body.appendChild(pista);
  const avance = function () {
    const alto = document.documentElement.scrollHeight - window.innerHeight;
    barra.style.width = (alto > 0 ? (window.scrollY / alto) * 100 : 0) + '%';
  };
  window.addEventListener('scroll', avance, { passive: true });
  window.addEventListener('resize', avance); avance();

  /* ---------- numeral grande en cada seccion ---------- */
  const titulos = Array.from(document.querySelectorAll('main h2'));
  titulos.forEach(function (h) {
    const ancla = h.querySelector('.anchor-link');
    const crudo = h.textContent.replace('¶', '').trim();
    const m = crudo.match(/^(\d+)\.\s+(.*)$/);
    if (!m) return;
    h.textContent = '';
    const num = document.createElement('span');
    num.className = 'num';
    num.textContent = m[1].padStart(2, '0');
    h.appendChild(num);
    h.appendChild(document.createTextNode(m[2]));
    if (ancla) h.appendChild(ancla);
    h.dataset.numero = m[1].padStart(2, '0');
    h.dataset.titulo = m[2];
  });

  /* ---------- llamados ---------- */
  const inicios = [
    [/^Por qu[eé]/i, 'nota-metodo'],
    [/^(Primer|Segundo|Tercer|Cuarto|Quinto) problema/i, 'nota-problema'],
    [/^Hallazgo \d/i, 'nota-hallazgo'],
    [/^Qu[ée] se hace con los at[ií]picos/i, 'nota-metodo'],
    [/^No son errores/i, 'nota-metodo']
  ];
  document.querySelectorAll('main .jp-RenderedMarkdown > p').forEach(function (p) {
    const fuerte = p.querySelector('strong');
    if (!fuerte || p.firstElementChild !== fuerte) return;
    const texto = fuerte.textContent.trim();
    for (const par of inicios) {
      if (par[0].test(texto)) { p.classList.add(par[1]); break; }
    }
  });

  /* ---------- encabezados de pregunta ---------- */
  document.querySelectorAll('main .jp-RenderedMarkdown > h3').forEach(function (h) {
    const ancla = h.querySelector('.anchor-link');
    const crudo = h.textContent.replace('¶', '').trim();
    const m = crudo.match(/^(Pregunta\s+\d+)\s*·\s*(.*)$/);
    if (!m) return;
    h.classList.add('pregunta');
    h.textContent = '';
    const chip = document.createElement('span');
    chip.className = 'chip-pregunta';
    chip.textContent = m[1];
    h.appendChild(chip);
    h.appendChild(document.createTextNode(m[2]));
    if (ancla) h.appendChild(ancla);
  });

  /* ---------- indice de contenido en la pagina ---------- */
  if (titulos.length) {
    const portada = document.querySelector('main > .jp-Cell:first-of-type');
    const bloque = document.createElement('nav');
    bloque.id = 'indice-pagina';
    bloque.innerHTML = '<h2>Contenido</h2><ol>' + titulos.map(function (h) {
      const titulo = h.dataset.titulo || h.textContent.replace('\u00b6', '').trim();
      const numero = h.dataset.numero || '';
      return '<li><a href="#' + h.id + '">' +
             '<span class="ip-num">' + numero + '</span>' +
             '<span>' + titulo + '</span></a></li>';
    }).join('') + '</ol>';
    if (portada && portada.parentNode) portada.parentNode.insertBefore(bloque, portada.nextSibling);
  }

  /* ---------- indice lateral ---------- */
  if (titulos.length) {
    const nav = document.createElement('nav');
    nav.id = 'indice';
    nav.innerHTML = '<ol>' + titulos.map(function (h) {
      const titulo = h.dataset.titulo || h.textContent.replace('¶', '').trim();
      const numero = h.dataset.numero
        ? '<span class="toc-num">' + h.dataset.numero + '</span>' : '';
      return '<li><a href="#' + h.id + '">' + numero + titulo + '</a></li>';
    }).join('') + '</ol>';
    document.body.appendChild(nav);
    const enlaces = Array.from(nav.querySelectorAll('a'));
    const observador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (!e.isIntersecting) return;
        enlaces.forEach(function (a) { a.classList.remove('activo'); });
        const activo = enlaces.find(function (a) {
          return a.getAttribute('href') === '#' + e.target.id;
        });
        if (activo) activo.classList.add('activo');
      });
    }, { rootMargin: '-8% 0px -72% 0px' });
    titulos.forEach(function (h) { observador.observe(h); });
  }

  /* ---------- figuras ampliables ---------- */
  const visor = document.createElement('div');
  visor.id = 'visor';
  visor.innerHTML = '<img alt="">';
  document.body.appendChild(visor);
  const grande = visor.querySelector('img');
  document.querySelectorAll('.jp-OutputArea-output img').forEach(function (img) {
    img.addEventListener('click', function () {
      grande.src = img.src;
      visor.classList.add('abierto');
      document.body.style.overflow = 'hidden';
    });
  });
  const cerrar = function () {
    visor.classList.remove('abierto');
    document.body.style.overflow = '';
  };
  visor.addEventListener('click', cerrar);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') cerrar(); });

  /* ---------- etiqueta y boton de copiar en el codigo ---------- */
  document.querySelectorAll('.jp-CodeCell .jp-InputArea').forEach(function (area) {
    const pre = area.querySelector('pre');
    if (!pre) return;
    const etiqueta = document.createElement('span');
    etiqueta.className = 'etiqueta-lenguaje';
    etiqueta.textContent = 'python';
    area.appendChild(etiqueta);

    const boton = document.createElement('button');
    boton.className = 'boton-copiar';
    boton.type = 'button';
    boton.textContent = 'copiar';
    boton.addEventListener('click', function () {
      const texto = pre.innerText;
      const listo = function () {
        boton.textContent = 'copiado';
        setTimeout(function () { boton.textContent = 'copiar'; }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(texto).then(listo, function () {});
      } else {
        const t = document.createElement('textarea');
        t.value = texto; document.body.appendChild(t); t.select();
        try { document.execCommand('copy'); listo(); } catch (err) {}
        document.body.removeChild(t);
      }
    });
    area.appendChild(boton);
  });
})();
</script>
"""

PIE = """
<footer id="pie-informe">
  <span>Marcela Heredia · análisis exploratorio de datos · noviembre de 2026</span>
  <span>Datos: Aeronáutica Civil de Colombia vía
    <a href="https://www.datos.gov.co/d/gb6w-ynu4">datos.gov.co</a> · licencia CC BY-SA 4.0</span>
</footer>
"""


def exportar() -> str:
    print("Exportando el cuaderno a HTML ...")
    subprocess.run(
        [sys.executable, "-m", "nbconvert", "--to", "html", "--template", "lab",
         "--embed-images", str(CUADERNO), "--output", SALIDA.name],
        cwd=str(CUADERNO.parent), check=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    return SALIDA.read_text(encoding="utf-8")


def estilizar(html: str) -> str:
    if 'id="estilo-informe"' in html:
        html = re.sub(r'<style id="estilo-informe">.*?</style>', "", html, flags=re.S)
    html = html.replace("</head>", CSS + "\n</head>", 1)
    html = html.replace("</body>", PIE + JS + "\n</body>", 1)
    return html


if __name__ == "__main__":
    SALIDA.write_text(estilizar(exportar()), encoding="utf-8")
    print(f"Listo: {SALIDA} ({SALIDA.stat().st_size/1e6:.1f} MB)")
