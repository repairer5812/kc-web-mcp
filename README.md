# KC Web MCP

Self-hosted coding tools for ChatGPT developer mode, built on
[SpaceDock](https://github.com/starlove7/spacedock). Each user installs this on
their own server and connects using their own account.

## 검증 상태

- 구현: SpaceDock 0.1.6 기반 Docker 배포 구성과 OAuth 인증, 파일 편집, 터미널 실행.
- 검증: Windows 로컬에서 실제 HTTP MCP와 OAuth 통합 테스트 18개 통과.
- Docker 빌드·원격 운영·ChatGPT 웹 실제 연결은 별도 확인 항목이다. 기능 테스트 통과만으로 실제 연결 완료를 뜻하지 않는다.

## 공개 프로젝트의 사용 범위

본인 서버와 본인 ChatGPT 계정에서 공식 MCP 연결로 사용하는 개발 도구다.
OpenAI 공식 제품이 아니며 사용량 제한 우회, 계정 공유, 웹 채팅 출력 수집,
모델 접근 재판매 기능을 제공하지 않는다. GitHub 코드 공개와 ChatGPT 공개
앱 디렉터리 등록은 별개다. [개인정보 안내](PRIVACY.md),
[보안 범위](SECURITY.md), [라이선스 고지](THIRD_PARTY_NOTICES.md)를 확인한다.

## 구성

```text
ChatGPT 개발자 모드
  → HTTPS 터널
  → SpaceDock OAuth 승인
  → kc_server의 전용 컨테이너
  → /workspace 프로젝트 파일·Git·Node.js·Python
```

원격 개발은 `/workspace`에서 진행한다. Windows 작업 폴더가 자동으로 연결되는 구성은 아니다. 서버에 모델을 설치하지 않으며 이 MCP 런타임 자체에는 OpenAI 모델 API 키가 필요 없다. 별도 코딩 에이전트 호출 권한은 부여하지 않았다.

## 설치

1. 본인 서버의 OS·메모리·디스크·기존 서비스·Docker 유무부터 확인한다.
2. 공개 저장소를 서버의 새 전용 폴더로 복제한다.

```bash
git clone https://github.com/repairer5812/kc-web-mcp.git
cd kc-web-mcp
```

키·다른 프로젝트·인증 파일은 이 저장소에 넣지 않는다.
3. Docker와 Compose가 설치된 서버에서 실행한다.

```bash
cd ~/kc-web-mcp
bash scripts/install.sh
docker compose logs --tail 30 runtime
docker compose exec -T runtime cat /state/connection-url.txt
```

처음 실행하면 임시 `https://….trycloudflare.com/mcp` 주소가 발급된다. 주소는 재시작하면 바뀌므로 첫 연결 검증에 사용한다. 상태와 작업 파일은 Docker 볼륨에 보존된다. `docker compose down -v`는 상태와 작업물을 지우므로 사용하지 않는다.

## ChatGPT 연결

1. 개발자 모드에서 MCP 연결 추가 화면을 연다.
2. 위에서 읽은 전체 `/mcp` URL을 입력하고 OAuth 인증을 선택한다.
3. 소유자 승인 화면이 열리면 아래 명령으로 **본인 터미널에서만** 읽은 토큰을 입력한다. 채팅·문서·로그에 토큰을 붙여 넣지 않는다.

```bash
docker compose exec -T runtime cat /state/oauth-owner.token
```

4. 새 대화에 MCP 연결을 추가하고 다음 요청으로 확인한다.

> projects 루트의 demo 작업 공간을 열고 calculator.mjs와 테스트를 읽어줘. subtract(a,b)를 추가하고 테스트도 추가한 뒤 node --test를 실행하고 git diff를 보여줘. 커밋과 push는 하지 마.

실제 공개 도구 이름은 `workspace_list`, `workspace_open`, `read_file`, `file_edit`, `exec_command`, `session_observe`, `session_act` 등이다.

## 고정 주소로 운영

임시 터널 확인 후 본인 Cloudflare 계정의 Named Tunnel과 소유 도메인으로 바꾼다.

1. `.env.example`을 `.env`로 복사하고 `PUBLIC_BASE_URL=https://본인서브도메인`을 설정한다.
2. Cloudflare 터널의 공개 호스트를 해당 도메인 → `http://127.0.0.1:8766`으로 설정하고 HTTP Host Header를 `localhost`로 지정한다. 터널 컨테이너는 런타임의 네트워크 공간을 공유한다. Go MCP SDK의 localhost Host 검사와 일치시키는 설정이다. 임시 터널에는 같은 설정이 환경변수로 적용된다.
3. 터널 토큰을 `cloudflare-tunnel.token`에 저장한다. 파일을 Git에 올리거나 채팅에 공유하지 않는다.
4. `bash scripts/install.sh --stable`로 실행하고 고정 `/mcp` URL을 ChatGPT에 등록한다.

Cloudflare 인증 비밀은 별도 터널 컨테이너에만 제공한다. MCP 컨테이너에 전달하지 않는다.

## 운영

```bash
docker compose ps
docker compose logs --tail 100 runtime
docker compose exec -T runtime node --test /workspace/demo/calculator.test.mjs
# 일시 중단; 볼륨은 유지
docker compose stop
```

Node.js 22, Python 3, Git, ripgrep이 포함된다. 의존성은 작업 폴더 안에 설치하고 Python 패키지는 `.venv`를 사용한다. SSH 키나 서버의 전체 홈 디렉터리, Docker 소켓은 마운트하지 않는다.

파일 도구는 허용 경로와 민감 파일을 검사하지만 **셸 명령은 컨테이너 사용자 권한으로 실행된다**. 파일 도구의 검사만으로 셸이 격리되는 것은 아니다. 호스트 파일 접근을 제한하는 실제 경계는 컨테이너이며, 외부 네트워크 접근은 가능하다. 같은 컨테이너의 프로젝트끼리도 접근할 수 있으므로 신뢰 수준이 다른 프로젝트는 별도 인스턴스에 둔다.

## 재현 가능한 기능 검증

```bash
npm ci --ignore-scripts
# Linux x64 기준; ARM 서버에서는 linux-arm64로 변경
python3 scripts/smoke_test.py node_modules/@starlove7/spacedock/npm/dist/linux-amd64/spacedock
```

테스트는 임시 폴더에만 기록하며 실제 OAuth PKCE 교환·갱신, 미인증 차단, 파일 읽기·쓰기, 경로 이탈·민감 파일 차단, Node 테스트 실행을 확인한다. 토큰은 출력하지 않는다.

## 약관과 라이선스

OpenAI [App Developer Terms](https://openai.com/policies/developer-apps-terms/)는
개발자 모드 커넥터와 MCP 앱 개발·공개를 다룬다. 이 프로젝트는 공식 MCP
연결 경로를 사용한다. 이 사실이 모든 사용 방법의 계약 준수를 보장하지는
않는다. 사용자는 당시의 약관, 정책, 계정 권한과 사용량 제한을 따라야 한다.
계정 공유, 제한 우회, 웹 채팅 자동 수집 등은 이 프로젝트의 사용 범위에
포함되지 않는다. 작성 설정·스크립트는 MIT이며 의존성의 라이선스는 별도로 유지한다.

## 조사 근거

- [DevSpace 원본](https://github.com/Waishnav/devspace): MCP 파일 편집·명령 실행 및 OAuth 구성 사례.
- [SpaceDock 원본](https://github.com/starlove7/spacedock): 선택한 경량 Go 런타임. 검토 소스 커밋 `41df6ed1519242e742079c84989cd15b5a4e441b`, 배포 패키지 `0.1.6`.
- [OpenAI 공식 연결 안내](https://developers.openai.com/plugins/deploy/connect-chatgpt): 개발자 모드·MCP HTTPS 연결.
- [OpenAI 공식 인증 안내](https://developers.openai.com/plugins/build/auth): OAuth 기반 인증.
- [Cloudflare Quick Tunnel](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/): 임시 URL은 테스트용이며 SSE를 지원하지 않음. 선택한 SpaceDock은 Stateless Streamable HTTP와 JSON 응답을 사용한다.

서버에 올라갔다는 사실과 ChatGPT 웹 연결 완료는 각각 실제 확인 후 기록한다.
