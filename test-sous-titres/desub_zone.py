"""Sous-titres d'origine centrés à ombre portée (sans contour noir), là où desub_auto.py échoue.
Repère les lettres blanches dans une bande fixe Y0..Y1, inpainte une boîte centrée couvrant le mot.
usage: Y0=497 Y1=533 python3 desub_zone.py IN.mp4 OUT.mp4  (vidéo sans audio en sortie)"""
import sys, os, subprocess, tempfile, cv2, numpy as np
from multiprocessing import Pool
K5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
def text_mask(f, y0, y1, grow=3):
    full = np.zeros(f.shape[:2], np.uint8)
    hsv = cv2.cvtColor(f[y0:y1], cv2.COLOR_BGR2HSV)
    white = ((hsv[...,2] > 205) & (hsv[...,1] < 55)).astype(np.uint8) * 255
    n, lab, st, _ = cv2.connectedComponentsWithStats(white, connectivity=8)
    ok = (st[:,3] >= 6) & (st[:,3] <= 30) & (st[:,2] <= 45) & (st[:,4] >= 8); ok[0] = False
    g = (ok[lab] * 255).astype(np.uint8)
    if not g.any(): return full
    w = cv2.dilate(g, cv2.getStructuringElement(cv2.MORPH_RECT, (19, 5)))
    m, wl, ws, _ = cv2.connectedComponentsWithStats(w, connectivity=8)
    keep = np.zeros(m, bool)
    for i in range(1, m):
        x, y, ww, hh, a = ws[i]
        cx = x + ww / 2
        if ww >= 22 and hh <= 40 and abs(cx - f.shape[1] / 2) < 200: keep[i] = True
    g = g & (keep[wl] * 255).astype(np.uint8)
    xs = np.nonzero(g.any(0))[0]
    if len(xs) and xs.max() - xs.min() >= 14:
        hw = int(max(abs(xs.min() - f.shape[1] // 2), abs(xs.max() - f.shape[1] // 2))) + 16
        c = f.shape[1] // 2; full[y0:y1, max(0, c - hw):c + hw] = 255
    return full
Y0, Y1 = int(os.environ.get("Y0", 488)), int(os.environ.get("Y1", 540))
def work(a):
    src, s, e, dst = a
    cap = cv2.VideoCapture(src); cap.set(1, s)
    W, H = int(cap.get(3)), int(cap.get(4))
    hold = 0; out = cv2.VideoWriter(dst, cv2.VideoWriter_fourcc(*"mp4v"), cap.get(5), (W, H)); prev = None
    for _ in range(s, e):
        ok, f = cap.read()
        if not ok: break
        raw = text_mask(f, Y0, Y1, grow=3)
        if raw.any(): hold = 8
        elif prev is not None and hold > 0: raw = prev; hold -= 1
        m = raw if prev is None else raw | prev; prev = raw
        if m.any(): f[Y0-10:] = cv2.inpaint(f[Y0-10:], m[Y0-10:], 7, cv2.INPAINT_TELEA)
        out.write(f)
    out.release()
if __name__ == "__main__":
    src, dst = sys.argv[1:3]
    n = int(cv2.VideoCapture(src).get(7)); k = os.cpu_count() or 4
    cuts = np.linspace(0, n, k + 1).astype(int); tmp = tempfile.mkdtemp()
    parts = [(src, cuts[i], cuts[i + 1], f"{tmp}/p{i}.mp4") for i in range(k)]
    with Pool(k) as p: p.map(work, parts)
    open(f"{tmp}/l.txt", "w").write("".join(f"file '{x[-1]}'\n" for x in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{tmp}/l.txt",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-y", dst], check=True)
