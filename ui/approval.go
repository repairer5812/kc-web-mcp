package mcp

import (
    "bytes"
    "embed"
    "html/template"
    "net/http"
    "net/url"
    "strings"
)

//go:embed approval.html approval.css approval.js portlane-font.woff2
var presentation embed.FS
var approvalTemplate = template.Must(template.ParseFS(presentation, "approval.html"))

type hiddenField struct { Name, Value string }
type approvalView struct {
    Pending, Invalid bool
    Client, Destination, Resource string
    Fields []hiddenField
}

func (o *OAuthHTTP) registerPresentation(m *http.ServeMux) {
    for _, asset := range []string{"approval.css", "approval.js", "portlane-font.woff2"} {
        asset := asset
        m.HandleFunc("/assets/" + asset, func(w http.ResponseWriter, r *http.Request) {
            if !method(w, r, "GET, HEAD") { return }
            data, _ := presentation.ReadFile(asset)
            types := map[string]string{"approval.css":"text/css; charset=utf-8", "approval.js":"text/javascript; charset=utf-8", "portlane-font.woff2":"font/woff2"}
            w.Header().Set("Content-Type", types[asset])
            w.Header().Set("Cache-Control", "public, max-age=3600")
            w.Header().Set("X-Content-Type-Options", "nosniff")
            if r.Method != "HEAD" { _, _ = w.Write(data) }
        })
    }
    m.HandleFunc("/{$}", func(w http.ResponseWriter, r *http.Request) {
        if r.URL.Path != "/" { http.NotFound(w, r); return }
        if !method(w, r, "GET, HEAD") { return }
        o.renderPresentation(w, r, approvalView{}, http.StatusOK)
    })
}

func (o *OAuthHTTP) renderApproval(w http.ResponseWriter, q url.Values, status int) {
    view := approvalView{Pending:true, Invalid:status == http.StatusUnauthorized, Client:"연결 앱"}
    if c, ok := o.store.Client(q.Get("client_id")); ok && strings.TrimSpace(c.ClientName) != "" { view.Client = c.ClientName }
    if u, e := url.Parse(q.Get("redirect_uri")); e == nil { view.Destination = u.Hostname() }
    view.Resource = q.Get("resource")
    for k, v := range q { if k != "owner_token" && len(v) > 0 { view.Fields = append(view.Fields, hiddenField{k,v[0]}) } }
    o.renderPresentation(w, nil, view, status)
}

func (o *OAuthHTTP) renderPresentation(w http.ResponseWriter, r *http.Request, view approvalView, status int) {
    // All request values are escaped by html/template. Owner tokens are never rendered.
    var body bytes.Buffer
    if err := approvalTemplate.Execute(&body, view); err != nil { http.Error(w,"page unavailable",500); return }
    w.Header().Set("Content-Security-Policy", "default-src 'none'; style-src 'self'; script-src 'self'; font-src 'self'; img-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'")
    w.Header().Set("Content-Type", "text/html; charset=utf-8")
    w.Header().Set("Cache-Control", "no-store")
    w.Header().Set("Referrer-Policy", "no-referrer")
    w.Header().Set("X-Content-Type-Options", "nosniff")
    w.Header().Set("X-Frame-Options", "DENY")
    w.WriteHeader(status)
    if r == nil || r.Method != "HEAD" { _, _ = w.Write(body.Bytes()) }
}
