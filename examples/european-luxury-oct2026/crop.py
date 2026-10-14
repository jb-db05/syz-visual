import sys
from PIL import Image
import numpy as np
S=2382/827
def crop(src,box,dst):
    im=Image.open(src); x0,y0,x1,y1=[int(v*S) for v in box]; im.crop((x0,y0,x1,y1)).save(dst)
# logo from page 1
im=Image.open("img/p-000.jpg").convert("RGBA"); x0,y0,x1,y1=[int(v*S) for v in (680,25,778,112)]
lg=np.array(im.crop((x0,y0,x1,y1))).astype(float)
rgb=lg[...,:3]; w=rgb.min(axis=2)  # whiteness
# alpha: distance from white using blue channel (orange/yellow have low blue)
a=np.clip((255-rgb[...,2])/255*1.6,0,1)
# unpremultiply against white
out=np.zeros_like(lg)
for c in range(3):
    out[...,c]=np.where(a>0.02,(rgb[...,c]-255*(1-a))/np.maximum(a,1e-3),255)
out[...,3]=a*255
out=np.clip(out,0,255).astype(np.uint8)
L=Image.fromarray(out); L=L.crop(L.getbbox()); L.save("img/logo.png"); print("logo",L.size)
for name,pg in [("cfr","004"),("mc","006"),("rms","008"),("ker","010")]:
    crop(f"img/p-{pg}.jpg",(64,162,770,516),f"img/{name}_top.png")
    crop(f"img/p-{pg}.jpg",(64,628,770,915),f"img/{name}_bot.png")
