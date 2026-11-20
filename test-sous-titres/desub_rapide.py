"""Effacement RAPIDE et propre des sous-titres incrustés : LaMa « manga » (entraîné sur anime/manga,
taille d'entrée libre) appliqué uniquement sur une bande serrée autour de la zone, 4 processus en parallèle,
réutilisation des images identiques (animation « en 2 »). ~5x plus rapide que desub_lama.py.

Usage :
  python3 desub_rapide.py IN.mp4 OUT.mp4 lama-manga-dynamic.onnx --zone x0,y0,x1,y1 [--zone ...]
                          [--overlay t0,t1,x0,y0,x1,y1,couleur ...]
  (mêmes options que desub_lama.py ; couleur = yellow|pink|blue|any)
Modèle : HF_HUB_DISABLE_XET=1 python3 -c "from huggingface_hub import hf_hub_download as d; d('ogkalu/lama-manga-onnx-dynamic','lama-manga-dynamic.onnx',local_dir='.')"
"""
import sys, os, time, argparse, subprocess, tempfile, cv2, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
from desub_lama import ov_mask

MARGIN_Y, MARGIN_X, REUSE = 40, 56, 2.0

def worker(a):
    src, s, e, dst, model, zones, ovs = a
    import onnxruntime as ort
    o = ort.SessionOptions(); o.intra_op_num_threads = 1; o.inter_op_num_threads = 1
    sess = ort.InferenceSession(model, o)
    cap = cv2.VideoCapture(src); cap.set(1, s); fps = cap.get(5); W, H = int(cap.get(3)), int(cap.get(4))
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(fps), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '15', '-pix_fmt', 'yuv420p', dst], stdin=subprocess.PIPE)
    prev_ov = None; cache = {}; runs = 0
    for i in range(s, e):
        ok, f = cap.read()
        if not ok: break
        m = np.zeros((H, W), np.uint8)
        for x0, y0, x1, y1 in zones: m[y0:y1, x0:x1] = 255
        ov = ov_mask(f, i / fps, ovs); cur = ov
        if prev_ov is not None: ov = prev_ov if ov is None else (ov | prev_ov)
        prev_ov = cur
        if ov is not None: m |= ov
        new = {}
        if m.any():
            nl, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
            for k in range(1, nl):
                x, y, w, h, _ = st[k]
                x0, y0 = max(0, x - MARGIN_X), max(0, y - MARGIN_Y); x1, y1 = min(W, x + w + MARGIN_X), min(H, y + h + MARGIN_Y)
                crop = f[y0:y1, x0:x1].copy(); mc = (lab[y0:y1, x0:x1] == k).astype(np.uint8)
                key = (x0, y0, x1, y1); res = None
                if key in cache:
                    pc, pm, pr = cache[key]
                    if np.array_equal(pm, mc) and np.abs(crop.astype(np.int16) - pc.astype(np.int16)).mean() < REUSE: res = pr
                if res is None:
                    hh, ww = mc.shape; Hp, Wp = (hh + 7) // 8 * 8, (ww + 7) // 8 * 8
                    c2 = cv2.copyMakeBorder(crop, 0, Hp - hh, 0, Wp - ww, cv2.BORDER_REFLECT)
                    m2 = cv2.copyMakeBorder(mc, 0, Hp - hh, 0, Wp - ww, cv2.BORDER_CONSTANT)
                    xin = c2[..., ::-1].transpose(2, 0, 1)[None].astype(np.float32) / 255
                    r = sess.run(None, {'image': xin, 'mask': m2[None, None].astype(np.float32)})[0][0].transpose(1, 2, 0)
                    if r.max() <= 1.5: r = r * 255
                    res = np.clip(r[:hh, :ww, ::-1], 0, 255).astype(np.uint8); runs += 1
                new[key] = (crop, mc, res)
                al = cv2.GaussianBlur(mc.astype(np.float32), (0, 0), 2)[..., None]
                f[y0:y1, x0:x1] = (res * al + crop * (1 - al)).astype(np.uint8)
        cache = new
        enc.stdin.write(f.tobytes())
    enc.stdin.close(); enc.wait()
    return runs

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('dst'); ap.add_argument('model')
    ap.add_argument('--zone', action='append', default=[]); ap.add_argument('--overlay', action='append', default=[])
    ap.add_argument('--proc', type=int, default=os.cpu_count() or 4)
    a = ap.parse_args()
    zones = [tuple(int(v) for v in z.split(',')) for z in a.zone]
    ovs = [(float(p[0]), float(p[1]), *map(int, p[2:6]), p[6]) for p in (o.split(',') for o in a.overlay)]
    n = int(cv2.VideoCapture(a.src).get(7)); t0 = time.time(); tmp = tempfile.mkdtemp()
    cuts = np.linspace(0, n, a.proc + 1).astype(int)
    parts = [(a.src, cuts[i], cuts[i + 1], f'{tmp}/p{i}.mp4', a.model, zones, ovs) for i in range(a.proc)]
    with Pool(a.proc) as p: runs = p.map(worker, parts)
    open(f'{tmp}/l.txt', 'w').write(''.join(f"file '{x[3]}'\n" for x in parts))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/l.txt', '-i', a.src,
                    '-map', '0:v', '-map', '1:a?', '-c', 'copy', a.dst], check=True)
    print('done', n, 'images,', sum(runs), 'passes,', round(time.time() - t0), 's', flush=True)

if __name__ == '__main__': main()
