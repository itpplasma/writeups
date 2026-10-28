(* Section 5: integrable resonance degeneracy and harmonic control.
   Every r### must evaluate to 0. *)

(* Coincident-resonance density: int_{-e}^{e} db int_{-|b|}^{|b|} da/|b| = 4 e. *)
r001 = 2*Integrate[Integrate[1/b, {a, -b, b}], {b, 0, ep}] - 4*ep;

(* Kapteyn exponent: with z = w/sqrt(1 + w^2), sqrt(1 - z^2) = 1/sqrt(1 + w^2) and
   cosh(beta) = 1/z gives sinh(beta) = 1/w, i.e. beta = arsinh(1/w);
   the saddle of z sinh(beta) - beta. *)
z = w/Sqrt[1 + w^2];
r002 = Cancel[Together[1 - z^2 - 1/(1 + w^2)]];
r003 = Expand[(1/z)^2 - 1 - 1/w^2];
r004 = Expand[D[zz*Sinh[be] - be, be] /. Cosh[be] -> 1/zz];

(* Eta integral of the resonance weight and the polarisation bound. *)
F3 = 1/(2*ua*(g - eta*ua)^2);
r005 = Together[D[F3, eta] - 1/(g - eta*ua)^3];
r006 = Together[(F3 /. eta -> 1) - (F3 /. eta -> -1) - 2*g/(g^2 - ua^2)^2];
r007 = Expand[(g - eta*ua)^2 - (g*eta - ua)^2 - (g^2 - ua^2)*(1 - eta^2)];
(* nu0 int deta g/q^3 * 2 (1 + w^2)/g^2 with g^2 - ua^2 = 1 + w^2. *)
r008 = Together[(nu0*g*(2*g/(1 + w^2)^2)*2*(1 + w^2)/g^2) - 4*nu0/(1 + w^2)];

(* Tail sum (5.10): T(m) = q^m [m^2/(1-q) + 2 m q/(1-q)^2 + q (1+q)/(1-q)^3]
   telescopes, T(m) - T(m+1) = m^2 q^m, and T(m) -> 0. qm stands for q^m. *)
Tm[m_] := m^2/(1 - q) + 2*m*q/(1 - q)^2 + q*(1 + q)/(1 - q)^3;
r009 = Together[qm*Tm[m] - qm*q*Tm[m + 1] - m^2*qm];

(* Thermal tail (5.11). With A = sqrt(1 + w^2), int dv e^(-mu sqrt(A^2 + v^2)) = 2 A K1(mu A),
   so the tail is (ne mu/K2) int_{A_W}^oo (A^2 - 1) A^2 K1(mu A) dA. Antiderivative: *)
Phi = -((A^4 - A^2)*BesselK[2, mu*A]/mu + 2*A^3*BesselK[3, mu*A]/mu^2);
rec = {BesselK[4, mu*A] -> BesselK[2, mu*A] + 6/(mu*A)*BesselK[3, mu*A]};
rec3 = {BesselK[3, mu*A] -> BesselK[1, mu*A] + 4/(mu*A)*BesselK[2, mu*A]};
rec0 = {BesselK[0, mu*A] -> BesselK[2, mu*A] - 2/(mu*A)*BesselK[1, mu*A]};
dPhi = ((D[Phi, A] /. rec) /. rec3) /. rec0;
r010 = Expand[dPhi - (A^2 - 1)*A^2*BesselK[1, mu*A]];
(* -Phi(A_W) times ne mu/K2 is Eq. (5.11) with W^2 = A^2 - 1. *)
r011 = Expand[(-Phi*ne*mu/K2) - ne/K2*((A^2 - 1)*A^2*BesselK[2, mu*A] + 2*A^3*BesselK[3, mu*A]/mu)];
