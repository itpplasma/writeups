(* Conditional jet-algebra correspondence, executed by native FortSym.
   Canonical physical RH (R,phi,Z), R>0, mu>0;
   B=(-psi_Z/R,F/R,psi_R/R), F=F(psi), p=p(psi).
   pr,pz,prr,pzz are independent jets of the smooth poloidal flux.
   fp=dF/dpsi, pp=dp/dpsi. No solution/convergence claim. *)
ClearAll["Global`*"];
lap = prr-pr/R+pzz;
br = -pz/R;
bphi = f/R;
bz = pr/R;
(* Derivatives of physical components; cylindrical curl includes bphi/R. *)
brz = -pzz/R;
bzr = prr/R-pr/R^2;
bpz = fp*pz/R;
bpr = fp*pr/R-f/R^2;
jr = -bpz/mu;
jphi = (brz-bzr)/mu;
jz = (bpr+bphi/R)/mu;
res = lap+f*fp+mu*R^2*pp;
(* Curl components and independent scalar GS residual projections. *)
r001 = Together[jphi+lap/(mu*R)];
r002 = Together[jr+fp*pz/(mu*R)];
r003 = Together[jz-fp*pr/(mu*R)];
r004 = Together[jphi*bz-jz*bphi-pp*pr+res*pr/(mu*R^2)];
r005 = Together[jr*bphi-jphi*br-pp*pz+res*pz/(mu*R^2)];
r006 = Together[jz*br-jr*bz];
(* DESC native chi=-psi: reversing every flux derivative gives the
   same physical GS equation after multiplication by -1. *)
r007 = Together[(-lap)+f*(-fp)+mu*R^2*(-pp)+res];
(* Native profile chain: rho=sqrt(s), chi_c'=-Phi*rho*iota_D/Pi. *)
r008 = Together[D[-Phi*(a*rho^2+b*rho^4)/(2*Pi),rho]+Phi*rho*(a+2*b*rho^2)/Pi];
(* Counterexample: nonlinear least-squares stationary point can retain
   nonzero force residual. Exact zero below verifies gradient at x=0. *)
r009 = Together[D[(x^2+1)^2/2,x]/.x->0];
r010 = Together[((x^2+1)/.x->0)-1];
