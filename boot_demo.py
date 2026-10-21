#!/usr/bin/env python3
"""Minimal Apple-inspired boot animation prototype. Python standard library only."""
import argparse
import tkinter as tk

BLACK = "#000000"
WHITE = "#F5F5F7"
MUTED = "#77777D"
TRACK = "#29292D"
DURATION_MS = 5200


class Boot:
    def __init__(self, root, fullscreen=False):
        self.root = root
        root.title("OS Startup")
        root.configure(bg=BLACK)
        root.resizable(False, False)
        self.fullscreen = fullscreen
        root.attributes("-fullscreen", fullscreen)
        if not fullscreen:
            w, h = 960, 600
            root.update_idletasks()
            x = (root.winfo_screenwidth() - w) // 2
            y = (root.winfo_screenheight() - h) // 2
            root.geometry(f"{w}x{h}+{x}+{y}")
        self.canvas = tk.Canvas(root, bg=BLACK, bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.started = root.tk.call("clock", "milliseconds")
        root.bind("<Escape>", lambda _e: root.destroy())
        root.bind("<F11>", self.toggle_fullscreen)
        root.bind("<Configure>", self.resize)
        self.draw()
        self.animate()

    def toggle_fullscreen(self, _event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def resize(self, _event=None):
        if hasattr(self, "canvas"):
            self.root.after_idle(self.draw)

    @staticmethod
    def ease(t):
        t = max(0.0, min(1.0, t))
        return t * t * (3 - 2 * t)

    def logo(self, cx, cy, s):
        # Simple vector silhouette: a design study, not an Apple product.
        points = [
            (cx-2*s,cy-15*s),(cx-12*s,cy-23*s),(cx-24*s,cy-18*s),
            (cx-30*s,cy-5*s),(cx-27*s,cy+12*s),(cx-19*s,cy+28*s),
            (cx-10*s,cy+31*s),(cx-2*s,cy+27*s),(cx+7*s,cy+30*s),
            (cx+18*s,cy+26*s),(cx+27*s,cy+9*s),(cx+29*s,cy-6*s),
            (cx+21*s,cy-18*s),(cx+10*s,cy-21*s),(cx+1*s,cy-16*s)]
        self.canvas.create_polygon(points, smooth=True, splinesteps=28,
                                   fill=WHITE, outline=WHITE, tags="logo")
        self.canvas.create_oval(cx+3*s,cy-42*s,cx+21*s,cy-28*s,
                                fill=WHITE, outline=WHITE, tags="logo")
        self.canvas.create_line(cx+5*s,cy-28*s,cx+17*s,cy-39*s,
                                fill=BLACK, width=max(1,s), tags="logo")
        self.canvas.create_oval(cx+18*s,cy-5*s,cx+36*s,cy+13*s,
                                fill=BLACK, outline=BLACK, tags="logo")

    def draw(self):
        w, h = max(1,self.canvas.winfo_width()), max(1,self.canvas.winfo_height())
        self.cx, self.cy = w/2, h*.435
        self.canvas.delete("all")
        self.logo(self.cx,self.cy,min(w,h)/600*.92)
        self.bw, self.by = min(170,w*.32), h*.72
        self.canvas.create_line(self.cx-self.bw/2,self.by,self.cx+self.bw/2,self.by,
                                fill=TRACK,width=3,capstyle=tk.ROUND,tags="track")
        self.canvas.create_text(self.cx,self.by+34,text="Starting up",fill=MUTED,
                                font=("Helvetica Neue",10),tags="status")

    def animate(self):
        elapsed = self.root.tk.call("clock","milliseconds") - self.started
        p = min(1,elapsed/DURATION_MS)
        self.canvas.delete("progress")
        left = self.cx-self.bw/2
        right = left+self.bw*self.ease(p)
        if right > left+1:
            self.canvas.create_line(left,self.by,right,self.by,fill=WHITE,width=3,
                                    capstyle=tk.ROUND,tags="progress")
        if p >= 1:
            self.canvas.itemconfigure("status",text="Ready")
            self.root.after(900,self.finish)
        else:
            self.root.after(16,self.animate)

    def finish(self):
        self.canvas.delete("track")
        self.canvas.delete("progress")
        self.canvas.delete("status")


def main():
    parser = argparse.ArgumentParser(description="Minimal OS boot animation")
    parser.add_argument("--fullscreen", action="store_true",
                        help="fullscreen mode; press Esc to exit")
    args = parser.parse_args()
    root = tk.Tk()
    Boot(root,args.fullscreen)
    root.mainloop()


if __name__ == "__main__":
    main()
