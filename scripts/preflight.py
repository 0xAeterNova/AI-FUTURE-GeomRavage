"""Offline readiness check for the organizer's Ollama model and data."""
from pathlib import Path
import json
import sys
import urllib.request
import urllib.error
import os
import subprocess
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
import main

def main_check():
    failures=[]
    print('BURHAN PREFLIGHT')
    print('Python:',sys.version.split()[0])
    print('Project:',ROOT)
    try:
        svcs=main.load_services(ROOT/'data')
        print('Source documents:',len(svcs),'| sections:',sum(len(s.sections) for s in svcs.values()))
    except Exception as e:
        failures.append('Service data: '+str(e))
    sample=ROOT/'questions.json'
    try:
        source=json.loads(sample.read_text(encoding='utf-8-sig'))
        print('Sample messages:',sum(len(chat['messages']) for chat in source['chats']))
    except Exception as e:
        failures.append('Sample JSON: '+str(e))
    try:
        host=os.getenv('OLLAMA_HOST','http://127.0.0.1:11434').rstrip('/')
        if host.startswith('http://0.0.0.0:'):
            host=host.replace('0.0.0.0','127.0.0.1',1)
        with urllib.request.urlopen(host+'/api/tags',timeout=8) as response:
            models=json.load(response).get('models',[])
        names={m.get('name') for m in models}
        if main.OFFICIAL_MODEL not in names:
            failures.append(f'Official model is not available in Ollama: {main.OFFICIAL_MODEL}. Run ollama pull {main.OFFICIAL_MODEL}')
        else:
            print('Official model: installed')
    except Exception as e:
        failures.append('Ollama server unavailable: '+str(e)+' | start Ollama or run ollama serve')
    try:
        output=subprocess.run(['nvidia-smi','--query-compute-apps=name,used_gpu_memory','--format=csv,noheader'],capture_output=True,text=True,timeout=5)
        print('NVIDIA driver tool:', 'available' if output.returncode==0 else 'unavailable')
    except (FileNotFoundError,subprocess.TimeoutExpired):
        print('NVIDIA driver tool: not detected (not required for CPU inference)')
    for item in failures:
        print('FAIL:',item)
    print('RESULT:', 'READY' if not failures else 'NOT READY')
    return 1 if failures else 0
if __name__=='__main__':
    sys.exit(main_check())
