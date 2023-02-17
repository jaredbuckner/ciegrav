#!/bin/env python3

import math

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


def _genpwgfun(mu, sig_low, sig_high):
    ntw_sig_low_sq = -2 * sig_low * sig_low
    ntw_sig_high_sq = -2 * sig_high * sig_high
    def _pwgfun(x):
        offset = x - mu;
        return(math.exp(offset * offset / ntw_sig_low_sq) if offset < 0 else
               math.exp(offset * offset / ntw_sig_high_sq))
    return _pwgfun

_xafn1=_genpwgfun(599.8, 37.9, 31.0)
_xafn2=_genpwgfun(442.0, 16.0, 26.7)
_xafn3=_genpwgfun(501.1, 20.4, 26.2)

_yafn1=_genpwgfun(568.8, 46.9, 40.5)
_yafn2=_genpwgfun(530.9, 16.3, 31.1)

_zafn1=_genpwgfun(437.0, 11.8, 36.0)
_zafn2=_genpwgfun(459.0, 26.0, 13.8)

def xbar(lmbda):
    return(1.056 * _xafn1(lmbda) +
           0.362 * _xafn2(lmbda) -
           0.065 * _xafn3(lmbda))

def ybar(lmbda):
    return(0.821 * _yafn1(lmbda) +
           0.286 * _yafn2(lmbda))

def zbar(lmbda):
    return(1.217 * _zafn1(lmbda) +
           0.681 * _zafn2(lmbda))

def spectrum2xyz(radiance, lmbda):
    return(radiance * xbar(lmbda), radiance * ybar(lmbda), radiance * zbar(lmbda))


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


