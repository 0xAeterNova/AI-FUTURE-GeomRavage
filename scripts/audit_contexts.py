"""Check official answers.json for missing or irrelevant contexts (no model calls)."""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
import main


def main_audit():
    questions=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'questions.json'
    answers=Path(sys.argv[2]) if len(sys.argv)>2 else ROOT/'answers.json'
    qs=json.loads(questions.read_text(encoding='utf-8-sig'))
    ans=json.loads(answers.read_text(encoding='utf-8-sig'))
    catalog=main.load_services(main.DATA)
    valid={sv.get(k):(service,k) for service,sv in catalog.items() for k,_ in main.FIELDS if sv.get(k)}
    warnings=0; checked=0
    for qc,ac in zip(qs['chats'],ans['chats']):
        last=[]
        for qm,am in zip(qc['messages'],ac['messages']):
            q=qm['question'];label=qm['message_id']
            keys,_=main.resolve_services(q,last)
            if keys:last=keys
            contexts=am.get('contexts',[])
            checked+=1
            sourced=[valid.get(c) for c in contexts]
            if any(x is None for x in sourced):
                print(f'WARN {label}: context does not match an official section')
                warnings+=1
            included={x[0] for x in sourced if x}
            missing=set(keys)-included
            if missing:
                print(f'WARN {label}: missing context for {", ".join(sorted(missing))}')
                warnings+=1
            if not keys and contexts:
                print(f'WARN {label}: cited sources although service is unresolved')
                warnings+=1
            if keys and not contexts:
                print(f'WARN {label}: no contexts for an identified service')
                warnings+=1
            primary=main.focus_fields(q)
            if primary and primary[0] in ('where','documents','duration'):
                irrelevant=[x for x in sourced if x and x[1] not in primary]
                if irrelevant:
                    print(f'WARN {label}: nonessential sections attached: '+', '.join(f'{k}/{f}' for k,f in irrelevant))
                    warnings+=1
    print(f'AUDIT: {checked} messages checked; {warnings} warnings')
    return 0 if warnings == 0 else 1

if __name__=='__main__':
    raise SystemExit(main_audit())
