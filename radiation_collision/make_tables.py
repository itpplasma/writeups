"""Write the verification tables of radiation_collision.tex from
numeric_results.json. Usage: python3 make_tables.py RESULTS.json OUTPUT_DIR"""
import json
import os
import re
import sys

results = json.load(open(sys.argv[1]))
out = sys.argv[2]


def tex(name):
    name = name.replace("_", r"\_").replace("<=", r"$\le$").replace("^2", "$^2$")
    name = name.replace("nu\\_R", r"$\nu_R$").replace("<w$^2$>", r"$\langle w^2\rangle$")
    name = name.replace("dE/dt", r"$\mathrm dE/\mathrm dt$")
    return re.sub(r"\((\d+\.\d+)\)", r"(\1)", name)


def sci(x):
    if x == 0:
        return r"$<10^{-30}$"
    m, e = f"{x:.1e}".split("e")
    return rf"${m}\times10^{{{int(e)}}}$"


rows = []
for name, v in results.items():
    if isinstance(v, dict):
        status = "" if v["pass"] else " (FAIL)"
        rows.append(f"{tex(name)} & {sci(v['max_relative_error'])}{status}\\\\")
open(os.path.join(out, "numeric_table.tex"), "w").write("\n".join(rows) + "\n")

g = [f"{mu:g} & {ge} & {gp} & {r}\\\\" for mu, ge, gp, r in results["G_table_ne_nu0_1"]]
open(os.path.join(out, "g_table.tex"), "w").write("\n".join(g) + "\n")
