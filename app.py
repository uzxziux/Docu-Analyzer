import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(
    page_title="인사이트 대시보드",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

ICONS = {
    "dashboard": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>',
    "document": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>',
    "upload": '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#5f6368" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>',
    "link": '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#5f6368" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',
    "lightbulb": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/></svg>',
    "target": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    "summary": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="17" y1="10" x2="3" y2="10"/><line x1="21" y1="6" x2="3" y2="6"/><line x1="21" y1="14" x2="3" y2="14"/><line x1="17" y1="18" x2="3" y2="18"/></svg>',
    "chart": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>',
    "alert": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
    "comment": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "check": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    "x": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
    "search": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
    "refresh": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>',
    "thumbsup": '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/></svg>',
    "list": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>',
    "cup": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 8h1a4 4 0 1 1 0 8h-1"/><path d="M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4Z"/><line x1="6" y1="2" x2="6" y2="4"/><line x1="10" y1="2" x2="10" y2="4"/><line x1="14" y1="2" x2="14" y2="4"/></svg>',
    "shirt": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20.38 3.46 16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"/></svg>',
    "music": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>',
    "empty": '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#9aa0a6" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>',
}

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
    
    .stApp {
        background-color: #f8f9fa;
    }
    
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        padding: 0.5rem 0;
    }
    
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1a1a1a;
        padding: 1rem 0;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .sidebar-section {
        font-size: 0.75rem;
        font-weight: 500;
        color: #5f6368;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 1.5rem 0 0.75rem 0;
    }
    
    .source-card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .source-card:hover {
        border-color: #1a73e8;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .source-card-title {
        font-size: 0.9rem;
        font-weight: 500;
        color: #1a1a1a;
        margin-bottom: 0.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .source-card-meta {
        font-size: 0.75rem;
        color: #5f6368;
        padding-left: 1.5rem;
    }
    
    .main-header {
        font-size: 1.75rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    
    .main-subheader {
        font-size: 0.95rem;
        color: #5f6368;
        margin-bottom: 2rem;
    }
    
    .upload-zone {
        background: #ffffff;
        border: 2px dashed #dadce0;
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        margin: 1rem 0;
        transition: all 0.2s ease;
    }
    
    .upload-zone:hover {
        border-color: #1a73e8;
        background: #f8fbff;
    }
    
    .upload-icon {
        margin-bottom: 1rem;
        display: flex;
        justify-content: center;
    }
    
    .upload-text {
        font-size: 1rem;
        color: #1a1a1a;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .upload-subtext {
        font-size: 0.85rem;
        color: #5f6368;
    }
    
    .result-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid #e8eaed;
    }
    
    .result-card-header {
        font-size: 1rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .icon-wrapper {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        color: #5f6368;
    }
    
    .insight-chip {
        display: inline-block;
        background: #f1f3f4;
        color: #3c4043;
        padding: 6px 12px;
        border-radius: 16px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid #e0e0e0;
    }
    
    .priority-high {
        background: #f1f3f4;
        border-color: #3c4043;
        color: #202124;
    }
    
    .priority-medium {
        background: #f8f9fa;
        border-color: #9aa0a6;
        color: #5f6368;
    }
    
    .priority-low {
        background: #fafafa;
        border-color: #dadce0;
        color: #80868b;
    }
    
    .summary-text {
        font-size: 0.95rem;
        line-height: 1.7;
        color: #3c4043;
    }
    
    .review-positive {
        background: #fafafa;
        border-left: 3px solid #3c4043;
        padding: 1rem 1.25rem;
        border-radius: 0 12px 12px 0;
        margin-bottom: 0.75rem;
    }
    
    .review-negative {
        background: #fafafa;
        border-left: 3px solid #9aa0a6;
        padding: 1rem 1.25rem;
        border-radius: 0 12px 12px 0;
        margin-bottom: 0.75rem;
    }
    
    .review-text {
        font-size: 0.9rem;
        color: #202124;
        font-style: italic;
        margin-bottom: 0.5rem;
    }
    
    .review-meta {
        font-size: 0.75rem;
        color: #5f6368;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        color: #80868b;
    }
    
    .empty-state-icon {
        margin-bottom: 1rem;
        display: flex;
        justify-content: center;
    }
    
    .empty-state-text {
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .empty-state-subtext {
        font-size: 0.9rem;
    }
    
    .stButton > button {
        background: #1a73e8;
        color: white;
        border: none;
        border-radius: 24px;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #1557b0;
        box-shadow: 0 2px 8px rgba(26,115,232,0.3);
    }
    
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #dadce0;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 1px solid #dadce0;
    }
    
    div[data-testid="stFileUploader"] {
        background: transparent;
    }
    
    .context-input-card {
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .context-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 500;
        color: #3c4043;
    }
    
    .section-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 500;
        color: #3c4043;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

MOCK_DATA_SETS = {
    "tumbler": {
        "product_name": "프리미엄 스테인리스 텀블러",
        "context": "20-30대 직장인 타겟의 프리미엄 텀블러 제품 리뷰",
        "topics": {
            "보온/보냉 성능": 35,
            "디자인/외관": 25,
            "세척 편의성": 20,
            "가격 대비 가치": 12,
            "배송/포장": 8
        },
        "comments": [
            {"text": "보온력이 정말 좋아요! 아침에 넣은 커피가 점심까지 따뜻해요.", "sentiment": "positive", "topic": "보온/보냉 성능", "likes": 234},
            {"text": "디자인이 깔끔하고 고급스러워서 회사에서 쓰기 좋아요.", "sentiment": "positive", "topic": "디자인/외관", "likes": 189},
            {"text": "뚜껑 틈새에 물때가 잘 끼어서 세척이 좀 불편해요.", "sentiment": "negative", "topic": "세척 편의성", "likes": 156},
            {"text": "가격이 좀 비싸긴 하지만 품질을 생각하면 괜찮은 것 같아요.", "sentiment": "neutral", "topic": "가격 대비 가치", "likes": 98},
            {"text": "배송은 빨랐는데 포장이 좀 부실해서 걱정됐어요.", "sentiment": "negative", "topic": "배송/포장", "likes": 87},
            {"text": "냉음료도 얼음이 6시간 넘게 안 녹아요. 대만족!", "sentiment": "positive", "topic": "보온/보냉 성능", "likes": 312},
            {"text": "뚜껑 분리가 안 돼서 세척이 정말 힘들어요. 개선 필요합니다.", "sentiment": "negative", "topic": "세척 편의성", "likes": 203},
        ],
        "summary": [
            "전반적으로 보온/보냉 성능에 대한 만족도가 매우 높으며, 특히 장시간 온도 유지력이 호평받고 있습니다.",
            "디자인과 품질에 대한 긍정적 반응이 많으나, 세척 편의성에 대한 개선 요구가 지속적으로 제기되고 있습니다.",
            "가격 대비 가치에 대해서는 의견이 나뉘며, 뚜껑 구조 개선이 시급한 과제로 도출되었습니다."
        ],
        "priorities": [
            {"task": "뚜껑 분리 구조 개선으로 세척 편의성 향상", "urgency": "높음", "frequency": 45, "impact": 8.5},
            {"task": "포장재 보강 및 배송 품질 관리", "urgency": "중간", "frequency": 23, "impact": 6.2},
            {"task": "가격 정책 또는 가성비 어필 마케팅 강화", "urgency": "낮음", "frequency": 18, "impact": 4.8},
        ]
    },
    "fashion": {
        "product_name": "여름 린넨 원피스",
        "context": "20대 여성 타겟의 여름 린넨 원피스 리뷰 (배송 지연 이슈 발생 중)",
        "topics": {
            "소재/착용감": 30,
            "사이즈/핏": 25,
            "배송": 22,
            "디자인": 15,
            "가격": 8
        },
        "comments": [
            {"text": "린넨 소재라 시원하고 가벼워요. 여름에 딱이에요!", "sentiment": "positive", "topic": "소재/착용감", "likes": 278},
            {"text": "배송이 2주나 걸렸어요. 여름 다 가겠어요...", "sentiment": "negative", "topic": "배송", "likes": 456},
            {"text": "평소 사이즈로 주문했는데 좀 크게 나와요. 한 사이즈 작게 추천!", "sentiment": "neutral", "topic": "사이즈/핏", "likes": 189},
            {"text": "사진이랑 실물이 똑같아요! 색감도 예쁘고 만족합니다.", "sentiment": "positive", "topic": "디자인", "likes": 234},
            {"text": "배송 문의했는데 답변이 너무 늦어요. 고객센터 개선 필요해요.", "sentiment": "negative", "topic": "배송", "likes": 312},
            {"text": "구김이 좀 잘 가는 게 아쉽지만 전체적으로 만족해요.", "sentiment": "neutral", "topic": "소재/착용감", "likes": 145},
            {"text": "이 가격에 이 퀄리티면 가성비 최고예요!", "sentiment": "positive", "topic": "가격", "likes": 198},
        ],
        "summary": [
            "린넨 소재의 시원한 착용감과 디자인에 대한 만족도는 높으나, 최근 배송 지연 이슈로 인한 불만이 급증하고 있습니다.",
            "사이즈 핏이 크게 나온다는 피드백이 다수 있어 사이즈 가이드 보완이 필요합니다.",
            "배송 및 고객센터 응대 속도 개선이 현재 가장 시급한 과제로 분석됩니다."
        ],
        "priorities": [
            {"task": "배송 프로세스 점검 및 물류 파트너 협의", "urgency": "긴급", "frequency": 89, "impact": 9.2},
            {"task": "고객센터 응대 인력 확충 및 응답 시간 단축", "urgency": "높음", "frequency": 67, "impact": 8.7},
            {"task": "사이즈 가이드 상세화 (실측 정보 추가)", "urgency": "중간", "frequency": 34, "impact": 6.5},
        ]
    },
    "youtube": {
        "product_name": "K-POP 아이돌 신곡 MV",
        "context": "인기 K-POP 그룹의 신곡 뮤직비디오 댓글 분석",
        "topics": {
            "음악/멜로디": 28,
            "안무/퍼포먼스": 25,
            "뮤직비디오/영상미": 22,
            "멤버별 반응": 15,
            "기타": 10
        },
        "comments": [
            {"text": "중독성 미쳤다ㅋㅋㅋ 벌써 100번 들었어요!", "sentiment": "positive", "topic": "음악/멜로디", "likes": 15234},
            {"text": "안무 누가 짰어요? 역대급인데?! 특히 2절 포인트 안무 최고", "sentiment": "positive", "topic": "안무/퍼포먼스", "likes": 12456},
            {"text": "뮤비 색감이랑 스토리라인 진짜 예술이다...", "sentiment": "positive", "topic": "뮤직비디오/영상미", "likes": 8934},
            {"text": "OO 파트가 너무 짧아요ㅠㅠ 다음엔 더 늘려주세요!", "sentiment": "negative", "topic": "멤버별 반응", "likes": 6721},
            {"text": "전작보다 멜로디가 좀 약한 것 같아요. 개인적인 의견입니다.", "sentiment": "negative", "topic": "음악/멜로디", "likes": 3421},
            {"text": "브릿지 부분에서 소름 돋았어요. 작곡가 천재인 듯", "sentiment": "positive", "topic": "음악/멜로디", "likes": 9876},
            {"text": "조명이랑 무대 세트 퀄리티가 영화급이네요", "sentiment": "positive", "topic": "뮤직비디오/영상미", "likes": 7654},
        ],
        "summary": [
            "신곡에 대한 반응은 전반적으로 매우 긍정적이며, 특히 음악의 중독성과 안무의 완성도에 대한 호평이 압도적입니다.",
            "뮤직비디오의 영상미와 스토리텔링에 대한 찬사가 이어지고 있으며, 팬덤의 열정적인 참여가 돋보입니다.",
            "일부 멤버의 파트 분배에 대한 아쉬움이 제기되고 있어, 향후 활동에서 고려가 필요합니다."
        ],
        "priorities": [
            {"task": "멤버별 파트 분배 균형 검토", "urgency": "중간", "frequency": 156, "impact": 7.2},
            {"task": "중독성 있는 훅 파트 더욱 강화", "urgency": "낮음", "frequency": 45, "impact": 5.8},
            {"task": "팬 소통 채널을 통한 피드백 수렴 강화", "urgency": "낮음", "frequency": 34, "impact": 5.2},
        ]
    }
}

def get_urgency_class(urgency):
    classes = {
        "긴급": "priority-high",
        "높음": "priority-high",
        "중간": "priority-medium",
        "낮음": "priority-low"
    }
    return classes.get(urgency, "priority-medium")

def simulate_loading():
    progress_messages = [
        "소스 분석 중...",
        "텍스트 추출 중...",
        "맥락 파악 중...",
        "감정 분류 중...",
        "주제 분류 중...",
        "인사이트 생성 중..."
    ]
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, msg in enumerate(progress_messages):
        status_text.text(msg)
        progress_bar.progress((i + 1) / len(progress_messages))
        time.sleep(0.25)
    
    status_text.empty()
    progress_bar.empty()

def render_sidebar():
    with st.sidebar:
        st.markdown(f'<div class="sidebar-title"><span class="icon-wrapper">{ICONS["dashboard"]}</span> 인사이트 대시보드</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section">소스</div>', unsafe_allow_html=True)
        
        if st.session_state.analysis_done and st.session_state.selected_data:
            st.markdown(f'''
            <div class="source-card">
                <div class="source-card-title"><span class="icon-wrapper">{ICONS["document"]}</span> {st.session_state.selected_data["product_name"]}</div>
                <div class="source-card-meta">분석 완료 · {len(st.session_state.selected_data["comments"])}개 댓글</div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown('''
            <div style="color: #80868b; font-size: 0.85rem; padding: 1rem 0;">
                소스를 추가하면 여기에 표시됩니다
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown('<div class="sidebar-section">설정</div>', unsafe_allow_html=True)
        
        use_demo = st.checkbox("데모 데이터 사용", value=True, key="demo_check")
        
        if use_demo:
            demo_option = st.selectbox(
                "시나리오 선택",
                options=["tumbler", "fashion", "youtube"],
                format_func=lambda x: {
                    "tumbler": "텀블러 리뷰",
                    "fashion": "패션 리뷰",
                    "youtube": "유튜브 댓글"
                }[x],
                key="demo_select"
            )
        else:
            demo_option = "tumbler"
        
        return use_demo, demo_option

def render_input_section():
    st.markdown('<h2 class="main-header">소스 추가하기</h2>', unsafe_allow_html=True)
    st.markdown('<p class="main-subheader">분석할 데이터를 업로드하거나 입력하세요</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'''
        <div class="upload-zone">
            <div class="upload-icon">{ICONS["upload"]}</div>
            <div class="upload-text">파일 업로드</div>
            <div class="upload-subtext">PDF, DOCX, 이미지 파일을 드래그하거나 클릭하세요</div>
        </div>
        ''', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "파일 선택",
            type=['pdf', 'docx', 'png', 'jpg', 'jpeg'],
            label_visibility="collapsed",
            key="file_upload"
        )
    
    with col2:
        st.markdown(f'''
        <div class="upload-zone">
            <div class="upload-icon">{ICONS["link"]}</div>
            <div class="upload-text">URL 입력</div>
            <div class="upload-subtext">웹페이지 URL을 입력하세요</div>
        </div>
        ''', unsafe_allow_html=True)
        
        url_input = st.text_input(
            "URL",
            placeholder="https://example.com/reviews",
            label_visibility="collapsed",
            key="url_input"
        )
    
    st.markdown("### 또는 텍스트 직접 입력")
    
    text_input = st.text_area(
        "텍스트",
        placeholder="분석할 리뷰나 댓글을 여기에 붙여넣으세요...",
        height=120,
        label_visibility="collapsed",
        key="text_input"
    )
    
    st.markdown(f'''
    <div class="context-input-card">
        <div class="context-header"><span class="icon-wrapper">{ICONS["lightbulb"]}</span> 분석 맥락 추가 (선택)</div>
        <p style="font-size: 0.85rem; color: #5f6368; margin-top: 0.5rem;">
            배경 정보나 특정 이슈를 입력하면 더 정확한 분석이 가능합니다.
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    user_context = st.text_area(
        "맥락",
        placeholder="예: 최근 배송 지연 이슈가 있었습니다...",
        height=80,
        label_visibility="collapsed",
        key="context_input"
    )
    
    return uploaded_file, url_input, text_input, user_context

def render_results(data, user_context=""):
    st.markdown(f'<h2 class="main-header">{data["product_name"]} 분석 결과</h2>', unsafe_allow_html=True)
    
    if user_context:
        st.markdown(f'<p class="main-subheader">맥락: {user_context}</p>', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="result-card">
        <div class="result-card-header"><span class="icon-wrapper">{ICONS["target"]}</span> 분석 맥락</div>
        <p class="summary-text">{data["context"]}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="result-card">
        <div class="result-card-header"><span class="icon-wrapper">{ICONS["summary"]}</span> AI 요약</div>
    ''', unsafe_allow_html=True)
    
    for summary in data['summary']:
        st.markdown(f'<p class="summary-text">• {summary}</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'''
        <div class="result-card">
            <div class="result-card-header"><span class="icon-wrapper">{ICONS["chart"]}</span> 주제별 분포</div>
        </div>
        ''', unsafe_allow_html=True)
        
        topics_df = pd.DataFrame({
            '주제': list(data['topics'].keys()),
            '비율': list(data['topics'].values())
        })
        
        fig = px.pie(
            topics_df, 
            values='비율', 
            names='주제',
            color_discrete_sequence=['#202124', '#5f6368', '#9aa0a6', '#bdc1c6', '#dadce0'],
            hole=0.4
        )
        fig.update_traces(textposition='outside', textinfo='percent+label')
        fig.update_layout(
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20),
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f'''
        <div class="result-card">
            <div class="result-card-header"><span class="icon-wrapper">{ICONS["alert"]}</span> 개선 과제</div>
        </div>
        ''', unsafe_allow_html=True)
        
        for priority in data['priorities']:
            urgency_class = get_urgency_class(priority['urgency'])
            st.markdown(f'''
            <div style="margin-bottom: 0.75rem;">
                <span class="insight-chip {urgency_class}">{priority['urgency']}</span>
                <span style="font-size: 0.9rem; color: #202124;">{priority['task']}</span>
                <div style="font-size: 0.75rem; color: #5f6368; margin-top: 0.25rem;">
                    언급 {priority['frequency']}회 · 영향도 {priority['impact']}/10
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="result-card">
        <div class="result-card-header"><span class="icon-wrapper">{ICONS["comment"]}</span> 대표 의견</div>
    </div>
    ''', unsafe_allow_html=True)
    
    positive_comments = sorted([c for c in data['comments'] if c['sentiment'] == 'positive'], key=lambda x: x['likes'], reverse=True)
    negative_comments = sorted([c for c in data['comments'] if c['sentiment'] == 'negative'], key=lambda x: x['likes'], reverse=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'<div class="section-label"><span class="icon-wrapper">{ICONS["check"]}</span> 긍정 리뷰</div>', unsafe_allow_html=True)
        if positive_comments:
            best = positive_comments[0]
            st.markdown(f'''
            <div class="review-positive">
                <div class="review-text">"{best['text']}"</div>
                <div class="review-meta">{best['topic']} · <span class="icon-wrapper">{ICONS["thumbsup"]}</span> {best['likes']:,}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="section-label"><span class="icon-wrapper">{ICONS["x"]}</span> 개선 필요 리뷰</div>', unsafe_allow_html=True)
        if negative_comments:
            worst = negative_comments[0]
            st.markdown(f'''
            <div class="review-negative">
                <div class="review-text">"{worst['text']}"</div>
                <div class="review-meta">{worst['topic']} · <span class="icon-wrapper">{ICONS["thumbsup"]}</span> {worst['likes']:,}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    with st.expander("전체 댓글 보기"):
        comments_df = pd.DataFrame(data['comments'])
        comments_df['감정'] = comments_df['sentiment'].map({
            'positive': '긍정',
            'negative': '부정',
            'neutral': '중립'
        })
        comments_df = comments_df.rename(columns={
            'text': '댓글',
            'topic': '주제',
            'likes': '공감'
        })
        st.dataframe(
            comments_df[['댓글', '주제', '감정', '공감']],
            use_container_width=True,
            hide_index=True
        )

def render_empty_state():
    st.markdown(f'''
    <div class="empty-state">
        <div class="empty-state-icon">{ICONS["empty"]}</div>
        <div class="empty-state-text">분석 결과가 없습니다</div>
        <div class="empty-state-subtext">소스를 추가하고 분석을 시작해주세요</div>
    </div>
    ''', unsafe_allow_html=True)

def main():
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
    if 'selected_data' not in st.session_state:
        st.session_state.selected_data = None
    if 'user_context' not in st.session_state:
        st.session_state.user_context = ""
    if 'current_view' not in st.session_state:
        st.session_state.current_view = "input"
    
    use_demo, demo_option = render_sidebar()
    
    if st.session_state.current_view == "input" or not st.session_state.analysis_done:
        uploaded_file, url_input, text_input, user_context = render_input_section()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("분석 시작", type="primary", use_container_width=True):
                has_input = uploaded_file or url_input or text_input or use_demo
                
                if not has_input:
                    st.warning("분석할 데이터를 입력하거나 데모 데이터를 선택해주세요.")
                else:
                    simulate_loading()
                    
                    if use_demo:
                        st.session_state.selected_data = MOCK_DATA_SETS[demo_option]
                    else:
                        st.session_state.selected_data = MOCK_DATA_SETS["tumbler"]
                    
                    st.session_state.user_context = user_context
                    st.session_state.analysis_done = True
                    st.session_state.current_view = "results"
                    st.rerun()
    
    else:
        if st.session_state.selected_data:
            render_results(st.session_state.selected_data, st.session_state.user_context)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("새로운 분석", type="primary", use_container_width=True):
                    st.session_state.analysis_done = False
                    st.session_state.selected_data = None
                    st.session_state.user_context = ""
                    st.session_state.current_view = "input"
                    st.rerun()
        else:
            render_empty_state()

if __name__ == "__main__":
    main()
