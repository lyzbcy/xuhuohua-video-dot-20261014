"""Read-only, allowlisted single-day training export; no real user records bundled."""
from pathlib import Path
import argparse,datetime,json,sys

def export(path:Path,day:str):
    datetime.date.fromisoformat(day)
    selected=[]
    with path.open(encoding='utf-8-sig') as f:
        for line_number,line in enumerate(f,1):
            if not line.strip():continue
            try:row=json.loads(line)
            except json.JSONDecodeError as e:raise ValueError(f'Invalid JSONL at line {line_number}') from e
            if not isinstance(row,dict):raise ValueError(f'Expected object at line {line_number}')
            if row.get('date')!=day or row.get('action')!='set':continue
            selected.append({k:row.get(k) for k in ['date','exercise','weight','reps','ts']})
    if not selected:raise ValueError('No matching set records; confirm shooting date, schema and path before displaying numbers')
    return dict(date=day,source='fitness/records.jsonl; action=set',set_record_count=len(selected),sets=selected,review='Match each record to actual footage; null fields are unverified; no fabricated values')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--records',type=Path,required=True);p.add_argument('--date',required=True);a=p.parse_args()
    try:print(json.dumps(export(a.records,a.date),ensure_ascii=False,indent=2))
    except (OSError,ValueError) as e:print(str(e),file=sys.stderr);raise SystemExit(2)
