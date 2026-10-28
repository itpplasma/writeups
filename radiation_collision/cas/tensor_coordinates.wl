(* Section 3.2: the tensor in (p, chi) and in (gamma, u_par), and the
   series of F and H at u = 0. Every r### must evaluate to 0. *)

(* Original coordinates, Eqs. (3.12)-(3.14), in units with
   k = e^2 wce^2 T/(m^2 c^5) and u = p/(m c): D^{uu}, D^{u chi}, D^{chi chi}. *)
g = Sqrt[1 + u^2];
sx = Sqrt[1 - cx^2];
Duu = 2*k*g^2*sx^2/3;
Duc = 2*k*sx*cx/(3*u);
Dcc = k/(24*u^2)*(F - G*cx^2);
(* gamma = g(u), u_par = u cos(chi): transform as a contravariant tensor. *)
dg = {D[g, u], 0};
dua = {cx, -u*sx};
Dm = {{Duu, Duc}, {Duc, Dcc}};
Dgg = dg . Dm . dg;
Dga = dg . Dm . dua;
Daa = dua . Dm . dua;
a = 2*k/3;
H = u^2 - 1 - G/16;
r001 = Expand[Dgg - a*u^2*sx^2];
r002 = Expand[(Dga - a*u*cx*u^2*sx^2/g)*g];
r003 = Expand[Daa - a*sx^2*(F/16 + H*cx^2)];
(* a = 2 nu0/3 with nu0 = e^2 wce^2/(m c^3 mu), mu = m c^2/T. *)
r004 = Together[(2/3)*e^2*wce^2/(m*c^3*(m*c^2/T)) - 2*(e^2*wce^2*T/(m^2*c^5))/3];

(* Series at the origin, Eqs. (3.16)-(3.17): the apparent poles cancel. *)
Fu = 10 + 3/u^2 - (9/(g*u) + 3*g/u^3)*ArcSinh[u];
Gu = 10 + 15/u^2 - (21/(g*u) + 15*g/u^3)*ArcSinh[u];
Hu = u^2 - 1 - Gu/16;
r005 = Expand[Normal[Series[Fu, {u, 0, 8}]] - (32/5*u^2 - 176/35*u^4 + 64/15*u^6 - 4352/1155*u^8)];
r006 = Expand[Normal[Series[Hu, {u, 0, 8}]] - (27/35*u^4 - 68/105*u^6 + 656/1155*u^8)];
(* The leading behaviour u_perp^2/u^2 [F/16 + ...] stays finite: F/u^2 and H/u^4. *)
r007 = Normal[Series[Fu/u^2, {u, 0, 0}]] - 32/5;
r008 = Normal[Series[Hu/u^4, {u, 0, 0}]] - 27/35;
