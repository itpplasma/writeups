(* Section 3.1: harmonic sums and their summation into Eq. (3.8).
   Every r### must evaluate to 0. *)

(* Parseval integrals in closed form. With D = 1 - z cos(phi),
   int_0^{2 pi} D^-k dphi = (-1)^(k-1)/(k-1)! d^(k-1)/dl^(k-1) [2 pi/Sqrt[l^2 - z^2]] at l = 1. *)
J0 = 2*Pi/Sqrt[l^2 - z^2];
I3 = (D[J0, l, l]/2) /. l -> 1;
I4 = (-D[J0, l, l, l]/6) /. l -> 1;
I5 = (D[J0, l, l, l, l]/24) /. l -> 1;
(* z^2 sin^2 = (z^2 - 1) + 2 D - D^2 and (cos - z)^2 = ((1 - z^2) - D)^2/z^2. *)
(* Residuals are multiplied by (1 - z^2)^(9/2) z^2, which makes them polynomial. *)
r001 = Expand[Expand[((z^2 - 1)*I5 + 2*I4 - I3 - 4*Pi*z^2*(4 + z^2)/(16*(1 - z^2)^(7/2)))*(1 - z^2)^(9/2)]];
r002 = Expand[Expand[(((1 - z^2)^2*I5 - 2*(1 - z^2)*I4 + I3)/z^2 - 4*Pi*(4 + 3*z^2)/(16*(1 - z^2)^(5/2)))*z^2*(1 - z^2)^(9/2)]];
(* The integrand rewrites themselves, with cos = (1 - D)/z. *)
c = (1 - DD)/z;
r003 = Expand[z^2*(1 - c^2) - ((z^2 - 1) + 2*DD - DD^2)];
r004 = Expand[z^2*(c - z)^2 - ((1 - z^2) - DD)^2];

(* Inserting the sums into Eq. (3.2). Q = q^2 - up^2 sigma, z^2 = up^2 sigma/q^2,
   1 - z^2 = Q/q^2 and RQ = Sqrt[Q] (q > 0). *)
z2 = up^2*sig/q^2;
sumO = z2*(4 + z2)/(16*(RQ/q)^7);
sumX = (4 + 3*z2)/(16*(RQ/q)^5);
lhs = g/q^3*(up^2/g^2*sumX + (g*eta - ua)^2/(g^2*sig)*sumO);
rhs = up^2/(16*g)*((4*q^2 + 3*up^2*sig)/RQ^5 + (g*eta - ua)^2*(4*q^2 + up^2*sig)/RQ^7);
r005 = Together[lhs - rhs];

(* Prefactor of Eq. (3.2): C0 * 2 pi (azimuth) * frequency Jacobian
   omega^2/(n wce) * (g/omega) I_RJ with I_RJ = omega^2 T/(8 pi^3 c^2) and
   omega = n wce/q, equals nu0 g n^2/q^3 with nu0 = e^2 wce^2 T/(m^2 c^5). *)
om = n*wce/q;
C0 = 4*Pi^2*e^2/(m^2*c^3);
IRJ = om^2*T/(8*Pi^3*c^2);
nu0 = e^2*wce^2*T/(m^2*c^5);
r006 = Together[C0*2*Pi*om^2/(n*wce)*(g/om)*IRJ - nu0*g*n^2/q^3];
