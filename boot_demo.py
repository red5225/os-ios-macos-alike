#!/usr/bin/env python3
"""Visual prototype for OS iOS/macOS alike. Python-only mockup, not a real OS."""
import tkinter as tk
import math
import time

BG = "#080b14"
PANEL = "#111827"
ACCENT = "#77d8ff"
WHITE = "#f3f7ff"
MUTED = "#8290a7"

class BootDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("OS — boot prototype")
        self.root.geometry("900x560")
        self.root.minsize(700, 450)
        self.root.configure(bg=BG)
        self.canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.start = time.monotonic()
        self.phase = "boot"
        self.root.bind("<Escape>", lambda _e: self.root.destroy())
        self.root.bind("<Return>", lambda _e: self.desktop())
        self.draw()
        self.tick()

    def centered(self, y, text, font, fill, **kw):
        self.canvas.create_text(self.root.winfo_width()/2, y, text=text,
                                font=font, fill=fill, **kw)

    def draw_logo(self, cx, cy, scale=1.0):
        # Original rounded-loop mark; intentionally not an Apple logo.
        r = 34 * scale
        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r,
                                outline=ACCENT, width=max(2, int(3*scale)))
        self.canvas.create_arc(cx-r*.56, cy-r*.56, cx+r*.56, cy+r*.56,
                               start=35, extent=290, style="arc",
                               outline=WHITE, width=max(2, int(4*scale)))
        self.canvas.create_oval(cx-4*scale, cy-4*scale, cx+4*scale, cy+4*scale,
                                fill=ACCENT, outline="")

    def draw(self):
        self.canvas.delete("all")
        w, h = max(self.root.winfo_width(), 700), max(self.root.winfo_height(), 450)
        cx = w / 2
        elapsed = time.monotonic() - self.start
        if self.phase == "boot":
            pulse = 1 + 0.05 * math.sin(elapsed * 3)
            self.draw_logo(cx, h*.31, pulse)
            self.centered(h*.31+64, "OS", ("Helvetica", 29, "bold"), WHITE)
            self.centered(h*.31+97, "A new system is starting", ("Helvetica", 11), MUTED)
            bar_w = min(330, w*.52)
            x0, y0 = cx-bar_w/2, h*.62
            self.canvas.create_rectangle(x0, y0, x0+bar_w, y0+5, fill="#263247", outline="")
            progress = min(1, elapsed/6.8)
            self.canvas.create_rectangle(x0, y0, x0+bar_w*progress, y0+5, fill=ACCENT, outline="")
            messages = [
                "Starting firmware interface…",
                "Checking memory map…",
                "Preparing display subsystem…",
                "Loading core services…",
                "Starting user interface…",
            ]
            idx = min(len(messages)-1, int(elapsed/1.35))
            self.centered(y0+27, messages[idx], ("Menlo", 10), MUTED)
            self.centered(h-28, "PROTOTYPE  •  PYTHON VISUALIZATION", ("Menlo", 8), "#536078")
            if elapsed >= 7:
                self.desktop()
        else:
            self.draw_desktop(w, h, elapsed)

    def draw_desktop(self, w, h, elapsed):
        # Wallpaper gradient illusion using layered dark bands.
        for i in range(18):
            shade = 14 + i
            color = f"#{shade:02x}{shade+4:02x}{min(45,shade+20):02x}"
            self.canvas.create_rectangle(0, i*h/18, w, (i+1)*h/18+1, fill=color, outline="")
        self.canvas.create_oval(w*.48, -h*.52, w*1.15, h*.78, fill="#172e48", outline="")
        self.canvas.create_oval(-w*.3, h*.48, w*.65, h*1.5, fill="#14243b", outline="")
        # Top menu bar
        self.canvas.create_rectangle(0, 0, w, 30, fill="#101722", outline="")
        self.canvas.create_text(18, 15, text="◉", fill=ACCENT, font=("Helvetica", 12, "bold"), anchor="w")
        self.canvas.create_text(42, 15, text="OS", fill=WHITE, font=("Helvetica", 10, "bold"), anchor="w")
        self.canvas.create_text(w-18, 15, text=time.strftime("%a  %H:%M"), fill=WHITE, font=("Helvetica", 9), anchor="e")
        # Welcome window
        ww, wh = min(430, w*.7), 225
        x, y = (w-ww)/2, (h-wh)/2
        self.canvas.create_rectangle(x+5, y+7, x+ww+5, y+wh+7, fill="#05070b", outline="")
        self.canvas.create_rectangle(x, y, x+ww, y+wh, fill=PANEL, outline="#344257", width=1)
        self.canvas.create_rectangle(x, y, x+ww, y+34, fill="#1a2535", outline="")
        for i, c in enumerate(("#ff6b6b", "#ffd166", "#6ee7a8")):
            self.canvas.create_oval(x+13+i*16, y+12, x+21+i*16, y+20, fill=c, outline="")
        self.canvas.create_text(x+ww/2, y+68, text="Welcome.", fill=WHITE, font=("Helvetica", 24, "bold"))
        self.canvas.create_text(x+ww/2, y+105, text="A familiar feel. A system of our own.", fill="#b9c7d9", font=("Helvetica", 11))
        self.canvas.create_rectangle(x+ww/2-70, y+145, x+ww/2+70, y+181, fill="#d9f3ff", outline="")
        self.canvas.create_text(x+ww/2, y+163, text="Explore desktop", fill="#102033", font=("Helvetica", 10, "bold"))
        # Dock
        dw = min(350, w*.68)
        dx = (w-dw)/2
        self.canvas.create_rectangle(dx, h-64, dx+dw, h-18, fill="#1a2636", outline="#40516a", width=1)
        for i, (symbol, color) in enumerate((("⌂","#86d7ff"),("▦","#b6a2ff"),("◇","#a7f0c0"),("⚙","#f5d38a"),("●","#f7a6bd"))):
            bx = dx+22+i*min(63,(dw-44)/4)
            self.canvas.create_rectangle(bx, h-55, bx+30, h-27, fill=color, outline="", width=0)
            self.canvas.create_text(bx+15, h-41, text=symbol, fill="#142033", font=("Helvetica", 14, "bold"))
        self.canvas.create_text(14, h-10, text="ESC to quit", fill="#8b9ab0", font=("Menlo", 8), anchor="w")

    def desktop(self):
        self.phase = "desktop"
        self.start = time.monotonic()
        self.draw()

    def tick(self):
        if self.root.winfo_exists():
            self.draw()
            self.root.after(40, self.tick)

def main():
    root = tk.Tk()
    BootDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main()
