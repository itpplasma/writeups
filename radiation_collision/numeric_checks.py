"""Independent numerical checks of the radiation-collision derivation.

The exact algebra is checked by fortsym (cas/run_cas.sh). This script tests
what is not purely algebraic: harmonic sums, the photon-angle quadrature of
the unsummed tensor, absorption series, Bessel moments, bounds, the
broadened cusp and the drag propagator. It needs mpmath only.

Usage: python3 numeric_checks.py [results.json]
"""
import json
import sys

import mpmath as mp

mp.mp.dps = 30
results = {}


def record(name, value, tol):
    value = float(value)
    ok = value <= tol
    results[name] = {"max_relative_error": value, "tolerance": tol, "pass": ok}
    print(f"{'PASS' if ok else 'FAIL'} {name}: {value:.3e} (tol {tol:.0e})")


def rel(a, b):
    return abs(a - b)/max(abs(b), mp.mpf(10)**-25)


# Harmonic sums (3.3)-(3.4) by direct summation.
err = 0
for z in (mp.mpf('0.3'), mp.mpf('0.7'), mp.mpf('0.9')):
    sJ = mp.nsum(lambda n: n**2*mp.besselj(n, n*z)**2, [1, mp.inf])
    sD = mp.nsum(lambda n: n**2*mp.besselj(n, n*z, 1)**2, [1, mp.inf])
    err = max(err, rel(sJ, z**2*(4 + z**2)/(16*(1 - z**2)**mp.mpf(3.5))),
              rel(sD, (4 + 3*z**2)/(16*(1 - z**2)**mp.mpf(2.5))))
record("harmonic sums (3.3)-(3.4)", err, 1e-20)


# Closed tensor (3.15) against the eta quadrature of the unsummed (3.2).
def F_(u):
    g = mp.sqrt(1 + u**2)
    return 10 + 3/u**2 - (9/(g*u) + 3*g/u**3)*mp.asinh(u)


def G_(u):
    g = mp.sqrt(1 + u**2)
    return 10 + 15/u**2 - (21/(g*u) + 15*g/u**3)*mp.asinh(u)


def H_(u):
    return u**2 - 1 - G_(u)/16


def D_closed(up, ua):
    u = mp.sqrt(up**2 + ua**2)
    g = mp.sqrt(1 + u**2)
    a = mp.mpf(2)/3          # nu0 = 1
    return (a*up**2, a*ua*up**2/g,
            a*up**2/u**2*(F_(u)/16 + H_(u)*ua**2/u**2))


def D_harmonic(up, ua, nmax=None):
    g = mp.sqrt(1 + up**2 + ua**2)

    def integrand(eta, i, j):
        q = g - eta*ua
        sig = 1 - eta**2
        z = up*mp.sqrt(sig)/q
        tot = 0
        n = 1
        while True:
            lam = n*z
            dx = up**2/g**2*mp.besselj(n, lam, 1)**2
            do = (g*eta - ua)**2/(g**2*sig)*mp.besselj(n, lam)**2 if sig else 0
            term = n**2*(dx + do)
            tot += term
            if (nmax and n >= nmax) or (n > 3 and term < mp.mpf(10)**-28*tot):
                break
            n += 1
        return g/q**3*tot*eta**(i + j)
    return tuple(mp.quad(lambda e: integrand(e, i, j), [-1, 0, 1])
                 for i, j in ((0, 0), (0, 1), (1, 1)))


mp.mp.dps = 20
err = 0
for up, ua in ((0.4, 0.3), (1.0, -0.5), (1.5, 1.2)):
    up, ua = mp.mpf(up), mp.mpf(ua)
    for x, y in zip(D_harmonic(up, ua), D_closed(up, ua)):
        err = max(err, rel(x, y))
record("closed tensor (3.15) vs harmonic quadrature (3.2)", err, 1e-12)
mp.mp.dps = 30


# Absorption normalisation: series (4.16)-(4.17) against quadrature, and the
# hypergeometric forms of M_j and T_j.
def M(j, a):
    return mp.beta(0.5, j + 1)*mp.hyp0f1(j + 1.5, a**2/4)


def T(j, a):
    return mp.beta(1.5, j + 1)*mp.hyp1f2(1.5, 0.5, j + 2.5, a**2/4)


def A(k, l):
    return mp.factorial(2*k + 2*l)/(mp.factorial(l)*mp.factorial(2*k + l)
                                   * mp.factorial(k + l)**2)


def B(k, l):
    return (2*(k + l)**2 - k**2)*A(k, l) - (4*A(k, l - 1) if l else 0)


err = 0
for j, a in ((0, 0.7), (2, -1.3), (5, 2.0)):
    a = mp.mpf(a)
    err = max(err,
              rel(M(j, a), mp.quad(lambda x: mp.e**(-a*x)*(1 - x**2)**j, [-1, 1])),
              rel(T(j, a), mp.quad(lambda x: x**2*mp.e**(-a*x)*(1 - x**2)**j, [-1, 1])))
record("M_j, T_j hypergeometric forms (4.12)-(4.13)", err, 1e-25)

err = 0
for k, a, b in ((1, 0.5, 0.8), (2, -1.0, 1.5), (3, 2.0, 3.0)):
    a, b = mp.mpf(a), mp.mpf(b)
    fo = mp.quad(lambda x: mp.e**(-a*x)*x**2*mp.besselj(k, b*mp.sqrt(1 - x**2))**2, [-1, 1])
    fx = mp.quad(lambda x: mp.e**(-a*x)*(1 - x**2)*mp.besselj(k, b*mp.sqrt(1 - x**2), 1)**2, [-1, 1])
    so = mp.nsum(lambda l: (-1)**l*A(k, int(l))*(b/2)**(2*k + 2*l)*T(k + int(l), a), [0, mp.inf])
    sx = mp.nsum(lambda l: (-1)**l*B(k, int(l))*(b/2)**(2*k + 2*l)*M(k + int(l), a), [0, mp.inf])/b**2
    err = max(err, rel(so, fo), rel(sx, fx))
record("absorption series (4.16)-(4.17)", err, 1e-20)


def S_M(s, eta, pol, mu, kmax=60):
    sig = 1 - eta**2
    tot = 0
    for k in range(1, kmax + 1):
        if (k*s)**2 <= sig:
            continue
        h = mp.sqrt((k*s)**2 - sig)
        a, b = mu*eta*h/sig, h/s
        if pol == 'O':
            f = mp.quad(lambda x: mp.e**(-a*x)*x**2*mp.besselj(k, b*mp.sqrt(1 - x**2))**2, [-1, 1])
        else:
            f = mp.quad(lambda x: mp.e**(-a*x)*(1 - x**2)*mp.besselj(k, b*mp.sqrt(1 - x**2), 1)**2, [-1, 1])
        tot += h**3/sig**2*mp.e**(-mu*k*s/sig)*f
    return tot


def S_direct(s, eta, pol, mu, kmax=60):
    """S_M from its definition sum_k int dg dua g^2 D_k delta(g - k s - eta ua) e^(-mu g)."""
    tot = 0
    for k in range(1, kmax + 1):
        def integrand(ua):
            g = k*s + eta*ua
            up2 = g**2 - ua**2 - 1
            if up2 <= 0:
                return 0
            lam = mp.sqrt(up2)*mp.sqrt(1 - eta**2)/s
            if pol == 'X':
                d = up2*mp.besselj(k, lam, 1)**2
            else:
                d = (g*eta - ua)**2/(1 - eta**2)*mp.besselj(k, lam)**2
            return d*mp.e**(-mu*g)
        sig = 1 - eta**2
        if (k*s)**2 <= sig:
            continue
        h = mp.sqrt((k*s)**2 - sig)
        lo, hi = (k*s*eta - h)/sig, (k*s*eta + h)/sig
        tot += mp.quad(integrand, [lo, hi])
    return tot


mp.mp.dps = 20
err = 0
for s, eta, mu in ((0.9, 0.3, 2.0), (1.2, -0.6, 5.0)):
    s, eta, mu = mp.mpf(s), mp.mpf(eta), mp.mpf(mu)
    for pol in 'OX':
        err = max(err, rel(S_M(s, eta, pol, mu, 12), S_direct(s, eta, pol, mu, 12)))
record("absorption normalisation (4.8) vs resonance-line integral", err, 1e-12)

# Axis limit (4.20).
s, mu = mp.mpf('1.3'), mp.mpf(3)
axis = s/(2*mu**2)*mp.e**(-mu/2*(s + 1/s))
err = 0
for pol in 'OX':
    err = max(err, rel(S_M(s, 1 - mp.mpf(10)**-8, pol, mu, 6), axis))
record("axis limit (4.20) at eta = 1 - 1e-8", err, 1e-6)
mp.mp.dps = 30


# Bessel moments and the thermal tail.
def avg(fun, mu):
    """<F>_0 for an isotropic function F(u)."""
    return mu/mp.besselk(2, mu)*mp.quad(lambda u: u**2*fun(u)*mp.e**(-mu*mp.sqrt(1 + u**2)), [0, mp.inf])


err = 0
for mu in (mp.mpf('0.5'), mp.mpf(3), mp.mpf(20)):
    K = [mp.besselk(n, mu) for n in range(4)]
    err = max(err, rel(avg(lambda u: 1, mu), 1),
              rel(avg(lambda u: u**2, mu), 3*K[3]/(mu*K[2])),
              rel(avg(lambda u: mp.asinh(u)/(u*mp.sqrt(1 + u**2)), mu), K[0]/K[2]))
record("Bessel moments (8.9), (8.12)", err, 1e-25)

err = 0
for mu, W in ((mp.mpf(1), mp.mpf('0.5')), (mp.mpf(4), mp.mpf(2))):
    Aw = mp.sqrt(1 + W**2)
    closed = (W**2*Aw**2*mp.besselk(2, mu*Aw) + 2*Aw**3*mp.besselk(3, mu*Aw)/mu)/mp.besselk(2, mu)
    # n_e = 1; d^3p = 2 pi w dw dv in units mc = 1.
    quad = mu/(4*mp.pi*mp.besselk(2, mu))*2*mp.pi*mp.quad(
        lambda w: w**3*2*mp.quad(lambda v: mp.e**(-mu*mp.sqrt(1 + w**2 + v**2)), [0, mp.inf]),
        [W, mp.inf])
    err = max(err, rel(quad, closed))
record("thermal tail (5.11)", err, 1e-20)


# G_E, G_P: closed Bessel forms against direct quadrature of int f0 D.
def GE_closed(mu):
    return 4*mp.besselk(3, mu)/(3*mu*mp.besselk(2, mu))


def GP_closed(mu):
    return 4*(mp.besselk(1, mu) + mp.besselk(3, mu))/(15*mu*mp.besselk(2, mu))


def GP_quad(mu):
    a = mp.mpf(2)/3

    def daa(u):
        return mp.quad(lambda xi: a*(1 - xi**2)*(F_(u)/16 + H_(u)*xi**2), [-1, 1])/2
    return avg(daa, mu)


def GE_quad(mu):
    return avg(lambda u: mp.mpf(2)/3*mp.mpf(2)/3*u**2, mu)


mp.mp.dps = 25
table = []
err = 0
for mu in (mp.mpf('0.5'), mp.mpf(1), mp.mpf(3), mp.mpf(6), mp.mpf(20)):
    ge, gp = GE_closed(mu), GP_closed(mu)
    err = max(err, rel(GE_quad(mu), ge), rel(GP_quad(mu), gp))
    table.append([float(mu), mp.nstr(ge, 15), mp.nstr(gp, 15), mp.nstr(gp/ge, 15)])
record("G_E (8.10), G_P (8.13) vs quadrature", err, 1e-15)
results["G_table_ne_nu0_1"] = table
lim_hi = GP_closed(mp.mpf(10)**4)/GE_closed(mp.mpf(10)**4)
lim_lo = GP_closed(mp.mpf(10)**-4)/GE_closed(mp.mpf(10)**-4)
record("G_P/G_E limits 2/5 and 1/5 (8.14)",
       max(abs(lim_hi - mp.mpf(2)/5)/0.4, abs(lim_lo - mp.mpf(1)/5)/0.2), 1e-3)
mp.mp.dps = 30


# Integration by parts b_alpha = int d^3p delta f H_alpha (8.21), with
# delta f = f0 fhat, in (u, xi) coordinates.
def HE(up, ua, mu):
    g = mp.sqrt(1 + up**2 + ua**2)
    return mp.mpf(2)/3*(mu*up**2 - (2 + 4*up**2)/g)


def HP(up, ua, mu):
    u2 = up**2 + ua**2
    u = mp.sqrt(u2)
    g = mp.sqrt(1 + u2)
    return -mp.mpf(2)/3*ua*(2 - mu*up**2/g - F_(u)/(8*u2) + (2/u2 - 4*ua**2/u2**2)*H_(u))


def safe_quad(f, pts):
    """mp.quad, re-split when its error estimate divides by an exact zero
    (consecutive levels agreeing exactly for near-polynomial integrands)."""
    try:
        return mp.quad(f, pts)
    except ZeroDivisionError:
        a, b = pts[0], pts[-1]
        return mp.quad(f, [a, a + (b - a)*mp.mpf('0.37'), a + (b - a)*mp.mpf('0.71'), b])


def moment(fun, mu):
    """int d^3p f0 fun(up, ua), n_e = 1, mc = 1."""
    pref = mu/(4*mp.pi*mp.besselk(2, mu))*2*mp.pi
    return pref*mp.quad(lambda u: u**2*mp.e**(-mu*mp.sqrt(1 + u**2))*safe_quad(
        lambda xi: fun(u*mp.sqrt(1 - xi**2), u*xi), [-1, 1]), [0, mp.inf])


mp.mp.dps = 20
mu = mp.mpf(2)
err = 0
# fhat = g^2 tests the energy source and fhat = ua^3 the momentum source;
# the other two pairings vanish by parity in ua. Gradients in (g, ua).
for fh, dg, dua, alpha, H in (
        (lambda up, ua: 1 + up**2 + ua**2, lambda up, ua: 2*mp.sqrt(1 + up**2 + ua**2),
         lambda up, ua: 0, 'E', HE),
        (lambda up, ua: ua**3, lambda up, ua: 0, lambda up, ua: 3*ua**2, 'P', HP)):
    def lhs(up, ua):
        Dg, Dga, Daa = D_closed(up, ua)
        if alpha == 'E':
            return Dg*dg(up, ua) + Dga*dua(up, ua)
        return Dga*dg(up, ua) + Daa*dua(up, ua)
    err = max(err, rel(moment(lambda up, ua: fh(up, ua)*H(up, ua, mu), mu),
                       moment(lhs, mu)))
record("scalar sources: b_alpha by parts (8.21)", err, 1e-10)
mp.mp.dps = 30


# Harmonic tail bound (5.9) at sample points.
mp.mp.dps = 20
worst = 0
for up, ua, N in ((0.5, 0.2, 3), (1.0, -0.8, 5), (2.0, 0.5, 8)):
    up, ua = mp.mpf(up), mp.mpf(ua)
    full = D_harmonic(up, ua)[0]
    trunc = D_harmonic(up, ua, nmax=N)[0]
    alpha = mp.asinh(1/up) - 1/mp.sqrt(1 + up**2)
    qw = mp.e**(-2*alpha)
    bound = 4/(1 + up**2)*mp.nsum(lambda n: n**2*qw**n, [N + 1, mp.inf])
    worst = max(worst, (full - trunc)/bound)
results["tail bound ratio (must be <= 1)"] = float(worst)
record("harmonic tail bound (5.9) holds", max(0, worst - 1), 0)
mp.mp.dps = 30


# Gaussian-broadened cusp (7.2).
err = 0
for x, l in ((-0.7, 0.4), (0.0, 1.0), (1.3, 0.5)):
    x, l = mp.mpf(x), mp.mpf(l)
    quad = mp.quad(lambda t: t**1.5*mp.e**(-(x - t)**2/(2*l**2)), [0, mp.inf])/(mp.sqrt(2*mp.pi)*l)
    closed = mp.gamma(2.5)*l**1.5/mp.sqrt(2*mp.pi)*mp.e**(-x**2/(4*l**2))*mp.pcfd(-2.5, -x/l)
    err = max(err, rel(quad, closed))
record("broadened cusp (7.2)", err, 1e-25)


# Drag trajectory (11.5) against direct integration of (11.2).
nR = mp.mpf(1)
w0, v0 = mp.mpf('1.5'), mp.mpf('0.8')
g0 = mp.sqrt(1 + w0**2 + v0**2)
sol = mp.odefun(lambda t, y: [-nR*y[0]*(1 + y[0]**2)/mp.sqrt(1 + y[0]**2 + y[1]**2),
                              -nR*y[1]*y[0]**2/mp.sqrt(1 + y[0]**2 + y[1]**2)], 0, [w0, v0])
beta = v0/g0
gpar = 1/mp.sqrt(1 - beta**2)
z0 = mp.asinh(1/w0)
err = 0
for t in (mp.mpf('0.5'), mp.mpf(2)):
    z = z0 + nR*t/gpar
    w, v = sol(t)
    err = max(err, rel(w, mp.csch(z)), rel(v, beta*gpar*mp.coth(z)))
record("drag characteristics (11.5)", err, 1e-15)

# Propagator (11.8) conserves particles: int d^3p f at t equals t = 0.
mp.mp.dps = 15


def fin(z, b):
    return mp.e**(-(z - 1)**2*4)*(1 - b**2)**3


def J(z, b):
    return (1 - b**2)**mp.mpf(-1.5)/mp.sinh(z)**2*mp.coth(z)**2


def number(t):
    def inner(b):
        gp = 1/mp.sqrt(1 - b**2)
        c = nR/gp
        return mp.quad(lambda z: J(z - c*t, b)*fin(z - c*t, b) if z - c*t > 0 else 0,
                       [c*t, c*t + 0.2, c*t + 3, mp.inf])
    return mp.quad(inner, [-1, 0, 1])


n0, n1 = number(0), number(mp.mpf('0.7'))
record("drag propagator conserves particles (11.8)", rel(n1, n0), 1e-8)

ok = all(v["pass"] for v in results.values() if isinstance(v, dict))
if len(sys.argv) > 1:
    with open(sys.argv[1], "w") as fh:
        json.dump(results, fh, indent=1)
print("ALL PASS" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
