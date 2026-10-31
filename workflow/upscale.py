"""Presenter track upscaled with Real-ESRGAN x2plus (BSD-3) on the Apple GPU, frame for frame.

  .venv-wan/bin/python -I workflow/upscale.py
Some of the plain upscale is mixed back so skin keeps its texture and the face does not change. No face-restoration model is used.
"""
import os, subprocess, time
import numpy as np
import spandrel
import torch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'work', 'source.mp4')
SEL = os.path.join(ROOT, 'work', 'select.txt')
OUT = os.path.join(ROOT, 'work', 'host.mp4')
W, H, MIX, BATCH = 544, 960, 0.72, 4

os.makedirs(os.path.dirname(OUT), exist_ok=True)
expr = open(SEL).read().strip()
dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', SRC, '-vf', f"select='{expr}',setpts=N/24/TB", '-an', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W * 2}x{H * 2}', '-r', '24', '-i', '-',
                        '-vf', 'crop=1080:1920,eq=contrast=1.04:saturation=1.07,format=yuv420p', '-c:v', 'libx264', '-crf', '15', '-preset', 'medium', '-g', '12', OUT], stdin=subprocess.PIPE)
model = spandrel.ModelLoader().load_from_file(os.path.join(ROOT, 'vendor', 'esrgan', 'RealESRGAN_x2plus.pth')).to('mps').eval()
n, t0 = 0, time.time()
while True:
    raw = dec.stdout.read(W * H * 3 * BATCH)
    if not raw:
        break
    b = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    x = torch.from_numpy(b.copy()).permute(0, 3, 1, 2).float().div(255).to('mps')
    with torch.no_grad():
        y = model.model(x).clamp(0, 1)
        base = torch.nn.functional.interpolate(x, scale_factor=2, mode='bicubic', align_corners=False, antialias=False).clamp(0, 1)
        y = MIX * y + (1 - MIX) * base
    enc.stdin.write((y.permute(0, 2, 3, 1).cpu().numpy() * 255 + .5).astype(np.uint8).tobytes())
    n += len(b)
    if n % 240 == 0:
        print(n, f'{n / (time.time() - t0):.2f} fps', flush=True)
enc.stdin.close(); enc.wait(); dec.wait()
print('frames', n, flush=True)
