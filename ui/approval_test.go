package mcp

import (
    "net/http"
    "net/http/httptest"
    "net/url"
    "strings"
    "testing"
)

func TestWebJjonkuApprovalEscapesAndDoesNotEchoOwner(t *testing.T) {
    o, _, _ := oauthHTTPFixture(t)
    w := httptest.NewRecorder()
    q := url.Values{"state":{`"><script>alert(1)</script>`}, "owner_token":{"secret-must-not-appear"}, "redirect_uri":{"https://chatgpt.com/callback"}}
    o.renderApproval(w, q, http.StatusUnauthorized)
    body := w.Body.String()
    if w.Code != 401 || !strings.Contains(body,"인증키가 일치하지 않습니다") { t.Fatal("missing approval error") }
    if strings.Contains(body, "secret-must-not-appear") || strings.Contains(body, "<script>alert(1)</script>") { t.Fatal("unsafe request reflection") }
    if !strings.Contains(body, `name="state"`) || !strings.Contains(body, "WebJjonku") { t.Fatal("form state missing") }
    if w.Header().Get("Cache-Control") != "no-store" || !strings.Contains(w.Header().Get("Content-Security-Policy"), "frame-ancestors 'none'") { t.Fatal("missing headers") }
}

func TestWebJjonkuHomeIsNotAnApproval(t *testing.T) {
    _, mux, _ := oauthHTTPFixture(t)
    w := httptest.NewRecorder()
    mux.ServeHTTP(w, httptest.NewRequest("GET", "/", nil))
    if w.Code != 200 || !strings.Contains(w.Body.String(),"승인 대기 중인 연결 요청이 없습니다") || strings.Contains(w.Body.String(),`name="owner_token"`) { t.Fatal("home must not impersonate an authorization request") }
    w = httptest.NewRecorder()
    mux.ServeHTTP(w, httptest.NewRequest("POST", "/", nil))
    if w.Code != 405 { t.Fatal("home must reject POST") }
}
