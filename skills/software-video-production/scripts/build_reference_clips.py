"""Rebuild study excerpts from local reference originals; never use these in deliverables."""
from pathlib import Path
import argparse, hashlib, json, subprocess
from datetime import date

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)]))

def digest(path):
    digest=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(8*1024*1024),b''):digest.update(block)
    return digest.hexdigest()

def within(root, relative):
    p=(root/relative).resolve()
    if not p.is_relative_to(root.resolve()):
        raise ValueError(f'Path outside root: {relative}')
    return p

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir',type=Path,required=True)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]/'examples'
    catalog=json.loads((root/'catalog.json').read_text(encoding='utf8'))
    report={'date':date.today().isoformat(),'purpose':'study_excerpts_only','clips':[]}
    for item in catalog['references']:
        src=within(args.source_dir,item['source_filename'])
        info=probe(src); duration=float(info['format']['duration'])
        offset=item.get('source_file_start_s',0)
        sha=digest(src)
        for clip in item['clips']:
            start=clip['source_in_s']-offset
            length=clip['source_out_s']-clip['source_in_s']
            if start<0 or length<=0 or start+length>duration+0.1:
                raise ValueError(f'Out of source bounds: {clip["path"]}')
            dst=within(root,clip['path']); dst.parent.mkdir(parents=True,exist_ok=True)
            subprocess.run(['ffmpeg','-y','-v','error','-ss',str(start),'-i',str(src),'-t',str(length),
                '-map','0:v:0','-map','0:a:0','-vf',"scale='min(1280,iw)':-2",'-c:v','libx264',
                '-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k',
                '-movflags','+faststart',str(dst)],check=True)
            out=probe(dst); v=next(s for s in out['streams'] if s['codec_type']=='video')
            if not any(s['codec_type']=='audio' for s in out['streams']):
                raise ValueError(f'Missing audio: {dst}')
            if abs(float(out['format']['duration'])-length)>.15:
                raise ValueError(f'Unexpected duration: {dst}')
            subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(dst),'-f','null','-'],check=True)
            row={'id':item['id'],'path':clip['path'],'duration_s':float(out['format']['duration']),
                 'width':v['width'],'height':v['height'],'audio':True,'decode':'passed',
                 'bytes':dst.stat().st_size,'sha256':digest(dst),'source_sha256':sha,
                 'source_in_s':clip['source_in_s'],'source_out_s':clip['source_out_s']}
            report['clips'].append(row)
            print(json.dumps(row,ensure_ascii=False),flush=True)
    (root/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')

if __name__=='__main__': main()
