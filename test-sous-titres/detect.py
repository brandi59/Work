"""Detect outlined subtitle glyphs (white/green/yellow fill + pure black outline)."""
import cv2
import numpy as np

K3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
K5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))


def text_mask(frame, y0, y1, grow=2):
    """Return a full-frame uint8 mask of subtitle pixels between rows y0..y1."""
    h, w = frame.shape[:2]
    full = np.zeros((h, w), np.uint8)
    band = frame[y0:y1]
    hsv = cv2.cvtColor(band, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(hsv)
    white = (V > 205) & (S < 60)
    green = (H > 35) & (H < 90) & (S > 90) & (V > 120)
    yellow = (H >= 15) & (H <= 35) & (S > 110) & (V > 170)
    bright = ((white | green | yellow) * 255).astype(np.uint8)
    dark = V < 60

    n, lab, stats, _ = cv2.connectedComponentsWithStats(bright, connectivity=8)
    if n <= 1:
        return full
    # ring around each component: dilate the label image (labels are disjoint)
    labf = lab.astype(np.float32)
    dil = cv2.dilate(labf, K5, iterations=1).astype(np.int32)
    ring = (lab == 0) & (dil > 0)
    ring_lab = dil[ring]
    tot = np.bincount(ring_lab, minlength=n)
    drk = np.bincount(ring_lab, weights=dark[ring].astype(np.float64), minlength=n)
    ratio = np.divide(drk, tot, out=np.zeros(n), where=tot > 0)

    area = stats[:, cv2.CC_STAT_AREA]
    hgt = stats[:, cv2.CC_STAT_HEIGHT]
    wid = stats[:, cv2.CC_STAT_WIDTH]
    ok = (ratio > 0.45) & (area >= 6) & (area < 6000) & (hgt < 90) & (wid < 400)
    ok[0] = False
    glyphs = (ok[lab] * 255).astype(np.uint8)
    if not glyphs.any():
        return full
    # keep only glyphs that belong to a text-like cluster (or are big single letters)
    words = cv2.dilate(glyphs, cv2.getStructuringElement(cv2.MORPH_RECT, (15, 7)))
    m, wl, ws, _ = cv2.connectedComponentsWithStats(words, connectivity=8)
    gl = cv2.connectedComponentsWithStats(glyphs, connectivity=8)[0] - 1
    keepw = np.zeros(m, bool)
    for i in range(1, m):
        x, y, ww, hh, a = ws[i]
        # reject blobs taller than ~2 lines or tiny noise
        if hh <= 170 and (ww >= 18 or hh >= 22):
            keepw[i] = True
    glyphs = glyphs & (keepw[wl] * 255).astype(np.uint8)
    # include the black outline and anti-aliasing around kept glyphs
    mask = cv2.dilate(glyphs, K5, iterations=grow + 1)
    full[y0:y1] = mask
    return full
