"""Effacement des sous-titres incrustés par inpainting LaMa (reconstruit le décor, pas de flou).

Usage :
  python3 desub_lama.py IN.mp4 OUT.mp4 MODELE.onnx --zone x0,y0,x1,y1 [--zone ...]
                        [--overlay t0,t1,x0,y0,x1,y1,couleur ...]

--zone    : rectangle effacé sur CHAQUE image (là où apparaissent les sous-titres mot à mot).
            Ex. vidéo JoJo 1080x1080 (mots centrés) : --zone 255,830,825,952
--overlay : texte incrusté ponctuel, effacé entre t0 et t1 (secondes) ; couleur = yellow|pink|blue|any
            (masque = pixels de cette couleur dans le rectangle, élargis).
Modèle : HF_HUB_DISABLE_XET=1 python3 -c "from huggingface_hub import hf_hub_download as d; d('Carve/LaMa-ONNX','lama_fp32.onnx',local_dir='.')"
Vitesse : ~2,7 s/image sur 4 CPU (les plans fixes sont réutilisés) -> ~1 h 45 pour 90 s.
"""
import sys, os, time, argparse, subprocess, cv2, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lama import Lama

K = lambda n: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n))

def ov_mask(f, t, overlays):
    full = np.zeros(f.shape[:2], np.uint8); hit = False
    for t0, t1, x0, y0, x1, y1, k in overlays:
        if not (t0 <= t <= t1): continue
        H, S, V = cv2.split(cv2.cvtColor(f[y0:y1, x0:x1], cv2.COLOR_BGR2HSV))
        if k == 'yellow': c = ((H <= 38) | (H >= 165)) & (S > 110) & (V > 120)
        elif k == 'pink': c = ((H <= 14) | (H >= 155)) & (S > 50) & (V > 120)
        elif k == 'blue': c = ((H >= 100) & (H <= 135) & (S > 120) & (V > 60)) | ((H >= 40) & (H <= 90) & (S > 60) & (V > 120))
        else: c = np.ones_like(H, bool)
        c = cv2.morphologyEx(c.astype(np.uint8) * 255, cv2.MORPH_OPEN, K(3))
        c = cv2.morphologyEx(cv2.dilate(c, K(23)), cv2.MORPH_CLOSE, K(31))
        full[y0:y1, x0:x1] |= cv2.dilate(c, K(15)); hit = True
    return full if hit else None

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('dst'); ap.add_argument('model')
    ap.add_argument('--zone', action='append', default=[]); ap.add_argument('--overlay', action='append', default=[])
    a = ap.parse_args()
    zones = [tuple(int(v) for v in z.split(',')) for z in a.zone]
    ovs = []
    for o in a.overlay:
        p = o.split(','); ovs.append((float(p[0]), float(p[1]), *map(int, p[2:6]), p[6]))
    cap = cv2.VideoCapture(a.src); n = int(cap.get(7)); fps = cap.get(5); W, Hh = int(cap.get(3)), int(cap.get(4))
    L = Lama(a.model)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{Hh}', '-r', str(fps), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '15', '-pix_fmt', 'yuv420p', a.dst + '.video.mp4'], stdin=subprocess.PIPE)
    prev_ov = None; cache = {}; t0 = time.time(); runs = 0
    for i in range(n):
        ok, f = cap.read()
        if not ok: break
        m = np.zeros(f.shape[:2], np.uint8)
        for x0, y0, x1, y1 in zones: m[y0:y1, x0:x1] = 255
        o = ov_mask(f, i / fps, ovs); cur = o
        if prev_ov is not None: o = prev_ov if o is None else (o | prev_ov)
        prev_ov = cur
        if o is not None: m |= o
        if m.any():
            nl, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
            for k in range(1, nl):
                x, y, w, h, _ = st[k]; mk = ((lab == k) * 255).astype(np.uint8)
                sz = min(min(W, Hh), max(512, int(max(w, h) * 1.35))); cx, cy = x + w // 2, y + h // 2
                x0 = int(np.clip(cx - sz // 2, 0, W - sz)); y0 = int(np.clip(cy - sz // 2, 0, Hh - sz))
                crop = f[y0:y0 + sz, x0:x0 + sz]; mc = mk[y0:y0 + sz, x0:x0 + sz]; key = (k, x0, y0, sz)
                res = None
                if key in cache:  # plan fixe : on réutilise (plus rapide, pas de scintillement)
                    pc, pm, pr = cache[key]
                    if np.array_equal(pm, mc) and np.abs(crop.astype(np.int16) - pc.astype(np.int16))[mc == 0].mean() < 1.2: res = pr
                if res is None: res = L.fill(crop, mc); runs += 1
                cache[key] = (crop.copy(), mc, res)
                al = cv2.GaussianBlur((mc > 0).astype(np.float32), (0, 0), 2)[..., None]
                f[y0:y0 + sz, x0:x0 + sz] = (res * al + crop * (1 - al)).astype(np.uint8)
        else: cache = {}
        enc.stdin.write(f.tobytes())
        if i % 150 == 0: print(i, '/', n, 'runs', runs, round(time.time() - t0), 's', flush=True)
    enc.stdin.close(); enc.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a.dst + '.video.mp4', '-i', a.src, '-map', '0:v', '-map', '1:a?', '-c', 'copy', a.dst], check=True)
    os.remove(a.dst + '.video.mp4'); print('done', runs, 'passes LaMa', round(time.time() - t0), 's')

if __name__ == '__main__': main()
