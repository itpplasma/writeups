# TC24 reference equilibrium provenance

**Reference: `ngfile_p1_run_eq_modx03_20260527`, distributed by Xingting Yan
on 2026-05-28 in the 20260527 package.** This is the modified CHEASE equilibrium
actually shared for the benchmark after the May meeting, and the best-supported
meaning of “the one most people used for everything”. It is not an exact-byte
claim about every historical MARS response. Keep all four received states.

## Received equilibria and use

All four are associated with ITER JINTRAC #53298, ppfseq 32305. Dates below are
receipt/distribution dates, not an inferred creation timestamp from blank headers.
Currents, F and q here are the native file values; q95 means s_pol=0.95.

| Equilibrium / producer | Receipt, settings and native scalars | Verified users / evidence |
|---|---|---|
| **[modx03](../../../../received/xingting/20260527/gfiles/ngfile_p1_run_eq_modx03_20260527)**; Xingting/MARS-F CHEASE workflow | May 28; R0=6.2 m, B0=5.3 T, Ip=15.563913 MA, F_edge=32.86 T m, q0=1.00106, q95≈3.12 | `GPEC/new_equil/equil.in` and `new_equil_l5/equil.in`; Logan August HDF5 names this file and its exact MD5. `MARSF_results/ngfile_p1`, `gfiles/…` and `BOOZER/ngfile/…` are byte-identical. NEO-RT MARS and GPEC campaigns use their corresponding converted Boozer backgrounds; NEO-2 matched campaigns inherit those backgrounds. |
| [gfile_chease](../../../../received/xingting/20260527/MARSF_results/gfile_chease); MARS CHEASE subsequent output | May 28; R0=6.2 m, Ip=15.564467 MA, F_edge=32.86, q0=1.00087, q95≈3.12 | Supplied MARS-F native response/geometry and the MARS-K replay lineage. `MARS-K/replay_chease.py` recovers the two-stage read/re-solve path from `MARSF_logfile/log_chease`. Edoardo explicitly compared this against modx03 in August. Distinct axis, edge pressure and edge q: not interchangeable bytes. |
| [JINTRAC original](../../../../received/xingting/20260527/gfiles/JINTRAC_53298_ppfseq32305_v5.eqdsk); ITER transport scenario source | May package; R0=6.2 m, Ip=15.000000 MA, q0=1.31166, q95≈3.13 | `GPEC/old_equil/equil.in` names the older JINTRAC conversion. The superseded October Phase 4b absolute-psi study selected this source. It is an ancestor/variant, not the current benchmark reference. |
| [Leonardo CHEASE](../../../../received/leonardo/20260127/CHEASEOUT_EQDSK_COCOS_2_53298_ppfseq32305); Leonardo Pigatto | January 27, export header January 22; explicit COCOS 2, 257² grid, R0=6.0 m, B0=5.3 T, Ip=15.299887 MA, F_edge=31.80, q0=1.40359 | January mail explains manual smaller-grid rewriting before CHEASE. Retained supplier intermediate; no evidence that the maintained May/August benchmark decks select it. R0=6.0 changes F_edge; do not silently relabel it 6.2. |

The first three links above are relative to the repository root via this file's
location; original bytes and supplier manifests remain authoritative.

The executed NEO backgrounds also differ in conversion: `NEO-RT/MARS_DT_testD/README.md`
identifies MARS-fed `BOOZER/ngfile/fromefit.bc` (MD5 prefix `18df623d67`, also NEO-2's
`ITER_axi.bc`) and GPEC-fed `ngfile_COCOS3` (`2a7025908e`). Shared modx03 ancestry
does not make these converted files or their historical COCOS interpretations identical.

## Producer deck and what 15.56 MA means

[Edoardo's August Drive snapshot](../../../../received/edoardo/20260818/README.md)
identifies `Input_equilibrium/INPUTS/modx03_20260527_CS_ITER-ELM` as EXPEQ and
modx03 as its corresponding EQDSK. Its supplied namelist specifies
`NCSCAL=4, CURRT=0.5951974902745026, NSTTP=2, NPPFUN=4, NFUNC=4`,
`R0EXP=6.2, B0EXP=5.3`, NS=NT=80, NPSI=300, NCHI=380.

**NCSCAL=4 performs no equilibrium current rescaling.** `CURRT*R0EXP*B0EXP/mu0`
is 15.563913 MA, but the executed selector uses the supplied normalized-flux
pprime and averaged toroidal-current-density Istar profiles. CHEASE's
`curent.f90` defines NSTTP=2; `norept.f90` rescales to CURRT only for NCSCAL=2;
`qplacs.f90` leaves q unscaled for 4. The received log gives 15.5614975 MA.
This small distinction must survive replay and must not be called round-off.
There is no mail evidence for a deliberate “15.56 MA target” beyond this deck.

The new common-code interior study uses an explicitly derived normalized
pprime/FFprime-shape law and the enclosed current of the selected source.
It is separated from the exact supplied Istar replay. Its input transfer,
source difference and finite-resolution errors must all be reported.

## Work-mail evidence, read only

Live searches used account 1 and the requested equilibrium/code/person terms;
50-result broad searches were narrowed with `53298` and `modx03`, and relevant
original messages/quoted thread context were fetched. No mail was sent or drafted.
Actionable facts only; the mailbox remains the owner of message text.

- January 27, Leonardo, `12ebc0c2-2c7a-4f4f-b62c-7cf22b0ee5fd@igi.cnr.it`:
  original reader/newline and 55,500-boundary-point problems; manually rewrote
  onto a smaller grid, ran CHEASE, attached his separate export.
- May 27, Nikolas in the remote-discussion thread: use the qmin>1 modification;
  GPEC can read CHEASE, but the truncation surface must be declared.
- May 27, Youwen's post-meeting agreement, retained in Xingting's May 28 mail:
  distribute revised CHEASE equilibrium and profiles to proceed with benchmarking.
- May 28, Xingting, `c8350203-771f-4880-b9be-e14b721ed3ab@ipp.ac.cn`:
  distributes the modified equilibrium in folder 20260527. May 31 repeats the
  link while adding MATLAB profile/NTVTOK files.
- May 27, Yueqiang, fetched 16:11 UTC reply distinguishes the older Li/Hu published ITER baseline from
  the newer JINTRAC scenario. Discussion of a fallback is not evidence of adoption.
- August 11, Edoardo, `CAGnun47_cM2Fh_fvaXK4mPtYvFEXrZxFA9cEG=P6vGBXe_4C9Q@mail.gmail.com`:
  reports an extra resonant surface with modx03 compared with gfile_chease.
- August 18, Edoardo, `CAGnun47KjjXCPJq6yeR=XxvuUnqYNuWuhQJo=Ni8dFcGzczLxQ@mail.gmail.com`:
  shares CHEASE/MARS input folders; the supplied README establishes the file link.
- No inspected message supplies a JINTRAC derivative-sign correction or explains
  Leonardo's R0=6.0. Those are file/code findings, not attributed collaborator claims.

## Checks and conventions

- Reference SHA-256: `fbf1b1c06253647263869efe7842e4c60214f2a1844197d2306e5b80d95833f2`.
  MD5 `420c63c7d4f7947c6750022bbeb59275` matches
  `received/logan/20260822/tc24_gpec_results.h5:equilibrium_md5` exactly.
- gfile_chease SHA-256: `298eb09af80079f44869c89401b5dd788b199eb7d1eab6a04f1a604b1b848b7a`.
  Other file hashes are in `reference/*_case.json` and the original manifests.
- We use the producer CHEASE COCOS-2 declaration, mapping explicitly to COCOS 3.
  The signed header tuple alone is also compatible with a different toroidal
  axis; it cannot infer the producer's laboratory direction. Historical direct
  NEO reader interpretations remain as executed, in `review/rotation_sign_audit.json`.
- JINTRAC integral(pprime)/Δp and integral(FFprime)/Δ(F²/2) are both −1.013007:
  a source-file inconsistency, invariant under a coherent COCOS transformation.
  The old absolute-psi formulation was our own setup mistake for source replay.
  Neither issue blocks selecting the consistent collaborator CHEASE reference.
- Run lineage: `results/run_registry.json`, `MARS-K/replay_chease.py`,
  `NEO-RT/MARS_DT_testD/README.md`, NEO-2 campaign provenance, GPEC executed decks,
  `review/provenance/correspondence/`, and `archive/equilibrium/dechurn/INDEX.md`.
  Brain work recall was cross-checked against these source files; it does not
  outrank a deck, hash or native output. Historical use is not accuracy validation.

Chris&AI
