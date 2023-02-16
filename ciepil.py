#!/bin/env python3

import cie
import itertools
import PIL.Image


#def _interp(p, v0, v1):
#    return tuple(x0 * (1-p) + x1 * p for x0, x1 in zip(v0, v1))

def _interp(p, v0, v1):
    q = 1-p
    return (v0[0] * q + v1[0] * p,
            v0[1] * q + v1[1] * p,
            v0[2] * q + v1[2] * p)

# def _clip(v):
#     r = tuple(int(x * 256) for x in v)
#     if any(x < 0 or x > 255 for x in r):
#         return tuple(0 for x in r)
#     else:
#         return r

def _clip(v, *, clipto=(0, 0, 0)):
    r = int(v[0] * 256)
    if r < 0 or r > 255: return clipto

    g = int(v[1] * 256)
    if g < 0 or g > 255: return clipto

    b = int(v[2] * 256)
    if b < 0 or b > 255: return clipto

    return (r, g, b)

def _linsweep(v0, v1, count):
    for i in range(0, count):
        yield _interp(i / max(count - 1, 1), v0, v1)

def _2dsweep(xcount, ycount, nn, nx, xn, xx):
    for i in range(0, ycount):
        v0 = _interp(i / max(ycount - 1, 1), nn, xn)
        v1 = _interp(i / max(ycount - 1, 1), nx, xx)
        yield from _linsweep(v0, v1, xcount)

def makeRaster(w, h, nn, nx, xn, xx):
    bytegen = (
        itertools.chain.from_iterable(_clip(cie.lab2srgb(v))
                                      for v in _2dsweep(w, h, nn, nx, xn, xx)))
    return PIL.Image.frombytes('RGB',(w, h), bytes(bytegen))
    

if __name__ == '__main__':
    import sys

    Lstar = 50
    try:
        Lstar = float(sys.argv[1])
    except:
        pass
    
    makeRaster(1920, 1080,
               (Lstar,-100,-100),
               (Lstar,-100,100),
               (Lstar,100,-100),
               (Lstar,100,100)).show()
