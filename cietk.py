#!/bin/env python3

import cie
import ciepil
import PIL.ImageTk
import queue
import threading
import tkinter as tk


class RasterWorker(threading.Thread):
    def __init__(self, inqueue, outqueue, quitevent):
        super().__init__(target=self._work);
        self._inqueue = inqueue
        self._outqueue = outqueue
        self._quitevent = quitevent

    def _work(self):
        while self._quitevent.wait(timeout=0.2) is False:
            try:
                w, h, nn, nx, xn, xx = self._inqueue.get(block=False)
                self._outqueue.put(ciepil.makeRaster(w, h, nn, nx, xn, xx))
            except queue.Empty:
                pass


class Swatch(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._nnbound = (50,-100,-100)
        self._nxbound = (50,-100,100)
        self._xnbound = (50,100,-100)
        self._xxbound = (50,100,100)
        self._reqqueue = queue.SimpleQueue();
        self._rspqueue = queue.SimpleQueue();
        self._quitevent = threading.Event();
        self._rasterworker = RasterWorker(self._reqqueue, self._rspqueue, self._quitevent)
        self._rasterworker.start()
        self._raster = None
        self.bind('<Configure>', self.doResize)
        self.bind_all('<Prior>', self.brighten)
        self.bind_all('<Next>', self.darken)
        self.after(200, func=self._draw)
        self.draw()
        
    def destroy(self):
        self._quitevent.set()
        self._rasterworker.join()

    def draw(self):
        w = self.winfo_width()
        h = self.winfo_height()
        # self.delete('mypicture')
        try:
            while True:
                self._reqqueue.get(block=False)
        except queue.Empty:
            pass
        
        self._reqqueue.put((w, h, self._nnbound, self._nxbound, self._xnbound, self._xxbound))
        
    
    def _draw(self):
        try:
            self._raster = PIL.ImageTk.PhotoImage(self._rspqueue.get(block=False))
            self.delete('mypicture')
            self.create_image(0, 0, anchor='nw', image=self._raster, tag='mypicture')
        except queue.Empty:
            pass
        self.after(200, func=self._draw)
                    
    def doResize(self, ev):
        self.draw()

    def brighten(self, ev=None):
        self._nnbound = (self._nnbound[0] + 10,) + self._nnbound[1:]
        self._nxbound = (self._nxbound[0] + 10,) + self._nxbound[1:]
        self._xnbound = (self._xnbound[0] + 10,) + self._xnbound[1:]
        self._xxbound = (self._xxbound[0] + 10,) + self._xxbound[1:]
        self.draw()

    def darken(self, ev=None):
        self._nnbound = (self._nnbound[0] - 10,) + self._nnbound[1:]
        self._nxbound = (self._nxbound[0] - 10,) + self._nxbound[1:]
        self._xnbound = (self._xnbound[0] - 10,) + self._xnbound[1:]
        self._xxbound = (self._xxbound[0] - 10,) + self._xxbound[1:]
        self.draw()
        

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Cie")

    root.rowconfigure(1, weight=1)
    root.columnconfigure(1, weight=1)

    swatch = Swatch(root)
    swatch.grid(row=1, column=1, sticky='news')

    root.mainloop()
    exit(0)

