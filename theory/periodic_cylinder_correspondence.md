# Periodic-cylinder equilibrium and the toroidal limit

The periodic screw pinch is an exact one-dimensional equilibrium benchmark. Freidberg's [Ideal MHD, Chapter 5, pp.85–122](https://www.cambridge.org/core/books/abs/ideal-mhd/equilibrium-onedimensional-configurations/611F4B794D9C6541921CB9DCE17D7A3D) is the book reference; his open [MIT Lecture 5](https://ocw.mit.edu/courses/22-615-mhd-theory-of-fusion-systems-spring-2007/a5c962e43b645b825b13715a131166e2_lecture5.pdf) gives radial force balance on p.1, winding on p.4 and the leading cylinder limit on p.7. The chapter's title/pages/DOI are verified; exact book equation numbers have not been obtained. The derivations below state their own conventions.

## Domain, currents and radial balance

Use right-handed cylindrical coordinates with \(0\le r\le a\), \(\theta\) modulo \(2\pi\), and \(z\) modulo an independently fixed axial period \(L\). A fixed conducting wall imposes \(B_r(a)=0\); no exterior or wall-current model is prescribed. For translational and rotational symmetry,

\[
\mathbf B=B_\theta(r)\mathbf e_\theta+B_z(r)\mathbf e_z,
\quad \nabla\cdot\mathbf B=0,
\quad \mu_0j_\theta=-B_z',
\quad \mu_0j_z=B_\theta'+B_\theta/r.
\]

The radial component of \(\mathbf j\times\mathbf B=\nabla p\) is

\[
\frac{d}{dr}\left[p+\frac{B_\theta^2+B_z^2}{2\mu_0}\right]
 +\frac{B_\theta^2}{\mu_0r}=0.
\]

Axis regularity requires finite even \(B_z\) and \(B_\theta=O(r)\). Uniform \(B_z\) and \(B_\theta=cr\) give radial force \(-2c^2r/\mu_0\), and therefore fail zero-pressure balance unless \(c=0\).

The signed winding and integrated fluxes are

\[
q_{\rm RH}=\frac{2\pi rB_z}{LB_\theta},\qquad
\Phi=2\pi\int_0^r sB_z(s)\,ds,\qquad
\Psi=L\int_0^r B_\theta(s)\,ds,\qquad
q_{\rm RH}=\frac{d\Phi}{d\Psi}.
\]

\(\Psi\) is meridional sheet flux with normal \(+\mathbf e_\theta\), not axial flux. Both fluxes use a zero-axis gauge. With \(u=B^2\), elimination of the pitch gives

\[
u'=-\frac{2ru}{[Lq_{\rm RH}(r)/(2\pi)]^2+r^2}-2\mu_0p'.
\]

This is the native KIM equilibrium ODE in SI. Its CGS pressure coefficient is \(-8\pi\). No derivative of q appears explicitly because the magnetic-pressure derivative is already in u'.

## Exact field families and independent checks

For zero pressure and constant winding, set \(\tau=2\pi/(Lq_{\rm RH})\). The regular solution is

\[
B_z=\frac{B_0}{1+\tau^2r^2},\qquad
B_\theta=\frac{B_0\tau r}{1+\tau^2r^2},\qquad
\nabla\times\mathbf B=\frac{2\tau}{1+\tau^2r^2}\mathbf B.
\]

Gold–Hoyle therefore has zero force, fixed winding and \(u=B_0^2/(1+\tau^2r^2)\). Its exact fluxes are

\[
\Phi=\frac{\pi B_0}{\tau^2}\log(1+\tau^2r^2),\qquad
\Psi=\frac{LB_0}{2\tau}\log(1+\tau^2r^2).
\]

Fix radius, period, amplitude and twist; measure flux/current. For a=.62m,L=2*pi*6.2m,B0=5.3T,|q_RH|=1.5 the edge axial flux is6.386248371Wb, distinct from the circular-tokamak benchmark's6.400429545Wb. Opposite twist and global field reversal are separate controls.

The Lundquist companion \(B_z=B_0J_0(\alpha r),B_\theta=B_0J_1(\alpha r)\) has \(\nabla\times\mathbf B=\alpha\mathbf B\) and sheared winding. At alpha*a=1.5 and the same scales, q_axis=.1333333,q_edge=.0917358, and the q=1/10 surface is r=.560728838m. Under phase \(e^{i(m\theta-2\pi nz/L)}\), resonance means q=m/n. Constant-q Gold–Hoyle resonates at every radius for its resonant mode; it cannot test localization.

[KIN6D's existing symbolic oracle](https://github.com/itpplasma/kin6d/blob/d615a54cee50e1f4b376c4072e0b7aa0722f061f/test/test_gs_symbolic.f90) proves the native Gold–Hoyle curl/force/winding identities. The [periodic benchmark evidence](https://gitlab.tugraz.at/plasma/proj/ntv/iter_tc24/-/tree/a373958a99239c7d4600e2326fa298f4d3c76cff/equilibrium/data/periodic_cylinder_reference_20261008) retains independent Cartesian/radial derivatives, axis series, flux/current quadratures and sign/negative controls. Additional native proofs/evaluator checks have separate receipts; numerical probes are not promoted to symbolic proofs.

## Matching a toroidal code to this cylinder

For \(R_{\rm major}=Aa\), retain a,L,p and the cylinder's signed flux and q profile. The right-handed winding around a full toroidal circumference is

\[
q_{t,\rm RH}=\frac{L}{2\pi R_{\rm major}}q_{\rm RH}.
\]

An explicit embedding is x=R-R_major,y=-Z,z=R_major*phi. Thus theta_canonical=-theta_RH and Btheta_canonical=-Btheta_RH. With \(A_z'=-B_\theta\), the canonical field \(\mathbf B=\nabla\psi\times\nabla\phi+F\nabla\phi\) has leading \(\psi=R_{\rm major}A_z\), \(F=R_{\rm major}B_z\), and

\[
q_{t,\rm canonical}=-\frac{L}{2\pi R_{\rm major}}q_{\rm RH}.
\]

The ordinary positive-canonical-q/axis-minimum branch uses q_RH=-1.5. Its canonical q values at A=10,20,40,80,160 are1.5,.75,.375,.1875,.09375. Holding toroidal q fixed instead changes the physical pitch and approaches a different cylinder.

At finite A, solve the declared toroidal inverse problem with boundary,p,q and flux fixed; release F/current and finite-A B_axis. Cylinder fields are asymptotic references, not extra finite-A constraints. Separate toroidal model differences from boundary, profile, PDE, export and derivative numerical error before interpreting convergence. The coordinate identities do not prove existence, a convergence rate or perturbation stability.

KIM's actual parallel wavenumber uses a plus sign: m*h_theta/r+n*h_z/R0. Therefore its native map is R0=L/(2*pi),m_KIM=m,n_KIM=-n, with cm/G/CGS units. At positive r_min its equilibrium seed is the exact u(r_min); B_axis is not the local Bz seed. KIM_PERIODIC controls radial-window periodicity. Native reader/build qualification, kinetic profiles, forcing and perturbation boundaries remain separate from this equilibrium reference.

Chris&AI
