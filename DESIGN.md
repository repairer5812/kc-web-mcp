---
name: WebJjonku
description: 한국어 안내를 우선하는 독립 오픈소스 작업 공간
colors:
  canvas: "#fff"
  rail: "#f0f3f7"
  ink: "#122143"
  muted: "#52647c"
  line: "#dae1ea"
  accent: "#2457d6"
  accent-hover: "#1945b7"
  notice: "#fff7ea"
  notice-ink: "#754a16"
  error: "#a52b2b"
  error-bg: "#fff1f1"
  field-line: "#b9c6d8"
  inset: "#f6f8fb"
typography:
  headline:
    fontFamily: "WebJjonku, 'Malgun Gothic', sans-serif"
    fontSize: "36px"
    fontWeight: 750
    lineHeight: 1.3
    letterSpacing: "-0.03em"
  title:
    fontFamily: "WebJjonku, 'Malgun Gothic', sans-serif"
    fontSize: "24px"
    fontWeight: 720
    lineHeight: 1.4
    letterSpacing: "-0.02em"
  body:
    fontFamily: "WebJjonku, 'Malgun Gothic', sans-serif"
    fontSize: "16px"
    lineHeight: 1.55
  label:
    fontFamily: "WebJjonku, 'Malgun Gothic', sans-serif"
    fontSize: "15px"
    fontWeight: 650
    lineHeight: 1.55
  code:
    fontFamily: "ui-monospace, monospace"
    fontSize: "13px"
    lineHeight: 1.55
rounded:
  panel: "8px"
  control: "5px"
  utility: "4px"
spacing:
  gap-sm: "8px"
  gap-md: "12px"
  inset-sm: "16px"
  inset-md: "20px"
  inset-lg: "24px"
  inset-xl: "36px"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.canvas}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "12px 18px"
  button-primary-hover:
    backgroundColor: "{colors.accent-hover}"
  button-secondary:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "10px 14px"
  button-secondary-hover:
    backgroundColor: "{colors.rail}"
  input:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "10px 52px 10px 14px"
    width: "100%"
  panel:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "20px 24px"
  notice:
    backgroundColor: "{colors.notice}"
    textColor: "{colors.notice-ink}"
    rounded: "{rounded.panel}"
    padding: "12px 16px"
  error:
    backgroundColor: "{colors.error-bg}"
    textColor: "{colors.error}"
    rounded: "{rounded.control}"
    padding: "14px"
---

# Design System: WebJjonku

## Overview

**Creative North Star: "명료한 작업 공간"**

WebJjonku의 시각 언어는 읽기 쉬운 한국어와 절제된 선, 차가운 중립 배경으로 정보를 정돈한다. 흰 바탕과 남색 글자가 기본이며 파란색은 현재 상태와 주요 행동을 드러낸다. 설명은 충분한 행간으로 읽히고 입력과 행동은 경계선으로 구분된다.

자체 심벌과 자체 제공 글꼴로 독립적인 정체성을 유지한다. OpenAI·ChatGPT 로고를 자체 브랜딩에 사용하지 않는다. 이 문서는 현재 구현에서 확인한 재사용 가능한 규칙을 기록한다. 개별 화면의 구성과 진행 순서는 `.impeccable/direction.md`에 남긴다.

**Key Characteristics:**

- 한국어 중심의 산세리프 위계
- 흰 표면, 차가운 회색 보조 영역, 남색 본문
- 주요 행동과 현재 상태를 나타내는 파란 강조
- 얇은 경계선과 완만한 모서리
- 짧은 상태 전환과 명확한 키보드 초점

## Colors

차가운 중립색이 읽기 영역을 만들고 파란 강조와 의미별 안내색이 상태를 구분한다. 정확한 색 값은 frontmatter를 따른다.

### Primary

- **WebJjonku Blue (`accent`)**: 자체 심벌, 현재 단계, 주요 버튼, 키보드 초점과 입력 커서.
- **Deep Action Blue (`accent-hover`)**: 주요 버튼에 포인터가 올라왔을 때.

### Neutral

- **White Canvas (`canvas`)**: 기본 문서 표면, 입력과 주요 버튼의 밝은 글자.
- **Cool Rail (`rail`)**: 보조 영역, 코드 블록, 보조 버튼과 표시 버튼의 hover 배경.
- **Navy Ink (`ink`)**: 제목과 본문, 선형 아이콘.
- **Slate Text (`muted`)**: 설명과 보조 정보.
- **Fine Divider (`line`)**: 패널, 행, 행동 영역의 경계.
- **Field Outline (`field-line`)**: 입력 및 보조 행동의 경계.
- **Inset Paper (`inset`)**: 표의 항목명 영역과 안내 컨테이너.

의미색 `notice` / `notice-ink`는 권한 안내에, `error-bg` / `error`는 인증 오류와 잘못된 입력 경계에 사용한다. 오류는 색뿐 아니라 설명과 `role="alert"`, 입력의 `aria-invalid`로도 전달한다.

## Typography

**Display / Body Font:** 자체 제공 **Pretendard**, CSS에서 `WebJjonku`이라는 family로 등록. 대체 글꼴은 Malgun Gothic과 sans-serif다. 글꼴 파일은 `ui/webjjonku-font.woff2`이며 외부 폰트 요청 없이 제공한다. 가변 굵기 범위는 100–900, 로딩 방식은 `swap`이다.

**Code Font:** 시스템 ui-monospace / monospace.

한국어 제목은 조금 조밀한 자간과 굵기로 위계를 만든다. 별도의 장식용 display 글꼴은 없다. 본문과 제목의 실제 크기·굵기·행간은 frontmatter의 역할별 토큰을 따른다.

### Hierarchy

- **Headline**: 화면 제목. 좁은 데스크톱에서는 (30px), 모바일에서는 (27px, 행간 1.35)로 줄인다.
- **Title**: 주요 섹션 제목. 모바일에서는 (21px)로 줄인다.
- **Body**: 기본 설명과 본문. 소개 설명은 데스크톱에서 (18px), 모바일에서 (16px).
- **Label**: 주요 버튼 및 짧은 행동 문구. 본문 항목명은 (16px, 650), 폼 라벨은 (16px, 620).
- **Code**: 기술 도움말. 모바일에서는 (12px), 긴 명령은 줄바꿈을 허용한다.

## Layout

정보의 관계를 정렬과 반복되는 간격으로 표현한다. 컨테이너 내부에는 주로 `inset-lg`를 쓰고 좁은 화면에서는 `inset-sm`로 줄인다. 제목과 본문, 입력과 도움말은 작은 간격으로 묶고 독립적인 영역은 더 넓게 띄운다.

현재 구현의 본문 컨테이너는 최대 너비 (1440px), 일반 데스크톱 수평 여백 (36px), 모바일 수평 여백 (20px)이다. 반응형 기준은 넓은 화면 (1600px 이상), 압축된 데스크톱 (1100px 이하), 단일 열 모바일 (760px 이하)이다. 보조 정보는 폭에 맞춰 재배치하고 긴 주소와 명령은 줄바꿈한다. 이 측정값은 현재 구현의 참고값이며 모든 새 화면에 같은 구성이나 열 너비를 강제하지 않는다.

## Elevation & Depth

표면의 깊이는 배경의 톤 차이와 얇은 경계선으로 표현한다. 패널은 정지 상태에서 그림자를 사용하지 않는다. 주요 버튼 hover에만 작은 그림자 (`0 4px 10px #17388920`)가 더해진다. 키보드 초점은 그림자가 아니라 파란 외곽선 (3px, offset 4px)이다.

## Shapes

컨테이너는 `panel` 모서리, 입력과 주요·보조 행동은 `control` 모서리, 작은 표시 버튼과 코드 블록은 `utility` 모서리를 사용한다. 경계선은 (1px)이다. 단계 상태는 원형 표식으로 구분한다. 아이콘은 채움 없는 선형 SVG이며 기본 선 굵기는 (1.8), 끝과 연결부는 round다. 브랜드 심벌은 세 개의 세로 선으로 구성한다.

## Components

### Buttons

주요 행동은 파란 바탕과 밝은 글자, 보조 행동은 가는 경계선과 본문색으로 구분한다. 주요·보조 행동의 최소 높이는 (44px). 주요 버튼은 hover, active, disabled 상태를 갖고 disabled 동안 wait 커서를 사용한다. 배경·그림자 전환은 (.18s ease)이며 모든 행동에 공통 키보드 초점이 보인다.

### Inputs / Fields

입력은 흰 표면과 얇은 경계, 최소 높이 (46px)를 사용한다. 오른쪽 표시 버튼을 위한 공간을 둔다. 비밀번호 표시 버튼은 hover 때 보조 배경을 사용하며 `aria-pressed`와 접근성 이름이 표시 상태를 반영한다. 오류 시 입력 경계는 오류색, 오류 설명은 별도 연한 표면에 배치한다.

### Cards / Containers

평평한 흰 컨테이너에 경계선과 완만한 모서리를 사용한다. 반복 행은 얇은 구분선으로 나눈다. 입력 컨테이너의 내부 여백은 `panel` 토큰을 따르고 모바일에서 (16px)로 줄어든다. 안내 영역은 의미색 배경과 선형 아이콘, 설명을 함께 사용한다.

### Navigation / Progress

진행 표식은 완료의 체크, 현재의 점, 다음의 빈 원으로 상태를 보여준다. 현재 항목은 파란 표식과 글자, 완료는 차분한 파란 회색을 사용한다. 텍스트를 함께 표시하고 현재 상태에 `aria-current`를 제공한다. 좁은 화면에서는 간결한 가로 배열을 사용한다.

### Disclosures

추가 설명은 네이티브 details / summary로 펼친다. 도움말 본문은 보조색과 최대 줄 길이 (75ch)를 사용한다. 기술 도움말을 열 때 (.22s, cubic-bezier(.16,1,.3,1))로 짧게 드러나며 reduced-motion에서는 애니메이션과 transition을 제거한다.

## Do's and Don'ts

### Do:

- **Do** 자체 제공 Pretendard와 한국어 문구를 유지한다.
- **Do** 기본 표면의 경계선과 톤 차이로 영역을 구분한다.
- **Do** 주요 행동, 현재 상태, 초점에 같은 파란 강조를 사용한다.
- **Do** 키보드 초점, 오류 설명, reduced-motion 대응을 유지한다.

### Don't:

- **Don't** OpenAI·ChatGPT 로고를 WebJjonku의 자체 브랜드로 사용한다.
- **Don't** 오류나 진행 상태를 색만으로 전달한다.
- **Don't** 외부 폰트 요청을 추가하거나 한국어 글리프를 확인하지 않은 장식 글꼴로 바꾼다.
- **Don't** 펼침 도움말을 위해 필수 안내나 주요 행동을 숨긴다.

출처: `ui/approval.css`, `ui/approval.html`, `ui/approval.js`, `PRODUCT.md`. 최종 데스크톱·모바일 캡처와 대조하여 추출했다. frontmatter가 토큰 기준이며 `.impeccable/design.json`은 확장 메타데이터와 독립 렌더링용 컴포넌트를 제공한다.
