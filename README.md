# OS iOS/macOS alike — C boot prototype

A small, native C visual prototype of the boot screen. It uses SDL2 for a window and rendering; Python/Tkinter is no longer used.

## Build

Install a C compiler, CMake, and SDL2 development files.

### macOS (Homebrew)
```sh
brew install cmake sdl2
cmake -S . -B build
cmake --build build --config Release
./build/os-boot
```

### Ubuntu / Debian
```sh
sudo apt-get install build-essential cmake libsdl2-dev
cmake -S . -B build
cmake --build build --config Release
./build/os-boot
```

Run fullscreen with `./build/os-boot --fullscreen`. Press Esc to exit; F11 toggles fullscreen.

This is only a desktop-rendered animation. SDL2 requires an operating system and graphics stack; it is not a bare-metal bootloader or kernel. The simple apple-like mark is an original prototype graphic, not an Apple logo.
