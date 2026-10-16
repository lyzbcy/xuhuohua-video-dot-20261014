"""Read-only single-day training projection; source notes require explicit opt-in."""
from pathlib import Path
import argparse,datetime,json,sys

def export(path:Path,day:str,include_training_notes=False):
    datetime.date.fromisoformat(day)
    selected=[];session_notes=[]
    with path.open(encoding='utf-8-sig') as f:
        for line_number,line in enumerate(f,1):
            if not line.strip():continue
            try:row=json.loads(line)
            except json.JSONDecodeError as e:raise ValueError(f'Invalid JSONL at line {line_number}') from e
            if not isinstance(row,dict):raise ValueError(f'Expected object at line {line_number}')
            if row.get('date')!=day:continue
            action=row.get('action')
            if action not in ['set','session_start','session_end']:continue
            if include_training_notes:
                note=row.get('note')
                if note is not None and not isinstance(note,str):raise ValueError(f'Unexpected note schema at line {line_number}')
                if action in ['session_start','session_end'] and note:session_notes.append(dict(record_action=action,training_note=note))
            if action!='set':continue
            entry={k:row.get(k) for k in ['date','exercise','weight','reps','ts']}
            if include_training_notes:entry['training_note']=row.get('note')
            selected.append(entry)
    if not selected:raise ValueError('No matching set records; confirm shooting date, schema and path before displaying numbers')
    result=dict(date=day,source='fitness/records.jsonl; action=set',set_record_count=len(selected),sets=selected,review='Match each record to actual footage and read notes; numeric zero may be an unreported placeholder; no fabricated values')
    if include_training_notes:result['session_training_notes']=session_notes
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--records',type=Path,required=True);p.add_argument('--date',required=True);p.add_argument('--include-training-notes',action='store_true');a=p.parse_args()
    try:print(json.dumps(export(a.records,a.date,a.include_training_notes),ensure_ascii=False,indent=2))
    except (OSError,ValueError) as e:print(str(e),file=sys.stderr);raise SystemExit(2)
