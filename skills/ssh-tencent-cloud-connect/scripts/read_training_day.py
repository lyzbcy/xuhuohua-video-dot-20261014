"""SSH identity check followed by read-only single-day export; no password handling."""
from pathlib import Path
import argparse,datetime,json,shlex,subprocess

def main():
    p=argparse.ArgumentParser();p.add_argument('--host',required=True);p.add_argument('--user',required=True);p.add_argument('--expected-hostname',required=True)
    p.add_argument('--port',type=int,default=22);p.add_argument('--key',type=Path);p.add_argument('--date',required=True);p.add_argument('--records',default='/home/openclaw-shared/fitness/records.jsonl');p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();datetime.date.fromisoformat(a.date)
    if any(s.startswith('-') or any(c.isspace() for c in s) for s in [a.host,a.user]):p.error('Invalid SSH target')
    if not 1<=a.port<=65535:p.error('Invalid port')
    if a.out.exists():p.error('Output exists; choose a new private output filename')
    cmd=['ssh','-p',str(a.port),'-o','BatchMode=yes','-o','ConnectTimeout=10','-o','StrictHostKeyChecking=accept-new']
    if a.key:
        if not a.key.is_file():p.error('Key file not found')
        cmd+=['-i',str(a.key),'-o','IdentitiesOnly=yes']
    cmd+=[a.user+'@'+a.host]
    who=subprocess.run(cmd+['hostname; whoami'],capture_output=True,text=True,encoding='utf8',timeout=30,check=True).stdout.strip().splitlines()
    if who!=[a.expected_hostname,a.user]:raise RuntimeError('Remote identity mismatch; stop and confirm with user')
    source=Path(__file__).with_name('export_training_day.py').read_text(encoding='utf8')
    remote='python3 - --records '+shlex.quote(a.records)+' --date '+shlex.quote(a.date)
    result=subprocess.run(cmd+[remote],input=source,capture_output=True,text=True,encoding='utf8',timeout=60,check=True)
    data=json.loads(result.stdout)
    if data.get('date')!=a.date or not data.get('sets'):raise RuntimeError('Invalid training export')
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open('x',encoding='utf8') as f:json.dump(data,f,ensure_ascii=False,indent=2)
    print(json.dumps(dict(date=a.date,matched_sets=data['set_record_count'],output=str(a.out),remote_modified=False),ensure_ascii=False))
if __name__=='__main__':main()
