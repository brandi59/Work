"""Incruste les sous-titres mot à mot (style wordimg) sur la vidéo montée, avec petit pop.
Usage : python3 incruster_mots.py base.mp4 mots.json sortie.mp4 <dossier de wordimg.py>
Réglages : OFF = durée miniature (0.4 s), CX,CY = centre (540,1305 = zone des anciens sous-titres)."""
import sys,json,random,subprocess,numpy as np,re
sys.path.insert(0,sys.argv[4])
from wordimg import render,clean,PAL
from PIL import Image
base,words,out=sys.argv[1:4]; OFF=0.4; FPS=30; W,H=1080,1920; CX,CY=540,1305
w=json.load(open(words)); random.seed(7)
ev=[]; last=-1
for i,(t,s,e) in enumerate(w):
    txt=clean(t)
    if not txt: continue
    c=random.choice([k for k in range(len(PAL)) if k!=last]); last=c
    ns=w[i+1][1] if i+1<len(w) else e+0.6
    end=ns if ns-e<0.5 else e+0.3
    im=render(txt,c); ev.append((max(OFF,s+OFF),end+OFF,im))
pops=[0.82,0.94,1.04,1.0]
def scaled(im,k):
    if k==1.0: return im
    return im.resize((max(1,int(im.width*k)),max(1,int(im.height*k))),Image.LANCZOS)
dec=subprocess.Popen(['ffmpeg','-v','error','-i',base,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',base,'-map','0:v','-map','1:a','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',out],stdin=subprocess.PIPE)
n=0; j=0
while True:
    buf=dec.stdout.read(W*H*3)
    if len(buf)<W*H*3: break
    t=n/FPS; f=np.frombuffer(buf,np.uint8).reshape(H,W,3).copy()
    while j<len(ev) and ev[j][1]<=t: j+=1
    if j<len(ev) and ev[j][0]<=t<ev[j][1]:
        s,e,im=ev[j]; k=pops[min(int((t-s)*FPS),3)]; im=scaled(im,k)
        a=np.asarray(im).astype(np.float32); x0=CX-im.width//2; y0=CY-im.height//2
        reg=f[y0:y0+im.height,x0:x0+im.width].astype(np.float32); al=a[...,3:]/255
        f[y0:y0+im.height,x0:x0+im.width]=(a[...,:3]*al+reg*(1-al)).astype(np.uint8)
    enc.stdin.write(f.tobytes()); n+=1
enc.stdin.close(); enc.wait(); print(n,'frames',len(ev),'words')
