# 기존 kc-web-mcp 설치 갱신

이름을 바꾸어도 기존 인증키와 작업 볼륨을 새로 만들면 안 된다.
기존 설치 폴더에서 진행하며 기존 `.env`를 보존한다.

1. `docker compose ls`와 `docker volume ls`로 기존 Compose 프로젝트 이름을 확인한다.
2. 기본 이름 `kc-web-mcp`로 설치했다면 기존 `.env`에 다음을 추가한다.
   이미 다른 `COMPOSE_PROJECT_NAME`을 사용했다면 그 값을 유지한다.

```dotenv
COMPOSE_PROJECT_NAME=kc-web-mcp
```

3. Git 원격을 `https://github.com/repairer5812/webjjonku.git`로 갱신하고 변경사항을 보존하며 업데이트한다.
4. `docker compose config`의 작업·상태 볼륨 이름이 기존 볼륨과 일치하는지 확인한 후 시작한다.
5. 재시작으로 임시 URL이 바뀌면 ChatGPT에 새 주소를 등록한다. 인증키는 기존 값을 유지한다.

이 호환 프로젝트 이름은 Docker의 기존 데이터 식별자다. 새 설치는 `webjjonku`를 사용한다.
폴더 이름을 바꾸거나 볼륨을 삭제할 필요가 없다. `down -v`는 실행하지 않는다.