import numpy as np

def getHands(result, width, height):
    """gets the mediapipe result, splits hands and landmarks into two arrays

    Args:
        result (dict): mediapipe result
        width (int): opencv frame width
        height (int): opencv frame height

    Returns:
        dict: hand landmarks in opencv frame coordinates
    """
    
    if not result.hand_landmarks:
        return {}

    hands = {}

    for i, hand_landmarks in enumerate(result.hand_landmarks):
        handedness = result.handedness[i][0].category_name

        coords = []

        for lm in hand_landmarks:
            coords.append((int(lm.x * width), int(lm.y * height)))

        hands[handedness] = coords

    return hands


def getQuad(hands, lPts, rPts):
    """Generates a numpy array of 4 points

    Args:
        hands (dict): see getHands()
        lPts (array[int]): landmarks to use on left hand
        rPts (array[int]): landmarks to use on right hand

    Returns:
        numpy array (int32): point positions in opencv frame
    """
    left = hands.get("Left")
    right = hands.get("Right")

    if left is None or right is None:
        return None

    l = [left[i] for i in lPts]
    r = [right[i] for i in rPts]

    pts = np.array(
        [
            l[0],
            r[0],            
            r[1],
            l[1],            
        ],
        dtype=np.int32,
    )

    return pts


def getHex(hands, lPts, rPts):
    """Generates a numpy array of 6 points

    Args:
        hands (dict): see getHands()
        lPts (array[int]): landmarks to use on left hand
        rPts (array[int]): landmarks to use on right hand

    Returns:
        numpy array (int32): point positions in opencv frame
    """
    left = hands.get("Left")
    right = hands.get("Right")

    if left is None or right is None:
        return None

    l = [left[i] for i in lPts]
    r = [right[i] for i in rPts]

    pts = np.array(
        [
            l[0],
            l[1],
            l[2],
            r[2],
            r[1],
            r[0],
        ],
        dtype=np.int32,
    )

    return pts


def getTempHex(hands, handedness, saved, cPts, sPts):
    """Generates a hex using saved hand position and current hand position

    Args:
        hands (_type_): _description_
        handedness (_type_): _description_
        savedHandPos (_type_): _description_
        cPts ():
        sPts ():

    Returns:
        _type_: _description_
    """
    current = hands.get(handedness)

    if current is None or saved is None:
        return None
    
    c = [current[i] for i in cPts]
    s = [saved[i] for i in sPts]

    pts = np.array(
        [
            s[0],       
            s[1],  
            s[2],  
            c[2],
            c[1],
            c[0], 
        ],
        dtype=np.int32,
    )

    return pts

def dist(a, b):
    return np.linalg.norm(np.array(a) - np.array(b)) # get straight line distance between two points, nothing special