#!/usr/bin/env python3
"""Freeze the 13 October 2026 TC24 results into report CSVs.

Reads finished job roots under the controller's storage (registered in iter_tc24
results/run_registry.json) and writes data/tc24_20261013/*.csv plus a source manifest
with the SHA256 of every file read. Values that exist only as registry or PLAN text
are copied with that owner as their source. Pending jobs are written as rows with
status 'pending' and empty values; the figures skip them and the report marks them.
"""
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "data" / "tc24_20261013"
R = Path("/mnt/storage/codex-equilibrium-20261011")
R10 = Path("/mnt/storage/codex-equilibrium-20261010")
TC24_REV = "eb6848388"  # iter_tc24 registry/PLAN revision read for text-owned values
SOURCES = {}


def load(path):
    path = Path(path)
    raw = path.read_bytes()
    SOURCES[str(path)] = hashlib.sha256(raw).hexdigest()
    return json.loads(raw) if path.suffix == ".json" else raw.decode()


def rows_csv(path):
    return list(csv.DictReader(load(path).splitlines()))


def write(name, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with (OUT / name).open("w") as f:
        w = csv.DictWriter(f, fieldnames=keys, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def ns640():
    """Five-plus-one-code TC24 cell against public CHEASE NS640 (1200 points, 80 labels)."""
    out = []
    mars = R / "finish/mars_native/jobs/tc24_mars_native_ns640_20261012_01"
    pub = load(mars / "inputs/public_ladder_vs_ns640.json")
    walls = {16: 5.5307, 32: 9.7341, 64: 36.4375, 128: 190.9365, 256: 475.6875}  # comparison_historical.csv
    for ns in [16, 32, 64, 128, 256]:
        m = pub[str(ns)]
        out.append(dict(code="chease_public", label=f"NS{ns}", resolution=ns, wall_s=walls[ns], threads=1,
                        native_stop=True, bpol_l2=m["bpol_l2"], q_max=m["q_max"], psi_l2=m["psi_l2"],
                        status="final", run_tag=Path(m["run"]).name,
                        source=str(mars / "inputs/public_ladder_vs_ns640.json")))
    k6 = R / "finish/kin_refine_luna/tc24k6_modx03_seed384_global_edge_midpoints_q5_k3direct_20261012_01"
    j = load(k6 / "analysis/ns512_ns640_k6_vs_640.json")
    s = j["context_pairs"]["step_512_640"]
    out.append(dict(code="chease_public", label="NS512", resolution=512, wall_s=13212, threads="",
                    native_stop=True, bpol_l2=s["bpol_l2"], q_max=s["q_max"], psi_l2=s["psi_l2"],
                    status="final", run_tag="tc24_public_ref_n512_20261011_01",
                    source=str(k6 / "analysis/ns512_ns640_k6_vs_640.json")))
    for ns in [64, 96, 128, 140]:
        m = load(mars / f"runs/ns{ns}/result.json")
        out.append(dict(code="chease_mars", label=f"NS{ns}", resolution=ns, wall_s=m["chease_wall_s"],
                        threads=1, native_stop=True, bpol_l2=m["bpol_l2"], q_max=m["q_max"],
                        psi_l2=m["psi_l2"], status="final",
                        run_tag="tc24_mars_native_ns640_20261012_01",
                        source=str(mars / f"runs/ns{ns}/result.json")))
    p = j["pairs_kin_vs_640"]
    out.append(dict(code="kin6d", label="K6", resolution=1549828, wall_s=98.4662, threads=48,
                    native_stop=True, bpol_l2=p["bpol_l2"], q_max=p["q_max"], psi_l2=p["psi_l2"],
                    status="final", run_tag=k6.name, source=str(k6 / "analysis/ns512_ns640_k6_vs_640.json")))
    out.append(dict(code="kin6d", label="K5", resolution=412903, wall_s=2262.75, threads=1,
                    native_stop=True, bpol_l2=5.67e-6, q_max="", psi_l2="", status="final",
                    run_tag="tc24k5_modx03_seed384_bands_q5_20261011_01",
                    source=f"iter_tc24 {TC24_REV} PLAN.md (K5 vs NS640); wall from raw-root run.log"))
    for root in ["vmecpp_tc24_ns640prof_cond_20261012_01", "vmecpp_tc24_ns640prof_cond_nsladder_20261012_01"]:
        f = R / "finish/vmec_cond" / root / "classification.csv"
        for r in rows_csv(f):
            if r["tag"].endswith("ns2049"):
                continue  # EQ-TC24-17: duplicates ns1025, never ran
            out.append(dict(code="vmecpp", label=f"ns{r['ns_final']} m{r['mpol']}", resolution=int(r["ns_final"]),
                            wall_s=float(r["wall_s"]), threads=r["max_threads"],
                            native_stop=r["converged"] == "True", bpol_l2=r["bpol_l2"], q_max=r["q_max"],
                            psi_l2=r["psi_l2"], status="final", run_tag=root, source=str(f)))
    f = R / "finish/desc_cond/desc_tc24_condradial_ladder_20261012_02/classification.csv"
    for r in rows_csv(f):
        if not r["bpol_l2"]:
            continue
        folded = float(r["jacobian_min"] or 0) < 0
        control = "_mod_" in r["tag"]  # old modx03-profile deck: a profile control, not the cell
        out.append(dict(code="desc", label=r["tag"].replace("s0995_cond4_", ""), resolution=int(r["L"]),
                        wall_s=float(r["wall_s"]), threads=r["threads"],
                        native_stop=r["converged"] == "True" and not folded, bpol_l2=r["bpol_l2"],
                        q_max=r["q_max"], psi_l2=r["psi_l2"],
                        status="control" if control else "final" + (" folded" if folded else ""),
                        run_tag=f.parent.name, source=str(f)))
    for L, b, stop in [(32, 3.2e-3, True), (40, 2.0e-3, False), (48, 1.25e-3, False)]:
        out.append(dict(code="desc", label=f"warm L{L}", resolution=L, wall_s="", threads=8,
                        native_stop=stop, bpol_l2=b, q_max="", psi_l2="", status="final",
                        run_tag="desc_tc24_reprhyp_20261012_03",
                        source=f"iter_tc24 {TC24_REV} run_registry.json admission text"))
    out.append(dict(code="gvec", label="ladder", resolution="", wall_s="", threads="", native_stop="",
                    bpol_l2="", q_max="", psi_l2="", status="pending",
                    run_tag="gvec_tc24_fixed_ladder_20261012_01", source="running (Slurm 3217025)"))
    write("tc24_ns640.csv", out)


def edge_scan():
    """GPEC n=3 |singflx| (T) versus edge treatment, both phasings."""
    cases = [("0.990", R / "gpec_edge_scan/gpec_edgescan_n3_bl2_20261013_01/cases/c0990_phi{p}"),
             ("0.995", R / "mephit_gpec_cut0995/gpec_cut0995_n3_bl2_20261012_01/cases/phi{p}"),
             ("0.997", R / "mephit_gpec_cut0997/gpec_cut0997_n3_bl2_20261012_02/cases/phi{p}"),
             ("0.999", R / "gpec_edge_scan/gpec_edgescan_n3_bl2_20261013_01/cases/c0999_phi{p}")]
    cases += [(f"full{v}", R / f"gpec_edge_scan/gpec_edgescan_n3_bl2_20261013_01/cases/full{v}_phi{{p}}")
              for v in "ADEF"]
    out = []
    for cut, pattern in cases:
        for p in ["000", "010"]:
            f = Path(str(pattern).format(p=p)) / "summary.json"
            for s in load(f)["singfld"]:
                if s["q"] >= 2.99:
                    out.append(dict(cut=cut, phasing=p, q=s["q"], psi=s["psi"],
                                    singflx_T=abs(complex(*s["singflx"])), source=str(f)))
    write("gpec_edge_scan.csv", out)


def marsf_gpec():
    """MARS-F ideal total resonant b_Boozer against GPEC bno at identical cuts and bl2 coils."""
    f = R / "marsf_cuts/marsf_n3_bl2_cuts_20261013_01/comparison.json"
    out = []
    for key, v in load(f)["comparison"].items():
        cut, ph, q = key.split("_")
        if cut == "xin":
            continue
        g = v["gpec"]
        bno = abs(complex(*g["bno_boozer_T"])) if isinstance(g["bno_boozer_T"], list) else abs(g["bno_boozer_T"])
        out.append(dict(cut=cut, phasing=ph.replace("phi", ""), q=q[1:], marsf_b_boozer_T=v["ideal"]["b_boozer"],
                        gpec_bno_T=bno, ratio=v["ideal"]["b_boozer"] / bno,
                        ideal_limit_rel=v["ideal_limit_rel"]["b_boozer"],
                        gpec_singflx_T=abs(complex(*g["singflx_T"])) if isinstance(g["singflx_T"], list)
                        else abs(g["singflx_T"]),
                        marsf_singflx_cyl_T=v["ideal"]["singflx_cyl_estimate_T"], source=str(f)))
    write("marsf_gpec.csv", out)


def gvec3d():
    """GVEC fixed-boundary 3D (0.995, ntor 1, 1 % of 90 kAt) versus fixed-boundary GPEC."""
    f = R / "gvec3d/gvec3d_fx_rmp_cut0995_ntor1_20261013_01/analysis.json"
    d = load(f)["gpec"]
    out = []
    for ph in ["phi000", "phi010"]:
        far = d[f"{ph}:fixed"]["series"]["mpol33_ntor1_ne32"]["far_summary"]
        for qty in ["xi_n", "bn_E"]:
            for psin, s in far[qty]["per_surface"].items():
                out.append(dict(phasing=ph[3:], quantity=qty, psiN=float(psin), rel_diff=s["rel_diff"],
                                abs_ratio=s["median_abs_ratio_dominant"],
                                phase_deg=s["median_phase_deg_dominant"], source=str(f)))
    write("gvec3d_gpec.csv", out)


def stability():
    """DCON least-stable n=3/n=6 eigenvalue without wall; values owned by PLAN.md."""
    src = f"iter_tc24 {TC24_REV} PLAN.md edge-cut decision"
    rows = [("hard 0.990", -0.047, ""), ("hard 0.995", -0.105, ""), ("hard 0.997", -0.097, ""),
            ("hard 0.999", -0.009, ""), ("full LCFS", 0.059, 0.006),
            ("FB-taper 0.997 w0.0228 (FreeGS)", 0.206, 0.103),
            ("FB-taper 0.997 w0.0228 (KIN6D)", 0.205, 0.102),
            ("FB-taper 0.995 w0.0276 (KIN6D)", 0.253, 0.124)]
    write("dcon_stability.csv", [dict(equilibrium=e, n3=a, n6=b, source=src) for e, a, b in rows])


def main():
    ns640(); edge_scan(); marsf_gpec(); gvec3d(); stability()
    (OUT / "sources.json").write_text(json.dumps(dict(
        description="Raw-root inputs of the 13 October 2026 TC24 revision", iter_tc24_revision=TC24_REV,
        files=SOURCES), indent=1) + "\n")
    print(f"{len(SOURCES)} source files frozen into {OUT.relative_to(HERE)}")


if __name__ == "__main__":
    main()
