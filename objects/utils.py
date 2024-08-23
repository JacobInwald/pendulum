import numpy as np

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

def clip(v, max):
    norm = np.linalg.norm(v)
    if norm <= 0.1: 
       return np.array([0.0, 0.0])
    return max * normalize(v) if norm > max else v

def is_degenerate_rect(rect):
    x1, y1, x2, y2 = rect
    return x1 >= x2 or y1 >= y2
