"""Fast subtitle removal: outline-based detection (detect.py) + OpenCV Telea inpainting."""
import sys, time, cv2
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from detect import text_mask
src, dst = sys.argv[1:3]
Y0, Y1 = 380, 880
cap = cv2.VideoCapture(src)
W, H = int(cap.get(3)), int(cap.get(4))
out = cv2.VideoWriter(dst, cv2.VideoWriter_fourcc(*"mp4v"), cap.get(5), (W, H))
prev, t0 = None, time.time()
while True:
    ok, f = cap.read()
    if not ok: break
    raw = text_mask(f, Y0, Y1)
    m = raw if prev is None else cv2.bitwise_or(raw, prev)
    prev = raw
    if m.any():
        b = f[Y0:Y1]
        b[:] = cv2.inpaint(b, m[Y0:Y1], 6, cv2.INPAINT_TELEA)
    out.write(f)
out.release(); print("done", round(time.time() - t0), "s")
