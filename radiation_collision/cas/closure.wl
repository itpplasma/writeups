(* Sections 8-10: the two-mode closure. Every r### must evaluate to 0.
   Modified Bessel functions are reduced to the basis {K1, K2} with
   K_(n+1)(x) = K_(n-1)(x) + (2 n/x) K_n(x). *)
rec4 = {BesselK[4, mu] -> BesselK[2, mu] + 6/mu*BesselK[3, mu]};
rec3 = {BesselK[3, mu] -> BesselK[1, mu] + 4/mu*BesselK[2, mu]};
rec0 = {BesselK[0, mu] -> BesselK[2, mu] - 2/mu*BesselK[1, mu]};
red[x_] := Expand[((x /. rec4) /. rec3) /. rec0];
K1 = BesselK[1, mu];
K2 = BesselK[2, mu];
K3 = BesselK[3, mu];
K0 = BesselK[0, mu];

(* Integral representation (DLMF 10.32.8):
   I_nu(mu) = int_1^oo e^(-mu g) (g^2 - 1)^(nu - 1/2) dg = 2^nu Gamma(nu + 1/2) K_nu(mu)/(Sqrt[Pi] mu^nu),
   and int_1^oo e^(-mu g) g (g^2 - 1)^(nu - 1/2) dg = -d I_nu/d mu. *)
Inu[nu_] := 2^nu*Gamma[nu + 1/2]*BesselK[nu, mu]/(Sqrt[Pi]*mu^nu);
r001 = Expand[Inu[0] - K0];
r002 = Expand[Inu[1] - K1/mu];
r003 = Expand[Inu[2] - 3*K2/mu^2];
(* Normalisation of f0: (mu/K2) int u^2 e^(-mu g) du = (mu/K2)(-dI_1/dmu) = 1. *)
r004 = red[(mu/K2)*(-D[Inu[1], mu])*K2 - K2];
(* <u^2> = (mu/K2)(-dI_2/dmu) = 3 K3/(mu K2), Eq. (8.9). *)
r005 = red[(mu/K2)*(-D[Inu[2], mu])*K2*mu - 3*K3];
(* <arsinh(u)/(g u)> = (mu/K2) int_1^oo arcosh(g) e^(-mu g) dg = (mu/K2) I_0/mu = K0/K2,
   after one integration by parts; d arcosh(g)/dg = 1/sqrt(g^2 - 1). *)
r006 = Cancel[Together[D[ArcCosh[gg], gg]^2*(gg^2 - 1) - 1]];

(* G_E = a ne <u_perp^2> = (2/3) a ne <u^2>, a = 2 nu0/3. *)
a = 2*nu0/3;
GE = 4*ne*nu0*K3/(3*mu*K2);
r007 = Together[a*ne*(2/3)*3*K3/(mu*K2) - GE];

(* Angular average of D^{ua ua} at fixed u, xi = cos(chi), Eq. (8.11). *)
Dpp = a*(1 - xi^2)*(F/16 + H*xi^2);
r008 = Expand[Integrate[Dpp, {xi, -1, 1}]/2 - a*(F/24 + 2*H/15)];
(* With F, G in terms of g (u^2 = g^2 - 1) and au = arsinh(u)/u:
   F/24 + 2 H/15 = (1/15)(3 + 2 u^2 - 3 au/g). *)
u2 = g^2 - 1;
Fg = 10 + 3/u2 - (9/g + 3*g/u2)*au;
Gg = 10 + 15/u2 - (21/g + 15*g/u2)*au;
Hg = u2 - 1 - Gg/16;
r009 = Expand[(Fg/24 + 2*Hg/15 - (3 + 2*u2 - 3*au/g)/15)*g*u2];
(* G_P = (a ne/15)(3 + 2 <u^2> - 3 K0/K2) = 4 ne nu0 (K1 + K3)/(15 mu K2), Eq. (8.13). *)
GP = 4*ne*nu0*(K1 + K3)/(15*mu*K2);
r010 = red[(a*ne/15*(3 + 6*K3/(mu*K2) - 3*K0/K2) - GP)*K2*mu];
(* G_P/G_E = (1 + K1/K3)/5. *)
r011 = Together[GP/GE - (1 + K1/K3)/5];

(* Scalar sources, Eqs. (8.18)-(8.20): H_alpha = -(1/(J f0)) d_i (J f0 D^{i alpha}),
   J f0 ~ g e^(-mu g). Coordinates (u, ua) with g = sqrt(1 + u^2), so
   d/dg at fixed ua is (g/u) d/du. *)
gu = Sqrt[1 + u^2];
up2 = u^2 - ua^2;
Fu = 10 + 3/u^2 - (9/(gu*u) + 3*gu/u^3)*ArcSinh[u];
Gu = 10 + 15/u^2 - (21/(gu*u) + 15*gu/u^3)*ArcSinh[u];
Hu = u^2 - 1 - Gu/16;
W = gu*Exp[-mu*gu];
Dgg = aa*up2;
Dga = aa*ua*up2/gu;
Daa = aa*(up2/u^2)*(Fu/16 + Hu*ua^2/u^2);
HE = -((gu/u)*D[W*Dgg, u] + D[W*Dga, ua])/W;
HP = -((gu/u)*D[W*Dga, u] + D[W*Daa, ua])/W;
r012 = Expand[(HE - aa*(mu*up2 - (2 + 4*up2)/gu))*gu];
r013 = Expand[(HP + aa*ua*(2 - mu*up2/gu - Fu/(8*u^2) + (2/u^2 - 4*ua^2/u^4)*Hu))*gu*u^6];

(* Variational algebra: q = Pq* + (1 - P)q*. Scalar model for one orthogonal
   component y* and the closure penalty kappa, Eqs. (9.9), (10.1)-(10.3). *)
qk = ys/(1 + kap);
r014 = Together[D[(y - ys)^2 + kap*y^2, y] /. y -> qk];
r015 = Together[((qk - ys)^2 + kap*qk^2) - kap*ys^2/(1 + kap)];
(* K_kappa = (K_ex + kappa K_2)/(1 + kappa) with K_2 - K_ex = ys^2. *)
r016 = Together[(Kex + kap*ys^2/(1 + kap)) - (Kex + kap*(Kex + ys^2))/(1 + kap)];
(* Two-mode normal equations: minimum over (a_E, a_P) of sum_modes N (a_E + a_P eta - q_star)^2
   gives K_2 = K_D - b_E^2/G_E - b_P^2/G_P for diagonal G. *)
fq = GEs*aE^2 + GPs*aP^2 - 2*bE*aE - 2*bP*aP;
r017 = Together[(fq /. {aE -> bE/GEs, aP -> bP/GPs}) + bE^2/GEs + bP^2/GPs];
r018 = Together[D[fq, aE] /. aE -> bE/GEs];
(* Bath: (G + Lambda) a = b and the residual exchange b - G (G + Lambda)^(-1) b
   = Lambda (G + Lambda)^(-1) b in one dimension. *)
r019 = Together[(bb - G1*bb/(G1 + L1)) - L1*bb/(G1 + L1)];
