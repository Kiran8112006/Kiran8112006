"""
Generate two animated GIFs for the GitHub README:
  1. sao-motion.gif  — atmospheric moon + drifting stars
  2. signal-motion.gif — engineering oscilloscope waveform pulse
"""

import math
import os
import random
from PIL import Image, ImageDraw

ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

BG = (13, 17, 23)          # GitHub dark #0d1117
PURPLE = (138, 124, 248)   # accent
DIM_PURPLE = (80, 70, 160)
WHITE = (255, 255, 255)
GREY = (139, 148, 158)
DARK_GREY = (33, 38, 45)


# -------------------------------------------------
# 1.  SAO atmospheric animation
#     Size: 700 x 180 px, 48 frames, 80 ms/frame
# -------------------------------------------------
def make_sao_motion():
    W, H = 700, 180
    N_FRAMES = 48
    DELAY = 80          # ms per frame

    rng = random.Random(42)
    stars = []
    for _ in range(55):
        x = rng.randint(0, W - 1)
        y = rng.randint(0, H - 1)
        r = rng.choice([0, 0, 0, 1, 1, 2])
        phase = rng.uniform(0, 2 * math.pi)
        speed = rng.uniform(0.05, 0.15)
        stars.append((x, y, r, phase, speed))

    particles = []
    for _ in range(8):
        x = rng.uniform(50, W - 50)
        y = rng.uniform(20, H - 20)
        phase = rng.uniform(0, 2 * math.pi)
        amp = rng.uniform(4, 10)
        speed = rng.uniform(0.03, 0.07)
        particles.append([x, y, phase, amp, speed])

    moon_cx = W - 90
    moon_cy = 45
    moon_r = 22

    frames = []
    for f in range(N_FRAMES):
        t = f / N_FRAMES

        img = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(img)

        for row in range(H):
            frac = row / H
            rv = int(13 + frac * 6)
            gv = int(17 + frac * 5)
            bv = int(23 + frac * 12)
            draw.line([(0, row), (W, row)], fill=(rv, gv, bv))

        for sx, sy, sr, phase, speed in stars:
            angle = phase + t * speed * 2 * math.pi * N_FRAMES
            brightness = int(140 + 115 * math.sin(angle) ** 2)
            col = (brightness, brightness, min(brightness + 15, 255))
            if sr == 0:
                draw.point((sx, sy), fill=col)
            else:
                draw.ellipse(
                    [sx - sr, sy - sr, sx + sr, sy + sr],
                    fill=col,
                )

        for g_r in range(moon_r + 22, moon_r - 1, -1):
            frac = (g_r - moon_r) / 22
            alpha = int(18 * (1 - frac) ** 2)
            col = (
                int(200 * alpha / 255 + BG[0] * (1 - alpha / 255)),
                int(210 * alpha / 255 + BG[1] * (1 - alpha / 255)),
                int(255 * alpha / 255 + BG[2] * (1 - alpha / 255)),
            )
            draw.ellipse(
                [moon_cx - g_r, moon_cy - g_r, moon_cx + g_r, moon_cy + g_r],
                outline=col,
            )

        moon_col = (230, 235, 255)
        draw.ellipse(
            [moon_cx - moon_r, moon_cy - moon_r, moon_cx + moon_r, moon_cy + moon_r],
            fill=moon_col,
        )
        draw.ellipse(
            [moon_cx - moon_r + 7, moon_cy - moon_r - 5,
             moon_cx + moon_r + 7, moon_cy + moon_r - 5],
            fill=BG,
        )

        for px_f, py_f, phase, amp, speed in particles:
            angle = phase + t * speed * 2 * math.pi * N_FRAMES
            dy = amp * math.sin(angle)
            bri = int(60 + 50 * (math.sin(angle * 0.7 + 1) + 1) / 2)
            col = (bri, bri, min(bri + 40, 255))
            px_i = int(px_f)
            py_i = int(py_f + dy)
            draw.ellipse([px_i - 2, py_i - 2, px_i + 2, py_i + 2], fill=col)

        frames.append(img)

    out_path = os.path.join(ASSETS_DIR, "sao-motion.gif")
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=DELAY,
        optimize=False,
    )
    print(f"Generated {out_path}  ({len(frames)} frames)")


# -------------------------------------------------
# 2.  Engineering signal animation
#     Size: 700 x 120 px, 36 frames, 55 ms/frame
# -------------------------------------------------
def make_signal_motion():
    W, H = 700, 120
    N_FRAMES = 36
    DELAY = 55

    GRID = (22, 30, 40)
    LINE_COL = (70, 85, 110)
    WAVE_COL = (100, 115, 148)
    DOT_COL = WHITE

    frames = []
    for f in range(N_FRAMES):
        t = f / N_FRAMES

        img = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(img)

        for row in range(H):
            frac = row / H
            rv = int(13 + frac * 4)
            gv = int(17 + frac * 4)
            bv = int(23 + frac * 10)
            draw.line([(0, row), (W, row)], fill=(rv, gv, bv))

        for gy in [H // 4, H // 2, 3 * H // 4]:
            draw.line([(0, gy), (W, gy)], fill=GRID)
        for gx in range(0, W, 70):
            draw.line([(gx, 0), (gx, H)], fill=GRID)

        cy = H // 2
        draw.line([(0, cy), (W, cy)], fill=LINE_COL)

        amplitude = H * 0.30
        freq = 2.5
        phase_shift = -t * 2 * math.pi * 2

        prev = None
        for px in range(W):
            angle = (px / W) * freq * 2 * math.pi + phase_shift
            py = int(cy - amplitude * math.sin(angle))
            py = max(2, min(H - 3, py))
            if prev is not None:
                draw.line([prev, (px, py)], fill=WAVE_COL, width=1)
            prev = (px, py)

        pulse_x = int(t * W)
        pulse_angle = (pulse_x / W) * freq * 2 * math.pi + phase_shift
        pulse_y = int(cy - amplitude * math.sin(pulse_angle))
        pulse_y = max(4, min(H - 5, pulse_y))

        for gr in range(12, 0, -1):
            alpha_f = (1 - gr / 12) ** 2
            col = (
                int(PURPLE[0] * alpha_f + BG[0] * (1 - alpha_f)),
                int(PURPLE[1] * alpha_f + BG[1] * (1 - alpha_f)),
                int(PURPLE[2] * alpha_f + BG[2] * (1 - alpha_f)),
            )
            draw.ellipse(
                [pulse_x - gr, pulse_y - gr, pulse_x + gr, pulse_y + gr],
                fill=col,
            )
        draw.ellipse(
            [pulse_x - 3, pulse_y - 3, pulse_x + 3, pulse_y + 3],
            fill=DOT_COL,
        )

        led_y = H - 14
        for li, led_x in enumerate([W - 22, W - 38, W - 54]):
            blink_phase = t * 2 * math.pi + li * (2 * math.pi / 3)
            on = math.sin(blink_phase) > 0.3
            col = PURPLE if on else (35, 40, 55)
            draw.ellipse([led_x - 4, led_y - 4, led_x + 4, led_y + 4], fill=col)

        frames.append(img)

    out_path = os.path.join(ASSETS_DIR, "signal-motion.gif")
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=DELAY,
        optimize=False,
    )
    print(f"Generated {out_path}  ({len(frames)} frames)")


if __name__ == "__main__":
    make_sao_motion()
    make_signal_motion()
    print("Done.")
