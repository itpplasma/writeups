# NTV source catalogue

- Intake date: 2026-10-07. [Structured catalogue](catalogue.json) records source identities; full local paths/receipts live in ignored .local/intake/.
- Status: targeted collection and source inspection. No fresh replay of historical algebra is claimed.

## Existing repository

| Source | Content | Algebra partner |
|---|---|---|
| [NTV torque](../writeup_ntv.lyx) / [TeX](../writeup_ntv.tex) | Momentum, radial current and perturbed/unperturbed surfaces | None found in this checkout |
| [EFIT to Boozer](../EFIT_to_Boozer.tex) | Signed EFIT field, tracing and coordinate construction | Numerical libneo implementation at its owner |
| [Differential geometry](../writeup_diffgeom.lyx) / [TeX](../writeup_diffgeom.tex) | Forms/densities and covariant/contravariant Fourier representation | None found in this checkout |
| [Flux coordinates](../flux_coordinates.lyx) | Magnetic charts and geometry | None found in this checkout |
| [Guiding centre](../guiding_center/guidingcenter.tex) | Lukas Grabenwarter's phase-space Lagrangian derivation and drift motion | None found in this checkout |
| [MHD](../mhd/mhd.tex) | Ideal/resistive and linear/nonlinear notes; experimental portions | None found in this checkout |
| [Hamiltonian scripts](../scripts/hamilton_chaos.py) | Numerical chaos illustration, with Fortran companion | NumPy numerical example, not symbolic CAS |

## Collected packages

- [libneo coordinates](../collections/libneo-coordinates/README.md): MIT-licensed converter writeup and near-axis Wolfram source; native implementations remain at libneo.
- [Chris's coordinate draft](../collections/boozer-hamada-chris/README.md): preserved historical draft; numerical Rath partners are indexed, not silently classified as CAS.

## Further intake

| Family | Material found | Remaining qualification |
|---|---|---|
| Hamada constructions | Andreas/Rath writeups, converter model notebook, numerical Python/MATLAB/Fortran | Authorship/terms, equation pairing, covariant/contravariant and rational-surface assumptions |
| Helical Shaing benchmark | Two 2015 analytical writeups and numerical MATLAB connected-formula implementation | Hydrogen/Zeff=1 scope, native signs and regime limits; MATLAB is not CAS |
| Hamiltonian NTV | Historical ntv_hamilton prose/notebook and current proof suites | Match equations and production source; retained results require fresh replay |
| Finite-amplitude/pendulum | Nonlinear notes, Mathematica notebooks and numerical solvers | Revision comparison, domains, perturbative limits and current code correspondence |
| NEO-2 collisions | Fokker–Planck/Burnett/Laguerre basis and matrix-element writeups | No executable CAS partner found in inspected historical folder |
| NEO-2 code derivations | Drive discretization, mode map and Lorentz closure Wolfram suites | Link owner and executed source; full collision coverage remains open |
| Analytical GS | GLISS/Solovev references and archived FreeFEM teaching example | FreeFEM weighting/source contract unresolved; not an admitted GS oracle |

- No original paired MARS/GPEC/SFINCS/NTVTOK CAS suite was found in the inspected archive roots. New correspondence checks remain required.
- Private collections and unknown-rights source material remain at their owners; catalogue entries preserve discoveries without republishing those sources.
- Existing theory may disagree with code or current conclusions. Record literature/code errata and open questions before promotion.
