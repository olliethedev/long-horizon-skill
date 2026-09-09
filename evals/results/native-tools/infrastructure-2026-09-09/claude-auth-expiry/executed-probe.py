import json,sys,tempfile,subprocess
from pathlib import Path
sys.path.insert(0,'evals')
from native_harnesses import discover,setup_home,bubble
from recall import utc_now
out=Path('evals/results/native-tools/infrastructure-2026-09-09/claude-auth-expiry');out.mkdir(exist_ok=False)
h=next(h for h in discover() if h.name=='claude')
with tempfile.TemporaryDirectory(prefix='native-auth-claude-',dir='evals/runs') as temp:
 t=Path(temp).resolve();w=t/'workspace';(w/'product').mkdir(parents=True);(w/'work').mkdir();home=t/'private-home';setup_home(h,home);base=bubble(w,home,h)
 rows=[]
 for label,cmd in [('auth-help',['auth','--help']),('auth-status',['auth','status','--json']),('login-help',['auth','login','--help'])]:
  r=subprocess.run(base+['/opt/harness']+cmd,capture_output=True,timeout=30)
  # Native auth status may include identity fields. Preserve only redacted status.
  text=r.stdout.decode(errors='replace')
  if label=='auth-status':
   try:
    obj=json.loads(text);text=json.dumps({k:v for k,v in obj.items() if k not in ['email','orgId','orgName','accountUuid','accountId']},indent=2)
   except ValueError: text='Non-JSON auth status output omitted; exit code retained.'
  (out/(label+'.stdout.txt')).write_text(text);(out/(label+'.stderr.txt')).write_bytes(r.stderr)
  rows.append({'command':cmd,'exit_code':r.returncode})
 p=home/'.claude/.credentials.json';v=json.loads(p.read_text()).get('claudeAiOauth',{})
 (out/'manifest.json').write_text(json.dumps({'recorded_at':utc_now(),'attempts':rows,'private_copy_expires_at_after_probe':v.get('expiresAt'),'model_calls':0,'live_config_modified':False},indent=2)+'\n')
print((out/'auth-status.stdout.txt').read_text())
print((out/'login-help.stdout.txt').read_text())
