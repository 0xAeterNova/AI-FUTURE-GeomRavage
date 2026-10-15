"""Validate organizer JSON schema, order, coverage, and source references."""
import json
import sys
from pathlib import Path

def main():
    source=Path(sys.argv[1] if len(sys.argv)>1 else 'questions.json')
    target=Path(sys.argv[2] if len(sys.argv)>2 else 'answers.json')
    orig=json.loads(source.read_text(encoding='utf-8-sig'))
    res=json.loads(target.read_text(encoding='utf-8-sig'))
    assert isinstance(res.get('chats'),list),'Missing chats array'
    assert len(orig['chats'])==len(res['chats']),'Changed chat count'
    errors=[]; total=0
    for o,r in zip(orig['chats'],res['chats']):
        if o.get('chat_id')!=r.get('chat_id'):errors.append('chat_id changed')
        if len(o['messages'])!=len(r['messages']):errors.append('message count changed');continue
        for a,b in zip(o['messages'],r['messages']):
            total+=1
            if a.get('message_id')!=b.get('message_id'):errors.append(f'{total}: message_id changed')
            if a.get('question')!=b.get('question'):errors.append(f'{total}: question changed')
            if not isinstance(b.get('answer'),str) or not b['answer'].strip():errors.append(f'{total}: blank answer')
            if not isinstance(b.get('contexts'),list) or not all(isinstance(x,str) for x in b['contexts']):errors.append(f'{total}: invalid contexts')
            if b.get('answer')=='error':errors.append(f'{total}: model call failed')
    if errors:
        print('VALIDATION FAILED:');print('\n'.join(errors[:30]));sys.exit(1)
    print(f'VALID FORMAT: {len(res["chats"])} chats, {total} answered messages, UTF-8 JSON')

if __name__=='__main__': main()
