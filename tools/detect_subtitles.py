#!/usr/bin/env python3
"""Détection des sous-titres incrustés d'une vidéo source (étape 3.5 du workflow).

Échantillonne des images sur toute la vidéo, repère les bandes horizontales où
apparaît du texte incrusté (blanc/jaune avec contour sombre), puis propose un
recadrage qui les exclut entièrement. Génère aussi une planche d'images avec
les bandes détectées et le recadrage proposé, pour la vérification visuelle.

Usage :
    python3 tools/detect_subtitles.py video.mp4 [--frames 24] [--out dossier]

Sortie : JSON sur stdout + <out>/planche.jpg
"""
import argparse
import json
import os
import subprocess
import sys

import cv2
import numpy as np


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height:format=duration",
         "-of", "json", path],
        capture_output=True, text=True, check=True).stdout
    info = json.loads(out)
    s = info["streams"][0]
    return s["width"], s["height"], float(info["format"]["duration"])


def grab(path, t):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", path,
         "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
        capture_output=True, check=True).stdout
    return cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)


def text_rows(frame):
    """Score par ligne : pixels clairs (blanc/jaune) collés à un contour sombre."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    white = (v > 200) & (s < 50)
    yellow = (h >= 20) & (h <= 35) & (s > 120) & (v > 180)
    bright = (white | yellow).astype(np.uint8)
    dark = (v < 60).astype(np.uint8)
    dark_near = cv2.dilate(dark, np.ones((5, 5), np.uint8))
    cand = bright & dark_near
    # Le texte forme des traits courts et denses horizontalement :
    # on garde les zones où les candidats se regroupent sur une même ligne.
    cand = cv2.morphologyEx(cand, cv2.MORPH_CLOSE, np.ones((3, 15), np.uint8))
    return cand.mean(axis=1)


def find_bands(score, height, thr):
    k = max(3, height // 120)
    smooth = np.convolve(score, np.ones(k) / k, mode="same")
    on = smooth > thr
    bands, start = [], None
    for y, flag in enumerate(on):
        if flag and start is None:
            start = y
        elif not flag and start is not None:
            bands.append([start, y])
            start = None
    if start is not None:
        bands.append([start, height])
    # Fusionne les bandes proches (lignes d'un même sous-titre sur 2 lignes)
    gap = height // 40
    merged = []
    for b in bands:
        if merged and b[0] - merged[-1][1] <= gap:
            merged[-1][1] = b[1]
        else:
            merged.append(b)
    # Ignore les bandes trop fines (bruit)
    return [b for b in merged if b[1] - b[0] >= height // 60], smooth


def best_crop(bands, width, height, margin):
    """Plus grande zone verticale pleine largeur sans aucune bande (+ marge)."""
    blocked = [(max(0, a - margin), min(height, b + margin)) for a, b in bands]
    cuts = [0]
    for a, b in sorted(blocked):
        cuts += [a, b]
    cuts.append(height)
    best = (0, 0)
    for i in range(0, len(cuts), 2):
        top, bot = cuts[i], cuts[i + 1]
        if bot - top > best[1] - best[0]:
            best = (top, bot)
    top, bot = best
    h = (bot - top) // 2 * 2
    return {"x": 0, "y": top, "w": width // 2 * 2, "h": h,
            "ffmpeg": f"crop={width // 2 * 2}:{h}:0:{top}"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--frames", type=int, default=24)
    ap.add_argument("--out", default=".")
    ap.add_argument("--seuil", type=float, default=0.02,
                    help="score min. d'une ligne pour être considérée texte")
    a = ap.parse_args()

    width, height, dur = probe(a.video)
    times = np.linspace(dur * 0.03, dur * 0.97, a.frames)
    frames, scores = [], []
    for t in times:
        f = grab(a.video, t)
        if f is None:
            continue
        frames.append((t, f))
        scores.append(text_rows(f))
    scores = np.array(scores)
    # Une ligne est "sous-titre" si du texte y apparaît sur une bonne part des
    # images (le décor change, la position des sous-titres non).
    presence = (scores > a.seuil).mean(axis=0)
    level = np.percentile(scores, 75, axis=0)
    combined = level * (presence > 0.2)
    bands, _ = find_bands(combined, height, a.seuil)

    margin = max(6, height // 50)
    crop = best_crop(bands, width, height, margin)

    os.makedirs(a.out, exist_ok=True)
    thumbs = []
    idx = np.linspace(0, len(frames) - 1, min(12, len(frames))).astype(int)
    for t, f in [frames[i] for i in idx]:
        img = f.copy()
        for y0, y1 in bands:
            cv2.rectangle(img, (0, y0), (width - 1, y1), (0, 0, 255), 3)
        cv2.rectangle(img, (crop["x"], crop["y"]),
                      (crop["x"] + crop["w"] - 1, crop["y"] + crop["h"] - 1),
                      (0, 255, 0), 3)
        cv2.putText(img, f"{t:.1f}s", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (0, 255, 255), 3)
        thumbs.append(cv2.resize(img, (480, int(480 * height / width))))
    while len(thumbs) % 3:
        thumbs.append(np.zeros_like(thumbs[0]))
    rows = [np.hstack(thumbs[i:i + 3]) for i in range(0, len(thumbs), 3)]
    sheet = os.path.join(a.out, "planche.jpg")
    cv2.imwrite(sheet, np.vstack(rows))

    json.dump({
        "video": {"largeur": width, "hauteur": height, "duree": round(dur, 2)},
        "bandes_sous_titres": [{"y0": y0, "y1": y1,
                                "pct": [round(y0 / height * 100, 1),
                                        round(y1 / height * 100, 1)]}
                               for y0, y1 in bands],
        "recadrage": crop,
        "zone_gardee_pct": round(crop["h"] / height * 100, 1),
        "planche": sheet,
    }, sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
