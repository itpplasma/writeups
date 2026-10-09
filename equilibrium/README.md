# Axisymmetric equilibrium companion

- [TC24 Phase 6 report](tc24/README.md): first complete LaTeX draft, regenerated numerical figures, defect ledger and consumer coverage; inverse and actual TC24 results remain pending.
- [Readable source](grad_shafranov.tex): signed GS reduction, weak form, exact references, selectors and review gates.
- Canonical derivations/checks belong in KIN6D; case inputs and disagreements belong in TC24. Links are in the PDF.
- Render: `equilibrium/render_grad_shafranov.sh /tmp/writeups-gs-20261007`.
- [Reproduction and artifact manifest](grad_shafranov_manifest.json): exact source pins/hashes, numerical receipts, PDF URL and expiry.
- PDF and raster images remain outside Git; no private or third-party source material was imported.

- [Source correspondence](../theory/gs_solver_source_correspondence.md): examined KIN/FreeGS/CHEASE routine paths, conventions, profile laws, diagnostics and unresolved paper–code bridges.
- C0 uses a right-handed straight-cylinder angle: native `q_RH=+1.5` maps to canonical toroidal-limit `q_c=-1.5` when its axis aligns physical +phi. Retained native plots show `q_RH`; outputs are unchanged.
