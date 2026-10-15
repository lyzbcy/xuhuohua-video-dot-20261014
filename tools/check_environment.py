"""Report actual capabilities without installing software or reading credentials."""
from pathlib import Path
import importlib.util,json,os,shutil,subprocess,sys

checks=dict(python=sys.version.split()[0],tools={x:shutil.which(x) for x in ['ffmpeg','ffprobe','ssh']},modules={x:bool(importlib.util.find_spec(x)) for x in ['PIL','numpy','faster_whisper','edge_tts','rapidocr_onnxruntime']})
fonts=[os.environ.get('VIDEO_CJK_FONT',''),'C:/Windows/Fonts/msyh.ttc','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc','/System/Library/Fonts/PingFang.ttc']
checks['cjk_font']=next((str(Path(p)) for p in fonts if p and Path(p).is_file()),None)
if checks['tools']['ffmpeg']:
    output=subprocess.run(['ffmpeg','-hide_banner','-encoders'],capture_output=True,text=True,encoding='utf8',errors='replace',timeout=15,check=True).stdout
    checks['encoders']={x:x in output for x in ['libx264','qtrle','aac','h264_nvenc']}
checks['scope']='Presence check only; no claims of cloud image/music generation, remote SSH login, song license or complete listening support'
print(json.dumps(checks,ensure_ascii=False,indent=2))
