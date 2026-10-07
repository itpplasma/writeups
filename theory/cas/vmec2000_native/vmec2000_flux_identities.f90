program vmec2000_flux_identities
    use fortsym_arena, only: arena_t
    use fortsym_expr, only: expr_t, sym, operator(+), operator(-), &
                           operator(*), operator(/), operator(**)
    use fortsym_engine, only: engine_result_t, VERDICT_TRUE
    use fortsym_engine_native, only: native_engine_t, make_native_engine
    implicit none
    type(arena_t), target :: arena
    type(native_engine_t) :: engine
    type(engine_result_t) :: verdict
    type(expr_t) :: tau, h, p, iota, u, v, iu, iv
    type(expr_t) :: dphi, dchi, dpsi, fullphi, fullchi, checks(8)
    integer :: sigma, k
    call arena%init()
    engine = make_native_engine(arena)
    tau = sym(arena, 'two_pi')
    h = sym(arena, 'radial_step')
    p = sym(arena, 'phip_half')
    iota = sym(arena, 'iota_half')
    u = sym(arena, 'phip_left')
    v = sym(arena, 'phip_right')
    iu = sym(arena, 'iota_left')
    iv = sym(arena, 'iota_right')
    ! tau=2*pi is nonzero; signgs=sigma is exactly +1 or -1.
    do sigma = -1, 1, 2
        dphi = sigma*tau*h*p
        dchi = tau*h*p*iota
        dpsi = sigma*dchi/tau
        fullphi = sigma*tau*(u+v)/2
        fullchi = sigma*tau*(u*iu+v*iv)/2
        checks(1) = dpsi - iota*dphi/tau
        checks(2) = dchi - sigma*iota*dphi
        checks(3) = sigma*dpsi - dchi/tau
        checks(4) = fullchi-fullphi*(iu+iv)/2 &
                    - sigma*tau*(u-v)*(iu-iv)/4
        checks(5) = sigma*tau*(u*iota+v*iota)/2-fullphi*iota
        checks(6) = sigma*tau*((-u)*iu+(-v)*iv)/2+fullchi
        checks(7) = sigma*tau*h*(-p)+dphi
        ! Check8 expresses the relation between signed internal/output flux.
        checks(8) = tau*h*p-sigma*dphi
        do k = 1, size(checks)
            verdict = engine%zero_test(checks(k))
            if (verdict%verdict /= VERDICT_TRUE) then
                write (*, '(a,i0,a,i0)') 'UNPROVED signgs=', sigma, ' identity=', k
                error stop 1
            end if
            write (*, '(a,i0,a,i0)') 'PASS signgs=', sigma, ' identity=', k
        end do
    end do
    ! Negative oracles: omit the native chi sign, or multiply averaged profiles.
    ! Both errors are nonzero for generic symbols and have integer witnesses.
    verdict = engine%zero_test(tau*h*p*iota + tau*h*p*iota)
    if (verdict%verdict == VERDICT_TRUE) error stop 'Wrong chi sign accepted'
    verdict = engine%zero_test((u-v)*(iu-iv))
    if (verdict%verdict == VERDICT_TRUE) error stop 'Mean product conflated'
    if ((1*2+3*4)/2 == ((1+3)/2)*((2+4)/2)) then
        error stop 'Integer mean-product witness invalid'
    end if
    write (*, '(a)') 'PASS wrong-sign and product-of-means negative witnesses'
end program vmec2000_flux_identities
