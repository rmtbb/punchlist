#!/usr/bin/env python3
"""Render media/loop.html frame-by-frame via window.render(t) and assemble a GIF.

Deterministic hyperframe pipeline: each frame is a pure function of normalized
time t in [0,1). Playwright captures retina PNGs; ffmpeg builds a palette and
emits a clean, looping GIF. Output: assets/demo.gif (+ assets/demo.mp4).
"""
import pathlib, shutil, subprocess, sys
from playwright.sync_api import sync_playwright

HERE   = pathlib.Path(__file__).resolve().parent
ROOT   = HERE.parent
HTML   = "file://" + str(HERE / "loop.html")
FRAMES = pathlib.Path("/tmp/pl-frames")
FPS    = 24
SECONDS = 6.5
N      = int(FPS * SECONDS)
OUT_W  = 760

def capture():
    if FRAMES.exists(): shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width":840,"height":480}, device_scale_factor=2)
        pg.goto(HTML)
        pg.wait_for_function("window.__ready === true", timeout=10000)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(400)  # let webfonts paint
        for i in range(N):
            pg.evaluate(f"window.render({i/N})")
            pg.wait_for_timeout(8)
            pg.screenshot(path=str(FRAMES / f"f{i:04d}.png"))
        b.close()
    print(f"captured {N} frames @ {FPS}fps ({SECONDS}s)")

def assemble():
    gif = ROOT / "assets" / "demo.gif"
    mp4 = ROOT / "assets" / "demo.mp4"
    vf = (f"scale={OUT_W}:-1:flags=lanczos,split[s0][s1];"
          f"[s0]palettegen=stats_mode=full[p];[s1][p]paletteuse=dither=sierra2_4a")
    subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",str(FRAMES/"f%04d.png"),
                    "-vf",vf,"-loop","0",str(gif)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",str(FRAMES/"f%04d.png"),
                    "-vf",f"scale={OUT_W}:-1:flags=lanczos,format=yuv420p",
                    "-movflags","+faststart",str(mp4)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    sz = gif.stat().st_size/1024
    print(f"wrote {gif}  ({sz:.0f} KB)")
    print(f"wrote {mp4}")

if __name__ == "__main__":
    capture()
    assemble()
