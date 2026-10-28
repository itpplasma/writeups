(* Section 3: the photon-angle integral of the harmonic-summed tensor.
   Run after angular_antiderivatives.wl (run_cas.sh concatenates them).
   Variables: g = gamma, ua = u_par, eta = cos(theta), u^2 = g^2 - 1,
   up2 = u_perp^2 = g^2 - 1 - ua^2, au = arsinh(u)/u.
   Every binding r### must evaluate to 0. *)
up2 = g^2 - 1 - ua^2;
Q = (g^2 - 1)*eta^2 - 2*g*ua*eta + 1 + ua^2;
q = g - eta*ua;
sig = 1 - eta^2;
P5 = 4*q^2 + 3*up2*sig;
P7 = (g*eta - ua)^2*(4*q^2 + up2*sig);

(* Q = q^2 - u_perp^2 sigma, Eq. (3.7), and its values on the axis. *)
r001 = Expand[Q - (q^2 - up2*sig)];
r002 = Expand[(Q /. eta -> 1) - (g - ua)^2];
r003 = Expand[(Q /. eta -> -1) - (g + ua)^2];

(* Derivative rule used for every candidate:
   d/deta [R Q^(-n)] Q^(n+1) = R' Q - n R Q'. Checked for generic
   polynomials R, Q1 at n = 3/2 and n = 5/2. *)
R1 = a0 + a1*eta + a2*eta^2 + a3*eta^3;
Q1 = b0 + b1*eta + b2*eta^2;
r004 = Expand[D[R1*Q1^(-3/2), eta]*Q1^(5/2) - (D[R1, eta]*Q1 - 3/2*R1*D[Q1, eta])];
r005 = Expand[D[R1*Q1^(-5/2), eta]*Q1^(7/2) - (D[R1, eta]*Q1 - 5/2*R1*D[Q1, eta])];
r006 = Simplify[D[Q1^(-1/2), eta]*Q1^(3/2) + D[Q1, eta]/2];

(* Antiderivatives of eta^j P5/Q^(5/2) and eta^j P7/Q^(7/2):
   (Rn' Q - n Rn Q' + Cn Q^((k-1)/2)) = Dn eta^j P. *)
r010 = Expand[D[Ra0, eta]*Q - 3/2*Ra0*D[Q, eta] + Ca0*Q^2 - Da0*P5];
r011 = Expand[D[Rb0, eta]*Q - 5/2*Rb0*D[Q, eta] + Cb0*Q^3 - Db0*P7];
r012 = Expand[D[Ra1, eta]*Q - 3/2*Ra1*D[Q, eta] + Ca1*Q^2 - Da1*eta*P5];
r013 = Expand[D[Rb1, eta]*Q - 5/2*Rb1*D[Q, eta] + Cb1*Q^3 - Db1*eta*P7];
r014 = Expand[D[Ra2, eta]*Q - 3/2*Ra2*D[Q, eta] + Ca2*Q^2 - Da2*eta^2*P5];
r015 = Expand[D[Rb2, eta]*Q - 5/2*Rb2*D[Q, eta] + Cb2*Q^3 - Db2*eta^2*P7];

(* The logarithmic part L = arsinh((u^2 eta - g ua)/u_perp)/u has
   L'^2 Q = 1, i.e. u^2 Q = u_perp^2 + (u^2 eta - g ua)^2 with g^2 = 1 + u^2.
   Its endpoint difference is L(1) - L(-1) = 2 au. *)
r016 = Expand[(g^2 - 1)*Q - up2 - ((g^2 - 1)*eta - g*ua)^2];

(* Endpoints. sqrt Q(+-1) = g -+ ua, so with w = (g - ua)^5 (g + ua)^5 the
   integrals I_j = Phi_j(1) - Phi_j(-1) satisfy w Dn I_j = Nj below. *)
Ia[R_, j_] := (R /. eta -> 1)*(g - ua)^2*(g + ua)^5 - (R /. eta -> -1)*(g + ua)^2*(g - ua)^5;
Ib[R_, j_] := (R /. eta -> 1)*(g + ua)^5 - (R /. eta -> -1)*(g - ua)^5;
w = (g - ua)^5*(g + ua)^5;

(* I_0 = 32 g/3 and I_1 = 32 ua/3: D^{gg} = a u_perp^2, D^{g u_par} = a u_par u_perp^2/g. *)
r020 = Expand[Ia[Ra0, 0] + Ib[Rb0, 0] - Da0*w*32*g/3];
r021 = Expand[Ia[Ra1, 1] + Ib[Rb1, 1] - Da1*w*32*ua/3];

(* I_2 = (32 g/(3 u^2)) [F/16 + H ua^2/u^2], Eq. (3.15), with
   g u^2 F = 10 g u^2 + 3 g - (9 u^2 + 3 g^2) au,
   g u^2 G = 10 g u^2 + 15 g - (21 u^2 + 15 g^2) au, H = u^2 - 1 - G/16.
   Db2 = 3 u^6 up2 and Db2/Da2 = u^2. *)
u2 = g^2 - 1;
gu2F = 10*g*u2 + 3*g - (9*u2 + 3*g^2)*au;
gu2G = 10*g*u2 + 15*g - (21*u2 + 15*g^2)*au;
expectedDb2 = 32*up2*(u2*gu2F/16 + ua^2*u2*g*(u2 - 1) - ua^2*gu2G/16);
r022 = Expand[u2*(Ia[Ra2, 2] + 2*Ca2*au*w) + Ib[Rb2, 2] + 2*Cb2*au*w - w*expectedDb2];
r023 = Expand[Db2 - 3*u2^3*up2];
r024 = Expand[Db2 - u2*Da2];
