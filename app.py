import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

st.set_page_config(
    page_title="올인원 인사이트 대시보드",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .empty-state {
        text-align: center;
        color: #999;
        font-size: 1.3rem;
        padding: 5rem 2rem;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 10px;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd6 0%, #6a4190 100%);
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

def get_urgency_color(urgency):
    colors = {
        "긴급": "#dc3545",
        "높음": "#fd7e14",
        "중간": "#ffc107",
        "낮음": "#28a745"
    }
    return colors.get(urgency, "#6c757d")

def simulate_loading():
    progress_messages = [
        "데이터 수집 중...",
        "게시물 본문 파악 중...",
        "댓글 맥락 분석 중...",
        "감정 분류 진행 중...",
        "주제별 분류 중...",
        "인사이트 도출 중...",
        "리포트 생성 중..."
    ]
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, msg in enumerate(progress_messages):
        status_text.text(msg)
        progress_bar.progress((i + 1) / len(progress_messages))
        time.sleep(0.3)
    
    status_text.empty()
    progress_bar.empty()

def display_dashboard(data, user_context=""):
    st.markdown("### 📋 분석 개요")
    context_text = f"**분석 대상:** {data['product_name']}"
    if user_context:
        context_text += f"\n\n**사용자 제공 맥락:** {user_context}"
    context_text += f"\n\n**AI 인식 맥락:** {data['context']}"
    
    st.info(context_text)
    
    st.markdown("---")
    
    st.markdown("### 🤖 AI 총평 요약")
    for i, summary in enumerate(data['summary'], 1):
        st.markdown(f"**{i}.** {summary}")
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 주제별 반응 점유율")
        
        topics_df = pd.DataFrame({
            '주제': list(data['topics'].keys()),
            '비율': list(data['topics'].values())
        })
        
        fig = px.pie(
            topics_df, 
            values='비율', 
            names='주제',
            color_discrete_sequence=px.colors.qualitative.Set2,
            hole=0.4
        )
        fig.update_traces(textposition='outside', textinfo='percent+label')
        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            margin=dict(t=20, b=80, l=20, r=20),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 우선순위 개선 과제")
        
        for priority in data['priorities']:
            urgency_color = get_urgency_color(priority['urgency'])
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid {urgency_color}; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong>{priority['task']}</strong>
                    <span style="background: {urgency_color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;">{priority['urgency']}</span>
                </div>
                <div style="color: #666; font-size: 0.85rem; margin-top: 0.5rem;">
                    언급 빈도: {priority['frequency']}회 | 영향도: {priority['impact']}/10
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 💬 대표 의견 하이라이트")
    
    positive_comments = [c for c in data['comments'] if c['sentiment'] == 'positive']
    negative_comments = [c for c in data['comments'] if c['sentiment'] == 'negative']
    
    positive_comments.sort(key=lambda x: x['likes'], reverse=True)
    negative_comments.sort(key=lambda x: x['likes'], reverse=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Best 리뷰")
        if positive_comments:
            best = positive_comments[0]
            st.success(f"""
            **"{best['text']}"**
            
            ---
            📁 주제: {best['topic']} | 👍 공감: {best['likes']:,}
            """)
    
    with col2:
        st.markdown("#### ⚠️ 개선 필요 리뷰")
        if negative_comments:
            worst = negative_comments[0]
            st.error(f"""
            **"{worst['text']}"**
            
            ---
            📁 주제: {worst['topic']} | 👍 공감: {worst['likes']:,}
            """)
    
    st.markdown("---")
    st.markdown("### 📝 전체 분석 댓글")
    
    comments_df = pd.DataFrame(data['comments'])
    comments_df['감정'] = comments_df['sentiment'].map({
        'positive': '긍정 😊',
        'negative': '부정 😞',
        'neutral': '중립 😐'
    })
    comments_df = comments_df.rename(columns={
        'text': '댓글 내용',
        'topic': '주제',
        'likes': '공감수'
    })
    
    st.dataframe(
        comments_df[['댓글 내용', '주제', '감정', '공감수']],
        use_container_width=True,
        hide_index=True
    )

def main():
    st.markdown('<h1 class="main-header">📊 올인원 인사이트 대시보드</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">비정형 텍스트 데이터를 AI가 분석하여 핵심 인사이트를 제공합니다</p>', unsafe_allow_html=True)
    
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
    if 'selected_data' not in st.session_state:
        st.session_state.selected_data = None
    if 'user_context' not in st.session_state:
        st.session_state.user_context = ""
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = "📥 데이터 입력"
    
    tab_options = ["📥 데이터 입력", "📈 분석 결과"]
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_tab = st.radio(
            "메뉴 선택",
            tab_options,
            index=tab_options.index(st.session_state.current_tab),
            horizontal=True,
            label_visibility="collapsed"
        )
    
    st.session_state.current_tab = selected_tab
    
    if selected_tab == "📥 데이터 입력":
        st.markdown("---")
        st.markdown("## 데이터 소스 입력")
        
        input_tab1, input_tab2, input_tab3, input_tab4 = st.tabs(["🔗 URL 입력", "📄 파일 업로드", "🖼️ 이미지 업로드", "📝 텍스트 붙여넣기"])
        
        with input_tab1:
            url_input = st.text_input(
                "분석할 페이지 URL을 입력하세요",
                placeholder="https://example.com/product/reviews",
                key="url_input"
            )
            st.caption("예: 쇼핑몰 상품 리뷰 페이지, 유튜브 영상 URL, 뉴스 기사 URL 등")
        
        with input_tab2:
            uploaded_file = st.file_uploader(
                "PDF 또는 DOCX 파일을 업로드하세요",
                type=['pdf', 'docx'],
                help="리뷰나 댓글이 포함된 문서 파일",
                key="file_upload"
            )
        
        with input_tab3:
            uploaded_image = st.file_uploader(
                "이미지 파일을 업로드하세요",
                type=['png', 'jpg', 'jpeg'],
                help="스크린샷이나 캡처 이미지 (OCR로 텍스트 추출)",
                key="image_upload"
            )
        
        with input_tab4:
            text_input = st.text_area(
                "분석할 텍스트를 직접 붙여넣으세요",
                height=150,
                placeholder="리뷰나 댓글을 여기에 붙여넣으세요...",
                key="text_input"
            )
        
        st.markdown("---")
        
        st.markdown("## 📌 게시물 추가 설명 (선택 사항)")
        user_context = st.text_area(
            "게시물에 대한 추가 설명이나 배경 상황을 적어주세요",
            placeholder="예: 이 제품은 최근 배송 지연 이슈가 있었습니다. / 이 영상은 컴백 후 첫 무대입니다.",
            height=100,
            key="user_context_input"
        )
        st.caption("💡 팁: 게시물의 내용을 요약하거나 유의해야 할 이슈를 적어주시면 분석 정확도가 올라갑니다.")
        
        st.markdown("---")
        
        st.markdown("## 🚀 분석 실행")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            use_demo = st.checkbox("더미 데이터로 예시 보기", value=True)
        
        with col2:
            if use_demo:
                demo_option = st.selectbox(
                    "데모 시나리오 선택",
                    options=["tumbler", "fashion", "youtube"],
                    format_func=lambda x: {
                        "tumbler": "🥤 텀블러 쇼핑몰 리뷰",
                        "fashion": "👗 여름 원피스 리뷰 (배송 이슈)",
                        "youtube": "🎵 K-POP MV 댓글"
                    }[x]
                )
            else:
                demo_option = "tumbler"
        
        if st.button("🔍 분석 시작하기 (Generate Analysis)", type="primary", use_container_width=True):
            has_input = url_input or uploaded_file or uploaded_image or text_input or use_demo
            
            if not has_input:
                st.warning("분석할 데이터를 입력하거나 더미 데이터 옵션을 선택해주세요.")
            else:
                simulate_loading()
                
                if use_demo:
                    st.session_state.selected_data = MOCK_DATA_SETS[demo_option]
                else:
                    st.session_state.selected_data = MOCK_DATA_SETS["tumbler"]
                
                st.session_state.user_context = user_context
                st.session_state.analysis_done = True
                st.session_state.current_tab = "📈 분석 결과"
                st.rerun()
    
    else:
        st.markdown("---")
        
        if st.session_state.analysis_done and st.session_state.selected_data:
            st.success("✅ 분석이 완료되었습니다!")
            
            display_dashboard(
                st.session_state.selected_data,
                st.session_state.user_context
            )
            
            st.markdown("---")
            if st.button("🔄 새로운 분석 시작하기", type="primary", use_container_width=True):
                st.session_state.analysis_done = False
                st.session_state.selected_data = None
                st.session_state.user_context = ""
                st.session_state.current_tab = "📥 데이터 입력"
                st.rerun()
        else:
            st.markdown("""
            <div class="empty-state">
                <p>분석할 내용을 입력해주세요</p>
                <p style="font-size: 0.9rem; margin-top: 1rem;">'데이터 입력' 탭에서 분석할 데이터를 입력하고 분석을 시작해주세요.</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
