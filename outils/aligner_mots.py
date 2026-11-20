"""Timing mot à mot gratuit : Whisper local (faster-whisper) + mots EXACTS du texte traduit.
Usage : HF_HUB_DISABLE_XET=1 python3 aligner_mots.py voix.wav texte.txt mots.json
(pip install faster-whisper ; HF_HUB_DISABLE_XET=1 obligatoire pour télécharger le modèle)"""
import json,sys,re,difflib
from faster_whisper import WhisperModel
script=open(sys.argv[2]).read().split()
m=WhisperModel('small',device='cpu',compute_type='int8')
import subprocess,numpy as np
pcm=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',sys.argv[1],'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
segs,_=m.transcribe(pcm,language='fr',word_timestamps=True)
W=[w for s in segs for w in s.words]
norm=lambda x:re.sub(r"[^\w']","",x.lower())
a=[norm(w.word) for w in W]; b=[norm(w) for w in script]
sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
t=[None]*len(script)
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=='equal':
        for k in range(i2-i1): t[j1+k]=(W[i1+k].start,W[i1+k].end)
    elif i2>i1:
        s0,e0=W[i1].start,W[i2-1].end; n=j2-j1
        for k in range(n): t[j1+k]=(s0+(e0-s0)*k/n,s0+(e0-s0)*(k+1)/n)
# fill gaps
for j in range(len(t)):
    if t[j] is None:
        p=next(x for x in t[j-1::-1] if x) if j else (0,0)
        nx=next((x for x in t[j+1:] if x),(p[1]+.3,p[1]+.3))
        t[j]=(p[1],nx[0]) if nx[0]>p[1] else (p[1],p[1]+.15)
json.dump([[w,s,e] for w,(s,e) in zip(script,t)],open(sys.argv[3],'w'),ensure_ascii=False)
print(sum(1 for o in sm.get_opcodes() if o[0]!='equal'),'non-equal ops;',len(a),len(b))
for o in sm.get_opcodes():
    if o[0]!='equal': print(o[0],a[o[1]:o[2]],b[o[3]:o[4]])
