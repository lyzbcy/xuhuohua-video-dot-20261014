from pathlib import Path
import argparse,math,subprocess
from PIL import Image
from animation import A,sprite_assets,rpg_scene

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--kind',choices=['shop','ice','save'],default='shop')
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--duration',type=float)
    p.add_argument('--frame',type=float)
    p.add_argument('--transparent',action='store_true')
    a=p.parse_args();duration=a.duration or dict(shop=2.8,ice=3.3,save=3.4)[a.kind]
    if not 0<duration<=60:p.error('duration must be positive and <=60s')
    a.out.parent.mkdir(parents=True,exist_ok=True)
    bg=Image.open(A/'商场像素场景.png').convert('RGB').resize((1400,788),Image.Resampling.NEAREST)
    sprites=sprite_assets()
    if a.frame is not None:
        rpg_scene(a.kind,a.frame,duration,bg,sprites).save(a.out)
        return
    if a.transparent and a.out.suffix.lower()!='.mov':p.error('transparent output requires .mov')
    cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgba','-s','1920x1080','-r','30','-i','-','-an']
    cmd+=['-c:v','qtrle','-pix_fmt','argb'] if a.transparent else ['-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart']
    proc=subprocess.Popen(cmd+[str(a.out)],stdin=subprocess.PIPE)
    try:
        for i in range(math.ceil(duration*30)):
            frame=rpg_scene(a.kind,i/30,duration,bg,sprites)
            if not a.transparent:
                canvas=Image.new('RGBA',frame.size,'#172e31');canvas.alpha_composite(frame);frame=canvas
            proc.stdin.write(frame.tobytes())
    finally:proc.stdin.close()
    if proc.wait():raise RuntimeError('FFmpeg failed')
if __name__=='__main__':main()
