"""Auto subtitle removal: finds the subtitle zone itself, then inpaints in parallel (4 CPUs).
usage: desub_auto.py IN.mp4 OUT.mp4"""
import sys, os, time, subprocess, tempfile, cv2, numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from detect import text_mask

def find_zone(src, samples=60):
    cap = cv2.VideoCapture(src); n = int(cap.get(7)); H = int(cap.get(4))
    rows = np.zeros(H)
    for i in np.linspace(0, n - 1, samples).astype(int):
        cap.set(1, i); ok, f = cap.read()
        if ok: rows += text_mask(f, int(H * .08), int(H * .95)).any(1)
    hit = np.nonzero(rows >= 2)[0]
    if not len(hit): return int(H * .35), int(H * .95)
    return max(0, hit.min() - 30), min(H, hit.max() + 30)

def work(a):
    src, s, e, y0, y1, dst = a
    cap = cv2.VideoCapture(src); cap.set(1, s)
    W, H = int(cap.get(3)), int(cap.get(4))
    out = cv2.VideoWriter(dst, cv2.VideoWriter_fourcc(*"mp4v"), cap.get(5), (W, H)); prev = None
    for _ in range(s, e):
        ok, f = cap.read()
        if not ok: break
        raw = text_mask(f, y0, y1); m = raw if prev is None else raw | prev; prev = raw
        if m.any(): f[y0:y1] = cv2.inpaint(f[y0:y1], m[y0:y1], 6, cv2.INPAINT_TELEA)
        out.write(f)
    out.release()

if __name__ == "__main__":
    src, dst = sys.argv[1:3]; t0 = time.time()
    y0, y1 = find_zone(src); print("zone", y0, y1, flush=True)
    n = int(cv2.VideoCapture(src).get(7)); k = os.cpu_count() or 4
    cuts = np.linspace(0, n, k + 1).astype(int); tmp = tempfile.mkdtemp()
    parts = [(src, cuts[i], cuts[i + 1], y0, y1, f"{tmp}/p{i}.mp4") for i in range(k)]
    with Pool(k) as p: p.map(work, parts)
    open(f"{tmp}/l.txt", "w").write("".join(f"file '{x[-1]}'\n" for x in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{tmp}/l.txt", "-i", src,
                    "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "copy", "-y", dst], check=True)
    print("done", round(time.time() - t0), "s")
