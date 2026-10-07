(* Native FortSym exact rational jets, not a convergence proof.
   h = full radial spacing. k=K=gvv/J; q=K*sqrt(s).
   x=normalized even lambda density; y=regular odd density.
   Jets assume s>0, smooth chart, both neighbouring half cells. *)
ClearAll["Global`*"];
kp = k0+h*k1/2+h^2*k2/8+h^3*k3/48+h^4*k4/384;
km = k0-h*k1/2+h^2*k2/8-h^3*k3/48+h^4*k4/384;
qp = q0+h*q1/2+h^2*q2/8+h^3*q3/48+h^4*q4/384;
qm = q0-h*q1/2+h^2*q2/8-h^3*q3/48+h^4*q4/384;
xp = x0+h*x1+h^2*x2/2+h^3*x3/6+h^4*x4/24;
xm = x0-h*x1+h^2*x2/2-h^3*x3/6+h^4*x4/24;
yp = y0+h*y1+h^2*y2/2+h^3*y3/6+h^4*y4/24;
ym = y0-h*y1+h^2*y2/2-h^3*y3/6+h^4*y4/24;
average = (kp*(xp+x0)+km*(xm+x0)+qp*(yp+y0)+qm*(ym+y0))/4;
alternative = ((kp+km)*x0+(qp+qm)*y0)/2;
delta = alternative-average;
r001 = Together[delta/.h->0];
r002 = Together[D[delta,h]/.h->0];
r003 = Together[(D[D[delta,h],h]/.h->0)/2+(k0*x2+k1*x1+q0*y2+q1*y1)/4];
r004 = Together[D[D[D[delta,h],h],h]/.h->0];
hybrid = (1-beta)*average+beta*alternative;
r005 = Together[hybrid-average-beta*delta];
(* Explicit exact-circle toroidal vacuum field with constant native B_phi. *)
denom = R0^2-a^2*rho^2*c^2;
K = -2*(R0+a*rho*c)/a^2;
aa = -a^2*f/2;
x = aa*R0/denom;
y = -aa*a*c/denom;
r006 = Together[K*(x+rho*y)-f];
r007 = Together[D[Together[K*(x+rho*y)],c]];
(* Constant radial density jets make the two stencils exactly equal. *)
r008 = Together[delta/.{x1->0,x2->0,x3->0,x4->0,y1->0,y2->0,y3->0,y4->0}];
