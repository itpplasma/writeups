# Plasma writeups

Notes, derivations and slides on plasma physics and numerical methods
from the plasma theory group at TU Graz (ITPcp), together with readable
companions that compare equilibrium codes against their source papers.

Status: a working collection. Older notes are kept as written and have not
all been reviewed again; check a derivation before reusing it.

## Contents

Notes and slides at the top level are LyX (`.lyx`) or LaTeX (`.tex`)
sources, for example:

- Plasma theory: `plasma_writeup.tex`, NTV torque (`writeup_ntv.lyx`,
  `writeup_ntv.tex`), MHD (`mhd/`), guiding-centre motion (`guiding_center/`),
  pedestal, RMPs, reduced models (`writeup_redmod_plasma.lyx`, `redmod.lyx`).
- Geometry and coordinates: differential geometry (`writeup_diffgeom.*`),
  flux coordinates, symplectic structure, EFIT to Boozer coordinates
  (`EFIT_to_Boozer.tex`).
- Numerics and statistics: numerics, finite elements (`fem.tex`,
  `writeup_fem.lyx`), advection, probability, regression, uncertainty
  quantification.
- Slides on software development and PCA (`slides_*.lyx`) and a note on
  polymorphism and performance ([software_dev_polymorphism.md](software_dev_polymorphism.md)).
- `scripts/`: a small Hamiltonian chaos example in Python and Fortran.

## Equilibrium companions

- [equilibrium/](equilibrium/README.md): a readable derivation of the
  Grad-Shafranov equation (signed reduction, weak form, profiles, limits);
  render it with `equilibrium/render_grad_shafranov.sh OUTPUT_DIR`
  (needs `pdflatex`).
- [theory/](theory/): source correspondences that map the equations in the
  papers to the actual routines of
  [KIN/FreeGS/CHEASE](theory/gs_solver_source_correspondence.md),
  [VMEC2000](theory/vmec2000_equilibrium_source_correspondence.md),
  [VMEC++](theory/vmecpp_hybrid_lambda_correspondence.md),
  [DESC](theory/desc_equilibrium_source_correspondence.md) and
  [GVEC](theory/gvec_equilibrium_source_correspondence.md) (including the
  [free-boundary case](theory/gvec_free_boundary_source_correspondence.md)),
  plus a [periodic-cylinder](theory/periodic_cylinder_correspondence.md)
  reference. Symbolic checks are in `theory/cas/`.
- [equilibrium/tc24/](equilibrium/tc24/README.md): draft report comparing
  equilibrium codes on the ITER TC24 benchmark cases, built from committed
  data with `equilibrium/tc24/build.sh`.
- [theory/rmp_model_correspondence_plan.md](theory/rmp_model_correspondence_plan.md):
  planned correspondence for RMP models.

Generated PDFs and plots are not committed; the sources, scripts and data
needed to rebuild them are.

## Kinetic theory

- [radiation_collision/](radiation_collision/README.md): relativistic radiation
  collision operator (Kasilov and Kernbichler 1996) with closed diffusion
  tensor, kernel series, a conservative two-mode closure and the radiation-drag
  propagator; exact fortsym checks in `radiation_collision/cas/`.

## NTV sources

[ntv/README.md](ntv/README.md) catalogues the NTV-related writeups in this
repository and elsewhere ([catalogue.json](ntv/catalogue.json)).
`collections/` holds collected material with its own notices, such as the
[libneo coordinate derivations](collections/libneo-coordinates/README.md).

## License

CC BY 4.0 ([LICENSE](LICENSE)) for the covered material; collected files keep
their individual notices and attribution.
