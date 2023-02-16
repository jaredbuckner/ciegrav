#!/bin/env python3

import ciegrav
import math
import tkinter as tk

def _makesort(lab, rgb):
    satsq = lab[1]**2 + lab[2]**2
    if satsq < 49:
        return(-1, lab[0], satsq, lab, rgb)
    else:
        angle=math.atan2(lab[2], lab[1])
        if angle < 0:
            angle += 2 * 3.14159265358932384626
        return(angle, lab[0], satsq, lab, rgb)

def rgb2tk(v):
    r = int(v[0] * 256) ; r = 255 if r > 255 else r
    g = int(v[1] * 256) ; g = 255 if g > 255 else g
    b = int(v[2] * 256) ; b = 255 if b > 255 else b
    return f'#{r:02X}{g:02X}{b:02X}'

class Sampler(tk.Canvas):
    def __init__(self, *args, count=2, background=rgb2tk((0.25,0.25,0.25)), **kwargs):
        super().__init__(*args, background=background, **kwargs)
        self.gs = ciegrav.GravSim(count)
        self.bind('<Configure>', self.draw)
        self.rungrav()
        self.bind_all('<Prior>', self.addpoint)
        self.bind_all('<Next>', self.delpoint)
        self.bind_all('<Return>', self.mix)
        self.bind_all('<space>', self.bump)
        self.draw()

    def rungrav(self, ev=None):
        ## anneal drops hyperbolically:
        ##  a(t) = a0 * thalve / (t + thalve)
        maxiter = 1009  ## Itzprime!
        fullAnneal = 0.5
        thalve = maxiter / 8
        for iteration in range(maxiter):
            fleeNN = 0.2
            anneal = fullAnneal * thalve / (iteration + thalve)
            self.gs.update(fleeNN = fleeNN, anneal = anneal)

    def draw(self, ev=None):
        w = self.winfo_width()
        h = self.winfo_height()
        self.delete("sample")
        parts = list()
        for idx, s in enumerate(sorted(_makesort(l, r) for l, r in zip(self.gs.labpoints, self.gs.rgbpoints))):
            val = s[-1]
            fill = rgb2tk(val)
            parts.append(fill)
            self.create_rectangle(idx * w / len(self.gs.rgbpoints), 0,
                                  (idx + 1) * w / len(self.gs.rgbpoints), h,
                                  fill = fill)
        print(' : '.join(parts))

    def addpoint(self, ev=None):
        self.gs.addpoint()
        self.rungrav()
        self.draw()

    def delpoint(self, ev=None):
        if len(self.gs.labpoints) > 2:
            self.gs.delpoint()
            self.rungrav()
            self.draw()

    def bump(self, ev=None):
        self.rungrav()
        self.draw()
        
    def mix(self, ev=None):
        self.gs.randomize()
        self.rungrav()
        self.draw()
            
if __name__ == '__main__':
    root = tk.Tk()
    root.title("CieGrav")

    root.rowconfigure(1, weight=1)
    root.columnconfigure(1, weight=1)

    sampler = Sampler(root)
    sampler.grid(row=1, column=1, sticky='news')

    root.mainloop()
    exit(0)
