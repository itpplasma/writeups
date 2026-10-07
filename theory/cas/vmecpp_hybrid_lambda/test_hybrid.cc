// Exercises the pinned native kernel; exact field oracle is independent.
#include "vmecpp/vmec/ideal_mhd_model/lambda_force_kernel.h"
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <vector>

constexpr double pi = 3.14159265358979323846;
constexpr double R0 = 6.2, a = .62, F = 32.86;
struct Result { double derivative, difference, exact_field_error, zero_blend; };

Result assess(double s, double h, double beta, int n, bool nonstationary = false,
              bool constant_density = false, bool native_axis = false) {
    std::vector<double> bsubu(2*n), bsubv(2*n), gvv(2*n), jac(2*n), zeros(2*n);
    std::vector<double> x(n), y(n), out(n), odd(n), scratch1(n), scratch2(n);
    std::vector<double> scratch3(n), scratch4(n), average(n), alternative(n);
    double roots[2] = {std::sqrt(s-h/2), std::sqrt(s+h/2)};
    double rootfull[] = {std::sqrt(s)}, blend[] = {beta};
    auto densities = [&](double v, double c) {
        double denominator = R0*R0-a*a*v*c*c;
        double A = -a*a*F/2;
        double xe = A*R0/denominator, yo = -A*a*c/denominator;
        if (constant_density) { xe = 1+.1*c; yo = .2*c; }
        if (nonstationary) xe += .02*v*v*(2*c*c-1);
        return std::pair<double,double>{xe,yo};
    };
    double axis_y_m1 = 0;
    if (native_axis) {
        if (std::abs(s-h) > 1e-14) throw std::runtime_error("axis test needs s=h");
        for (int k=0; k<n; ++k) {
            double c=std::cos(2*pi*k/n);
            axis_y_m1 += 2*densities(h,c).second*c/n;
        }
        // Native extrapolation acts on lambda BEFORE multiplication by Phi'.
        axis_y_m1 *= std::sqrt(R0*R0-a*a*h)/R0;
        // Independent closed Fourier integral, evaluated without cancellation.
        double A=-a*a*F/2;
        double expected=-2*A*a/(R0*R0*(1+std::sqrt(1-a*a*h/(R0*R0))));
        if (std::abs(axis_y_m1-expected)>1e-13)
            throw std::runtime_error("closed m1 Fourier integral failed");
    }
    double physical_error = 0;
    double mean_density = 0;
    for (int k=0; k<n; ++k) {
        double c = std::cos(2*pi*k/n);
        auto centre = densities(s,c);
        x[k]=centre.first; y[k]=centre.second;
        mean_density += (x[k]+std::sqrt(s)*y[k])/n;
        auto inner = densities(s-h,c), outer = densities(s+h,c);
        if (native_axis) inner.second = axis_y_m1*c;
        double kval[2];
        for (int q=0; q<2; ++q) {
            double r = R0+a*roots[q]*c;
            gvv[q*n+k]=r*r; jac[q*n+k]=-a*a*r/2;
            kval[q]=gvv[q*n+k]/jac[q*n+k];
            auto neighbour = q==0 ? inner : outer;
            double lh = (centre.first+neighbour.first)/2
                       +roots[q]*(centre.second+neighbour.second)/2;
            bsubv[q*n+k]=kval[q]*lh;
        }
        average[k]=(bsubv[k]+bsubv[n+k])/2;
        alternative[k]=(kval[0]+kval[1])*x[k]/2
                     +(kval[0]*roots[0]+kval[1]*roots[1])*y[k]/2;
        if (!constant_density && !nonstationary) {
            double K=-2*(R0+a*std::sqrt(s)*c)/(a*a);
            physical_error=std::max(physical_error,std::abs(K*(x[k]+std::sqrt(s)*y[k])-F));
        }
    }
    if (!constant_density && !nonstationary) {
        double expected_mean=-a*a*F/(2*std::sqrt(R0*R0-a*a*s));
        if (std::abs(mean_density-expected_mean)>1e-13)
            throw std::runtime_error("known toroidal flux-density mean failed");
    }
    // One interior full knot and its two neighbouring half knots.
    vmecpp::ComputeHybridLambdaForce(bsubu.data(),bsubv.data(),gvv.data(),jac.data(),
        zeros.data(),zeros.data(),x.data(),y.data(),roots,rootfull,blend,1,false,n,
        1,1,0,2,2,scratch1.data(),scratch2.data(),scratch3.data(),scratch4.data(),
        out.data(),odd.data(),nullptr,nullptr);
    double error=0, d2=0, difference2=0;
    const double dt=2*pi/n;
    auto value=[&](int k) { return -out[(k+n)%n]; };
    for (int k=0; k<n; ++k) {
        double expected=(1-beta)*average[k]+beta*alternative[k];
        error=std::max(error,std::abs(value(k)-expected));
        double d=(-value(k+2)+8*value(k+1)-8*value(k-1)+value(k-2))/(12*dt);
        d2+=d*d/n;
        difference2+=std::pow(alternative[k]-average[k],2)/n;
    }
    if (error>1e-12) throw std::runtime_error("native kernel/formula mismatch");
    return {std::sqrt(d2),std::sqrt(difference2),physical_error,error};
}

int main() {
    std::cout << std::setprecision(17);
    for (double s: {.25,.5,.75}) {
        double previous=0;
        for (int steps: {32,64,128,256,512}) {
            double h=1.0/steps, beta=.1*(1-s);
            auto r=assess(s,h,beta,2048);
            double ratio=previous ? previous/r.derivative : 0;
            if (steps>=128 && (ratio<3.8 || ratio>4.2))
                throw std::runtime_error("interior second-order rate failed");
            if (r.exact_field_error>1e-12) throw std::runtime_error("exact vacuum field failed");
            std::cout << "core," << s << ',' << steps << ',' << r.derivative
                      << ',' << r.difference << ',' << ratio << '\n';
            previous=r.derivative;
        }
    }
    double previous_axis=0;
    for (int steps: {32,64,128,256,512}) {
        double h=1.0/steps;
        auto analytic=assess(h,h,.1*(1-h),2048);
        auto native=assess(h,h,.1*(1-h),2048,false,false,true);
        double leading=a*a*a*F/(32*R0*R0*R0)*(1-.1*(1-h))*std::pow(h,1.5);
        double axis_ratio=previous_axis ? previous_axis/native.derivative : 0;
        if (steps>=128 && (axis_ratio<2.7 || axis_ratio>3))
            throw std::runtime_error("first-interior native-axis rate failed");
        if (steps==512 && std::abs(native.derivative/leading-1)>.01)
            throw std::runtime_error("axis leading-coefficient oracle failed");
        std::cout << "first_full," << steps << ',' << analytic.derivative
                  << ',' << native.derivative << ',' << axis_ratio
                  << ',' << native.derivative/leading << '\n';
        previous_axis=native.derivative;
    }
    auto zero=assess(.5,1.0/64,0,2048);
    auto constant=assess(.5,1.0/64,.05,2048,false,true);
    if (zero.zero_blend>1e-13 || constant.difference>1e-13)
        throw std::runtime_error("zero-weight/constant-density oracle failed");
    auto wrong32=assess(.5,1.0/32,.05,2048,true);
    auto wrong512=assess(.5,1.0/512,.05,2048,true);
    if (wrong512.derivative<.1 || wrong32.derivative/wrong512.derivative>1.1)
        throw std::runtime_error("nonstationary rejection control failed");
    auto fine=assess(.5,1.0/512,.05,4096);
    auto coarse=assess(.5,1.0/512,.05,2048);
    if (std::abs(fine.derivative/coarse.derivative-1)>1e-5)
        throw std::runtime_error("angular diagnostic refinement failed");
    std::cout << "negative," << wrong32.derivative << ',' << wrong512.derivative << '\n';
    std::cout << "angular," << coarse.derivative << ',' << fine.derivative << '\n';
    std::cout << "PASS native hybrid manufactured oracles\n";
}
