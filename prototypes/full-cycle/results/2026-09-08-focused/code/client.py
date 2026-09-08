#!/usr/bin/env python3
"""Public fixture client. Only the loopback evaluation service is contacted."""
import json
from pathlib import Path
import sys
import urllib.request

if __name__=='__main__':
    connection=json.loads((Path(__file__).parent/'connection.json').read_text())
    op=sys.argv[1]
    raw=sys.argv[2] if len(sys.argv)>2 else '{}'
    args=json.loads(Path(raw[1:]).read_text() if raw.startswith('@') else raw)
    data=json.dumps({'trial':connection['trial'],'op':op,'args':args}).encode()
    request=urllib.request.Request(connection['url'],data,{'Content-Type':'application/json'})
    with urllib.request.urlopen(request,timeout=15) as response:
        result=json.load(response)
    print(json.dumps(result,indent=2))
