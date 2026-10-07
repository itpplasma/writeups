(* Exact scalar amplitude sector; trigonometric orthogonality supplied as a
   separate explicit assumption, independently tested against native kernels.
   Fixed multiplier/filter and offsets. No claim of live geometry-dependent
   preconditioner being a fixed global energy penalty. *)
ClearAll["Global`*"];
cminus=a*p*e/2;
cplus=-a*p*e/2;
cdouble=-k*p*e^2/2;
energy=(cminus^2*wminus+cplus^2*wplus+cdouble^2*wdouble)/4;
exact=a^2*p^2*e*(wminus+wplus)/8+k^2*p^2*e^3*wdouble/4;
r001=Together[D[energy,e]-exact];
(* Chain derivative C_e=(P deltaR) R_theta + PR deltaR_theta. *)
C=p*e*ck*(-a*s1-k*e*sk);
r002=Together[D[C,e]-p*ck*(-a*s1-k*e*sk)-p*e*ck*(-k*sk)];
(* Source P0=P1=0, hence an m0/m1 circle or ellipse has no constraint,
   provided initial offsets are zero. *)
r003=Together[m*(m-1)/.m->0];
r004=Together[m*(m-1)/.m->1];
(* Fixed filter self-adjoint energy derivative, independent of above sector. *)
r005=Together[(D[(u+e*v)^2*w/2,e]/.e->0)-u*v*w];
(* Negative control: missing derivative test-function term changes derivative. *)
r006=Together[(D[C,e]-p*ck*(-a*s1-k*e*sk))/.{p->2,e->1,k->2,ck->1,sk->1}];

(* h=1/(ns-1): geometric part of live tcon scaling has a nonzero
   limit IF tcon_base stays finite/nonzero; no assumption that it does. *)
scale=64*h^2*(1+(1+1/h)/60+(1+1/h)^2/24000);
r007=Together[(Together[scale]/.h->0)-1/375];

(* Boundary inherited fixed offset d*cos(k theta), differentiated as fixed. *)
energyOffset=(a^2*(p*e-d)^2*(wminus+wplus)+k^2*e^2*(p*e-d)^2*wdouble)/16;
exactOffset=a^2*p*(p*e-d)*(wminus+wplus)/8+k^2*e*(p*e-d)*(2*p*e-d)*wdouble/8;
r008=Together[D[energyOffset,e]-exactOffset];
