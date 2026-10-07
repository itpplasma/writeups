(* Native exact correspondence, not a convergence or source-execution proof.
   RH basis; g=Jacobian!=0, 1+lambda_t!=0, rho>0 away from axis.
   rr=F_rho, hh=g*J^rho, bt=B^theta,bz=B^zeta. *)
ClearAll["Global`*"];
(* Straight-field-line derivative d(theta+lambda)/dzeta=iota. *)
r001 = Together[((iota-lz)/(1+lt))*(1+lt)+lz-iota];
(* Native toroidal flux derivative under s=rho^2. *)
r002 = Together[D[flux*rho^2/(2*Pi),rho]-flux*rho/Pi];
(* Native curl-current route equals the direct covariant radial curl-cross route. *)
r003 = Together[g*(((brz-bzr)/(mu*g))*bz-((btr-brt)/(mu*g))*bt)-pp-((brz-bzr)*bz+(brt-btr)*bt)/mu+pp];
(* Signed physical helical coefficient is -hh, unlike optimizer raw +hh. *)
r004 = Together[-g*jr*bz-(-bz*hh)/.hh->g*jr];
r005 = Together[g*jr*bt-(bt*hh)/.hh->g*jr];
(* The isolated helical sign does not change a zero-target squared cost. *)
r006 = Together[(rr^2+hh^2)-(rr^2+(-hh)^2)];
(* Full physical norm includes metric cross term. *)
r007 = Together[rr^2*grr+hh^2*bz^2*gtt+hh^2*bt^2*gzz-2*rr*hh*bz*grt+2*rr*hh*bt*grz-2*hh^2*bz*bt*gtz-(rr^2*grr+hh^2*(bz^2*gtt+bt^2*gzz-2*bz*bt*gtz)-2*rr*hh*(bz*grt-bt*grz))];
(* Coordinate reversal preserves physical toroidal/poloidal circulation. *)
r008 = Together[(-iota)*(-1)-iota];
(* Exact chain rule for a cubic P(s), rather than a rho spline fit. *)
r009 = Together[D[a*rho^6+b*rho^4+c*rho^2+d,rho]-2*rho*(3*a*rho^4+2*b*rho^2+c)];
(* SPD metric example: full norm 3, omitted-cross norm 4. *)
r010 = Together[(1^2*2+1^2*(1^2*2+0^2*2)-2*1*1*(1*(1/2)-0*0))-3];
