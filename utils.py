def smoothstep(t):
    return t * t * (3 - 2 * t)


def interpolate(a, b, t):
    return a + smoothstep(t) * (b - a)
