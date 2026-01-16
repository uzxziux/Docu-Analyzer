# 인사이트 대시보드

## Overview
비정형 텍스트 데이터(댓글, 리뷰 등)를 분석하여 핵심 인사이트를 제공하는 PoC 웹 애플리케이션입니다.
NotebookLM 스타일의 깔끔하고 현대적인 UI/UX를 적용했습니다.

## Project Structure
- `app.py` - Streamlit 메인 애플리케이션
- `.streamlit/config.toml` - Streamlit 서버 설정

## UI/UX Design
- **NotebookLM 스타일**: 사이드바 네비게이션, 카드 기반 레이아웃
- **Google 디자인 시스템**: 깔끔한 색상, 둥근 모서리, 미니멀한 디자인
- **사이드바**: 소스 목록, 설정 옵션
- **메인 영역**: 입력 화면 / 분석 결과 대시보드

## Features
1. **데이터 입력**: 파일 업로드, URL 입력, 텍스트 붙여넣기
2. **맥락 기반 분석**: 사용자가 제공한 배경 정보 반영
3. **분석 결과 대시보드**:
   - 분석 맥락 카드
   - AI 요약 (핵심 포인트)
   - 주제별 분포 차트
   - 우선순위 개선 과제
   - 대표 의견 하이라이트

## Tech Stack
- Python 3.11
- Streamlit
- Pandas
- Plotly

## Running the App
```bash
streamlit run app.py --server.port 5000
```

## Demo Scenarios
- 텀블러 쇼핑몰 리뷰
- 패션 (여름 원피스) 리뷰
- K-POP 유튜브 댓글

## Recent Changes
- 2026-01-16: NotebookLM 스타일 UI/UX 적용
- 2026-01-16: 사이드바 네비게이션 추가
- 2026-01-16: 카드 기반 결과 레이아웃 구현
