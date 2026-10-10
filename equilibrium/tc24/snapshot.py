#!/usr/bin/env python3
"""Copy committed report inputs; never consume a dirty working-tree result."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
TC24 = "d37ae2cc4"
KIN6D = "3c851d7"
REFRESH = "014ff0caee2bea5a130400c4111aab4104ac7e73"
REFRESH_PATHS = {
    'equilibrium/phase3/results/kin6d_consumers_gpec.csv',
    'equilibrium/phase3/results/kin6d_consumers_hamada.csv',
    'equilibrium/phase3/results/kin6d_consumers_neo2.csv',
    'equilibrium/phase3/results/kin6d_consumers_neo2_controls.csv',
    'equilibrium/phase3/results/kin6d_effectivity_native_circular.csv',
    'equilibrium/phase3/results/kin6d_effectivity_native_solovev.csv',
    'equilibrium/phase3/results/README.md',
    'equilibrium/phase3/results/kin6d.md',
    'equilibrium/phase5/results/README.md',
}


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tc24", type=Path, required=True)
    parser.add_argument("--kin6d", type=Path, required=True)
    args = parser.parse_args()
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    sources = []

    def read(repo, rev, path, destination=None):
        if repo == args.tc24 and path in REFRESH_PATHS:
            rev = REFRESH
        full = git(repo, "rev-parse", rev).decode().strip()
        raw = git(repo, "show", f"{full}:{path}")
        if raw.startswith(b"version https://git-lfs.github.com/spec/"):
            raise ValueError(f"Unmaterialized LFS input: {path}")
        source = {"repository": "iter_tc24" if repo == args.tc24 else "kin6d", "commit": full, "path": path,
                  "sha256": hashlib.sha256(raw).hexdigest(),
                  "git_blob": git(repo, "rev-parse", f"{full}:{path}").decode().strip()}
        if destination:
            target = out / destination
            target.parent.mkdir(parents=True, exist_ok=True)
            snapshot = raw.rstrip() + b"\n" if destination.startswith('context/') else raw
            target.write_bytes(snapshot)
            source["snapshot"] = destination
            if snapshot != raw:
                source['snapshot_sha256'] = hashlib.sha256(snapshot).hexdigest()
                source['snapshot_transform'] = 'remove trailing blank lines from context text only'
            if target.suffix == ".csv":
                source["rows"] = len(list(csv.DictReader(io.StringIO(raw.decode()))))
        sources.append(source)
        return raw

    for name in ["PLAN.md", "equilibrium/CASE_CONTRACT.md", "equilibrium/ERRATA.md",
                 "review/UPSTREAM_PRS.md", "equilibrium/phase1/README.md",
                 "equilibrium/phase1/results/README.md",
                 "equilibrium/phase1/results_export/README.md",
                 "equilibrium/phase2/results/README.md",
                 "equilibrium/phase4/results/README.md",
                 "equilibrium/phase4/tc24/README.md",
                 "equilibrium/phase4/tc24/EQUILIBRIUM_PROVENANCE.md",
                 "equilibrium/phase4/tc24/EXPORTS.md",
                 "equilibrium/phase4/tc24/kin6d_performance/README.md",
                 "equilibrium/phase3/results/README.md",
                 "equilibrium/phase3/results/kin6d.md",
                 "equilibrium/phase5/results/README.md"]:
        read(args.tc24, TC24, name, "context/" + name.replace("/", "__"))

    files = ["phase1/results/solovev_lcfs_A3.csv", "phase1/results/solovev_cerfon_iter.csv",
             "phase1/results_export/summary.csv"]
    for phase, cases in [("phase2", [f"{law}_A{a}" for law in ["E1", "E2"]
                                    for a in ["40", "20", "10", "3p1"]]),
                         ("phase4", ["E4_E1", "E4_E2"])]:
        files += [f"{phase}/results/{c}.csv" for c in cases]
        files += [f"{phase}/results/{f}.csv" for f in
                  ["best_cost", "finest", "qualified", "rates", "reference_errors",
                   "exports", "boozer", "boozer_volume"]]
    files += ["phase2/results/physics.csv", "phase4/results/cost_by_bpol.csv",
              "phase4/tc24/source_consistency.csv", "phase4/tc24/capability.csv"]
    files += [f"phase5/results/{f}.csv" for f in
              ["runs", "finest", "aspect_rates", "resolution", "signs", "failures"]]
    files += [f"phase3/results/{f}.csv" for f in
              ["comparison", "finest", "self_convergence", "exports", "consumers",
               "boozer", "boozer_m48", "failures", "kin6d_comparison",
               "kin6d_finest", "kin6d_self_convergence", "kin6d_exports",
               "kin6d_consumers_gpec", "kin6d_consumers_hamada", "kin6d_consumers_neo2",
               "kin6d_consumers_neo2_controls", "kin6d_effectivity_native_circular",
               "kin6d_effectivity_native_solovev"]]
    files += [f"phase4/tc24/reference/{f}.csv" for f in
              ["comparison", "convergence", "runs", "replay", "variants", "exports", "consumers", "execution"]]
    files += ["phase4/tc24/reference/reference_case.json",
              "phase4/tc24/kin6d_performance/timings.csv",
              "phase4/tc24/kin6d_performance/convergence-fine.csv"]
    for path in files:
        read(args.tc24, TC24, "equilibrium/" + path, path)
    read(args.kin6d, KIN6D, "benchmarks/gs-phase1/p2-p3.csv", "kin6d/p2-p3.csv")
    read(args.kin6d, KIN6D, "benchmarks/gs-phase1/README.md", "context/kin6d-p2-p3.md")

    # Keep scalar input definitions as rows; boundary arrays remain at their owner.
    parameters = []
    def flatten(obj, prefix, path, case):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key not in {"R", "Z", "terms", "coefficients"}:
                    flatten(value, f"{prefix}.{key}".strip("."), path, case)
        elif not isinstance(obj, list):
            parameters.append({"source": path, "case": case, "key": prefix, "value": obj})
    for phase in ["phase1", "phase2", "phase3", "phase4", "phase5"]:
        path = f"equilibrium/{phase}/cases.json"
        obj = json.loads(read(args.tc24, TC24, path))
        if phase == "phase5":
            flatten(obj, "", path, "C0")
            for a in obj["aspects"]:
                parameters.append({"source": path, "case": "C0", "key": "aspect", "value": a})
        else:
            for case, values in obj.items():
                flatten(values, "", path, case)
    path = "equilibrium/phase4/tc24/reference/reference_case.json"
    flatten(json.loads(git(args.tc24, "show", f"{TC24}:{path}")), "", path, "E5_modx03")
    with (out / "parameters.csv").open("w") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "case", "key", "value"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(parameters)
    support = []
    for revision in ["99fa2c8", "82d4d1f", "fa5c388", "451fa5b", "a50f8b6", "2d8142a", "5dfb9df", "313cde5", "60bef4c", "fde93a9", "f1d1791"]:
        support.append({"commit": git(args.kin6d, "rev-parse", revision).decode().strip(),
                        "subject": git(args.kin6d, "show", "-s", "--format=%s", revision).decode().strip()})
    manifest = {"description": "Committed inputs for the consolidated Phase 6 report; executed pins remain historical.",
                "tc24_commit": git(args.tc24, "rev-parse", TC24).decode().strip(),
                "kin6d_current_main": git(args.kin6d, "rev-parse", "f1d1791").decode().strip(), "kin6d_data_commit": git(args.kin6d, "rev-parse", KIN6D).decode().strip(),
                "kin6d_support_history": support, "sources": sources}
    (HERE / "sources.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Copied {len(sources)} committed sources; {len(parameters)} scalar input rows.")


if __name__ == "__main__":
    main()
