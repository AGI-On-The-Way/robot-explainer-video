"""Editing sounds, synthesised here so nothing needs licensing.

TARGET is how loud each sound is on a phone speaker: its loudest 150 ms between 320 Hz and 9 kHz, in dB, against speech at about -17 dB there.
A phone cannot play low notes, so the low sounds carry their weight in harmonics above 320 Hz, and no sound peaks above -13 dBFS.
The editor's brief puts sounds at -18 to -24 dB; these sit in that range on a phone, six to eleven dB under the voice.
"""
import numpy as np

SR = 48000
TARGET = dict(boom=-23, deng=-24, ding=-24, di=-25, tick=-26, shua=-27, low=-26, qiang=-24, card=-26, bubble=-26, chime=-24, fade=-28)
MAX_PEAK = -13


def _t(sec):
    return np.arange(int(sec * SR)) / SR


def _fin(x):
    x = x.astype(np.float32)
    x[:48] *= np.linspace(0, 1, 48)
    x[-240:] *= np.linspace(1, 0, 240)
    return x / np.abs(x).max()


def _partials(t, freqs, amps, decays):
    return sum(a * np.exp(-t / d) * np.sin(2 * np.pi * f * t) for f, a, d in zip(freqs, amps, decays))


def _noise(n, seed=1):
    return np.random.default_rng(seed).standard_normal(n).astype(np.float32)


def _sweep_noise(sec, f0, f1, seed=1):
    """Noise through a resonant band moving from f0 to f1."""
    n = int(sec * SR)
    x, out = _noise(n, seed), np.zeros(n, np.float32)
    lo = band = 0.0
    for i in range(n):
        f = 2 * np.sin(np.pi * (f0 + (f1 - f0) * i / n) / SR)
        lo += f * band
        band += f * (x[i] - lo - 0.5 * band)
        out[i] = band
    return out


def boom():
    t = _t(1.1)
    sub = np.sin(2 * np.pi * np.cumsum(45 + 95 * np.exp(-t / .09)) / SR) * np.exp(-t / .42)
    body = np.sin(2 * np.pi * np.cumsum(330 + 420 * np.exp(-t / .05)) / SR) * np.exp(-t / .16)
    return _fin(sub + 1.1 * body + .5 * np.sin(2 * np.pi * 495 * t) * np.exp(-t / .22) + .35 * _sweep_noise(1.1, 900, 300, 5) * np.exp(-t / .03))


def deng():
    t = _t(.5)
    return _fin(_partials(t, [98, 196, 392, 588, 784, 1176], [.8, .7, 1, .55, .5, .22], [.2, .15, .14, .1, .08, .05]) + .08 * _noise(len(t)) * np.exp(-t / .006))


def ding():
    t = _t(.9)
    return _fin(_partials(t, [1568, 3136, 4328, 7050], [1, .28, .22, .06], [.34, .2, .1, .05]))


def di():
    t = _t(.26)
    return _fin((np.sin(2 * np.pi * 1320 * t) + .2 * np.sin(2 * np.pi * 2640 * t)) * np.minimum(1, (t[-1] - t) / .05))


def tick():
    t = _t(.09)
    return _fin(_partials(t, [1320, 2640, 3960], [1, .6, .3], [.024, .014, .008]) + .12 * _noise(len(t), 2) * np.exp(-t / .003))


def shua():
    t = _t(.3)
    return _fin(_sweep_noise(.3, 1200, 7000, 3) * np.sin(np.pi * t / .3) ** 2)


def low():
    t = _t(1.3)
    wob = 1 + .25 * np.sin(2 * np.pi * 5.5 * t)
    return _fin(_partials(t, [73, 146, 219, 438, 657, 876], [.7, .8, .8, .7, .4, .18], [1, 1, .9, .8, .6, .4]) * wob * np.minimum(1, t / .08) * np.minimum(1, (t[-1] - t) / .5))


def qiang():
    t = _t(.7)
    return _fin(_partials(t, [523, 1312, 2350, 3710], [1, .7, .45, .25], [.26, .16, .1, .06]) + .3 * _noise(len(t), 4) * np.exp(-t / .01))


def card():
    t = _t(.13)
    return _fin(np.sin(2 * np.pi * np.cumsum(620 + 5200 * t) / SR) * np.exp(-t / .05))


def bubble():
    t = _t(.1)
    a = np.sin(2 * np.pi * np.cumsum(420 + 7000 * t) / SR) * np.exp(-t / .03)
    return _fin(np.concatenate([a, .8 * a]))


def chime():
    t = _t(1.3)
    return _fin(_partials(t, [1319, 2638], [1, .2], [.45, .2]) + np.pad(_partials(t[:-9600], [1760, 3520], [.9, .18], [.5, .2]), (9600, 0)))


def fade():
    t = _t(1.8)
    return _fin(_partials(t, [82, 164, 330, 494, 660], [.8, .7, .7, .4, .2], [.7, .6, .55, .4, .3]) * np.minimum(1, t / .1))


SOUNDS = dict(boom=boom, deng=deng, ding=ding, di=di, tick=tick, shua=shua, low=low, qiang=qiang, card=card, bubble=bubble, chime=chime, fade=fade)


def phone_db(x):
    """Loudest 150 ms of x between 320 Hz and 9 kHz."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < 320) | (f > 9000)] = 0
    y = np.fft.irfft(X, len(x))
    w = min(len(y), int(.15 * SR))
    return 10 * np.log10(max((y[i:i + w] ** 2).sum() / w for i in range(0, len(y) - w + 1, w // 4)) + 1e-12)


def sound(name):
    x = SOUNDS[name]()
    return x * min(10 ** ((TARGET[name] - phone_db(x)) / 20), 10 ** (MAX_PEAK / 20))
