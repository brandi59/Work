"""Génère les sous-titres (ASS) style TikTok à partir de words.txt.

words.txt : une ligne par mot -> "mot debut_ms fin_ms"
Usage : python3 make_ass.py words.txt caps.ass [--y 1345] [--title "LIGNE 1\\NLIGNE 2"]
          [--title-y 1347] [--thumb-end 0.10] [--size 124]
"""
import argparse
import re

p = argparse.ArgumentParser()
p.add_argument("words")
p.add_argument("out")
p.add_argument("--y", type=int, default=1345, help="centre vertical des sous-titres (canevas 1080x1920)")
p.add_argument("--size", type=int, default=124)
p.add_argument("--title", default="", help="titre de la miniature, \\N pour un retour à la ligne")
p.add_argument("--title-y", type=int, default=1347)
p.add_argument("--title-size", type=int, default=112)
p.add_argument("--thumb-end", type=float, default=0.10, help="fin de la miniature (s) ; sous-titres après")
a = p.parse_args()

words = []
for line in open(a.words, encoding="utf-8"):
    line = line.strip()
    if line:
        *t, s, e = line.split(" ")
        words.append([" ".join(t), int(s) / 1000, int(e) / 1000])

MAX_WORDS, MAX_CHARS, GAP = 3, 14, 0.35
groups, cur = [], []
for w in words:
    if cur:
        prev = cur[-1]
        chars = sum(len(x[0]) for x in cur) + len(cur) + len(w[0])
        if (len(cur) >= MAX_WORDS or chars > MAX_CHARS or w[1] - prev[2] > GAP
                or re.search(r"[.,?!;:]$", prev[0])):
            groups.append(cur)
            cur = []
    cur.append(w)
groups.append(cur)


def ts(t):
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


WHITE, YELLOW = r"{\c&HFFFFFF&}", r"{\c&H00E5FF&}"
T = a.thumb_end
events = []
if a.title:
    events.append(f"Dialogue: 1,{ts(0)},{ts(T)},Thumb,,0,0,0,,{{\\an5\\pos(540,{a.title_y})}}{a.title}")
for gi, g in enumerate(groups):
    g_start = max(g[0][1], T)
    nxt = groups[gi + 1][0][1] if gi + 1 < len(groups) else g[-1][2] + 0.6
    g_end = min(nxt, g[-1][2] + 0.4) if nxt - g[-1][2] > 0.4 else nxt
    for wi, w in enumerate(g):
        if wi + 1 < len(g) and g[wi + 1][1] <= T:
            continue
        s = g_start if wi == 0 else max(w[1], T)
        e = g[wi + 1][1] if wi + 1 < len(g) else g_end
        parts = [(YELLOW if j == wi else WHITE) + x[0].upper() for j, x in enumerate(g)]
        pop = r"{\fscx112\fscy112\t(0,90,\fscx100\fscy100)}" if wi == 0 else ""
        events.append(f"Dialogue: 0,{ts(s)},{ts(e)},Cap,,0,0,0,,{{\\an5\\pos(540,{a.y})}}{pop}" + " ".join(parts))

head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Anton,{a.size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,1,0,1,9,3,5,50,50,0,1
Style: Thumb,Anton,{a.title_size},&H00000000,&H00000000,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open(a.out, "w", encoding="utf-8").write(head + "\n".join(events) + "\n")
print(len(groups), "lignes,", len(events), "événements")
