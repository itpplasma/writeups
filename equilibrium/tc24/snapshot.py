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
TC24 = "916dc6d9da0ca843d6b4a6d67b46e62ff37ef94e"
KIN6D = "3c851d7"


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
    for phase in ["phase1", "phase2", "phase4", "phase5"]:
        path = f"equilibrium/{phase}/cases.json"
        obj = json.loads(read(args.tc24, TC24, path))
        if phase == "phase5":
            flatten(obj, "", path, "C0")
            for a in obj["aspects"]:
                parameters.append({"source": path, "case": "C0", "key": "aspect", "value": a})
        else:
            for case, values in obj.items():
                flatten(values, "", path, case)
    with (out / "parameters.csv").open("w") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "case", "key", "value"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(parameters)
    support = []
    for revision in ["99fa2c8", "82d4d1f", "fa5c388", "451fa5b", "a50f8b6"]:
        support.append({"commit": git(args.kin6d, "rev-parse", revision).decode().strip(),
                        "subject": git(args.kin6d, "show", "-s", "--format=%s", revision).decode().strip()})
    manifest = {"description": "Committed inputs for the first Phase 6 draft; source metadata is historical.",
                "tc24_commit": TC24, "kin6d_data_commit": git(args.kin6d, "rev-parse", KIN6D).decode().strip(),
                "kin6d_support_history": support, "sources": sources}
    (HERE / "sources.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Copied {len(sources)} committed sources; {len(parameters)} scalar input rows.")


if __name__ == "__main__":
    main()
