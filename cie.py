#!/bin/env python3

def xyz2srgblin(v):
    return(+.0324096994 * v[0] - .0153738318 * v[1] - .0049861076 * v[2],
           -.0096924364 * v[0] + .0187596750 * v[1] + .0004155506 * v[2],
           +.0005563008 * v[0] - .0020397696 * v[1] + .0105697151 * v[2])

def srgblin2srgb(v):
    return(tuple(12.92 * u if u <= 0.0031308 else 1.055 * u ** (1 / 2.4) - 0.055 for u in v))

def srgb2srgblin(v):
    return(tuple(u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4 for u in v ))

def srgblin2xyz(v):
    return(41.239080 * v[0] + 35.758434 * v[1] + 18.048079 * v[2],
           21.263901 * v[0] + 71.516868 * v[1] + 07.219232 * v[2],
           01.933082 * v[0] + 11.919478 * v[1] + 95.053215 * v[2])


_labXYZnomD65 = (95.0489, 100, 108.8840)
_labdel = 6/29

def _labfun(t, *, withdel=_labdel):
    return t**(1/3) if t > withdel**3 else t / 3 / withdel**2 + 4/29

def _labfuninv(t, *, withdel=_labdel):
    return t**3 if t > withdel else 3 * withdel**2 * (t - 4/29)

def xyz2lab(v, *, withnom=_labXYZnomD65):
    return(116 * _labfun(v[1] / withnom[1]) - 16,
           500 * (_labfun(v[0] / withnom[0]) - _labfun(v[1] / withnom[1])),
           200 * (_labfun(v[1] / withnom[1]) - _labfun(v[2] / withnom[2])))

def lab2xyz(v, *, withnom=_labXYZnomD65):
    return(withnom[0] * _labfuninv((v[0] + 16) / 116 + v[1] / 500),
           withnom[1] * _labfuninv((v[0] + 16) / 116),
           withnom[2] * _labfuninv((v[0] + 16) / 116 - v[2] / 200))


def xyz2srgb(v):
    return(srgblin2srgb(xyz2srgblin(v)))

def srgb2xyz(v):
    return(srgblin2xyz(srgb2srgblin(v)))

def lab2srgb(v):
    return(xyz2srgb(lab2xyz(v)))

def srgb2lab(v):
    return(xyz2lab(srgb2xyz(v)))


