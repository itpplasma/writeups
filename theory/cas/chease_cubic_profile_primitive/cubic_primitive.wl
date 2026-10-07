(* Actual CHEASE ISOFUN cubic-cell primitive. M0/M1 are second derivatives.
   Coordinate t=(psi-psi0)/h; h!=0. No equilibrium accuracy claim. *)
ClearAll["Global`*"];
spline=(1-t)*f0+t*f1+h^2*((((1-t)^3-(1-t))*M0)+(t^3-t)*M1)/6;
primitive=f0*(t-t^2/2)+f1*t^2/2+h^2*(M0*(-t^2+t^3-t^4/4)+M1*(t^4/4-t^2/2))/6;
integral=h*((primitive/.t->1)-(primitive/.t->0));
cell=h*((f0+f1)/2-h^2*(M0+M1)/24);
r001=Together[D[primitive,t]-spline];
r002=Together[integral-cell];
r003=Together[(upper-cell)-upper+integral];
r004=Together[(lower+cell)-lower-integral];
wrongDown=h*((f0+f1)/2-h^3*(M0+M1)/48);
wrongUp=h*((f0+f1)/2+h^3*(M0+M1)/48);
b001=Together[(wrongDown-integral)/.{h->1,M0->1,M1->1}];
b002=Together[(wrongUp-integral)/.{h->1,M0->1,M1->1}];
