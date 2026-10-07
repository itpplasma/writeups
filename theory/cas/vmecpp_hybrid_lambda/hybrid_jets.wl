(* Native FortSym exact single-sector jet lemma.
   Apply independently to (K,x) and (K*sqrt(s),y), then add.
   h=full radial spacing, s>0, smooth jets, both half neighbours. *)
ClearAll["Global`*"];
kp = k0+h*k1/2+h^2*k2/8+h^3*k3/48+h^4*k4/384;
km = k0-h*k1/2+h^2*k2/8-h^3*k3/48+h^4*k4/384;
xp = x0+h*x1+h^2*x2/2+h^3*x3/6+h^4*x4/24;
xm = x0-h*x1+h^2*x2/2-h^3*x3/6+h^4*x4/24;
average = (kp*(xp+x0)+km*(xm+x0))/4;
alternative = (kp+km)*x0/2;
delta = alternative-average;
r001 = Together[delta/.h->0];
r002 = Together[D[delta,h]/.h->0];
r003 = Together[(D[D[delta,h],h]/.h->0)/2+(k0*x2+k1*x1)/4];
r004 = Together[D[D[D[delta,h],h],h]/.h->0];
(* Linear composition is independent of the jet polynomial. *)
r005 = Together[(1-beta)*(ce+co)+beta*(ae+ao)-(ce+co)-beta*((ae-ce)+(ao-co))];
denom = R0^2-a^2*rho^2*c^2;
K = -2*(R0+a*rho*c)/a^2;
aa = -a^2*f/2;
x = aa*R0/denom;
y = -aa*a*c/denom;
r006 = Together[K*(x+rho*y)-f];
r007 = Together[D[Together[K*(x+rho*y)],c]];
r008 = Together[delta/.{x1->0,x2->0,x3->0,x4->0}];
(* Negative control: wrong h^2 coefficient, known nonzero scalar jet. *)
wrong = (D[D[delta,h],h]/.h->0)/2+(k0*x2+k1*x1)/8;
r009 = Together[wrong/.{k0->1,k1->1,x1->3,x2->2}];
(* Axis m1 Fourier moment: 2<cos^4>=3/4, 2<cos^6>=5/8.
   Native closure multiplies m1(y(h)) by Phi'(0)/Phi'(h). *)
axisratio = (1-t/2-t^2/8)*(1+3*t/4+5*t^2/8);
r010 = Together[(D[axisratio,t]/.t->0)-1/4];
(* Leading derivative RMS after the inner-half and outer-average factors.
   beta<1,f>0; two sqrt(2) denominators multiply to2. *)
normcoef = (1-beta)*(-2*R0/a^2)*(-aa*a^3/(4*R0^4))/(4*2);
r011 = Together[-normcoef-(1-beta)*a^3*f/(32*R0^3)];
(* Pure toroidal constant F/R has zero physical cylindrical curl. *)
r012 = Together[D[f/R,R]+f/R^2];
