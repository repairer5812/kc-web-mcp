# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

자기 서버를 웹 채팅에 연결해 프로젝트 파일을 수정하고 테스트하려는 개인 사용자. 공개 저장소 이용자는 자기 서버와 자기 계정을 사용한다.

## Product Purpose

MCP를 통해 웹 채팅에서 전용 작업 공간의 파일 읽기·수정, Git 조회와 테스트 명령 실행을 가능하게 한다. 연결 화면의 성공은 서버 소유자가 부여되는 권한을 이해하고 Owner token으로 OAuth 승인을 완료하는 것이다.

## Operating Context

ChatGPT 개발자 모드에서 등록한 MCP 앱이 별도 HTTPS OAuth 승인 페이지를 연다. 사용자는 서버가 생성한 Owner token을 붙여넣고 승인한 뒤 채팅으로 돌아간다.

## Capabilities and Constraints

- SpaceDock 0.1.6 기반 OAuth·PKCE·MCP. 인증 검증은 기존 서버 코드가 담당한다.
- 기본 배포는 컨테이너 작업 볼륨만 연결하며 호스트 프로젝트 폴더를 연결하지 않는다.
- 파일 읽기·수정, 명령 실행, Git 조회, 작업 공간 및 recall 도구 사용 권한이 있다. 셸 명령 실행 권한은 파일 도구 경로 검사보다 넓다.
- 임시 Cloudflare 주소는 재시작 시 변경된다. 공개 저장소는 MIT 라이선스다.
- 이름은 기존 KC Web MCP에서 **Portlane**으로 변경 확정됐다. 사용자는 밝은 연결 승인서와 왼쪽 단계 안내 구성을 선택했다.

## Brand Commitments

인터넷 커뮤니티 용어를 제품명으로 사용하지 않는다. 사용자 요청은 서비스 설명을 갖춘 완성도 높은 독립 디자인이다. OpenAI·ChatGPT와 관계를 오인시키는 브랜딩을 피하고 자체 심벌을 사용한다. 한국어 안내를 우선한다.

## Evidence on Hand

README.md, SECURITY.md, PRIVACY.md와 실제 OAuth·MCP 통합 검증 스크립트. 서버 배포 및 공개 HTTPS 검증 완료. 고객 수·성능 비교·공식 제휴에 대한 증거는 없다.

## Product Principles

- 연결 전에 작업 권한을 명확하게 설명한다.
- Owner token은 서버 소유자 인증키이며 ChatGPT 비밀번호와 구분한다.
- 오류는 원인과 다시 시도할 방법을 안내한다.
- 독립 서비스임을 분명하게 표현한다.
