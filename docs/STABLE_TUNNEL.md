# 고정 HTTPS 주소

임시 주소로 연결을 확인한 뒤 본인 Cloudflare 계정의 Named Tunnel과 소유 도메인을 사용한다.

1. `.env.example`을 `.env`로 복사하고 `PUBLIC_BASE_URL=https://본인서브도메인`을 설정한다.
2. Cloudflare 터널의 공개 호스트를 해당 도메인 → `http://127.0.0.1:8766`으로 설정한다.
   HTTP Host Header는 `localhost`로 지정한다. 터널은 runtime의 네트워크 공간을 공유한다.
3. 터널 토큰은 `cloudflare-tunnel.token`에 보관한다. 채팅·Git에 올리지 않는다.
4. macOS/Linux에서 `bash scripts/install.sh --stable`로 실행한다.
   Windows는 `docker compose -f compose.yaml -f compose.stable.yaml up -d --build --wait --wait-timeout 180`을 사용한다.
5. 고정 `/mcp` URL로 OAuth 연결을 등록하고 공개 연결 검사와 실제 대화를 검증한다.

Cloudflare 토큰은 별도 터널 컨테이너에만 제공된다. MCP 컨테이너에는 전달하지 않는다.
Quick Tunnel은 테스트용이며 SSE를 지원하지 않는다. 이 구성은 SpaceDock의 Stateless
Streamable HTTP·JSON 응답을 사용한다.

- [Cloudflare Quick Tunnel](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/)
- [OpenAI 연결 안내](https://developers.openai.com/plugins/deploy/connect-chatgpt)