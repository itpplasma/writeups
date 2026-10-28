(* Section 11: optically thin radiation drag. w = u_perp, v = u_par,
   gp = gamma_par = 1/sqrt(1 - beta^2). Hyperbolic functions of zeta are
   written through E = exp(zeta): csch = 2E/(E^2 - 1), coth = (E^2 + 1)/(E^2 - 1).
   Every r### must evaluate to 0. *)

(* Consistency of the characteristics (11.2): g^2 = 1 + w^2 + v^2. *)
gam = Sqrt[1 + w^2 + v^2];
wd = -nR*w*(1 + w^2)/gam;
vd = -nR*v*w^2/gam;
r001 = Cancel[Together[(w*wd + v*vd)/gam + nR*w^2]];
(* beta = v/g is constant. *)
r002 = Cancel[Together[vd*gam - v*(w*wd + v*vd)/gam]];

(* Trajectory (11.5) with dE/dt = E nR/gp. *)
csch = 2*E1/(E1^2 - 1);
coth = (E1^2 + 1)/(E1^2 - 1);
wt = csch;
gt = gp*coth;
vt = be*gp*coth;
dt[x_] := D[x, E1]*E1*nR/gp;
r003 = Together[dt[wt] + nR*wt*(1 + wt^2)/gt];
r004 = Together[dt[vt] + nR*vt*wt^2/gt];
r005 = Together[dt[gt] + nR*wt^2];
(* g^2 = 1 + w^2 + v^2 holds with gp^2 = 1/(1 - beta^2). *)
r006 = Cancel[Together[(gt^2 - 1 - wt^2 - vt^2) /. gp -> 1/Sqrt[1 - be^2]]];
(* g = gp sqrt(1 + w^2) when v = beta g, gp^2 = 1/(1 - beta^2); then
   zeta = arsinh(1/w) has d zeta/dt = -wdot/(w sqrt(1 + w^2)) = nR/gp. *)
r007 = Cancel[Together[((1 + w^2 + v^2) /. v -> be*gp*Sqrt[1 + w^2]) - gp^2*(1 + w^2) /. gp -> 1/Sqrt[1 - be^2]]];
r012 = Cancel[Together[(-(-nR*w*(1 + w^2)/(gp*Sqrt[1 + w^2]))/(w*Sqrt[1 + w^2])) - nR/gp]];

(* Phase-space Jacobian (11.6): w dw dv = J dzeta dbeta / (2 pi (m c)^3),
   J/(2 pi (m c)^3) = gp^3 csch^2 coth^2. Derivatives in zeta via dE = E dzeta. *)
gpb = 1/Sqrt[1 - be^2];
r008 = Expand[D[be*gpb, be]*(1 - be^2)^(3/2) - 1];
dwdz = D[csch, E1]*E1;
r009 = Together[Abs[dwdz] - csch*coth /. Abs[dwdz] -> -dwdz];
r010 = Together[csch*(csch*coth)*(coth*gp^3) - gp^3*csch^2*coth^2];

(* Continuity: J f = J(zeta0) f_in(zeta0) with zeta0 = zeta - c t solves
   d_t (J f) + c d_zeta (J f) = 0; witness with a concrete f_in. *)
J0f = Exp[-(ze - cc*t)^2]*(ze - cc*t)^3;
r011 = Expand[D[J0f, t] + cc*D[J0f, ze]];
