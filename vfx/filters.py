import cv2
import numpy as np

def greyscale(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

def invert(frame):
    return cv2.bitwise_not(frame)

def edge(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

def pixelate(frame):
    small = cv2.resize(frame, (40, 40))
    return cv2.resize(small, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)

def thermal(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.applyColorMap(gray, cv2.COLORMAP_JET)

def redglass(frame):
    h, w = frame.shape[:2]

    blurred = cv2.GaussianBlur(frame, (21, 21), 0)

    cx, cy = w // 2, h // 2

    x, y = np.meshgrid(np.arange(w), np.arange(h))

    dx = x - cx
    dy = y - cy

    dist = np.sqrt(dx*dx + dy*dy)

    factor = 1.0 + 0.0005 * dist

    map_x = (cx + dx * factor).astype(np.float32)
    map_y = (cy + dy * factor).astype(np.float32)

    warped = cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR)

    # tint = np.full_like(warped, (255, 80, 30))
    tint = np.full_like(warped, (30, 80, 255))

    warped = cv2.addWeighted(warped, 0.7, tint, 0.3, 0)

    return cv2.addWeighted(warped, 0.7, blurred, 0.9, 0)

def glass(frame):
    h, w = frame.shape[:2]

    blurred = cv2.GaussianBlur(frame, (21, 21), 0)

    cx, cy = w // 2, h // 2

    x, y = np.meshgrid(np.arange(w), np.arange(h))

    dx = x - cx
    dy = y - cy

    dist = np.sqrt(dx*dx + dy*dy)

    factor = 1.0 + 0.0005 * dist

    map_x = (cx + dx * factor).astype(np.float32)
    map_y = (cy + dy * factor).astype(np.float32)

    warped = cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR)

    # tint = np.full_like(warped, (255, 80, 30))
    tint = np.full_like(warped, (150, 0, 0))

    warped = cv2.addWeighted(warped, 0.7, tint, 0.3, 0)

    return cv2.addWeighted(warped, 0.7, blurred, 0.9, 0)

def chromatic_aberration(frame, shift=5, radial_strength=0.0008, blur=0):
    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2

    if blur > 0:
        frame = cv2.GaussianBlur(frame, (blur*2+1, blur*2+1), 0)

    b, g, r = cv2.split(frame)

    x, y = np.meshgrid(np.arange(w), np.arange(h))
    dx = x - cx
    dy = y - cy
    dist = np.sqrt(dx*dx + dy*dy)

    factor = 1.0 + radial_strength * dist

    map_x = (cx + dx * factor).astype(np.float32)
    map_y = (cy + dy * factor).astype(np.float32)

    shift_x = shift

    b_shift = cv2.remap(b, map_x + shift_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    g_shift = cv2.remap(g, map_x,         map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    r_shift = cv2.remap(r, map_x - shift_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    return cv2.merge([b_shift, g_shift, r_shift])
  
FILTERS = {
    'grey': greyscale,
    'invert': invert,
    'edge': edge,
    'pixelate': pixelate,
    'thermal': thermal,
    'glass': glass,
    'rglass': redglass,
    'chroma': chromatic_aberration
}

def applyFilter(frame, filters):
    out = frame.copy()

    for p in filters:
        if isinstance(p, tuple):
            name, *args = p
            out = FILTERS[name](out, *args)
        else:
            out = FILTERS[p](out)

    return out