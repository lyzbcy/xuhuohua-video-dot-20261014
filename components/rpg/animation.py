"""Portable original RPG/sticker motion functions; scenario-specific sample, not a fixed video template."""
from pathlib import Path
import math,os
from PIL import Image,ImageDraw,ImageFont,ImageOps
A=Path(__file__).resolve().parent/'assets'
FONT_CANDIDATES=[os.environ.get('VIDEO_CJK_FONT',''),'C:/Windows/Fonts/msyh.ttc','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc','/System/Library/Fonts/PingFang.ttc']
FONT_PATH=next((p for p in FONT_CANDIDATES if p and Path(p).is_file()),None)
if not FONT_PATH:raise RuntimeError('Install CJK fonts or set VIDEO_CJK_FONT to a real font file')
def font(n):return ImageFont.truetype(FONT_PATH,n)
F={n:font(n) for n in [13,15,18,20,22,26,28,32]}
def ease(x):x=max(0,min(1,x));return 1-(1-x)**3

def smooth(x):x=max(0,min(1,x));return x*x*(3-2*x)

def star(d,x,y,r,c):
 d.polygon([(x,y-r),(x+r*.24,y-r*.24),(x+r,y),(x+r*.24,y+r*.24),(x,y+r),(x-r*.24,y+r*.24),(x-r,y),(x-r*.24,y-r*.24)],fill=c)

def heart(d,x,y,s,c):
 pts=[(0,2),(1,0),(3,0),(4,1),(5,0),(7,0),(8,2),(8,4),(4,8),(0,4)]
 d.polygon([(int(x+a*s),int(y+b*s)) for a,b in pts],fill=c)

def sprite_assets():
 sheet=Image.open(A/'双人行走精灵.png').convert('RGBA');w,h=sheet.size
 sprites=[]
 for row in range(2):
  current=[]
  for col in range(4):
   im=sheet.crop((col*w//4,row*h//2,(col+1)*w//4,(row+1)*h//2))
   alpha=im.getchannel('A').point(lambda x:255 if x>140 else 0);box=alpha.getbbox()
   im=im.crop(box)
   im=im.resize((round(im.width*136/im.height),136),Image.Resampling.NEAREST)
   current.append(im)
  sprites.append(current)
 return sprites

def rpg_scene(kind,t,duration,bg,sprites):
 # Compose at a deliberate logical game resolution, then enlarge with nearest-neighbour.
 if kind=='shop':
  progress=smooth(t/2.25);cam=round(195*progress);xm=245+450*progress;xf=xm+90
  title='饭后支线 · 随便逛逛';hint='双人队伍，继续出发'
 elif kind=='ice':
  progress=smooth(t/1.1);cam=440;xm=1010+70*progress;xf=xm+100
  title='获得道具 · 两支冰淇淋';hint='今晚的甜度 +1'
 else:
  progress=smooth(t/.9);cam=180;xm=610-35*progress;xf=680-35*progress
  title='普通的一天，也值得存档';hint='回忆存档：2026.10.04'
 im=bg.crop((cam,180,cam+960,720)).convert('RGBA')
 d=ImageDraw.Draw(im)
 # Foreground floor lights; stars shimmer sparsely, no full-screen particle clutter.
 for k in range(5):
  sx=80+k*179;sy=373+(k%2)*24
  v=max(0,math.sin(t*2.2+k*1.9))
  if v>.6:star(d,sx,sy,2+v,'#ffe8ad')
 def person(which,x,foot,moving,flip=False):
  phase=int(t*7)%4 if moving else 1
  sp=sprites[which][phase]
  if flip:sp=ImageOps.mirror(sp)
  sx=round(x-cam);bob=[0,1,0,-1][phase] if moving else 0
  d.ellipse((sx-25,foot-5,sx+25,foot+5),fill=(22,29,35,65))
  im.alpha_composite(sp,(sx-sp.width//2,foot-sp.height+bob))
 moving=t<(2.2 if kind=='shop' else .95)
 # Two depth planes and distinct footstep phases.
 person(0,xm,464,moving)
 person(1,xf,470,moving,flip=((kind=='shop' and t>2.15) or (kind=='save' and t>.9)))
 d=ImageDraw.Draw(im)
 # Native game HUD: small identity and quest headers, not a presentation card.
 d.rounded_rectangle((27,24,665,93),radius=3,fill=(29,44,49,233),outline='#e5c992',width=2)
 d.text((44,36),title,font=F[26],fill='#fff5db')
 d.text((46,70),hint,font=F[13],fill='#d9e8de')
 d.text((786,30),'回忆小剧场',font=F[18],fill='#fff1d2',stroke_width=1,stroke_fill='#344a48')
 for k in range(2):heart(d,799+k*38,64,2,'#efadb6')
 # World interactions have a clear trigger and result.
 if kind=='shop' and t>1.9:
  star(d,round(xf-cam)+2,310,10,'#ffe5a1')
  if t>2.15:d.text((round(xf-cam)-11,282),'!',font=F[26],fill='#fff7d6',stroke_width=2,stroke_fill='#5b4439')
 if kind=='ice':
  # Cones fly once from the counter into the two characters' hands.
  for k,x in enumerate([xm,xf]):
   u=smooth((t-1.1-k*.12)/.55)
   if t<1.1+k*.12:continue
   xx=(1-u)*817+u*(x-cam+20);yy=(1-u)*285+u*395-46*math.sin(u*math.pi)
   cone(d,round(xx),round(yy),1.8)
  if t>1.7:
   star(d,int(xf-cam)+38,346,7,'#fff3b1')
   d.text((580,130),'两支，一人一支',font=F[22],fill='#fff0c8',stroke_width=2,stroke_fill='#344b4b')
 if kind=='save':
  if t>.8:
   heart(d,round((xm+xf)/2-cam)-8,294,3,'#ef9aaf')
  # Save icon fills, check arrives, then the result holds.
  xx,yy=818,139
  d.rectangle((xx,yy,xx+65,yy+65),fill='#334a4c',outline='#e8ce9d',width=2)
  d.rectangle((xx+12,yy+8,xx+51,yy+25),fill='#a8c2bd')
  d.rectangle((xx+15,yy+37,xx+50,yy+57),fill='#eedfc1')
  if t>1.6:
   d.line([(xx+13,yy+44),(xx+28,yy+57),(xx+53,yy+29)],fill='#9ce0b3',width=5)
   d.text((653,218),'这一天，已存档',font=F[22],fill='#fff2d7',stroke_width=2,stroke_fill='#344b4b')
 # Staggered tile reveal/conceal; each block uncovers the real camera footage.
 mask=Image.new('L',(960,540),0);md=ImageDraw.Draw(mask)
 for row in range(15):
  for col in range(24):
   offset=((col*7+row*11)%17)/100
   level=min((t-offset)/.17,(duration-t-offset)/.17,1)
   if level>0:md.rectangle((col*40,row*36,(col+1)*40,(row+1)*36),fill=round(255*min(1,level)))
 im.putalpha(mask)
 return im.resize((1920,1080),Image.Resampling.NEAREST)

def cone(d,x,y,z=1):
 d.polygon([(x-5*z,y),(x+5*z,y),(x,y+14*z)],fill='#dca56e',outline='#825e43')
 for dy,ww in [(0,7),(-5,6),(-9,4),(-12,2)]:
  d.rounded_rectangle((x-ww*z,y+(dy-3)*z,x+ww*z,y+(dy+1)*z),radius=max(1,int(z*2)),fill='#abdeed',outline='#527f93')

def sticker_frame(src,kind,t,duration):
 im=Image.new('RGBA',(320,340));d=ImageDraw.Draw(im)
 entry=ease(t/.3);exit=min(1,max(0,(duration-t)/.18))
 # One anticipation / overshoot / settle, followed by a readable hold.
 scale=.78+.22*entry
 if .20<t<.56:scale+=.07*math.sin((t-.2)/.36*math.pi)
 dx=0;dy=0;angle=0
 if kind=='sleep':dx=45*(1-entry);angle=4*(1-entry)
 elif kind=='meal':dy=55*(1-entry)
 elif kind=='giggle':
  dx=-80*(1-entry)
  if .35<t<.95:angle=3*math.sin((t-.35)*18)*(1-(t-.35)/.6)
 elif kind=='shopping':dx=95*(1-entry);angle=-7*(1-entry)
 elif kind=='sweet':dy=18*(1-entry)
 elif kind=='hug':angle=-6*(1-entry)
 w=round(236*scale);sp=src.copy();sp.thumbnail((w,w),Image.Resampling.LANCZOS)
 if angle:sp=sp.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
 sp.putalpha(sp.getchannel('A').point(lambda a:round(a*entry*exit)))
 im.alpha_composite(sp,(round(160-sp.width/2+dx),round(48+dy+(236-sp.height)/2)))
 d=ImageDraw.Draw(im)
 if kind=='sleep':
  for i in range(3):
   u=(t-.55-i*.23)/.8
   if 0<u<1:d.text((238+i*14,49-i*19-round(u*12)),'z',font=F[15],fill=(65,93,127,round(230*math.sin(math.pi*u)*exit)))
 if kind in ['sweet','shopping'] and .35<t<1.4:
  alpha=round(255*math.sin(math.pi*(t-.35)/1.05)*exit)
  for x,y in [(46,88),(275,157)]:star(d,x,y,10,(239,194,100,alpha))
 if kind=='hug' and .4<t<1.2:
  alpha=round(255*math.sin(math.pi*(t-.4)/.8)*exit)
  heart(d,243,43,2,(235,133,161,alpha))
 return im
