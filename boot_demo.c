/*
 * OS boot animation prototype — C + SDL2.
 * A minimal, black-screen startup sequence with a restrained vector mark.
 * This is a desktop visual prototype, not a firmware bootloader.
 */
#include <SDL.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>

#define START_WIDTH 960
#define START_HEIGHT 600
#define BOOT_DURATION_MS 5200u
#define WHITE ((SDL_Color){245, 245, 247, 255})
#define BLACK ((SDL_Color){0, 0, 0, 255})
#define TRACK ((SDL_Color){41, 41, 45, 255})
#define MUTED ((SDL_Color){119, 119, 125, 255})

static float clamp01(float x) {
    if (x < 0.0f) return 0.0f;
    if (x > 1.0f) return 1.0f;
    return x;
}

static float smoothstep(float x) {
    x = clamp01(x);
    return x * x * (3.0f - 2.0f * x);
}

static void set_color(SDL_Renderer *r, SDL_Color c) {
    SDL_SetRenderDrawColor(r, c.r, c.g, c.b, c.a);
}

static void fill_circle(SDL_Renderer *r, int cx, int cy, int radius, SDL_Color c) {
    set_color(r, c);
    for (int y = -radius; y <= radius; ++y) {
        int x = (int)sqrt((double)(radius * radius - y * y));
        SDL_RenderDrawLine(r, cx - x, cy + y, cx + x, cy + y);
    }
}

/* Small custom apple-like silhouette drawn with filled circles/ellipses.
   It is a visual design study, not an Apple logo or an Apple product. */
static void draw_mark(SDL_Renderer *r, int cx, int cy, float scale) {
    int s = (int)lroundf(scale);
    if (s < 1) s = 1;
    set_color(r, WHITE);

    SDL_Rect body = {cx - 30*s, cy - 22*s, 60*s, 55*s};
    SDL_RenderFillRect(r, &body);
    fill_circle(r, cx - 14*s, cy - 7*s, 16*s, WHITE);
    fill_circle(r, cx + 14*s, cy - 7*s, 16*s, WHITE);
    fill_circle(r, cx - 13*s, cy + 13*s, 15*s, WHITE);
    fill_circle(r, cx + 13*s, cy + 13*s, 15*s, WHITE);

    /* Bite cut-out */
    fill_circle(r, cx + 29*s, cy - 2*s, 10*s, BLACK);

    /* Leaf: a restrained tilted oval approximated by a polygon. */
    SDL_Point leaf[] = {
        {cx + 2*s, cy - 28*s}, {cx + 5*s, cy - 39*s},
        {cx + 17*s, cy - 46*s}, {cx + 20*s, cy - 35*s},
        {cx + 12*s, cy - 27*s}
    };
    set_color(r, WHITE);
    SDL_RenderDrawLines(r, leaf, (int)(sizeof leaf / sizeof leaf[0]));
    for (int i = 0; i < 5; ++i)
        fill_circle(r, leaf[i].x, leaf[i].y, 2*s, WHITE);
}

static void draw_boot(SDL_Renderer *renderer, int width, int height,
                      Uint32 elapsed, bool finished) {
    set_color(renderer, BLACK);
    SDL_RenderClear(renderer);

    int cx = width / 2;
    int cy = (int)(height * 0.435f);
    float scale = fminf((float)width, (float)height) / 600.0f;
    draw_mark(renderer, cx, cy, scale);

    if (!finished) {
        int bar_width = (int)fminf(170.0f, width * 0.32f);
        int bar_y = (int)(height * 0.72f);
        SDL_Rect track = {cx - bar_width / 2, bar_y, bar_width, 3};
        set_color(renderer, TRACK);
        SDL_RenderFillRect(renderer, &track);

        float progress = smoothstep((float)elapsed / (float)BOOT_DURATION_MS);
        SDL_Rect fill = {track.x, track.y, (int)(bar_width * progress), 3};
        if (fill.w > 0) {
            set_color(renderer, WHITE);
            SDL_RenderFillRect(renderer, &fill);
        }
        /* Keep text out of the prototype: the boot screen is deliberately quiet. */
    }

    SDL_RenderPresent(renderer);
}

int main(int argc, char **argv) {
    bool fullscreen = false;
    for (int i = 1; i < argc; ++i) {
        if (SDL_strcmp(argv[i], "--fullscreen") == 0) fullscreen = true;
        else if (SDL_strcmp(argv[i], "--help") == 0) {
            SDL_Log("Usage: %s [--fullscreen]", argv[0]);
            return 0;
        }
    }

    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_TIMER) != 0) {
        SDL_Log("SDL initialization failed: %s", SDL_GetError());
        return 1;
    }

    Uint32 flags = SDL_WINDOW_SHOWN;
    if (fullscreen) flags |= SDL_WINDOW_FULLSCREEN_DESKTOP;
    SDL_Window *window = SDL_CreateWindow(
        "OS Startup", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
        START_WIDTH, START_HEIGHT, flags);
    if (!window) {
        SDL_Log("Window creation failed: %s", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    SDL_Renderer *renderer = SDL_CreateRenderer(
        window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    if (!renderer) renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_SOFTWARE);
    if (!renderer) {
        SDL_Log("Renderer creation failed: %s", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    bool running = true;
    bool finished = false;
    Uint32 started = SDL_GetTicks();
    Uint32 finish_at = 0;

    while (running) {
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) running = false;
            if (event.type == SDL_KEYDOWN) {
                if (event.key.keysym.sym == SDLK_ESCAPE) running = false;
                if (event.key.keysym.sym == SDLK_F11) {
                    Uint32 current = SDL_GetWindowFlags(window);
                    SDL_SetWindowFullscreen(window,
                        (current & SDL_WINDOW_FULLSCREEN_DESKTOP) ? 0 : SDL_WINDOW_FULLSCREEN_DESKTOP);
                }
            }
        }

        int width, height;
        SDL_GetRendererOutputSize(renderer, &width, &height);
        Uint32 elapsed = SDL_GetTicks() - started;
        if (!finished && elapsed >= BOOT_DURATION_MS) {
            finished = true;
            finish_at = SDL_GetTicks();
        }
        draw_boot(renderer, width, height, elapsed, finished);
        if (finished && SDL_GetTicks() - finish_at >= 1000u) running = false;
        SDL_Delay(16);
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}
