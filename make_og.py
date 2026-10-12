#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Erzeugt og-preview.jpg (1200x630) aus dem Teamfoto mit Verlauf + Titel + Logo."""
from PIL import Image, ImageDraw, ImageFont
import os
BASE=os.path.dirname(os.path.abspath(__file__))
FONTS="/home/openclaw/.openclaw/workspace/tmp/koord-vortrag/fonts"
W,H=1200,630

# --- Hintergrund: Teamfoto auf 1200x630 'cover' ---
src=Image.open(os.path.join(BASE,"team.jpg")).convert("RGB")
sw,sh=src.size
scale=max(W/sw,H/sh)
nw,nh=int(sw*scale),int(sh*scale)
src=src.resize((nw,nh),Image.LANCZOS)
# leicht nach oben versetzt, damit Gesichter sichtbar bleiben
left=(nw-W)//2; top=int((nh-H)*0.30)
bg=src.crop((left,top,left+W,top+H))

# --- dunkler Verlauf von links für Lesbarkeit ---
overlay=Image.new("RGBA",(W,H),(0,0,0,0))
od=ImageDraw.Draw(overlay)
for x in range(W):
    a=int(252*max(0,(1-(x/ (W*0.92)))))  # links sehr dunkel -> rechts transparent
    od.line([(x,0),(x,H)],fill=(3,18,38,a))
# flacher dunkler Grundschleier links (garantiert Kontrast für Text)
for x in range(int(W*0.60)):
    od.line([(x,0),(x,H)],fill=(3,18,38,70))
# zusätzlicher dunkler Streifen unten (höher gezogen, deckt Untertitel + Badges)
for y in range(H):
    a=int(195*max(0,((y-H*0.44)/(H*0.56))))
    od.line([(0,y),(W,y)],fill=(2,14,32,a))
comp=Image.alpha_composite(bg.convert("RGBA"),overlay)
d=ImageDraw.Draw(comp)

HELLBLAU=(0,159,227); WHITE=(255,255,255); SOFT=(210,226,240)
def font(path,sz): return ImageFont.truetype(os.path.join(FONTS,path),sz)
f_eye=font("Montserrat-SemiBold.ttf",26)
f_h1=font("Montserrat-SemiBold.ttf",72)
f_sub=font("Montserrat-Light.ttf",30)
f_badge=font("Montserrat-SemiBold.ttf",24)

M=70
# Eyebrow
d.text((M,86),"KARRIERE · GRUNDL LEADERSHIP INSTITUT",font=f_eye,fill=HELLBLAU)
# Titel (2 Zeilen)
d.text((M,150),"Organisation &",font=f_h1,fill=WHITE)
d.text((M,230),"Koordination",font=f_h1,fill=WHITE)
mwd_font=font("Montserrat-SemiBold.ttf",38)
d.text((M+ d.textlength("Koordination",font=f_h1)+24,262),"(m/w/d)",font=mwd_font,fill=HELLBLAU)
# Sub (auf dezenter dunkler Leiste für garantierten Kontrast)
_subtxt="Das organisatorische Rückgrat unseres Seminar- & Inhouse-Betriebs."
_stw=d.textlength(_subtxt,font=f_sub)
_sbar=Image.new("RGBA",(W,H),(0,0,0,0))
ImageDraw.Draw(_sbar).rounded_rectangle([M-16,334,M+_stw+18,334+50],radius=12,fill=(3,15,32,245))
comp.alpha_composite(_sbar)
d=ImageDraw.Draw(comp)
d.text((M,344),_subtxt,font=f_sub,fill=(242,247,252))

# Badges (dunkel hinterlegt, weißer Text)
badges=["Vollzeit 100 %","Standort Trossingen","Homeoffice möglich"]
bx=M; by=412
for b in badges:
    tw=d.textlength(b,font=f_badge); pad=24; bw=tw+pad*2; bh=54
    d.rounded_rectangle([bx,by,bx+bw,by+bh],radius=27,fill=(4,26,50,210),outline=(0,159,227,230),width=2)
    d.text((bx+pad,by+15),b,font=f_badge,fill=WHITE)
    bx+=bw+16

# Logo (weiß) unten links
try:
    logo=Image.open(os.path.join(BASE,"grundl-logo-trans.png")).convert("RGBA")
    # auf weiß umfärben
    r,g,bl,al=logo.split()
    white=Image.new("RGBA",logo.size,(255,255,255,255)); white.putalpha(al)
    lw=260; lh=int(logo.size[1]*(lw/logo.size[0]))
    white=white.resize((lw,lh),Image.LANCZOS)
    comp.alpha_composite(white,(M, H-lh-40))
except Exception as e:
    print("logo-skip",e)

out=os.path.join(BASE,"og-preview.jpg")
comp.convert("RGB").save(out,"JPEG",quality=88)
print("WROTE",out,comp.size)
