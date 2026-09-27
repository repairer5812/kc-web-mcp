"""Apply a presentation-only extension to pinned upstream SpaceDock source."""
from pathlib import Path
import sys

root = Path(sys.argv[1])
ui = Path(sys.argv[2])
source = root / 'internal/mcp/oauth_http.go'
text = source.read_text()
start = text.index('func (o *OAuthHTTP) renderApproval(')
end = text.index('func (o *OAuthHTTP) token(', start)
text = text[:start] + text[end:]
text = text.replace('\t"html/template"\n', '')
anchor = '\tm.HandleFunc("/oauth/authorize", o.authorize)'
assert text.count(anchor) == 1
text = text.replace(anchor, anchor + '\n\to.registerPresentation(m)')
source.write_text(text)
for name in ('approval.go', 'approval_test.go', 'approval.html', 'approval.css', 'approval.js', 'webjjonku-font.woff2'):
    (root / 'internal/mcp' / name).write_bytes((ui / name).read_bytes())
