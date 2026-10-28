(* Section 4: the two-electron kernel and the absorption normalisation.
   Every r### must evaluate to 0. *)

(* Common photon of two resonances g - eta ua = n s, gp - eta uap = np s,
   Eq. (4.3), and the Jacobian |d(r, r')/d(s, eta)| = |Delta|. *)
Dl = np*ua - n*uap;
etas = (np*g - n*gp)/Dl;
ss = (ua*gp - g*uap)/Dl;
r001 = Together[g - etas*ua - n*ss];
r002 = Together[gp - etas*uap - np*ss];
jac = Det[{{D[g - n*s - eta*ua, s], D[g - n*s - eta*ua, eta]}, {D[gp - np*s - eta*uap, s], D[gp - np*s - eta*uap, eta]}}];
r003 = Expand[jac - (n*uap - np*ua)];

(* Photon-space prefactor: C0 * 2 pi * (d omega = wce ds/s^2) * I_RJ/omega
   with omega = wce/s equals nu0/s^3, nu0 = e^2 wce^2 T/(m^2 c^5). *)
om = wce/s;
C0 = 4*Pi^2*e^2/(m^2*c^3);
IRJ = om^2*T/(8*Pi^3*c^2);
nu0 = e^2*wce^2*T/(m^2*c^5);
r004 = Together[C0*2*Pi*(wce/s^2)*IRJ/om - nu0/s^3];
(* Denominator: d^3p f0 = (ne mu/(2 K2)) e^(-mu g) g dg dua, so
   int dP g D delta f0 = (ne mu/(2 K2)) S_M and P0 = 2 nu0 K2/(ne mu). *)
f0pref = ne*mu/(4*Pi*K2);
r005 = Together[f0pref*2*Pi - ne*mu/(2*K2)];
P0 = 2*e^2*wce^2*K2/(m*c^3*ne*mu^2);
r006 = Together[(nu0 /. T -> m*c^2/mu)/(ne*mu/(2*K2)) - P0];

(* Regular resonance coordinate x, Eq. (4.6): h^2 = (k s)^2 - sigma. *)
sig = 1 - eta^2;
gx = (k*s + eta*h*x)/sig;
ux = (k*s*eta + h*x)/sig;
r007 = Together[gx - eta*ux - k*s];
r008 = Together[Expand[(gx^2 - ux^2 - 1 - h^2*(1 - x^2)/sig) /. h -> Sqrt[k^2*s^2 - sig]]];
r009 = Together[(gx*eta - ux) + h*x];
r010 = Together[D[ux, x] - h/sig];
(* Bessel argument on resonance: lambda = n up sqrt(sigma)/(g - eta ua) = up sqrt(sigma)/s,
   and lambda^2 = b^2 (1 - x^2) with b = h/s. *)
r011 = Together[(h^2*(1 - x^2)/sig)*sig/s^2 - (h/s)^2*(1 - x^2)];
(* g^2 D^X = up^2 J'^2 and g^2 D^O = (g eta - ua)^2 J^2/sigma = h^2 x^2 J^2/sigma. *)
r012 = Together[(gx*eta - ux)^2/sig - h^2*x^2/sig];
(* Exponential: mu g = mu k s/sigma + a x with a = mu eta h/sigma. *)
r013 = Together[mu*gx - (mu*k*s/sig + (mu*eta*h/sig)*x)];

(* Tail bound: k s - |eta| h >= k s (1 - |eta|) because h <= k s, and
   sigma = (1 - |eta|)(1 + |eta|). *)
r014 = Expand[(k*s)^2 - h^2 - sig /. h^2 -> k^2*s^2 - sig];
r015 = Expand[(1 - et)*(1 + et) - (1 - et^2)];

(* Axis eta = 1: only n = 1 resonates, g - ua = s, up^2 = 2 s (g - gmin),
   gmin = (s + 1/s)/2. *)
ua1 = g - s;
r016 = Expand[g^2 - ua1^2 - 1 - 2*s*(g - (s + 1/s)/2)];
(* Both polarisations: D_1^X -> up^2/(4 g^2) and D_1^O -> up^2/(4 g^2) as sigma -> 0
   (lambda = up rs/s with rs = sqrt(sigma)). *)
r017 = Normal[Series[D[BesselJ[1, lm], lm]^2, {lm, 0, 0}]] - 1/4;
r018 = Expand[Normal[Series[BesselJ[1, up*rs/s]^2/rs^2, {rs, 0, 0}]]*s^2 - up^2/4];
(* S(s, 1) = int dg (up^2/4) e^(-mu g) from gmin; with t = mu (g - gmin):
   (s/2) e^(-mu gmin) mu^-2 int_0^oo t e^(-t) dt. *)
r019 = Integrate[t*Exp[-t], {t, 0, Infinity}] - 1;

(* Nonrelativistic perpendicular moments, Eq. (4.21): with x = w^2/(2 tau),
   w^3 e^(-w^2/(2 tau)) dw/(2 tau^2) = x e^(-x) dx, so Pi[w^(2j)] = (2 tau)^j (j+1)!. *)
r020 = Together[(w^3/(2*tau^2))*(w/tau)^(-1) - w^2/(2*tau)];
r021 = Integrate[x^1*Exp[-x], {x, 0, Infinity}] - Factorial[1];
r022 = Integrate[x^2*Exp[-x], {x, 0, Infinity}] - Factorial[2];
r023 = Integrate[x^3*Exp[-x], {x, 0, Infinity}] - Factorial[3];
r024 = Integrate[x^5*Exp[-x], {x, 0, Infinity}] - Factorial[5];

(* Series of the absorption integrals, Eqs. (4.14)-(4.17) and (B.1)-(B.3).
   Bessel equation identity used for the derivative square, with J'' eliminated. *)
Jpp = -Jp/zz - (1 - kk^2/zz^2)*J;
J2pp = 2*Jp^2 + 2*J*Jpp;
r025 = Expand[(zz^2/2)*J2pp + (zz/2)*2*J*Jp + (zz^2 - kk^2)*J^2 - zz^2*Jp^2];
Akl[k_, l_] := Factorial[2*k + 2*l]/(Factorial[l]*Factorial[2*k + l]*Factorial[k + l]^2);
Bkl[k_, l_] := (2*(k + l)^2 - k^2)*Akl[k, l] - 4*If[l > 0, Akl[k, l - 1], 0];
(* Coefficients against the Taylor series of J_k^2 and z^2 J_k'^2, k = 1, 2. *)
s1 = Expand[Normal[Series[BesselJ[1, z]^2, {z, 0, 8}]]];
s2 = Expand[Normal[Series[BesselJ[2, z]^2, {z, 0, 10}]]];
t1 = Expand[Normal[Series[z^2*D[BesselJ[1, z], z]^2, {z, 0, 8}]]];
t2 = Expand[Normal[Series[z^2*D[BesselJ[2, z], z]^2, {z, 0, 10}]]];
r026 = Expand[s1 - ((-1)^0*Akl[1, 0]*(z/2)^2 + (-1)^1*Akl[1, 1]*(z/2)^4 + (-1)^2*Akl[1, 2]*(z/2)^6 + (-1)^3*Akl[1, 3]*(z/2)^8)];
r027 = Expand[s2 - ((-1)^0*Akl[2, 0]*(z/2)^4 + (-1)^1*Akl[2, 1]*(z/2)^6 + (-1)^2*Akl[2, 2]*(z/2)^8 + (-1)^3*Akl[2, 3]*(z/2)^10)];
r028 = Expand[t1 - ((-1)^0*Bkl[1, 0]*(z/2)^2 + (-1)^1*Bkl[1, 1]*(z/2)^4 + (-1)^2*Bkl[1, 2]*(z/2)^6 + (-1)^3*Bkl[1, 3]*(z/2)^8)];
r029 = Expand[t2 - ((-1)^0*Bkl[2, 0]*(z/2)^4 + (-1)^1*Bkl[2, 1]*(z/2)^6 + (-1)^2*Bkl[2, 2]*(z/2)^8 + (-1)^3*Bkl[2, 3]*(z/2)^10)];
(* Ratio (B.3) at a few indices. *)
ratio[k_, l_] := (2*k + 2*l + 2)*(2*k + 2*l + 1)/((l + 1)*(2*k + l + 1)*(k + l + 1)^2);
r030 = Akl[1, 3]/Akl[1, 2] - ratio[1, 2];
r031 = Akl[3, 4]/Akl[3, 3] - ratio[3, 3];
