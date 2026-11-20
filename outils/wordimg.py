"""Rendu d'un mot façon sous-titres « JoJo » d'origine : minuscules, Fredoka Bold penchée,
dégradé de couleur par mot, ombre noire épaisse, halo. Police : fonts/Fredoka.ttf
(curl -L -o fonts/Fredoka.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/fredoka/Fredoka%5Bwdth,wght%5D.ttf")"""
import numpy as np, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter
PAL=[((200,255,0),(255,255,170)),((0,225,90),(170,255,215)),((255,90,0),(255,200,120)),((0,170,255),(140,255,255)),
     ((0,230,170),(170,255,230)),((255,0,50),(255,120,140)),((255,60,200),(255,190,240)),((255,215,0),(255,250,170)),((150,90,255),(220,190,255))]
def clean(t): return re.sub(r"[.,;:?!…]|\.\.\.","",t)
def render(word,ci,size=78,font='fonts/Fredoka.ttf'):
    f=ImageFont.truetype(font,size); f.set_variation_by_name('Bold')
    l,t,r,b=f.getbbox(word); w,h=r-l,b-t; P=40
    W,H=w+2*P+30,h+2*P
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).text((P-l+10,P-t),word,font=f,fill=255)
    sh=0.2; m=m.transform(m.size,Image.AFFINE,(1,sh,-sh*H/2,0,1,0),Image.BICUBIC)  # italic slant
    a=np.asarray(m).astype(np.float32)/255
    # gradient fill left->right
    c0,c1=PAL[ci%len(PAL)]; xs=np.nonzero(a.max(0)>0.1)[0]; x0,x1=xs.min(),xs.max()
    g=np.clip((np.arange(W)-x0)/max(1,x1-x0),0,1)**1.4
    col=(np.array(c0)[None,:]*(1-g[:,None])+np.array(c1)[None,:]*g[:,None])
    fill=np.broadcast_to(col[None],(H,W,3))
    # dark outline/shadow (thick, soft)
    o=np.asarray(m.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(3))).astype(np.float32)/255
    o=np.clip(o*1.6,0,1)
    # soft glow (colored-white) larger
    gl=np.asarray(m.filter(ImageFilter.MaxFilter(13)).filter(ImageFilter.GaussianBlur(14))).astype(np.float32)/255*0.55
    glc=np.array(c1)*0.5+127
    rgb=np.zeros((H,W,3)); A=np.zeros((H,W))
    # composite glow, then shadow, then fill
    rgb=glc[None,None]*1.0*np.ones((H,W,1)); A=gl
    rgb=rgb*(1-o[...,None])*A[...,None]/np.maximum(1e-6,A+o*(1-A))[...,None]; A=A*(1-o)+o; 
    rgb=rgb+0  # shadow is black
    rgb=fill*a[...,None]+rgb*(1-a[...,None]); A=a+A*(1-a)
    img=np.dstack([np.clip(rgb,0,255),np.clip(A*255,0,255)]).astype(np.uint8)
    return Image.fromarray(img,'RGBA')
if __name__=="__main__":
    import sys
    ws=["JoJo","absolument","esthétique","musclés","l'histoire","spectateurs","grandiose","est-il"]
    bg=Image.new('RGBA',(1080,120*len(ws)),(90,120,170,255))
    for i,w in enumerate(ws):
        im=render(w,i); bg.alpha_composite(im,(540-im.width//2,120*i+60-im.height//2))
    bg.save(sys.argv[1])
