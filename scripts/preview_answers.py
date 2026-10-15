"""Show concise model answers during a live demonstration."""
import json
import sys
from pathlib import Path

path = Path(sys.argv[1] if len(sys.argv) > 1 else 'answers.json')
data = json.loads(path.read_text(encoding='utf-8-sig'))
for chat in data.get('chats', []):
    print(f"\nCHAT {chat.get('chat_id', '?')}")
    for msg in chat.get('messages', []):
        print(f"  Q: {msg.get('question', '')}")
        print(f"  A: {msg.get('answer', '')}")
        print(f"  Source sections: {len(msg.get('contexts', []))}")
