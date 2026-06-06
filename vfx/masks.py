import numpy as np

def applyMask(frame, filtered, mask):
    mask_f = mask.astype(np.float32) / 255.0

    mask_f = mask_f[:, :, None]

    return (filtered * mask_f + frame * (1 - mask_f)).astype(np.uint8)