// Actual pinned native constraint kernel against independent exact Fourier laws.
#include "vmecpp/vmec/ideal_mhd_model/constraint_force_kernel.h"
#include <cmath>
#include <iostream>
#include <stdexcept>
#include <vector>
constexpr double pi=3.14159265358979323846;
constexpr int M=24,N=256,H=N/2+1;
using V=std::vector<double>;
void require(bool ok,const char* msg){if(!ok)throw std::runtime_error(msg);}
V filter(const V& input,bool asym,double multiplier=1.) {
 V fac(M),tc(1,multiplier),si(M*H),ci(M*H),sf(M*H),cf(M*H);
 // Same public basis formulas as FourierBasis; expectations below are closed
 // continuous harmonics rather than a second DFT/normalization implementation.
 for(int m=0;m<M;++m){if(m>0&&m<M-1)fac[m]=.25/std::pow(m*(m+1.),2);
  for(int l=0;l<H;++l){double t=2*pi*l/N,scale=m?std::sqrt(2.):1.;int j=m*H+l;
   sf[j]=scale*std::sin(m*t);cf[j]=scale*std::cos(m*t);
   si[j]=sf[j]/(H-1);ci[j]=cf[j]/(H-1);if(l==0||l==H-1)ci[j]*=.5;}}
 V co(1,1),sn(1),gs(1),gc(1),cc(1),ss(1),a(N),refl(H),out(N);
 vmecpp::ComputeDeAliasConstraintForce(input.data(),fac.data(),tc.data(),
  si.data(),ci.data(),co.data(),sn.data(),sf.data(),cf.data(),1,2,1,
  asym?N:H,H,N,M,0,0,asym,gs.data(),gc.data(),cc.data(),ss.data(),
  a.data(),refl.data(),out.data());
 return out;
}
double gain(int m){return m>0&&m<M-1?.25/std::pow(m*(m+1.),2):0.;}
int main(){
 double worst=0.;int checks=0;
 for(bool asym:{false,true})for(int m:{0,1,2,21,22,23,24,46})
  for(bool cosine:{false,true}){
   if(!asym&&cosine)continue;
   V input(N);for(int l=0;l<N;++l){double t=2*pi*l/N;input[l]=cosine?std::cos(m*t):std::sin(m*t);}
   auto out=filter(input,asym);int stop=asym?N:H;
   for(int l=0;l<stop;++l){double err=std::abs(out[l]-gain(m)*input[l]);worst=std::max(worst,err);require(err<2e-14,"native bandpass closed harmonic mismatch");}
   ++checks;
  }
 // Exact circle/ellipse m0,m1 has P_m=m(m-1)=0 and zero offset => C=0.
 V zero(N);auto null=filter(zero,true);for(double x:null)require(x==0.,"circle zero constraint");
 // R=R0+a*cos(theta)+eps*cos(k*theta), Z=a*sin(theta).
 // C=P_k eps*cos(k theta)*(-a sin(theta)-k eps sin(k theta)).
 // Independent product-to-sum law exposes modes k-1,k+1,2k.
 for(int k:{2,12,23}){
  const double a=.62,e=.017,P=k*(k-1.);V input(N),expected(N);
  for(int l=0;l<N;++l){double t=2*pi*l/N;
   input[l]=P*e*std::cos(k*t)*(-a*std::sin(t)-k*e*std::sin(k*t));
   double law=-a*P*e/2*(std::sin((k+1)*t)-std::sin((k-1)*t))-k*P*e*e/2*std::sin(2*k*t);
   require(std::abs(law-input[l])<3e-13,"manufactured exact convolution mismatch");
   expected[l]=-a*P*e/2*(gain(k+1)*std::sin((k+1)*t)-gain(k-1)*std::sin((k-1)*t))-k*P*e*e/2*gain(2*k)*std::sin(2*k*t);}
  auto out=filter(input,true);for(int l=0;l<N;++l){double err=std::abs(out[l]-expected[l]);worst=std::max(worst,err);require(err<2e-14,"manufactured geometry native filter mismatch");}
  V cr(N),cz(N),rt(N),zt(N),offset(N),be(N),bo(N),ze(N),zo(N),fe(N),fo(N),fz(N),fzo(N);
  double root=std::sqrt(.5);
  for(int l=0;l<N;++l){double t=2*pi*l/N;cr[l]=P*e*std::cos(k*t);rt[l]=-a*std::sin(t)-k*e*std::sin(k*t);zt[l]=a*std::cos(t);}
  vmecpp::AddConstraintForces(cr.data(),offset.data(),cz.data(),offset.data(),rt.data(),zt.data(),out.data(),&root,N,1,1,2,be.data(),bo.data(),ze.data(),zo.data(),fe.data(),fo.data(),fz.data(),fzo.data());
  double weak=0.;
  for(int l=0;l<N;++l){double t=2*pi*l/N;
   require(std::abs(bo[l]-root*be[l])<1e-15,"odd radial chain");
   weak+=(P*fe[l]*std::cos(k*t)-k*be[l]*std::sin(k*t))/N;}
  // Exact derivative of half<C,L C>, with FIXED filter/gains and zero offsets.
  double exact=a*a*P*P*e/8*(gain(k-1)+gain(k+1))+k*k*P*P*e*e*e/4*gain(2*k);
  require(std::abs(weak-exact)<2e-13,"native weak assembly analytic energy derivative");
  // Fixed boundary offsets survive; test exact nonzero-offset energy chain.
  const double d=.003;V rc0(N),zc0(N),actualC(N);
  for(int l=0;l<N;++l){double t=2*pi*l/N;rc0[l]=d*std::cos(k*t);}
  vmecpp::ComputeEffectiveConstraintForce(cr.data(),rc0.data(),cz.data(),zc0.data(),rt.data(),zt.data(),N,1,2,actualC.data());
  auto offsetG=filter(actualC,true);
  be.assign(N,0.);bo.assign(N,0.);ze.assign(N,0.);zo.assign(N,0.);
  vmecpp::AddConstraintForces(cr.data(),rc0.data(),cz.data(),zc0.data(),rt.data(),zt.data(),offsetG.data(),&root,N,1,1,2,be.data(),bo.data(),ze.data(),zo.data(),fe.data(),fo.data(),fz.data(),fzo.data());
  double offsetWeak=0.;
  for(int l=0;l<N;++l){double t=2*pi*l/N;offsetWeak+=(P*fe[l]*std::cos(k*t)-k*be[l]*std::sin(k*t))/N;}
  double offsetExact=a*a*P*(P*e-d)/8*(gain(k-1)+gain(k+1))+k*k*e*(P*e-d)*(2*P*e-d)/8*gain(2*k);
  require(std::abs(offsetWeak-offsetExact)<2e-13,"nonzero fixed-offset native weak derivative");
  auto disabled=filter(input,true,0.);for(double x:disabled)require(x==0.,"tcon0 not disabled");
  // Constant scalar C lies in excluded m0, despite nonzero magnitude.
  ++checks;
 }
 V constant(N,3.);auto dropped=filter(constant,true);for(double x:dropped)require(std::abs(x)<1e-14,"excluded m0");
 // Negative control: treating highest geometry mode as retained scalar is wrong.
 require(gain(23)==0.&&gain(22)>0.,"upper band edge negative control");
 std::cout<<"PASS "<<checks<<" exact harmonic/manufactured cases, max_abs="<<worst
          <<"; excluded scalar m0,23,24,46; tcon0 zero; no live TC24 residual claim\n";
}
