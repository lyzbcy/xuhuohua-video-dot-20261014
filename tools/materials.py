"""Verify transport parts, join original ZIPs, safely unpack and verify source hashes."""
from pathlib import Path,PurePosixPath
import argparse,csv,hashlib,shutil,zipfile

R=Path(__file__).resolve().parents[1]
def sha(path):
    digest=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(8*1024*1024),b''):digest.update(chunk)
    return digest.hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    rows=list(csv.DictReader((R/'分包清单.csv').open(encoding='utf-8-sig')))
    for row in rows:
        f=a.input/row['file']
        if not f.is_file() or f.stat().st_size!=int(row['bytes']) or sha(f)!=row['sha256']:raise ValueError('Missing/corrupt part: '+row['file'])
    hashes={name:digest for digest,name in (line.split(None,1) for line in (R/'SHA256SUMS.txt').read_text(encoding='utf-8-sig').splitlines() if line.strip())}
    out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    archive_dir=out/'verified-archives';archive_dir.mkdir(exist_ok=True)
    for name in dict.fromkeys(row['archive'] for row in rows):
        target=archive_dir/name
        if not target.exists():
            with target.open('xb') as dst:
                for row in sorted((r for r in rows if r['archive']==name),key=lambda r:int(r['part'])):
                    with (a.input/row['file']).open('rb') as src:shutil.copyfileobj(src,dst,8*1024*1024)
        if sha(target)!=hashes[name]:raise ValueError('Joined ZIP hash mismatch: '+name)
        with zipfile.ZipFile(target) as z:
            for entry in z.infolist():
                rel=PurePosixPath(entry.filename.replace('\\','/'))
                dest=(out/str(rel)).resolve()
                if not dest.is_relative_to(out) or rel.is_absolute() or '..' in rel.parts:raise ValueError('Unsafe ZIP path')
                if (entry.external_attr>>16)&0o170000==0o120000:raise ValueError('ZIP symlink unsupported')
                if entry.is_dir():dest.mkdir(parents=True,exist_ok=True);continue
                if dest.exists():raise FileExistsError('Do not overwrite original: '+str(dest))
                dest.parent.mkdir(parents=True,exist_ok=True)
                with z.open(entry) as src,dest.open('xb') as dst:shutil.copyfileobj(src,dst,8*1024*1024)
        print('Verified and extracted:',name,flush=True)
    for row in csv.DictReader((R/'素材清单.csv').open(encoding='utf-8-sig')):
        f=out/row['原相对路径']
        if not f.is_file() or f.stat().st_size!=int(row['字节数']) or sha(f)!=row['SHA256']:raise ValueError('Original source mismatch: '+str(f))
    print('All original media hashes verified; no transcoding performed')
if __name__=='__main__':main()
