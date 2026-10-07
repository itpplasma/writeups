(* Native axisymmetric half-cell sector, signgs=-1 and gamma0.
   Contravariant numerators u,v and signed Jacobian j; metrics gu,gv.
   Pressure is already multiplied by mu0. Fixed numerators in metric sector.
   Native angular quadrature and radial weight are separate assumptions. *)
ClearAll["Global`*"];
energy=-(gu*u^2+gv*v^2)/(2*j)+p*j;
r001=Together[D[energy,gu]+u^2/(2*j)];
r002=Together[D[energy,gv]+v^2/(2*j)];
r003=Together[D[energy,j]-(p+(gu*u^2+gv*v^2)/(2*j^2))];
r004=Together[D[energy,v]+gv*v/j];
(* Exact chain under a normalized lambda-density variation v -> v+L*e. *)
r005=Together[(D[energy/.v->v+L*e,e]/.e->0)+L*gv*v/j];
(* Finite-stencil hybrid difference in lambda dual, no energy identity assumed. *)
r006=Together[-L*((1-b)*C+b*A)-(-L*C)-(-L*b*(A-C))];
(* Deliberately omitting the lambda normalization must be rejected. *)
r007=Together[(-L*gv*v/j+gv*v/j)/.{L->2,gv->3,v->4,j->2}];
