"""Write the verification tables of radiation_collision.tex from
numeric_results.json. Usage: python3 make_tables.py RESULTS.json OUTPUT_DIR"""
import json
import os
import re
import sys

results = json.load(open(sys.argv[1]))
out = sys.argv[2]


LABELS = (
    ("harmonic sums", r"harmonic sums, Eq.~\eqref{eq:sums}"),
    ("closed tensor", r"closed tensor \eqref{eq:Dclosed} vs.\ quadrature of \eqref{eq:Dsum}"),
    ("M_j, T_j", r"$M_j$, $T_j$ as hypergeometric functions"),
    ("absorption series", r"absorption series, Eq.~\eqref{eq:Fseries}"),
    ("absorption normalisation", r"$S_M$, Eq.~\eqref{eq:SM}, vs.\ resonance-line integral"),
    ("axis limit", r"axis limit \eqref{eq:axis} at $\eta=1-10^{-8}$"),
    ("Bessel moments", r"$\langle u^2\rangle_0$, $\langle\arsinh u/(\gamma u)\rangle_0$"),
    ("thermal tail", r"thermal tail $T_W$"),
    ("G_E", r"$G_E$, $G_P$ vs.\ quadrature"),
    ("G_P/G_E limits", r"$G_P/G_E\to2/5$, $1/5$ at $\mu=10^{\pm4}$"),
    ("scalar sources", r"$b_\alpha=\int\dd^3p\,\delta f\,\sH_\alpha$ (by parts)"),
    ("harmonic tail bound", r"tail $\le$ bound \eqref{eq:tail}: largest ratio"),
    ("broadened cusp", r"broadened cusp, Sec.~\ref{sec:modified}"),
    ("drag characteristics", r"drag trajectory vs.\ ODE integration"),
    ("drag propagator (11.8): particle", r"propagator: particle number"),
    ("drag propagator (11.8): dE", r"propagator: $\dd E/\dd t=-\nu_R\langle w^2\rangle$"),
)


def tex(name):
    for key, label in LABELS:
        if name.startswith(key):
            return label
    raise KeyError(name)


def sci(x):
    if x == 0:
        return r"$<10^{-30}$"
    m, e = f"{x:.1e}".split("e")
    return rf"${m}\times10^{{{int(e)}}}$"


rows = []
for name, v in results.items():
    if isinstance(v, dict):
        status = "" if v["pass"] else " (FAIL)"
        value = sci(v['max_relative_error'])
        if name.startswith("harmonic tail bound"):
            value = f"${results['tail bound ratio (must be <= 1)']:.2f}$"
        rows.append(f"{tex(name)} & {value}{status}\\\\")
open(os.path.join(out, "numeric_table.tex"), "w").write(
    "\\begin{tabular}{lr}\n\\toprule\nCheck & Result\\\\\n\\midrule\n"
    + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n")

g = [f"{mu:g} & {ge} & {gp} & {r}\\\\" for mu, ge, gp, r in results["G_table_ne_nu0_1"]]
open(os.path.join(out, "g_table.tex"), "w").write(
    "\\begin{tabular}{rrrr}\n\\toprule\n$\\mu$ & $G_E$ & $G_P$ & $G_P/G_E$\\\\\n\\midrule\n"
    + "\n".join(g) + "\n\\bottomrule\n\\end{tabular}\n")
