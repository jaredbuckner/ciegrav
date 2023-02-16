#!/bin/env python3

import cie
import math
import random

class GravSim:
    def __init__(self, count=2):
        self.labpoints = []  # These are in cielab space.  They are canonical.
        self.rgbpoints = []  # These are in srgb space.  They are cached from
                             # the lab points.

        for i in range(count):
            self.addpoint()

    def addpoint(self):
        v_rgb = (random.random(), random.random(), random.random());
        self.rgbpoints.append(v_rgb);
        self.labpoints.append(cie.srgb2lab(v_rgb))

    def delpoint(self):
        if self.labpoints:
            idx = random.randrange(0, len(self.labpoints))
            del self.labpoints[idx]
            del self.rgbpoints[idx]

    def randomize(self):
        count = len(self.labpoints)
        self.labpoints = []
        self.rgbpoints = []
        for iteration in range(count):
            self.addpoint()
        
    def update(self, fleeNN = 0.5, anneal = 0.2):
        nn = [None] * len(self.labpoints)
        for aidx, a in enumerate(self.labpoints[:-1]):
            for bidx, b in enumerate(self.labpoints[aidx+1:], start=aidx+1):
                norm = (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2
                if nn[aidx] is None or nn[aidx][1] > norm:
                    nn[aidx] = (b, norm)
                if nn[bidx] is None or nn[bidx][1] > norm:
                    nn[bidx] = (a, norm)

        for aidx, a in enumerate(self.labpoints):
            newa = None
            if nn[aidx] is not None:
                b, norm = nn[aidx]
                # print(f"  {aidx}: {a!r} {nn[aidx]!r}")
                if norm > 0.0:
                    renorm = math.sqrt(norm)
                    newa = (a[0] + fleeNN * (a[0] - b[0]) / renorm + (2 * random.random() - 1) * anneal,
                            a[1] + fleeNN * (a[1] - b[1]) / renorm + (2 * random.random() - 1) * anneal,
                            a[2] + fleeNN * (a[2] - b[2]) / renorm + (2 * random.random() - 1) * anneal)

            if newa is None:
                newa = (a[0] + (2 * random.random() - 1) * anneal,
                        a[1] + (2 * random.random() - 1) * anneal,
                        a[2] + (2 * random.random() - 1) * anneal)

            a_rgbr = cie.lab2srgb(newa)
            a_rgb = (0 if a_rgbr[0] < 0 else 1 if a_rgbr[0] > 1 else a_rgbr[0],
                     0 if a_rgbr[1] < 0 else 1 if a_rgbr[1] > 1 else a_rgbr[1],
                     0 if a_rgbr[2] < 0 else 1 if a_rgbr[2] > 1 else a_rgbr[2])

            a_lab = cie.srgb2lab(a_rgb)

            # print(f'  {newa!r} -> {a_rgbr!r} -> {a_rgb!r} -> {a_lab!r}')
            # a_lab = newa
            self.labpoints[aidx] = a_lab
            self.rgbpoints[aidx] = a_rgb
            
    
if __name__ == '__main__':
    import sys

    entries = 2
    iterations = 1000

    try:
        entries = int(sys.argv[1])
        iterations = int(sys.argv[2])
    except IndexError:
        pass

    gs = GravSim(entries)

    for idx in range(iterations):
        print(f"Iteration {idx + 1}...")              
        gs.update()

    for lab, rgb in zip(gs.labpoints, gs.rgbpoints):
        print(f"{lab[0]:6.2f}L {lab[1]:6.2f}a {lab[2]:6.2f}b  :  {int(rgb[0]*256):3d}R {int(rgb[1]*256):3d}G {int(rgb[2]*256):3d}B")
