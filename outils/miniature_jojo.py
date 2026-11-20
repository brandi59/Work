"""Miniature JoJo : fond quadrillé rose/noir sur toute l'image, 1re image au centre, titre FR Anton noir 2 lignes.
Usage : python3 miniature_jojo.py image.png miniature.png Anton-Regular.ttf  (titre : variable lines)"""
import sys
from PIL import Image,ImageDraw,ImageFont
frame,out,font=sys.argv[1:4]
W,H=1080,1920; C=120
img=Image.new('RGB',(W,H)); d=ImageDraw.Draw(img)
for y in range(0,H,C):
    for x in range(0,W,C):
        d.rectangle([x,y,x+C-1,y+C-1],fill=(255,62,165) if (x//C+y//C)%2==0 else (0,0,0))
f=Image.open(frame).convert('RGB').resize((960,960),Image.LANCZOS)
fy=780
d.rectangle([60-14,fy-14,60+960+13,fy+960+13],fill=(255,255,255))
img.paste(f,(60,fy))
lines=["POURQUOI JOJO EST SI","DUR À RECOMMANDER ?"]
ft=ImageFont.truetype(font,118)
bx0,by0,bx1,by1=50,150,1030,690
d.rounded_rectangle([bx0,by0,bx1,by1],radius=36,fill=(255,255,255),outline=(0,0,0),width=10)
ys=[220,440]
for t,y in zip(lines,ys):
    s=ft.getbbox(t); w=s[2]-s[0]
    while w>900:
        ft2=ImageFont.truetype(font,ft.size-4); ft=ft2; s=ft.getbbox(t); w=s[2]-s[0]
    d.text(((W-w)//2-s[0],y),t,font=ft,fill=(0,0,0))
img.save(out)
