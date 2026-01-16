# 올인원 인사이트 대시보드

## Overview
비정형 텍스트 데이터(댓글, 리뷰 등)를 분석하여 핵심 인사이트를 제공하는 PoC(Proof of Concept) 웹 애플리케이션입니다.

## Project Structure
- `app.py` - Streamlit 메인 애플리케이션
- `.streamlit/config.toml` - Streamlit 서버 설정

## Features
1. **데이터 입력**: URL, 파일(PDF/DOCX), 이미지, 텍스트 붙여넣기 지원
2. **맥락 기반 분석**: 사용자가 제공한 추가 설명을 분석에 반영
3. **분석 결과 대시보드**:
   - 분석 개요 (Context Overview)
   - AI 총평 요약 (3줄 요약)
   - 주제별 점유율 (Plotly 원형 차트)
   - 우선순위 개선 과제
   - 대표 의견 하이라이트 (Best/Worst 리뷰)

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
- 여름 원피스 리뷰 (배송 이슈 상황)
- K-POP MV 댓글 분석

## Recent Changes
- 2026-01-16: 초기 PoC 구현 완료
