(* Sections 6-7: threshold cusp and line broadening. Every r### must be 0. *)

(* Opening of the fundamental absorbing harmonic: J1'(0) = 1/2, J1(x) ~ x/2. *)
r001 = Normal[Series[D[BesselJ[1, x], x]^2, {x, 0, 0}]] - 1/4;
r002 = Normal[Series[BesselJ[1, x]^2/x^2, {x, 0, 0}]] - 1/4;
r003 = Integrate[(1 - x^2)/4, {x, -1, 1}] - 1/3;
r004 = Integrate[x^2*(1 - x^2)/4, {x, -1, 1}] - 1/15;
(* With h^3 = delta^(3/2) and b^2 = delta/s^2: S_O ~ delta^(5/2) e/(15 s^2 sigma^2). *)
r005 = Expand[de^(3/2)*(de/s^2)*(1/15) - de^(5/2)/(15*s^2)];

(* Reciprocal expansion (6.4). *)
r006 = Together[1/(B + aX*d32) - (1/B - aX*d32/B^2 + aX^2*d32^2/(B^2*(B + aX*d32)))];
(* Second derivative of the cusp: (delta^(3/2))'' = (3/4) delta^(-1/2). *)
r007 = Expand[D[de^(3/2), de, de] - (3/4)*de^(-1/2)];

(* Counterstreaming slice: g - eta v = n s, g + eta v = np s. *)
sol = {s -> 2*g/(n + np), eta -> (np - n)*g/((n + np)*v)};
r008 = Together[(g - eta*v - n*s) /. sol];
r009 = Together[(g + eta*v - np*s) /. sol];
(* Fundamental threshold s^2 = 1 - eta^2 at g = N v/sqrt(d^2 + 4 v^2). *)
thr = {g -> NN*v/Sqrt[dd^2 + 4*v^2]};
r010 = Together[Expand[((2*g/NN)^2 - (1 - (dd*g/(NN*v))^2)) /. thr]];
r011 = Together[Expand[((dd*g/(NN*v))^2 /. thr) - dd^2/(dd^2 + 4*v^2)]];

(* Gaussian broadening of x_+^(3/2), Eq. (7.2): substitution t = l y. *)
(* For l, y > 0: ((l y)^(3/2))^2 = l^3 y^3, and the l from dt cancels 1/l. *)
r012 = Expand[((l*y)^(3/2))^2 - l^3*y^3];
r013 = Expand[-(x - l*y)^2/(2*l^2) - (-x^2/(2*l^2) - y^2/2 + x*y/l)];
r014 = Gamma[5/2] - 3*Sqrt[Pi]/4;
