# VIZO : Frame Guide

A lightweight, offline-ready tool for video production — calculate frame dimensions instantly by aspect ratio.

> 영상 제작 현장을 위한 경량 오프라인 프레임 가이드 계산기

---

## Changelog / 업데이트 내역

# VIZO : Frame Guide — Changelog

---

## v1.3.1 — 2026.03

### 🇺🇸 English

**Web App (`index.html`)**
- Replaced Camera Overlay with Frame Overlay — no camera permission required
- Frame Overlay now launches with `2.35:1 (CinemaScope)` as the default ratio
- Added center brightness toggle in overlay HUD: **Dark** / **Light** mode
- DESKTOP OVERLAY button relocated to the header — accessible from both Pixel and Physics tabs
- DESKTOP OVERLAY button styled in amber to match the Python desktop edition
- Physics tab layout restructured to match the Python app: Monitor settings + Result on the left, Simulation canvas (full height) + Usage guide on the right
- Physics mode: removed `readonly` from height input field — both width and height are now freely editable
- Physics mode: height input now auto-calculates width (16:9 ratio), and vice versa
- Physics mode: input placeholder updated to `세로 ex) 297`
- F11 fullscreen toast notification added when overlay opens

**Python Desktop (`vizo_frame_guide.py`)**
- Overlay transparency fixed: using `-transparentcolor #010101` chroma key on Windows — center area is now fully transparent, letterbox bars are fully opaque
- Opacity slider range expanded to `0–100%`; bar brightness responds to slider value
- Overlay always launches with `2.35:1 (CinemaScope)` as the default ratio
- ESC key binding extended to `hud_win` and `hud` frame for reliable close behavior
- Physics tab: height input field made editable — `readonly` removed
- Physics tab: height → width auto-calculation added (`_on_phys_h`)
- Physics tab: input placeholder changed to `세로 ex) 297`
- Scrollable frame removed; layout is now fixed (non-resizable window at `1100×820`)
- Physics tab layout restructured: left column (Monitor + Result), right column (Simulation + Usage guide)

---

### 🇰🇷 한국어

**웹앱 (`index.html`)**
- 카메라 오버레이 제거 → Frame Overlay로 교체 (카메라 권한 불필요)
- Frame Overlay 실행 시 기본 종횡비 `2.35:1 (CinemaScope)`로 고정
- 오버레이 HUD에 중앙 밝기 선택 추가: **■ 어둡게** / **□ 밝게**
- DESKTOP OVERLAY 버튼을 헤더로 이동 — 픽셀/물리 탭 어디서든 접근 가능
- DESKTOP OVERLAY 버튼 색상을 파이썬 버전과 동일한 amber(주황)로 변경
- 물리 탭 레이아웃을 파이썬 앱과 동일하게 재구성: 좌측(모니터 설정 + 결과 수치), 우측(시뮬레이션 캔버스 + 사용법)
- 물리 모드 세로 입력칸 `readonly` 제거 — 가로/세로 모두 자유 입력 가능
- 물리 모드 세로 입력 시 가로 자동 계산(16:9 기준), 반대도 동일하게 작동
- 물리 모드 입력 placeholder `세로 ex) 297`로 변경
- 오버레이 열릴 때 F11 전체화면 안내 토스트 표시

**파이썬 데스크톱 (`vizo_frame_guide.py`)**
- 오버레이 투명도 수정: Windows에서 `-transparentcolor #010101` 크로마키 방식 적용 — 중앙 영역 완전 투명, 레터박스 바 완전 불투명
- Opacity 슬라이더 범위 `0–100%`로 확장, 슬라이더 값에 따라 바 밝기 반응
- 오버레이 실행 시 기본 종횡비 `2.35:1 (CinemaScope)`로 고정
- ESC 키 바인딩을 `hud_win` 및 `hud` 프레임까지 확장 — 안정적인 닫기 동작 보장
- 물리 탭 세로 입력칸 `readonly` 제거 — 자유 입력 가능
- 물리 탭 세로 입력 → 가로 자동 계산 기능 추가 (`_on_phys_h`)
- 물리 탭 입력 placeholder `세로 ex) 297`로 변경
- 스크롤 프레임 제거, 창 고정 크기(`1100×820`) 비조절 방식으로 변경
- 물리 탭 레이아웃 재구성: 좌측(모니터 설정 + 결과), 우측(시뮬레이션 + 사용법)

---

## v1.3.1 — Initial Python Desktop Release

### 🇺🇸 English
- Initial release of Python desktop edition (`vizo_frame_guide.py`)
- Two-column layout matching the web app, window size `1060×720`
- Desktop Overlay with fullscreen letterbox rendering
- Overlay HUD moved to top bar
- Semi-transparent overlay support with opacity toggle
- Pixel mode and Physics (tape marking) mode

### 🇰🇷 한국어
- 파이썬 데스크톱 버전 최초 출시 (`vizo_frame_guide.py`)
- 웹앱과 동일한 2컬럼 레이아웃, 창 크기 `1060×720`
- 전체화면 레터박스 렌더링 데스크톱 오버레이
- 오버레이 HUD 상단으로 이동
- Opacity 토글을 통한 반투명 오버레이 지원
- 픽셀 모드 및 물리(테이프 마킹) 모드

---

## v1.2.1 — Web App

### 🇺🇸 English
- Web PWA version (`index.html`) with Pixel mode and Physics mode
- Camera overlay for on-set framing reference
- Tape marking simulation canvas

### 🇰🇷 한국어
- 웹 PWA 버전 (`index.html`) — 픽셀 모드 및 물리 모드
- 현장 프레이밍 참고용 카메라 오버레이
- 테이프 마킹 시뮬레이션 캔버스


### v1.2.0
**English**

- **Tab UI** — The interface is now split into two tabs: *Pixel Mode* and *Physics Mode*
- **Physics Mode (new)** — A new mode designed for on-set monitor marking
  - Monitor ratio is locked to **16:9** by default (the standard for most production monitors), with a Custom option for manual input
  - Enter the monitor's actual width in **mm** — height is calculated automatically
  - Select a target aspect ratio (e.g. 2.35:1 Cinemascope)
  - Results show the **guide frame size** (W × H in mm) and the **tape marking offset** for each edge (top / bottom / left / right in mm)
  - Canvas preview renders the tape guide position visually on the monitor
- **Visual consistency** — Pixel Mode and Physics Mode now share identical layout, typography, and color language

**한국어**

- **탭 UI 추가** — 인터페이스가 *픽셀 모드*와 *물리 모드* 두 탭으로 분리됨
- **물리 모드 신규 추가** — 현장 모니터에 테이프로 가이드를 붙이기 위한 실측 계산 모드
  - 모니터 비율은 기본값 **16:9** 고정 (현장 표준), Custom 선택 시 직접 입력 가능
  - 모니터 실측 가로(mm) 입력 시 세로 자동 계산
  - 목표 종횡비 선택 (예: 2.35:1 시네마스코프)
  - 결과값: **종횡비 적용 프레임 크기** (가로 × 세로 mm) + **테이프 마킹 위치** (상/하/좌/우 각각 mm)
  - Canvas 프리뷰로 모니터 위 테이프 위치를 시각적으로 확인 가능
- **UI 일관성 개선** — 픽셀 모드와 물리 모드의 레이아웃, 서체, 색상이 완전히 통일됨

---

### v1.1.0
**English**
- Initial release with Pixel Mode
- Aspect ratio selector with common presets (16:9, 4:3, 2.35, 2.39, 2.40, etc.)
- Lock / unlock chain for width–height coupling
- One-click copy for width and height values

**한국어**
- 픽셀 모드 최초 출시
- 16:9, 4:3, 2.35, 2.39, 2.40 등 주요 종횡비 프리셋 지원
- 가로·세로 연동 체인 잠금/해제 기능
- 가로·세로 값 원클릭 복사

---

## Usage / 사용법

### Pixel Mode / 픽셀 모드
1. Select an aspect ratio from the dropdown
2. Enter width or height in px — the other value is calculated automatically
3. Click **Copy** to copy either value

> 종횡비를 선택하고 가로 또는 세로 픽셀값을 입력하면 나머지가 자동 계산됩니다.

### Physics Mode / 물리 모드
1. Set monitor ratio — leave as **16:9** for most production monitors
2. Enter the monitor's actual screen width in **mm** (measure with a ruler)
3. Select the target aspect ratio
4. Read the guide frame size and tape offset for each edge
5. Place tape on the monitor at the indicated distances from each edge

> 모니터 실측 가로(mm)를 입력하고 목표 종횡비를 선택하면, 테이프를 붙여야 할 위치(각 가장자리에서 몇 mm 안쪽인지)가 계산됩니다.

---

## Files / 파일 구성

| File | Description |
|------|-------------|
| `index.html` | Main application / 메인 앱 |
| `style.css` | Global styles / 전역 스타일 |
| `script.js` | Pixel Mode logic / 픽셀 모드 로직 |
| `manifest.json` | PWA manifest |
| `icon.png` | App icon |

---

## License
MIT


VIZO : Frame Guide (v1.1)
[English]
VIZO : Frame Guide is a versatile tool designed to calculate image dimensions based on aspect ratios. It is available as a Progressive Web App (PWA) for instant web access and as a Native Desktop Application (.exe) for offline use.

[한국어]
VIZO : Frame Guide는 종횡비를 기반으로 최적의 이미지 해상도를 계산해주는 도구입니다. 웹에서 즉시 사용할 수 있는 PWA(웹 앱) 버전과, 오프라인에서도 사용 가능한 데스크톱 실행 파일(.exe) 버전을 모두 지원합니다.

🚀 Key Features / 주요 기능 (v1.1 Update)
Real-time & Offline: Instant calculations via web or native desktop app. / 웹 또는 데스크톱 앱을 통한 즉각적인 계산.

Resolution Guide: Includes static reference tables for standard resolutions (SD, HD, FHD, 4K, 8K). / 표준 해상도(SD, HD, FHD 등) 가이드 포함.

Clipboard Copy: One-click copy for width and height values. / 가로/세로 수치를 한 번에 복사하는 기능.

Aspect Ratio Presets: Support for various cinematic and social media standards. / 영화 및 SNS용 다양한 종횡비 프리셋 지원.

Desktop UX: Native icons (title bar & taskbar) and fixed-window layout for professional workflow. / 아이콘 지원 및 창 크기 고정으로 전문적인 작업 환경 제공.

🛠 Usage / 사용법
1. Web App (PWA)
Visit the project website: https://<여기에_새로운_주소를_입력하세요>/

Install: Click the "Install" icon in the address bar (Chrome/Edge) or select "Add to Home Screen" on mobile.

프로젝트 웹사이트에 접속하세요: https://<여기에_새로운_주소를_입력하세요>/

설치: 브라우저 주소창의 '설치' 아이콘을 클릭하거나 모바일의 경우 '홈 화면에 추가'를 눌러 설치하세요.

2. Desktop Application (.exe)
Download the latest VIZO_Guide.exe from the Releases section.

Run the file directly. No installation is required.

Use the '🔗' lock button to toggle ratio locking and 'Copy' buttons to export values.

릴리즈(Releases) 섹션에서 VIZO_Guide.exe 파일을 다운로드하세요.

설치 없이 바로 실행하여 사용합니다.

'🔗' 잠금 버튼을 통해 비율을 고정하거나 해제할 수 있으며, 'Copy' 버튼으로 필요한 수치를 클립보드에 복사하세요.

📜 Version History / 버전 정보
v1.1
Resolution Guide: Added static reference list for standard resolutions.

Clipboard: Added 'Copy' buttons for quick data export.

UI/UX: Fixed window size and consistent icon support.

Localization: Added full aspect ratio descriptions in the dropdown.

Created by NOTELOG
