# CHEASE curved-profile primitive

- Implemented quantity: ISOFUN integrates native TTP into TMF=F²/2, before taking sqrt(2*TMF). Native SPLINE/TRIDAG define D2TTP as its second derivative in native poloidal flux.
- Source: MARS-associated CHEASE at [8824bb18](https://github.com/krystophny/MARS-Q/blob/8824bb18e1514b4a27f6357d5fe859d4fe690542/CheaseMerge/chease.f#L16504); [fork fix PR30](https://github.com/krystophny/MARS-Q/pull/30). Public CHEASE ISOFUN already uses the correct downward expression.
- Let t=(psi−psi0)/h, h=psi1−psi0. The cubic spline cell is `(1−t)f0+t*f1+h²*[((1−t)³−(1−t))*M0+(t³−t)*M1]/6`.
- Its exact integral is `h*[0.5*(f0+f1)−h²*(M0+M1)/24]`. Downward accumulation subtracts it; upward accumulation adds it. Endpoint direction does not change the curvature expression.
- Baseline used h³/48 in both branches and the wrong upward curvature sign. Constants and linear profiles have zero curvature and are unaffected.
- [Native FortSym derivation](cas/chease_cubic_profile_primitive/cubic_primitive.wl): four exact identities and two nonzero baseline rejection witnesses. Run directly with `fortsym_wl_run`; Python is unnecessary for the derivation.
- Independently extracted native SPLINE/TRIDAG and both executed primitive branches: baseline8/12, fixed12/12 against polynomial antiderivatives on nonuniform knots, including four mutation controls. Controller independently replays fixed12/12.
- Scope: selected profile primitive only. Registered equilibrium pair, downstream MARS PairA/B and human review remain open. The separate E0 boundary-gradient/q discrepancy is not explained by this repair.
- [Campaign source, fixtures and receipts](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/tree/plan/circular-tokamak-benchmark-20261007/equilibrium/data/chease_lane_closure_20261007); [CHEASE reference](https://doi.org/10.1016/0010-4655(96)00046-X). The native defect is a code erratum, not an asserted literature erratum.

Chris&AI
