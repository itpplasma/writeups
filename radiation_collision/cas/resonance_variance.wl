(* Section 2: resonance, variational form and null space.
   g = gamma, ua = u_par, up = u_perp; every r### must evaluate to 0. *)

(* On resonance g - eta ua = n s the derivative L_n = (n s/up) d_up + eta d_ua
   acts as d_g + eta d_ua: L_n g = 1 and L_n ua = eta, Eq. (2.5). *)
gp = Sqrt[1 + up^2 + ua^2];
Lng = (n*s/up)*D[gp, up] + eta*D[gp, ua];
r001 = Expand[Lng*gp - (n*s + eta*ua)];
r002 = Expand[(Lng /. s -> (gp - eta*ua)/n) - 1];
r003 = Simplify[(n*s/up)*D[ua, up] + eta*D[ua, ua] - eta];

(* Off resonance, L_n g = 1 - r_n/g and L_n f0 + mu f0 = mu (r_n/g) f0, Eq. (7.4). *)
rn = gp - n*s - eta*ua;
f0 = Exp[-mu*gp];
r004 = Expand[Lng - (1 - rn/gp)];
r005 = Expand[((n*s/up)*D[f0, up] + eta*D[f0, ua] + mu*f0)/f0 - mu*rn/gp];

(* Completing the square over three resonant weights A_i, Eq. (2.9):
   sum A (L - q)^2 = sum A L^2 - B^2/N + N (q - B/N)^2. *)
Nw = A1 + A2 + A3;
Bw = A1*L1 + A2*L2 + A3*L3;
r006 = Together[A1*(L1 - q)^2 + A2*(L2 - q)^2 + A3*(L3 - q)^2 - (A1*L1^2 + A2*L2^2 + A3*L3^2 - Bw^2/Nw + Nw*(q - Bw/Nw)^2)];

(* Null space: in (g, ua) coordinates, L_eta = d_g + eta d_ua. Constancy of
   L_eta f along the tangent eta d_g + d_ua of a resonance line, Eq. (2.11). *)
f = c00 + c10*g + c01*ua + c20*g^2 + c11*g*ua + c02*ua^2 + c30*g^3 + c21*g^2*ua + c12*g*ua^2 + c03*ua^3;
Lf = D[f, g] + eta*D[f, ua];
r007 = Expand[eta*D[Lf, g] + D[Lf, ua] - (eta*D[f, g, g] + (1 + eta^2)*D[f, g, ua] + eta*D[f, ua, ua])];
(* L_eta (g^2 - ua^2)/2 = g - eta ua = n s, so it differs between harmonics. *)
r008 = Expand[D[(g^2 - ua^2)/2, g] + eta*D[(g^2 - ua^2)/2, ua] - (g - eta*ua)];
(* L_eta of the collision invariants is mode-constant. *)
r009 = Expand[D[1 + cE*g + cP*ua, g] + eta*D[1 + cE*g + cP*ua, ua] - (cE + cP*eta)];
