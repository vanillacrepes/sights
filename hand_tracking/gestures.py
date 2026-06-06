import numpy as np

def dist(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))
  
def isClosed(hand, threshold=1):
    wrist = hand[0]

    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]

    h = max(1, dist(hand[0], hand[9]))

    tip_dist = [
        dist(hand[i], wrist) / h
        for i in tips
    ]

    close_to_palm = np.mean(tip_dist) < threshold

    fold_dist = []

    for tip, pip in zip(tips, pips):
        fold_dist.append(dist(hand[tip], hand[pip]) / h)

    fingers_folded = np.mean(fold_dist) < threshold

    return close_to_palm and fingers_folded