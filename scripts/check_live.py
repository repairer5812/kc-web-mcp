"""Run inside the operator's container; never prints authentication secrets."""
import base64
import hashlib
import json
from pathlib import Path
import secrets
import urllib.error
import urllib.parse
import urllib.request

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args): return None

def main():
    origin = Path('/state/connection-url.txt').read_text().strip().removesuffix('/mcp')
    opener = urllib.request.build_opener(NoRedirect)
    checks = []
    token = None
    def req(path, body=None, form=False, authorized=False):
        headers = {'Accept': 'application/json, text/event-stream', 'MCP-Protocol-Version': '2025-03-26'}
        if body is not None:
            headers['Content-Type'] = 'application/x-www-form-urlencoded' if form else 'application/json'
            body = urllib.parse.urlencode(body).encode() if form else json.dumps(body).encode()
        if authorized: headers['Authorization'] = 'Bearer ' + token
        try: response = opener.open(urllib.request.Request(origin+path, data=body, headers=headers), timeout=30)
        except urllib.error.HTTPError as error: response = error
        with response:
            raw=response.read().decode()
            try: data=json.loads(raw)
            except json.JSONDecodeError: data={}
            return response.status,response.headers,data
    def check(label, condition):
        if not condition: raise RuntimeError('Failed: '+label)
        checks.append(label)
        print('PASS',label,flush=True)
    check('public HTTPS health',req('/healthz')[0]==200)
    check('public unauthenticated MCP denied',req('/mcp',{})[0]==401)
    status,_,metadata=req('/.well-known/oauth-protected-resource/mcp')
    check('public OAuth discovery',status==200 and metadata.get('resource')==origin+'/mcp')
    status,_,client=req('/register',{'client_name':'KC Live Verification','redirect_uris':['http://127.0.0.1/callback'],
        'grant_types':['authorization_code','refresh_token'],'response_types':['code'],'token_endpoint_auth_method':'none'})
    check('public client registration',status in (200,201) and bool(client.get('client_id')))
    verifier=secrets.token_urlsafe(40)
    challenge=base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()
    auth={'client_id':client['client_id'],'redirect_uri':'http://127.0.0.1/callback','response_type':'code',
          'resource':origin+'/mcp','scope':'spacedock','code_challenge_method':'S256','code_challenge':challenge,
          'owner_token':Path('/state/oauth-owner.token').read_text().strip()}
    status,headers,_=req('/oauth/authorize',auth,form=True)
    check('public owner approval',status==302)
    code=urllib.parse.parse_qs(urllib.parse.urlparse(headers['Location']).query)['code'][0]
    status,_,pair=req('/oauth/token',{'grant_type':'authorization_code','client_id':client['client_id'],
        'redirect_uri':auth['redirect_uri'],'resource':auth['resource'],'code':code,'code_verifier':verifier},form=True)
    check('public PKCE exchange',status==200 and bool(pair.get('access_token')))
    token=pair['access_token']
    sequence=0
    def rpc(method,params):
        nonlocal sequence
        sequence+=1
        status,_,data=req('/mcp',{'jsonrpc':'2.0','id':sequence,'method':method,'params':params},authorized=True)
        if status!=200 or 'error' in data:
            error=data.get('error', {})
            reason=error.get('message','') if isinstance(error,dict) else str(error)
            raise RuntimeError(f'RPC failed: {method}; HTTP {status}; {reason}')
        return data['result']
    initialized=rpc('initialize',{'protocolVersion':'2025-03-26','capabilities':{},'clientInfo':{'name':'live-check','version':'1'}})
    check('public MCP initialization',initialized['serverInfo']['name']=='spacedock')
    def call(name,args): return rpc('tools/call',{'name':name,'arguments':args})
    opened=call('workspace_open',{'root_id':'projects','path':'demo','mode':'checkout'})
    check('public workspace open',not opened.get('isError'))
    wid=opened['structuredContent']['workspace_id']
    result=call('file_edit',{'workspace_id':wid,'action':'write','path':'live-verification.txt','content':'verified over HTTPS\n'})
    check('public file write',not result.get('isError'))
    result=call('read_file',{'workspace_id':wid,'path':'live-verification.txt'})
    check('public file read',not result.get('isError') and 'verified over HTTPS' in json.dumps(result))
    result=call('exec_command',{'workspace_id':wid,'command':'node --test','yield_ms':5000})
    check('public command/test execution',not result.get('isError') and result['structuredContent'].get('exit_code')==0)
    call('file_edit',{'workspace_id':wid,'action':'delete','path':'live-verification.txt'})
    call('workspace_close',{'workspace_id':wid})
    Path('/state/live-verification.json').write_text(json.dumps({'passed':checks,'scope':'public HTTPS OAuth+MCP; ChatGPT UI not tested'},indent=2))

if __name__=='__main__': main()
