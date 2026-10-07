program gvec_local_identities
    use fortsym_arena, only: arena_t
    use fortsym_expr, only: expr_t, sym, operator(+), operator(-), &
                           operator(*), operator(/), operator(**)
    use fortsym_diff, only: diff
    use fortsym_engine, only: engine_result_t, VERDICT_TRUE
    use fortsym_engine_native, only: native_engine_t, make_native_engine
    implicit none
    type(arena_t), target :: arena
    type(native_engine_t) :: engine
    type(engine_result_t) :: verdict
    type(expr_t) :: r, a, b, c, d, pp, bt, bz, fluxp, chip, iota
    type(expr_t) :: jp, jac, gtt, energy, dw, lt, lz, checks(16)
    integer :: k
    call arena%init()
    engine = make_native_engine(arena)
    r = sym(arena, 'r'); a = sym(arena, 'r_rho')
    b = sym(arena, 'r_theta'); c = sym(arena, 'z_rho')
    d = sym(arena, 'z_theta'); pp = sym(arena, 'mu0_pressure')
    bt = sym(arena, 'btheta_density'); bz = sym(arena, 'bzeta_density')
    fluxp = sym(arena, 'phi_prime'); chip = sym(arena, 'chi_prime')
    iota = sym(arena, 'iota_gvec')
    lt = sym(arena, 'lambda_theta'); lz = sym(arena, 'lambda_zeta')
    jp = a*d - b*c
    jac = r*jp
    gtt = b**2 + d**2
    energy = -pp*jac + (bt**2*gtt + bz**2*r**2)/(2*jac)
    dw = pp + (bt**2*gtt + bz**2*r**2)/(2*jac**2)
    checks(1) = diff(jac, a) - r*d
    checks(2) = diff(jac, b) + r*c
    checks(3) = diff(jac, c) + r*b
    checks(4) = diff(jac, d) - r*a
    ! Negative energy derivatives equal native RZ weak coefficients.
    checks(5) = -diff(energy, r) - dw*jp + bz**2*r/jac
    checks(6) = -diff(energy, a) - dw*r*d
    checks(7) = -diff(energy, b) + dw*r*c + bt**2*b/jac
    checks(8) = -diff(energy, c) + dw*r*b
    checks(9) = -diff(energy, d) - dw*r*a + bt**2*d/jac
    ! At axisymmetry btheta=chi'; psi=chi-chi_edge, canonical phi=-zeta.
    checks(10) = chip*b/jac - (-(-chip*b/jp)/r)
    checks(11) = chip*d/jac - (chip*d/jp)/r
    checks(12) = (-1/iota)*(-iota) - 1
    bt = chip - fluxp*lz
    bz = fluxp*(1 + lt)
    energy = -pp*jac + (bt**2*gtt + bz**2*r**2)/(2*jac)
    checks(13) = -diff(energy, lt) + fluxp*bz*r**2/jac
    checks(14) = -diff(energy, lz) - fluxp*bt*gtt/jac
    checks(15) = diff(bt, lz) + fluxp
    checks(16) = diff(bz, lt) - fluxp
    do k = 1, size(checks)
        verdict = engine%zero_test(checks(k))
        if (verdict%verdict /= VERDICT_TRUE) then
            write (*, '(a,i0)') 'UNPROVED native exact identity ', k
            error stop 1
        end if
        write (*, '(a,i0)') 'PASS native exact identity ', k
    end do
end program gvec_local_identities
