# sights

real-time hand-tracking vfx, put your hands up and watch the magic happen. built with mediapipe + opencv.

---

## what it does

you use your hands as the shape. the app tracks your finger landmarks and maps visual effects into the polygons your hands define.

**three modes** (hotkeys `1` `2` `3`):

- `1` — **quad mode**: three stacking quads between both hands
- `2` — **hex mode**: a six-pointed polygon between your fingertips
- `3` — **temp hex**: close fist to save, open to clear. the hex stretches between past and present

**effects available:**

- `glass` : barrel distortion + blue tint, looks like glass
- `rglass` : same but red tint
- `chroma` : chromatic aberration (rgb channel split)
- `grey`, `invert`, `edge`, `pixelate`, `thermal` : the classic vfx filters

effects chain. `['glass', 'chroma']` runs glass first then chroma on top.

**camera switcher** (hotkey `space`):

- the program will automatically look through your webcams on initialization, press `space` to scroll through them.

---

## demo

uhhh sometime soon

---

## manual setup

**requirements**
- python 3.10+
- a webcam

**install deps**

```
pip install opencv-python mediapipe numpy keyboard
```

**grab the mediapipe hand landmark model**

download `hand_landmarker.task` from [mediapipe's model page](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker) and drop it in:

```
sights/
└── mediapipe_tasks/
    └── hand_landmarker.task   ← here
```

**run it**

```
python main.py
```

press `ESC` to exit.

---

## config

edit `config.py` to tweak things:

---

## how it works

mediapipe gives you 21 landmarks per hand in normalized coords — sights converts those to pixel coords and uses specific landmark indices as polygon corners.

all effects run on the full frame first, then get composited into the polygon mask using alpha blending. so the "source" under the effect is always the real unfiltered frame, not the already-processed one.

---

## built with

- [mediapipe](https://ai.google.dev/edge/mediapipe) — hand landmark detection
- [opencv](https://opencv.org/) — frame capture and rendering  
- [numpy](https://numpy.org/) — all the math
- [keyboard](https://github.com/boppreh/keyboard) — hotkeys