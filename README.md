# VIZO : Frame Guide — Web

<p align="center">
  <b>Aspect Ratio Calculator & Letterbox Overlay — Web Version</b><br/>
  <sub>종횡비 계산기 및 레터박스 오버레이 — 웹 버전</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.3.2-00d1ff?style=flat-square"/>
  <img src="https://img.shields.io/badge/platform-Web-blueviolet?style=flat-square"/>
  <img src="https://img.shields.io/badge/PWA-ready-f5a623?style=flat-square"/>
</p>

---

## English

### Overview

**VIZO : Frame Guide (Web)** is the browser-based version of the Frame Guide tool.  
Calculate aspect ratios in pixels, find physical tape marking positions on monitors, and use the full-screen overlay to preview letterbox framing live — no installation required.

🔗 **Live**: [your-github-pages-url]

---

### Features

#### 📐 Pixel Mode
- Calculate width/height from any aspect ratio
- Lock ratio to freely adjust one dimension
- Presets: 16:9, 19.5:9, 1:1, 4:3, 1.85, 2.35, 2.39, 2.40
- Custom ratio input
- Resolution guide: SD / HD / FHD / QHD / 4K / 8K
- One-click copy of W/H values

#### 📏 Physics Mode (Tape Marking)
- Input physical monitor size in millimeters
- Auto-calculates opposing dimension in 16:9 mode
- Outputs exact tape positions: Top / Bottom / Left / Right
- Visual simulation of tape markings
- Click any value to copy

#### ◉ Full-Screen Overlay
- Letterbox frame rendered over the entire browser window
- Floating HUD with:
  - Ratio selector: 2.35, 2.39, 2.40, 1.85, 16:9, 4:3, 1:1
  - Bar color: Black / Green
  - Center brightness: Dark / Light
  - HUD toggle button (⊟ HUD)
  - Close button
- HUD auto-hides after 3 seconds
- Click/touch anywhere to show HUD again
- Mouse movement does **not** trigger HUD (intentional)
- Keyboard shortcut: `Esc` to exit overlay
- PWA installable (Add to Home Screen)

---

### Version History

| Version | Type | Changes |
|---------|------|---------|
| **1.3.2** | 🐛 Bug Fix | HUD auto-hides 3s after overlay opens. Click/touch to show HUD again. Manual HUD toggle button (⊟ HUD) added. Mouse move no longer triggers HUD |
| 1.3.1 | ✨ Feature | Full-screen overlay mode. Floating HUD with controls. F11 toast guide. PWA support |
| 1.1.0 | 🎉 Initial | Pixel Mode, Physics Mode, basic overlay, aspect ratio calculator |

---

### License

© 2026 NOTELOG. All rights reserved.

---
---

## 한국어

### 개요

**VIZO : Frame Guide (웹)**은 Frame Guide 도구의 브라우저 버전입니다.  
픽셀 단위 종횡비 계산, 모니터 테이프 마킹 위치 산출, 전체화면 오버레이로 레터박스를 실시간 미리보기 — 설치 없이 사용 가능합니다.

🔗 **라이브**: [your-github-pages-url]

---

### 기능

#### 📐 픽셀 모드
- 종횡비 기준 가로·세로 픽셀 수 자동 계산
- 비율 잠금/해제로 한 쪽 값만 자유 조정
- 프리셋: 16:9, 19.5:9, 1:1, 4:3, 1.85, 2.35, 2.39, 2.40
- 사용자 정의 비율 입력
- 해상도 가이드: SD / HD / FHD / QHD / 4K / 8K
- 원클릭 값 복사

#### 📏 물리 모드 (테이프 마킹)
- 모니터 실측 크기(mm) 입력
- 16:9 모드에서 한 쪽 값 입력 시 자동 계산
- 테이프 부착 위치 수치 출력: 상단 / 하단 / 좌측 / 우측
- 화면 위 테이프 마킹 시각 시뮬레이션
- 클릭으로 수치 복사

#### ◉ 전체화면 오버레이
- 브라우저 전체에 레터박스 프레임 표시
- 플로팅 HUD 제공:
  - 비율 선택: 2.35, 2.39, 2.40, 1.85, 16:9, 4:3, 1:1
  - 바 색상: 검정 / 초록
  - 중앙 밝기: 어둡게 / 밝게
  - HUD 토글 버튼 (⊟ HUD)
  - 닫기 버튼
- HUD 3초 후 자동 숨김
- 클릭/터치 시 HUD 재표시
- 마우스 이동으로는 HUD 재표시 안 됨 (의도된 동작)
- 키보드 단축키: `Esc`로 오버레이 종료
- PWA 설치 지원 (홈 화면 추가)

---

### 버전 히스토리

| 버전 | 유형 | 변경 사항 |
|------|------|-----------|
| **1.3.2** | 🐛 버그 픽스 | 오버레이 열리면 HUD 3초 후 자동 숨김. 클릭/터치 시 HUD 재표시. HUD 수동 토글 버튼(⊟ HUD) 추가. 마우스 이동으로는 HUD 재표시 안 됨 |
| 1.3.1 | ✨ 기능 추가 | 전체화면 오버레이 모드. 플로팅 HUD (비율·색상·밝기·닫기). F11 안내 토스트. PWA 지원 |
| 1.1.0 | 🎉 최초 릴리스 | 픽셀 모드, 물리 모드, 기본 오버레이, 종횡비 계산기 |

---

### 라이선스

© 2026 NOTELOG. All rights reserved.