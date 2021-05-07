import jihuo
def yh(xiao,da,prexiao,preda):
    if (abs(prexiao - xiao) >= 1):
        if (xiao - prexiao >= 0):
            xiao = prexiao + 0.2 * jihuo.jh(xiao - prexiao)
        else:
            xiao = prexiao - 0.2 * jihuo.jh(abs(xiao - prexiao))
    if (abs(prexiao - xiao) > 0.2 and abs(prexiao - xiao) < 1):
        if (xiao - prexiao >= 0):
            xiao = prexiao + 0.8 * jihuo.jh(xiao - prexiao)
        else:
            xiao = prexiao - 0.8 * jihuo.jh(abs(xiao - prexiao))

    if (abs(preda - da) >= 1):
        if (da - preda >= 0):
            da = preda + 0.2 * jihuo.jh(da - preda)
        else:
            da = preda - 0.2 * jihuo.jh(abs(da - preda))
    if (abs(preda - da) >= 0.5 and abs(preda - da) < 1):
        if (da - preda >= 0):
            da = preda + 0.4 * jihuo.jh(da - preda)
        else:
            da = preda - 0.4 * jihuo.jh(abs(da - preda))
    if (abs(preda - da) > 0.2 and abs(preda - da) < 1):
        if (da - preda >= 0):
            da = preda + 0.8 * jihuo.jh(da - preda)
        else:
            da = preda - 0.8 * jihuo.jh(abs(da - preda))

    return xiao,da