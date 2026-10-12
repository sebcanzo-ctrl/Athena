from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageFilter,ImageEnhance
import numpy as np,subprocess,sys
D='/usr/share/fonts/opentype/inter/'; U='/root/.claude/uploads/68138d4f-dbab-593b-b40d-97aebcd1b3b1/'
GOLD=(236,184,72); WHITE=(245,243,238); TOT=14
HF=lambda s:ImageFont.truetype(D+'InterDisplay-Black.otf',s)
QF=ImageFont.truetype(D+'InterDisplay-BoldItalic.otf',46); SF=ImageFont.truetype(D+'InterDisplay-Bold.otf',32)
LF=ImageFont.truetype(D+'Inter-Bold.otf',22); NF=ImageFont.truetype(D+'Inter-Bold.otf',24)
def fit(img,box=None,focus=(0.5,0.5)):
    im=ImageOps.exif_transpose(img).convert('RGB')
    if box: im=im.crop(box)
    w,h=im.size; tw=w; th=int(w*1.25)
    if th>h: th=h; tw=int(h*0.8)
    x0=int(min(max(focus[0]*w-tw/2,0),w-tw)); y0=int(min(max(focus[1]*h-th/2,0),h-th))
    return im.crop((x0,y0,x0+tw,y0+th)).resize((1080,1350),Image.LANCZOS)
def wrap(d,t,f,maxw):
    out=['']
    for wd in t.split():
        s=(out[-1]+' '+wd).strip()
        if d.textlength(s,font=f)<=maxw: out[-1]=s
        else: out.append(wd)
    return out
def overlay(i,head,quote,pos='bottom',hsize=96):
    L=Image.new('RGBA',(1080,1350),(0,0,0,0)); d=ImageDraw.Draw(L)
    # top label gradient
    a=np.zeros((1350,1080,4),np.uint8)
    for y in range(200): a[y,:,3]=int(150*(1-y/200)**1.5)
    hf=HF(hsize); hl=wrap(d,head,hf,948); ql=wrap(d,'"'+quote+'"',QF,948)
    bh=len(hl)*int(hsize*0.98)+22+len(ql)*58+50
    if pos=='bottom':
        y0=1350-80-bh; G=bh+380
        for y in range(1350-G,1350): t=(y-(1350-G))/G; a[y,:,3]=np.maximum(a[y,:,3],int(225*min(1,t*1.4)**1.4))
    else:
        y0=120; G=bh+330
        for y in range(0,G): t=1-y/G; a[y,:,3]=np.maximum(a[y,:,3],int(235*t**1.1))
    L=Image.alpha_composite(L,Image.fromarray(a)); d=ImageDraw.Draw(L)
    t='MEET THE CO-PILOT'; x=65
    for c in t: d.text((x,52),c,font=LF,fill=WHITE+(255,)); x+=LF.getlength(c)+3.4
    s=f'{i:02d}'; r=f' / {TOT:02d}'; wa=d.textlength(s,font=NF); wr=d.textlength(r,font=NF); x=1014-wa-wr
    d.text((x,50),s,font=NF,fill=GOLD+(255,)); d.text((x+wa,50),r,font=NF,fill=WHITE+(255,))
    y=y0
    for l in hl: d.text((66,y-hf.getbbox('T')[1]),l,font=hf,fill=WHITE+(255,)); y+=int(hsize*0.98)
    y+=22
    for l in ql: d.text((66,y),l,font=QF,fill=WHITE+(255,)); y+=58
    d.text((66,y+6),'— Coco',font=SF,fill=GOLD+(255,))
    return L
def photo(i,src,head,quote,pos='bottom',box=None,focus=(0.5,0.5),bright=1.0,hsize=96):
    im=fit(Image.open(U+src),box,focus)
    if bright!=1: im=ImageEnhance.Brightness(im).enhance(bright)
    out=Image.alpha_composite(im.convert('RGBA'),overlay(i,head,quote,pos,hsize)).convert('RGB')
    out.save(f'out/intro_{i:02d}.jpg',quality=94); return out
def video(i,src,head,quote,pos='bottom',hsize=96):
    ov=overlay(i,head,quote,pos,hsize); ov.save(f'out/ov_{i:02d}.png')
    subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-i',f'out/ov_{i:02d}.png','-filter_complex','[0:v][1:v]overlay=0:0,format=yuv420p[v]','-map','[v]','-map','0:a?','-c:v','libx264','-profile:v','high','-crf','18','-r','30','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','copy','-movflags','+faststart',f'out/intro_{i:02d}.mp4'],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-ss','2.5','-i',f'out/intro_{i:02d}.mp4','-frames:v','1',f'out/intro_{i:02d}_frame.jpg'],check=True)
C='/tmp/c/desert/cuts/'
photo(1,'34199adb-image.jpg','LET ME INTRODUCE MYSELF',"Coco. Co-pilot. Head of social media.",hsize=92)
photo(2,'9eab1547-image.jpg','DAY ONE','They came to look. I chose them.',focus=(0.45,0.5))
video(3,'src_stairs.mp4','MY BROTHERS','I let him win. Obviously.',pos='top')
photo(4,'4cbcb6ea-image.jpg','THE RINGLEADER','Loki knocks it off. I eat it. Teamwork.',focus=(0.5,0.55))
video(5,'src_shred.mp4','THE NAUGHTY YEARS','Spots was here too. Just saying.')
photo(6,'4eda7ba9-image.jpg','EXHIBIT B',"I only took one. I'm not an animal.",focus=(0.5,0.5))
video(7,C+'clip_ball_jump.mp4','BALLS','Throw it. Throw it. THROW IT.',pos='top')
video(8,C+'clip_snack_on_dune.mp4','SNACK RADAR','Climbed a dune. Got paid.',pos='top')
photo(9,'06a3bb03-image.jpg','THE ORANGE YEARS','Before the Jeep, there was the orange one. Co-pilot then too.',focus=(0.53,0.5))
photo(10,'50fddfca-image.jpg','DRESS CODE',"Dressed for the desert. He didn't ask.",box=(470,420,1932,2576),focus=(0.5,0.45))
video(11,C+'clip_sunset.mp4','GOLDEN HOUR','Still the main attraction.',pos='top')
photo(12,'b7376696-image.jpg','MY SPOT',"Found the best spot. Not moving.",box=(330,0,1932,2576),focus=(0.5,0.42))
photo(13,'cb87589f-image.jpg','SUMMER IS OVER',"Where's my Jeep?",pos='top',focus=(0.5,0.55))
