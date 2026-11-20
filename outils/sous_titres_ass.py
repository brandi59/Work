"""Sous-titres « workflow » (2-3 mots Anton capitales, mot prononcé en jaune) en ASS.
Usage : python3 sous_titres_ass.py mots.json subs.ass 0.4   (puis ffmpeg ass=subs.ass:fontsdir=fonts)"""
import json,sys,re
w=json.load(open(sys.argv[1])); OFF=float(sys.argv[3])
clean=lambda t:re.sub(r"[.,;:]","",t).replace("...","").upper()
chunks=[];cur=[]
for i,(t,s,e) in enumerate(w):
    cur.append(i)
    L=sum(len(clean(w[j][0])) for j in cur)
    nxt=clean(w[i+1][0]) if i+1<len(w) else ''
    endp=bool(re.search(r"[.,?;:]|\.\.\.$",t))
    if len(cur)>=3 or endp or (len(cur)>=2 and L+len(nxt)>14) or i==len(w)-1 or (w[i+1][1]-e>0.35 if i+1<len(w) else True):
        chunks.append(cur);cur=[]
# merge lone tiny chunks? keep
def ts(x):
    h=int(x//3600);m=int(x%3600//60);s=x%60;return f"{h}:{m:02d}:{s:05.2f}"
hdr="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: S,Anton,112,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,10,3,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
out=[hdr]
starts=[w[c[0]][1]+OFF for c in chunks]
for ci,c in enumerate(chunks):
    cend=starts[ci+1] if ci+1<len(chunks) else w[c[-1]][2]+OFF+0.6
    for k,j in enumerate(c):
        s=w[j][1]+OFF if k else starts[ci]
        e=w[c[k+1]][1]+OFF if k+1<len(c) else cend
        if ci==0 and k==0: s=max(s,OFF)
        txt=" ".join(("{\\c&H00FFFF&}"+clean(w[m][0])+"{\\c&HFFFFFF&}") if m==j else clean(w[m][0]) for m in c)
        out.append(f"Dialogue: 0,{ts(s)},{ts(e)},S,,0,0,0,,{{\\pos(540,1305)\\fsp-1}}{txt}\n")
open(sys.argv[2],'w').write("".join(out))
print(len(chunks),"chunks"); print([" ".join(clean(w[j][0]) for j in c) for c in chunks][:25])
