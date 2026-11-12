"""Remove burned-in outlined subtitles from a band of each frame via OpenCV inpainting."""
import sys
import cv2
import numpy as np

src, dst = sys.argv[1], sys.argv[2]
Y0, Y1 = int(sys.argv[3]), int(sys.argv[4])

cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(dst, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
k3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
k5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
prev = None
while True:
    ok, frame = cap.read()
    if not ok:
        break
    band = frame[Y0:Y1]
    hsv = cv2.cvtColor(band, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(hsv)
    white = (V > 215) & (S < 50)
    green = (H > 35) & (H < 85) & (S > 150) & (V > 170)
    bright = ((white | green) * 255).astype(np.uint8)
    dark = ((V < 35) * 255).astype(np.uint8)
    # text = where pure white/green sits right against a pure-black outline
    edge = cv2.bitwise_and(cv2.dilate(bright, k3, iterations=2),
                           cv2.dilate(dark, k3, iterations=2))
    # drop tiny isolated specks (scene noise)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(edge, connectivity=8)
    keep = np.zeros(n, np.uint8)
    keep[1:] = (stats[1:, cv2.CC_STAT_AREA] >= 25) * 255
    edge = keep[lab]
    # fill glyph interiors and cover outline + anti-aliasing
    mask = cv2.morphologyEx(edge, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
    mask = cv2.dilate(mask, k5, iterations=2)
    # temporal smoothing to reduce flicker
    if prev is not None:
        mask = cv2.bitwise_or(mask, cv2.erode(prev, k3))
    prev = mask
    band[:] = cv2.inpaint(band, mask, 5, cv2.INPAINT_TELEA)
    out.write(frame)
out.release()
