# Original VMEC auxiliary constraint force

- Source: itpplasma/STELLOPT `f0c7c61d9cf92c9e876abea388e6bd943e3f2259`; MPI-enabled isotropic fixed-boundary axisymmetric lane, without `_HBANGLE`.
- Evidence: source algebra traced below. Full discrete-energy variation, all modes and an independent compiled constraint-kernel oracle remain open. This is not a symbolic-proof completion claim.
- Genealogy: original VMEC and VMEC++ share this construction; matching results do not constitute independent implementation evidence.

## Executed construction

- `bcovar.f:462–481` (parallel) and `:896–912` (serial) replace the input by `tau=min(abs(tcon0),1)` and form
  `C=tau*[1+NS*(1/60+NS/24000)]/(16*R0scale^4)`.
- At interior radial nodes, `tcon(j)=min(abs(ard(j,1)/arnorm),abs(azd(j,1)/aznorm))*C*(32*hs)^2`; the edge uses half the preceding value. `arnorm`/`aznorm` are weighted squared angular geometry derivatives.
- This formula requires nonzero finite normalization denominators. Parallel source sets an error flag for a zero denominator; serial source stops. Removing the coefficient is not a proof that singular geometry is admissible.
- `funct3d.f:763–766` contracts geometry discrepancy against angular derivatives, then `alias.f:164–237` resets the output and reconstructs its filtered Fourier content. Every projected contribution is multiplied by `tcon(j)`.
- `fixaray.f:249–251` gives zero filter weight at m=0 and the highest requested m; intermediate weights contain `-signgs/4` and the native m-scaling denominator. Interior basis size and boundary harmonics therefore remain distinct inputs.
- `forces.f:205–215` (parallel), `:396–406` (serial) add the reconstructed coefficient to radial/vertical force kernels and provide derivative kernels to the Fourier transform. These are additions to the MHD kernels used by the native residual.
- For finite admissible geometry, setting `tcon0=0` makes the coefficient, filtered output and these additions zero. It changes the finite-basis native force operator; whether the nonzero operator is an exact gauge direction of the continuous constrained MHD problem still requires proof.

## Benchmark interpretation

- Retained VMEC++ TC24 controls lower continuous force when only `tcon0` is removed. This supports an auxiliary-force contribution to the finite-discrete residual; it does not establish a general solver defect or physical instability.
- Both VMEC implementations miss the strict native tolerance in corrected ordinary cold `tcon0=0` starts. VMEC++ A10 zero/finite-pressure `tcon0=1` first stages converge with the unchanged tolerance; dependent zero-coefficient warm stages are separate registered experiments.
- Original VMEC default first stages converge on the explicitly approximate compressed100 law. Corrected short local restarts load genuinely but miss the unchanged strict tolerance; long absolute paths previously exceeded the native120-character argument limit and invalidated those warm-start experiments. Keep native stopping and physical force separate.
- Open: independent native constraint-kernel negative/zero controls; discrete MHD-energy directional derivatives for original VMEC; proof of continuous gauge versus finite-basis contribution; three independent resolution levels and strong physical force admission.

- Cross-code status and source/runtime errata: [TC24 PLAN](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/blob/plan/circular-tokamak-benchmark-20261007/PLAN.md), [equilibrium errata](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/blob/plan/circular-tokamak-benchmark-20261007/equilibrium/ERRATA.md). Exact-X nested-coordinate limitations are outside the repair scope; smooth-boundary discrepancies remain open.
