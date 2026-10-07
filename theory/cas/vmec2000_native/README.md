# Native original-VMEC signed flux identities

- External correspondence only: no CAS dependency or files added to upstream VMEC.
- Solver source: STELLOPT f0c7c61d9cf92c9e876abea388e6bd943e3f2259. Output sign map: profil1d67, fileout216–220, eqfor177–183, add_fluxes53–89, wrout1283–1285.
- Conditions: signgs exactly ±1; `two_pi=2*pi` nonzero; fixed native chart; gamma0/ncurr0/lrfpfalse. Generic scalar symbols model native half/full-grid variables. No numerical field fitting or imported Mathematica output.
- Native FortSym proves16 exact identities and rejects two false generic identities. Independent integer mean-product witness supplies a concrete counterexample.
- FortSym pin a6142712af998b727c245fb6cfbb3745b296ec24; librarySHA70c99a46f67998540f6eedb5897f26897ce612b6a26299de292d5a369a79d8fd.
- Reproduce: `cmake -S . -B /tmp/vmec-flux-build -DFORTSYM_BUILD=<verified-build>`, `cmake --build /tmp/vmec-flux-build -j1`, `ctest --test-dir /tmp/vmec-flux-build --output-on-failure`.
- Fresh native CMake/CTest1/1 passed. Fo CMake capture limitation tracked by issue193; no resident Gremlin evidence claimed.
- [Physical/native sign ledger](https://gitlab.tugraz.at/plasma/proj/plasma-sign-conventions/-/blob/main/docs/VMEC2000_NATIVE_FLUX_MAP.md) records exact source/output maps and excluded modes.
- Open: full energy/constraint/discrete-force derivation, physical field-polarity controls, general APHI/current/LRFP/anisotropy modes, independent resolution convergence. Scalar sign identities do not prove those bridges.
