# OS iOS/macOS alike

An early visual prototype for an original operating-system interface inspired by the polish of macOS and iOS. This is deliberately a **Python animation mockup**, not a kernel or a bootable OS yet. The plan is to use it to settle the visual direction before porting the graphics and boot flow to C and eventually integrating them with a real kernel.

## Run

Requires Python 3 with Tkinter available. No pip packages are required.

```bash
python3 boot_demo.py
```

A window shows an animated boot logo, simulated initialization messages, a progress bar, then a desktop concept. Press **Esc** to quit. Press **Enter** to jump to the desktop early.

## Current scope

- Animated boot screen and progress bar
- Simulated system startup messages
- Desktop-style mockup with menu bar, welcome window, and dock
- Standard-library-only Python implementation

## Roadmap

1. Confirm the look and animation timing.
2. Port the drawing and animation logic to C.
3. Define the graphics/display abstraction for the target boot environment.
4. Replace simulated messages with real boot-stage status from a kernel/loader.

No real hardware checks, kernel startup, or OS booting occur in this prototype.
