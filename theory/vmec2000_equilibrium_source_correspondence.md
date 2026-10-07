# Original VMEC: equations, profiles and current evidence

- Source: PrincetonUniversity/STELLOPT `8060f5e5b1bfe11b2f8809c8dfa90459ee72f9ba`, `develop`, 2026-10-04. This is the current Fortran/PARVMEC source, not the older serial VMEC8.52 validation tag.
- Scope: fixed-boundary, axisymmetric, isotropic, `GAMMA=0`, `NCURR=0`, `LRFP=F`, default `APHI(1)=1`. Other modes below are source-audited alternatives, not executed equilibria.
- Ownership: canonical GS theory and analytical oracles in kin6d; case admission in TC24; this external sidecar pins correspondence. No FortSym dependency is added upstream.
- Genealogy: VMEC++ shares VMEC's variational model and numerical ancestry. Agreement between them is useful regression evidence, not two independent confirmations of correctness.

## Governing and discrete model

- Ideal nested-surface equilibrium: `div B=0`, `curl B=mu0 j`, `j cross B=grad p`, `B dot grad s=0`.
- Geometry uses Fourier phase `m*u-n*v`; `v` is the cylindrical toroidal angle. For the current CCW poloidal/cylindrical chart, `signgs=-1`.
- With signed Jacobian `J=e_s dot (e_u cross e_v)`, normalized toroidal coordinate `s`, and straight-field-line angle `u*=u+lambda`, the continuous contravariant field is `B^u=(chi' - Phi'*lambda_v)/J`, `B^v=Phi'*(1+lambda_u)/J`. Internal fluxes are signed fluxes per radian; physical flux outputs restore `2*pi*signgs`.
- The covariant field is `B_u=g_uu B^u+g_uv B^v`, `B_v=g_uv B^u+g_vv B^v`; `B^2=B^i B_i`. Distinguish coordinate components from cylindrical orthonormal components.
- Source: [bcovar.f](https://github.com/PrincetonUniversity/STELLOPT/blob/8060f5e5b1bfe11b2f8809c8dfa90459ee72f9ba/VMEC2000/Sources/General/bcovar.f), lines188–264: signed volume quadrature, full-to-half radial averaging with odd/even mode regularity, contravariant/covariant fields, magnetic pressure and `pres=mass/vp**gamma`.
- Input `pmass` is multiplied by `mu0*pres_scale`; with `GAMMA=0` this prescribes pressure directly. For nonzero gamma it supplies a mass function with geometry-dependent pressure, so a fixed pressure table is a different physical contract.
- Energy principle: magnetic energy plus constrained internal energy; variation at fixed toroidal/poloidal flux and mass yields force balance. For positive shell volume derivative `V'` and fixed mass `M`, `p=M/(V')**gamma`; the shell term is `M*(V')**(1-gamma)/(gamma-1)` for `gamma!=1`, whose variation is `-p*delta V'`. Thus `GAMMA=0` has a finite `-M*V'` constrained term, not a singular limit. Native output `wp` stores integrated pressure, not that signed constrained-energy term.
- Native solver projects geometry/field forces onto angular Fourier modes and uses radial full/half meshes, regularity, constraints and preconditioned pseudo-time iteration. Native normalized force measures are not the independently reconstructed SI pointwise force.
- Open: complete line-by-line variation/discrete stencil derivation, constraint-force terms, current-constrained and anisotropic branches, and independent E0/native-output residual checks. These are not claimed checked by a profile probe.

## Profile selector catalogue

- Authority: [profile_functions.f](https://github.com/PrincetonUniversity/STELLOPT/blob/8060f5e5b1bfe11b2f8809c8dfa90459ee72f9ba/LIBSTELL/Sources/Miscel/profile_functions.f), pressure707–872, iota555–703, current8–551; selectors are lowercased.
- Scalar coefficient arrays `AM`, `AI`, `AC` are indexed0:20. This supports several analytic models; the auxiliary-table bound does not bound all profile representations.
- Original auxiliary arrays have101 entries (`vparams.f:16`, `vmec_input.f:29–35`). Table functions find active length using `minloc(aux_s(2:))`; ascending nonnegative knots need a remaining `-1` sentinel, hence100 active knots in this input convention.

| Quantity | Native selector | Representation |
| --- | --- | --- |
| Pressure | `power_series` | Degree20 polynomial in `s`, Horner evaluation; pressure in Pa before internal `mu0` scaling. |
| Pressure | `gauss_trunc` | Edge-truncated Gaussian, normalized to `AM(0)` on axis. |
| Pressure | `two_power`, `two_power_gs` | `A*(1-s**b)**c`; optionally six Gaussian modifiers. |
| Pressure | `two_lorentz` | Weighted sum of two normalized, edge-subtracted Lorentz-type profiles. |
| Pressure | `pedestal` | Degree15 polynomial plus a normalized tanh pedestal in `sqrt(s)`; updates internal coefficient normalization. |
| Pressure | `rational` | Numerator degree9 / denominator degree10; zero denominator returns `HUGE`. |
| Pressure | `akima_spline`, `cubic_spline`, `line_segment` | Auxiliary knots/values; interpolation details below. |
| Iota | `power_series`, `nice_quadratic` | Degree20 polynomial; or prescribed axis/edge values plus `4*a2*s*(1-s)`. |
| Iota | `sum_atan` | Offset plus five arctangent terms, explicit edge limit. |
| Iota | `rational` | Numerator degree9 / denominator degree10; zero denominator returns `HUGE`. |
| Iota | `akima_spline`, `cubic_spline`, `line_segment` | Auxiliary knots/values; no pressure scaling. |
| Current | `power_series` | Parameterizes `I'(s)` degree20 and integrates analytically. |
| Current | `power_series_i` | Parameterizes `I(s)=sum AC(k)*s**(k+1)`; no constant term. |
| Current | `gauss_trunc`, `two_power`, `two_power_gs` | Parameterize `I'`; fixed10-point Gauss–Legendre quadrature integrates0→s. |
| Current | `sum_cossq_s`, `sum_cossq_sqrts`, `sum_cossq_s_free` | Windowed cosine-squared contributions with analytic integrals; uniform centres in `s`/`sqrt(s)`, or seven freely placed contributions. |
| Current | `sum_atan`, `pedestal`, `rational` | Direct enclosed-current families. |
| Current | `akima_spline_i`, `cubic_spline_i`, `line_segment_i` | Interpolate enclosed `I`. |
| Current | `akima_spline_ip`, `cubic_spline_ip`, `line_segment_ip` | Integrate auxiliary `I'`; spline integrations require first knot near0. |

- Unknown selectors warn and change to `power_series`, rather than rejecting the run. Explicitly verify selector spelling and executed status.
- Analytic families are not automatically admissible: check finite values, positive pressure where intended, endpoint behavior, denominator zeros and widths/powers. The cosine-count checks admit1 although the uniform-width expression divides by `count-1`; this is an unverified source-level edge-case concern, not an executed benchmark finding.
- Anisotropic/rotation helper functions `photp`, `ptrat`, `protf` expose related families; their mode-specific physical derivation remains outside this isotropic lane.

## Interpolation, constraints and normalization

- `cubic_spline`: first/last derivative from a quadratic through the corresponding three knots; global clamped cubic in `s`, minimum4 active knots. This is neither a natural spline nor a spline in `rho=sqrt(s)`.
- `akima_spline`: local slope weighting; fictitious endpoint points extrapolated quadratically. Latest official pin contains the right-edge Akima fix. It is a different between-knot law from the frozen cubic.
- Spline requests outside the knot interval fail; cubic also checks strict knot ordering. Line segments extrapolate from endpoint segments, require at least two knots and only explicitly check the first interval's ordering; validate the full grid separately.
- Source: [spline_cubic.f](https://github.com/PrincetonUniversity/STELLOPT/blob/8060f5e5b1bfe11b2f8809c8dfa90459ee72f9ba/LIBSTELL/Sources/Miscel/spline_cubic.f), [spline_akima.f](https://github.com/PrincetonUniversity/STELLOPT/blob/8060f5e5b1bfe11b2f8809c8dfa90459ee72f9ba/LIBSTELL/Sources/Miscel/spline_akima.f), [line_segment.f](https://github.com/PrincetonUniversity/STELLOPT/blob/8060f5e5b1bfe11b2f8809c8dfa90459ee72f9ba/LIBSTELL/Sources/Miscel/line_segment.f).
- Pressure/current evaluate `min(abs(s*bloat),1)`; iota does not apply this transform itself. Native input rejects nonunit `BLOAT` with `NCURR!=1`.
- Default `APHI(1)=1`, `LRFP=F` makes the radial argument normalized toroidal flux. Altering `APHI` or using `LRFP=T` changes the radial map; in RFP mode `AI` supplies q and `piota` returns its reciprocal. Flux primitives use101-point composite trapezoidal quadrature, a separate mapping error source when the derivative is nonconstant.
- `NCURR=0` keeps prescribed iota and sets `chi'=iota*Phi'`; `NCURR=1` normalizes enclosed-current shape to `CURTOR` and updates iota from the covariant current constraint. These are different equilibrium inputs; current is not a drop-in replacement for the frozen iota table.
- Source: [profil1d.f](https://github.com/PrincetonUniversity/STELLOPT/blob/8060f5e5b1bfe11b2f8809c8dfa90459ee72f9ba/VMEC2000/Sources/Initialization_Cleanup/profil1d.f), lines64–175; [add_fluxes.f90](https://github.com/PrincetonUniversity/STELLOPT/blob/8060f5e5b1bfe11b2f8809c8dfa90459ee72f9ba/VMEC2000/Sources/General/add_fluxes.f90), lines28–58.

## Output and evidence

- Current native control: exact circular A10, p=0, q=1.5, Phi=6.400429545 Wb. Original VMEC and VMEC++/DESC/GVEC converge and agree on signed physical fields; maximum all-pair Bpol RMS difference 0.0254% on 216 frozen interior points.
- Reconstruction respects odd-m parity: interpolate coefficient/sqrt(s), then restore sqrt(s). Ordinary cubic-in-s creates false near-axis current; exact geometry and independent R/Z curl controls demonstrate it. This is numerical evidence, not a new symbolic proof.
- Confirmed parallel LASYM storage defect: `funct3d.f` passes physical pr1/pz1 as force scratch to `symforce_par`; first-step high-force repair then calls `guess_axis_par` with overwritten geometry. [Fork PR #2](https://github.com/itpplasma/STELLOPT/pull/2) preserves/restores it; native E0 wout is byte-identical, unchanged TC24 now converges. Serial/multirank checks remain open.
- TC24 force/gradp about 1.63 remains unexplained after storage/parity repairs. Half-grid pressure/iota match input; full-grid values average/extrapolate them. Exact input-pressure differentiation barely changes the discrepancy.
- Original TC24 field has a separatrix saddle; executed CHEASE/Fourier boundaries avoid it by roughly 9–13 cm. Exact nested-surface singularity and regularized-boundary errors need distinct checks.
- Retained source/data and interpretations: [ordinary diagnosis](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/blob/plan/circular-tokamak-benchmark-20261007/review/EQUILIBRIUM_VMEC_PP_SIMPLE_CONTROL.md), [storage audit](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/blob/plan/circular-tokamak-benchmark-20261007/equilibrium/data/vmec2000_20261007/axis_initialization_source_audit.md).

- `wrout.f:1281–1285` writes pressure in Pa, full fluxes in Wb and derivatives with `2*pi*signgs`; geometry is on the full radial mesh, most field spectra on the half mesh with a dummy axis row. `lambda` output is renormalized and radially averaged; it is not the raw internal optimization variable.
- `cdf_define` arguments establish shape/type; a reused array there does not establish a wrong written value. In particular `chipf` is correctly written from `chipf`, not from `phipf`.
- Initial E0 attempt: original source/binary, same129-knot input, process exit0 but parser rejects `AM_AUX_S(102)`, no `wout`. The original129-knot TC24 deck was prepared but never launched and is explicitly superseded.
- Registered existing100-knot E0 repeat: native converged; exact off-angle physical-field checks give Bpol RMS `9.39e-5`, psi RMS `1.69e-5`, F `8.48e-8`, pressure `2.79e-7`. Controller accepts signed-field/input translation with measured errors; full continuous-force/refinement qualification remains open.
- Registered100-knot TC24 baseline: native boundary convergence failed, `ier=16`, nonfinite FSQR/FSQZ; retain rejected output. The unchanged-input repair above supersedes this outcome for native convergence, while physical acceptance remains open.
- Native input axis `R=6.4127m,Z=0.56469m`; baseline automatic repair reports `R=-6976.20m`. Source trace and native storage oracle establish the parallel scratch-alias cause. Input profile capacity is not implicated.
- Standalone profile probes rebuilt original101-entry profile/input modules and demonstrate existing polynomial and100-knot representations. These are not equilibrium runs or native force validation.
- TC24 diagnostics live in `equilibrium/data/vmec2000_20261007/profile_model_audit/`; retain input hashes, knot choices and value/derivative errors. Capacity patch is suspended pending comparison of existing representations.
- Official [VMEC documentation](https://princetonuniversity.github.io/STELLOPT/VMEC.html) describes the energy/field model. Its linked [namelist page](https://princetonuniversity.github.io/STELLOPT/VMEC%20Input%20Namelist%20(v8.47)) labels itself v8.47 and omits current auxiliary-model details. The variation equation on the theory page appears to omit the square of field magnitude; compare dimensionally and with implemented `B^i B_i` before reusing it. No code error follows from that documentation typo.
