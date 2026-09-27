# 웹쫀쿠 · WebJjonku

**웹 ChatGPT로 내 작업 공간의 파일을 수정하고 명령·테스트를 실행하는 도구.**
[SpaceDock](https://github.com/starlove7/spacedock) 기반의 독립 오픈소스 프로젝트다.

```text
PC 브라우저의 ChatGPT → HTTPS·OAuth → 내 PC 또는 소형 서버의 Docker 작업 공간
```

## 어디에 설치하나요?

- **내 PC — 기본 선택:** Windows/macOS/Linux. PC가 켜져 있고 Docker가 실행 중일 때 사용한다.
- **소형 웹서버 — 상시 실행:** Linux 서버에 같은 구성을 설치한다. PC를 꺼도 서버는 실행된다.

ChatGPT를 사용하는 화면과 작업 공간이 실행되는 위치는 별개다. 서버에 설치해도
PC 브라우저에서 사용한다. 모바일 전용 기능과 사용자별 호스팅은 제공하지 않는다.
ChatGPT 개발자 모드와 사용하려는 MCP 작업 권한이 계정에 있어야 한다.
[현재 공식 지원 안내](https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt)를 확인한다.
이 런타임에는 모델 설치나 OpenAI 모델 API 키가 필요 없다.

## AI에게 설치 맡기기

아래 내용을 설치할 PC 또는 서버에 접근할 수 있는 AI에게 전달한다.

> https://github.com/repairer5812/webjjonku 를 읽고 이 환경에 설치해줘.
> README의 AI 설치 절차에 따라 환경 확인, 필요한 도구 설치, Docker 실행,
> HTTPS 터널 공개, OAuth 연결 및 demo 검증까지 진행해줘.
> 별도 요청이 없으면 현재 PC에 설치하고 임시 터널과 전용 Docker 볼륨을 사용해.
> 이 설치에 필요한 변경과 HTTPS 공개를 승인하며, 선택 질문은 기본값으로 처리해.
> 기존 파일·서비스·Docker 볼륨·인증키를 보존하고 비밀값은 채팅이나 로그에 출력하지 마.
> 로그인, OS 승인, 재부팅 등 내가 직접 해야 하는 단계에서만 필요한 행동을 알려줘.
> 검증 결과와 다음 실행·중지 방법을 짧게 보고해줘.

### AI 설치 절차

1. **환경 확인:** OS/CPU·여유 메모리/디스크, Git, Docker 및 Compose 확인.
   Windows/macOS는 Docker Desktop의 Linux 엔진, Linux는 Docker Engine+Compose를 사용한다.
   없는 도구는 공식 배포본으로 설치하고 실행한다. OS 권한·라이선스 동의·재부팅이
   필요하면 사용자에게 해당 단계만 안내한다. 다른 설치 방식·도메인 선택 질문은 하지 않는다.
2. **전용 폴더:** 저장소를 새 `webjjonku` 폴더에 복제한다. 이미 있으면 변경 상태를
   확인하고 보존한다. 비밀파일이나 기존 프로젝트를 복사하지 않는다.
3. **실행:** 아래 OS 명령으로 빌드·시작한다. 처음 빌드에는 이미지 다운로드와 저장 공간이
   필요하다. 작은 서버는 `.env`에 `MCP_MEMORY_LIMIT=256m`, `MCP_CPUS=0.5`를 설정할 수 있다.
   호스트 메모리와 컨테이너 제한은 별개이며 무거운 빌드에는 더 많은 자원이 필요하다.
4. **자동 검증:** runtime이 healthy인지 확인하고 아래 `verify`를 실행한다. 실패하면
   상태와 제한된 로그로 원인을 해결한다. 로그에 비밀값이 있으면 출력하지 않는다.
5. **ChatGPT 연결:** 출력된 `/mcp` URL로 OAuth 앱을 등록한다. 브라우저 조작이 가능하고
   사용자가 로그인해 있으면 직접 진행한다. Owner token은 캡처·채팅·명령 인수에 남기지 말고
   해당 인스턴스의 검증된 승인 화면에만 입력한다. 자동화할 수 없으면 사용자에게 정확한
   연결 절차만 안내한다. 계정에 기능이 없으면 설치 성공과 ChatGPT 연결 불가를 구분한다.
6. **실제 대화 검증:** demo에서 아래 요청을 실행한다. HTTP 검사 통과를 실제 대화 성공으로
   보고하지 않는다. 완료 시 설치 위치, URL, 검증 결과, 시작·중지 명령을 보고한다.

## 직접 설치

```bash
git clone https://github.com/repairer5812/webjjonku.git
cd webjjonku
```

Docker와 Compose가 설치·실행된 상태에서 진행한다.

**Windows — PowerShell**

```powershell
.\scripts\pc.ps1 start
.\scripts\pc.ps1 verify
.\scripts\pc.ps1 connection
```

실행 정책이 차단하면 시스템 정책을 임의로 낮추지 말고 허용된 실행 방법을 사용한다.

**macOS / Linux PC / Linux 소형 서버**

```bash
bash scripts/install.sh
docker compose exec -T runtime python3 /opt/kc-mcp/scripts/check_live.py
docker compose exec -T runtime cat /state/connection-url.txt
```

Linux에서 Docker 접근에 관리자 권한이 필요하면 운영 환경에 맞게 `sudo`를 사용한다.
임시 HTTPS 주소는 재시작하면 바뀔 수 있다. 바뀌면 ChatGPT 연결 주소도 갱신한다.

## ChatGPT 연결·사용

1. **PC의 ChatGPT 웹**에서 개발자 모드를 켜고 새 MCP 앱을 추가한다.
2. `connection`에서 확인한 전체 `/mcp` URL을 입력하고 **OAuth**를 선택한다.
3. 소유자 인증키는 본인 터미널에서 확인해 **해당 인스턴스의 승인 페이지에만** 입력한다.

```bash
docker compose exec -T runtime cat /state/oauth-owner.token
```

4. 새 ChatGPT 대화에 연결한 앱을 선택하고 다음을 요청한다.

> projects 루트의 demo 작업 공간을 열고 calculator.mjs와 테스트를 읽어줘.
> subtract(a,b)를 추가하고 테스트를 추가한 뒤 node --test와 git diff로 확인해줘.
> 이미 구현되어 있다면 기존 테스트를 실행하고 확인해줘. 커밋과 push는 하지 마.

프로젝트는 Docker의 `/workspace` 볼륨에 만들거나 저장소를 복제한다.
**PC에 설치해도 기존 PC 폴더가 자동 연결되지는 않는다.** Node.js·Python·Git·ripgrep이 포함된다.
SSH 키·홈 폴더·Docker 소켓은 연결하지 않는다.

## 시작·중지·데이터 보존

| 작업 | Windows | macOS / Linux |
|---|---|---|
| 시작 | `.\scripts\pc.ps1 start` | `bash scripts/install.sh` |
| 상태 | `.\scripts\pc.ps1 status` | `docker compose ps` |
| 중지 | `.\scripts\pc.ps1 stop` | `docker compose stop` |

중지해도 인증 상태와 작업 파일은 유지된다. **`docker compose down -v`는 사용하지 않는다.**
기존 `kc-web-mcp` 설치를 갱신할 때는 [데이터 보존 안내](docs/MIGRATION.md)를 먼저 읽는다.
고정 주소가 필요할 때만 [고정 터널 설정](docs/STABLE_TUNNEL.md)을 사용한다.

## 검증과 사용 범위

원본 OAuth/MCP 통합 검사 18개, 커스텀 컨테이너 검사 18개, 공개 HTTPS 검사 11개를
검증했다. GitHub Actions가 컨테이너 빌드와 통합 검사를 수행한다.
PC 실행 스크립트는 PowerShell 구문·명령 전달을 점검했다. Docker Desktop 실기 검증과
각 사용자의 실제 ChatGPT 대화 검증은 별도다.

파일 도구의 경로 검사는 셸을 격리하지 않는다. 셸은 해당 컨테이너의 상태와 네트워크에
접근할 수 있다. 단일 신뢰 사용자용이며 서로 신뢰하지 않는 사용자는 인스턴스를 공유하지 않는다.

OpenAI 공식 서비스가 아니다. 각자 계정의 권한·약관·사용 제한을 따른다.
계정 공유·웹 출력 자동 수집·사용 제한 우회·모델 접근 재판매 기능은 제공하지 않는다.
코드 공개와 ChatGPT 앱 디렉터리 등록은 별개다.
[개인정보](PRIVACY.md) · [보안](SECURITY.md) · [MIT 및 의존성 고지](THIRD_PARTY_NOTICES.md)