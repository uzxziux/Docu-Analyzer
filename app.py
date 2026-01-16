import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import re

st.set_page_config(
    page_title="OpiniQ - 인사이트 대시보드",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

PROFANITY_REPLACEMENTS = {
    "시발": "정말",
    "씨발": "정말",
    "ㅅㅂ": "정말",
    "ㅆㅂ": "정말",
    "병신": "문제가 있는",
    "ㅂㅅ": "문제가 있는",
    "지랄": "난리",
    "ㅈㄹ": "난리",
    "개새끼": "나쁜 사람",
    "새끼": "사람",
    "ㅅㄲ": "사람",
    "미친": "믿기 힘든",
    "존나": "정말",
    "ㅈㄴ": "정말",
    "꺼져": "그만해요",
    "닥쳐": "조용히 해요",
    "죽어": "싫어요",
    "뒤져": "싫어요",
    "썅": "아이고",
    "좆": "정말",
    "ㅈ같": "별로",
    "씹": "정말",
}

def filter_profanity(text):
    """Filter profanity and contextualize with appropriate replacement"""
    modified = False
    filtered_text = text
    for word, replacement in PROFANITY_REPLACEMENTS.items():
        if word in filtered_text:
            filtered_text = filtered_text.replace(word, replacement)
            modified = True
    return filtered_text, modified

ICONS = {
    "logo": '<svg width="28" height="28" viewBox="0 0 24 24" fill="none"><text x="4" y="18" font-family="Inter, sans-serif" font-size="18" font-weight="700" fill="url(#logoGrad)">Q</text><defs><linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#6366f1"/><stop offset="100%" style="stop-color:#8b5cf6"/></linearGradient></defs></svg>',
    "history": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#5f6368" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "document": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#5f6368" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
    "plus": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
    "upload": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#5f6368" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>',
    "link": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#5f6368" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',
    "text": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#5f6368" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 7 4 4 20 4 20 7"/><line x1="9" y1="20" x2="15" y2="20"/><line x1="12" y1="4" x2="12" y2="20"/></svg>',
    "image": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#5f6368" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>',
    "context": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#5f6368" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "lightbulb": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/></svg>',
    "summary": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="17" y1="10" x2="3" y2="10"/><line x1="21" y1="6" x2="3" y2="6"/><line x1="21" y1="14" x2="3" y2="14"/><line x1="17" y1="18" x2="3" y2="18"/></svg>',
    "chart": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>',
    "sentiment": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>',
    "alert": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "comment": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "thumbsup": '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#5f6368" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/></svg>',
    "check": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    "x": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
    "test": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#5f6368" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
    "empty": '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#dadce0" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>',
    "signal_red": '<svg width="14" height="14" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#ef4444"/></svg>',
    "signal_yellow": '<svg width="14" height="14" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#f59e0b"/></svg>',
    "signal_green": '<svg width="14" height="14" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#10b981"/></svg>',
    "detail": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>',
    "chevron_down": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#5f6368" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>',
    "chevron_up": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#5f6368" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"/></svg>',
    "chevron_right": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#5f6368" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>',
    "priority": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
    "more": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>',
}

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background-color: #f5f5f5;
    }
    
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e5e5;
    }
    
    .brand-header {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 0.75rem 0 1.5rem 0;
        border-bottom: 1px solid #e5e5e5;
        margin-bottom: 1rem;
    }
    
    .brand-logo {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .brand-name {
        font-size: 1.25rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .brand-tagline {
        font-size: 0.7rem;
        color: #9ca3af;
        margin-top: 2px;
    }
    
    .main-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 0.5rem;
    }
    
    .main-brand-name {
        font-size: 1.75rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .sidebar-section {
        font-size: 0.7rem;
        font-weight: 600;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 1.25rem 0 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .history-card {
        background: #f9fafb;
        border: 1px solid #e5e5e5;
        border-radius: 10px;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.15s ease;
    }
    
    .history-card:hover {
        background: #f3f4f6;
        border-color: #d1d5db;
    }
    
    .history-card-title {
        font-size: 0.85rem;
        font-weight: 500;
        color: #374151;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .history-card-meta {
        font-size: 0.7rem;
        color: #9ca3af;
        margin-top: 0.25rem;
        padding-left: 1.5rem;
    }
    
    .main-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.25rem;
    }
    
    .main-subheader {
        font-size: 0.9rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
    }
    
    .drop-zone {
        background: #ffffff;
        border: 2px dashed #d1d5db;
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        margin: 1rem 0;
        transition: all 0.2s ease;
    }
    
    .drop-zone:hover {
        border-color: #9ca3af;
        background: #fafafa;
    }
    
    .drop-zone-text {
        font-size: 1rem;
        color: #374151;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .drop-zone-subtext {
        font-size: 0.85rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
    }
    
    .source-buttons {
        display: flex;
        justify-content: center;
        gap: 0.75rem;
        flex-wrap: wrap;
    }
    
    .source-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: #ffffff;
        border: 1px solid #e5e5e5;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        font-size: 0.8rem;
        font-weight: 500;
        color: #4b5563;
        cursor: pointer;
        transition: all 0.15s ease;
    }
    
    .source-btn:hover {
        background: #f9fafb;
        border-color: #d1d5db;
    }
    
    .source-btn.active {
        background: #f3f4f6;
        border-color: #9ca3af;
        color: #374151;
    }
    
    .result-section {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .result-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    
    .result-card-header {
        font-size: 1rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #f3f4f6;
    }
    
    .result-card-content {
        background: #ffffff;
        padding: 0;
    }
    
    .icon-wrapper {
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    
    .insight-chip {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.75rem;
    }
    
    .priority-high {
        background: #fef2f2;
        color: #dc2626;
    }
    
    .priority-medium {
        background: #fffbeb;
        color: #d97706;
    }
    
    .priority-low {
        background: #ecfdf5;
        color: #059669;
    }
    
    .summary-text {
        font-size: 0.9rem;
        line-height: 1.8;
        color: #4b5563;
        padding: 0.25rem 0;
    }
    
    .review-card {
        background: #f9fafb;
        border-left: 3px solid #e5e5e5;
        padding: 1rem 1.25rem;
        border-radius: 0 10px 10px 0;
        margin-bottom: 0.75rem;
    }
    
    .review-positive {
        border-left-color: #10b981;
        background: #ecfdf5;
    }
    
    .review-negative {
        border-left-color: #ef4444;
        background: #fef2f2;
    }
    
    .review-text {
        font-size: 0.9rem;
        color: #1f2937;
        font-style: italic;
        margin-bottom: 0.5rem;
        line-height: 1.6;
    }
    
    .review-meta {
        font-size: 0.75rem;
        color: #6b7280;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        color: #9ca3af;
    }
    
    .empty-state-icon {
        margin-bottom: 1rem;
        display: flex;
        justify-content: center;
    }
    
    .empty-state-text {
        font-size: 1rem;
        color: #6b7280;
        margin-bottom: 0.5rem;
    }
    
    .stButton > button {
        background: #374151;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1.25rem;
        font-weight: 500;
        font-size: 0.85rem;
        transition: all 0.15s ease;
        width: auto !important;
    }
    
    .stButton > button:hover {
        background: #1f2937;
    }
    
    .stButton > button[kind="primary"] {
        background: #374151;
    }
    
    .stButton > button[kind="secondary"] {
        background: #f3f4f6;
        color: #374151;
        border: 1px solid #e5e5e5;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #e5e5e5;
    }
    
    .start-btn-wrapper {
        display: flex;
        justify-content: center;
        width: 100%;
        margin: 1.5rem 0;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 1px solid #e5e5e5;
        font-size: 0.9rem;
    }
    
    div[data-testid="stFileUploader"] {
        background: transparent;
    }
    
    div[data-testid="stFileUploader"] section {
        padding: 0;
    }
    
    div[data-testid="stFileUploader"] section > div {
        padding: 0.5rem;
    }
    
    .section-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        font-size: 0.85rem;
        color: #4b5563;
        margin-bottom: 0.75rem;
    }
    
    .task-item {
        padding: 0.875rem 0;
        border-bottom: 1px solid #f3f4f6;
    }
    
    .task-item:last-child {
        border-bottom: none;
    }
    
    .task-title {
        font-size: 0.9rem;
        color: #1f2937;
        margin-bottom: 0.25rem;
        display: flex;
        align-items: flex-start;
    }
    
    .task-desc {
        font-size: 0.8rem;
        color: #6b7280;
        line-height: 1.5;
        margin-top: 0.25rem;
        padding-left: 4.5rem;
    }
    
    .task-meta {
        font-size: 0.75rem;
        color: #9ca3af;
        margin-top: 0.25rem;
        padding-left: 4.5rem;
    }
    
    .alert-card {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.875rem 1.25rem;
        border-radius: 12px;
        margin-bottom: 1.25rem;
    }
    
    .alert-red {
        background: #fef2f2;
        border: 1px solid #fecaca;
    }
    
    .alert-yellow {
        background: #fffbeb;
        border: 1px solid #fde68a;
    }
    
    .alert-green {
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
    }
    
    .alert-text {
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .alert-red .alert-text { color: #dc2626; }
    .alert-yellow .alert-text { color: #d97706; }
    .alert-green .alert-text { color: #059669; }
    
    .topic-table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .topic-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.875rem 1rem;
        background: #f9fafb;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.15s ease;
    }
    
    .topic-header:hover {
        background: #f3f4f6;
    }
    
    .topic-header.active {
        background: #f3f4f6;
        border-color: #d1d5db;
    }
    
    .topic-name {
        font-size: 0.9rem;
        font-weight: 500;
        color: #374151;
    }
    
    .topic-ratio {
        font-size: 0.85rem;
        font-weight: 600;
        color: #6b7280;
    }
    
    .micro-view {
        background: #ffffff;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .micro-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .sub-topic-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.625rem 0;
        border-bottom: 1px solid #f3f4f6;
    }
    
    .sub-topic-item:last-child {
        border-bottom: none;
    }
    
    .sub-topic-name {
        font-size: 0.85rem;
        font-weight: 500;
        color: #374151;
    }
    
    .sub-topic-sample {
        font-size: 0.75rem;
        color: #6b7280;
        font-style: italic;
        margin-top: 0.25rem;
    }
    
    .sub-topic-bar {
        width: 100px;
        height: 6px;
        background: #e5e5e5;
        border-radius: 3px;
        overflow: hidden;
    }
    
    .sub-topic-fill {
        height: 100%;
        background: #3b82f6;
        border-radius: 3px;
    }
    
    .modified-badge {
        background: #dbeafe;
        color: #2563eb;
        font-size: 0.7rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 4px;
        margin-left: 0.5rem;
    }
    
    div[data-testid="stExpander"] {
        border: 1px solid #e5e5e5;
        border-radius: 10px;
        background: #ffffff;
    }
    
    div[data-testid="stExpander"] summary {
        font-weight: 600;
        color: #374151;
    }
    
    .input-section {
        background: #ffffff;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    
    .input-section-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
        font-weight: 500;
        color: #374151;
        margin-bottom: 0.75rem;
        cursor: pointer;
    }
    
    .context-input {
        background: #f9fafb;
        border: 1px solid #e5e5e5;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
    }
    
    .context-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.85rem;
        font-weight: 500;
        color: #4b5563;
        margin-bottom: 0.5rem;
    }
    
    .more-btn {
        background: #f3f4f6;
        color: #374151;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 0.8rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.15s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        justify-content: center;
        width: 100%;
    }
    
    .more-btn:hover {
        background: #e5e5e5;
    }
    
    .new-analysis-btn {
        background: #374151;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-size: 0.85rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.15s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        justify-content: center;
        width: 100%;
    }
    
    .new-analysis-btn:hover {
        background: #1f2937;
    }
</style>
""", unsafe_allow_html=True)

MOCK_DATA_SETS = {
    "tumbler": {
        "product_name": "프리미엄 스테인리스 텀블러",
        "topics": {
            "보온/보냉 성능": 35,
            "디자인/외관": 25,
            "세척 편의성": 20,
            "가격 대비 가치": 12,
            "배송/포장": 8
        },
        "topic_details": {
            "보온/보냉 성능": {
                "subtopics": [
                    {"name": "온도 유지력", "ratio": 40, "sample": "6시간 지나도 따뜻해요"},
                    {"name": "보냉 성능", "ratio": 30, "sample": "얼음이 안 녹아요"},
                    {"name": "뚜껑 밀폐력", "ratio": 15, "sample": "새지 않아서 좋아요"},
                    {"name": "단열 구조", "ratio": 10, "sample": "이중 구조가 좋아요"},
                    {"name": "온도 표시", "ratio": 5, "sample": "온도계가 있으면 좋겠어요"},
                ]
            },
            "디자인/외관": {
                "subtopics": [
                    {"name": "색상 만족도", "ratio": 35, "sample": "색깔이 고급스러워요"},
                    {"name": "크기/휴대성", "ratio": 30, "sample": "가방에 쏙 들어가요"},
                    {"name": "로고/마감", "ratio": 20, "sample": "마감 처리가 깔끔해요"},
                    {"name": "무게감", "ratio": 10, "sample": "적당히 가벼워요"},
                    {"name": "그립감", "ratio": 5, "sample": "손에 잘 잡혀요"},
                ]
            },
            "세척 편의성": {
                "subtopics": [
                    {"name": "뚜껑 분리", "ratio": 40, "sample": "뚜껑이 분리가 안돼요"},
                    {"name": "내부 세척", "ratio": 30, "sample": "손이 안 들어가요"},
                    {"name": "물때/냄새", "ratio": 15, "sample": "물때가 잘 껴요"},
                    {"name": "세척 도구", "ratio": 10, "sample": "브러시가 필요해요"},
                    {"name": "건조 용이성", "ratio": 5, "sample": "건조가 오래 걸려요"},
                ]
            },
            "가격 대비 가치": {
                "subtopics": [
                    {"name": "품질 만족", "ratio": 50, "sample": "비싸지만 품질이 좋아요"},
                    {"name": "가격 부담", "ratio": 30, "sample": "좀 비싼 것 같아요"},
                    {"name": "내구성", "ratio": 15, "sample": "오래 쓸 수 있을 것 같아요"},
                    {"name": "AS 정책", "ratio": 5, "sample": "AS가 잘 되면 좋겠어요"},
                ]
            },
            "배송/포장": {
                "subtopics": [
                    {"name": "배송 속도", "ratio": 45, "sample": "배송이 빨랐어요"},
                    {"name": "포장 상태", "ratio": 35, "sample": "포장이 좀 부실해요"},
                    {"name": "박스 디자인", "ratio": 15, "sample": "선물용으로 좋아요"},
                    {"name": "구성품", "ratio": 5, "sample": "스트랩이 있으면 좋겠어요"},
                ]
            },
            "기타": {
                "subtopics": [
                    {"name": "사용 후기", "ratio": 40, "sample": "전반적으로 만족해요"},
                    {"name": "재구매 의향", "ratio": 35, "sample": "다시 살 것 같아요"},
                    {"name": "선물 추천", "ratio": 25, "sample": "선물하기 좋아요"},
                ]
            },
        },
        "urgent_issue": {"level": "green", "message": "현재 특별한 이슈가 없습니다"},
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
            {"task": "뚜껑 분리 구조 개선", "desc": "현재 뚜껑이 일체형으로 되어 있어 내부 세척이 어렵습니다. 분리 가능한 구조로 변경하여 물때와 냄새 문제를 해결하고 고객 만족도를 높일 수 있습니다.", "urgency": "높음", "frequency": 45, "impact": 8.5},
            {"task": "포장재 보강 및 품질 관리", "desc": "배송 중 제품 손상 우려가 있다는 피드백이 있습니다. 완충재를 추가하고 포장 박스를 강화하여 제품 보호와 개봉 경험을 개선해야 합니다.", "urgency": "중간", "frequency": 23, "impact": 6.2},
            {"task": "가격 정책 및 마케팅 강화", "desc": "가격 대비 가치에 대한 인식이 다양합니다. 품질 대비 적정 가격임을 알리는 마케팅과 함께 할인 이벤트를 통해 진입 장벽을 낮추는 것을 권장합니다.", "urgency": "낮음", "frequency": 18, "impact": 4.8},
        ]
    },
    "fashion": {
        "product_name": "여름 린넨 원피스",
        "topics": {
            "소재/착용감": 30,
            "사이즈/핏": 25,
            "배송": 22,
            "디자인": 15,
            "가격": 8
        },
        "topic_details": {
            "소재/착용감": {
                "subtopics": [
                    {"name": "시원함", "ratio": 35, "sample": "린넨이라 시원해요"},
                    {"name": "구김", "ratio": 25, "sample": "구김이 잘 가요"},
                    {"name": "촉감", "ratio": 20, "sample": "부드러워요"},
                    {"name": "통기성", "ratio": 12, "sample": "바람이 잘 통해요"},
                    {"name": "두께감", "ratio": 8, "sample": "적당한 두께예요"},
                ]
            },
            "사이즈/핏": {
                "subtopics": [
                    {"name": "사이즈 정확도", "ratio": 40, "sample": "크게 나와요"},
                    {"name": "핏/실루엣", "ratio": 30, "sample": "라인이 예뻐요"},
                    {"name": "기장", "ratio": 18, "sample": "기장이 적당해요"},
                    {"name": "어깨선", "ratio": 12, "sample": "어깨가 넓어요"},
                ]
            },
            "배송": {
                "subtopics": [
                    {"name": "배송 지연", "ratio": 50, "sample": "2주나 걸렸어요"},
                    {"name": "고객센터 응대", "ratio": 25, "sample": "답변이 늦어요"},
                    {"name": "배송 추적", "ratio": 15, "sample": "추적이 안 돼요"},
                    {"name": "포장 상태", "ratio": 10, "sample": "구겨져 왔어요"},
                ]
            },
            "디자인": {
                "subtopics": [
                    {"name": "색상", "ratio": 40, "sample": "색감이 예뻐요"},
                    {"name": "스타일", "ratio": 35, "sample": "사진이랑 똑같아요"},
                    {"name": "디테일", "ratio": 15, "sample": "단추가 예뻐요"},
                    {"name": "트렌드", "ratio": 10, "sample": "올해 트렌드에요"},
                ]
            },
            "가격": {
                "subtopics": [
                    {"name": "가성비", "ratio": 60, "sample": "이 가격에 최고예요"},
                    {"name": "할인 혜택", "ratio": 25, "sample": "쿠폰 적용됐어요"},
                    {"name": "가격 인상", "ratio": 15, "sample": "가격이 올랐어요"},
                ]
            },
            "기타": {
                "subtopics": [
                    {"name": "세탁 방법", "ratio": 40, "sample": "드라이클리닝 해야 해요"},
                    {"name": "코디 추천", "ratio": 35, "sample": "어디에나 잘 어울려요"},
                    {"name": "재구매 의향", "ratio": 25, "sample": "다른 색도 살 거예요"},
                ]
            },
        },
        "urgent_issue": {"level": "red", "message": "지금 '배송 지연' 관련 불만 급증!"},
        "comments": [
            {"text": "린넨 소재라 시원하고 가벼워요. 여름에 딱이에요!", "sentiment": "positive", "topic": "소재/착용감", "likes": 278},
            {"text": "배송이 2주나 걸렸어요. 여름 다 가겠어요... 정말 늦어요 진짜", "sentiment": "negative", "topic": "배송", "likes": 456},
            {"text": "평소 사이즈로 주문했는데 좀 크게 나와요. 한 사이즈 작게 추천!", "sentiment": "neutral", "topic": "사이즈/핏", "likes": 189},
            {"text": "사진이랑 실물이 똑같아요! 색감도 예쁘고 만족합니다.", "sentiment": "positive", "topic": "디자인", "likes": 234},
            {"text": "배송 문의했는데 답변이 너무 늦어요. 고객센터 개선 필요해요.", "sentiment": "negative", "topic": "배송", "likes": 312},
            {"text": "구김이 좀 잘 가는 게 아쉽지만 전체적으로 만족해요.", "sentiment": "neutral", "topic": "소재/착용감", "likes": 145},
            {"text": "이 가격에 이 퀄리티면 가성비 최고예요!", "sentiment": "positive", "topic": "가격", "likes": 198},
            {"text": "ㅅㅂ 배송 왜이리 느려요 답답해 죽겠네", "sentiment": "negative", "topic": "배송", "likes": 89},
        ],
        "summary": [
            "린넨 소재의 시원한 착용감과 디자인에 대한 만족도는 높으나, 최근 배송 지연 이슈로 인한 불만이 급증하고 있습니다.",
            "사이즈 핏이 크게 나온다는 피드백이 다수 있어 사이즈 가이드 보완이 필요합니다.",
            "배송 및 고객센터 응대 속도 개선이 현재 가장 시급한 과제로 분석됩니다."
        ],
        "priorities": [
            {"task": "배송 프로세스 점검 및 개선", "desc": "현재 평균 배송 기간이 2주 이상 소요되어 고객 불만이 급증하고 있습니다. 물류 파트너사와 협의하여 배송 시간을 단축하고, 예상 배송일을 정확히 안내해야 합니다.", "urgency": "긴급", "frequency": 89, "impact": 9.2},
            {"task": "고객센터 응대 품질 향상", "desc": "문의 응답 시간이 길어 고객 이탈이 발생하고 있습니다. 상담 인력을 확충하고, 자주 묻는 질문에 대한 자동 응답 시스템을 도입하여 응답 시간을 24시간 이내로 단축해야 합니다.", "urgency": "높음", "frequency": 67, "impact": 8.7},
            {"task": "사이즈 가이드 상세화", "desc": "고객들이 평소 사이즈로 주문 시 크게 느낀다는 피드백이 많습니다. 실측 정보와 함께 체형별 추천 사이즈를 상품 페이지에 추가하여 교환/반품률을 낮춰야 합니다.", "urgency": "중간", "frequency": 34, "impact": 6.5},
        ]
    },
    "youtube": {
        "product_name": "K-POP 아이돌 신곡 MV",
        "topics": {
            "음악/멜로디": 28,
            "안무/퍼포먼스": 25,
            "뮤직비디오/영상미": 22,
            "멤버별 반응": 15,
            "기타": 10
        },
        "topic_details": {
            "음악/멜로디": {
                "subtopics": [
                    {"name": "중독성/훅", "ratio": 30, "sample": "중독성 미쳤어요"},
                    {"name": "보컬 파트", "ratio": 25, "sample": "고음이 대박이에요"},
                    {"name": "랩 파트", "ratio": 20, "sample": "랩이 찢었어요"},
                    {"name": "브릿지 구간", "ratio": 15, "sample": "브릿지에서 소름"},
                    {"name": "프로듀싱", "ratio": 10, "sample": "프로듀서 천재"},
                ]
            },
            "안무/퍼포먼스": {
                "subtopics": [
                    {"name": "안무 퀄리티", "ratio": 35, "sample": "안무가 역대급이에요"},
                    {"name": "안무 실력", "ratio": 25, "sample": "칼군무 미쳤어요"},
                    {"name": "포인트 동작", "ratio": 20, "sample": "2절 안무 최고"},
                    {"name": "무대 구성", "ratio": 12, "sample": "포메이션이 예술"},
                    {"name": "표정 연기", "ratio": 8, "sample": "표정이 살아있어요"},
                ]
            },
            "뮤직비디오/영상미": {
                "subtopics": [
                    {"name": "색감/색보정", "ratio": 30, "sample": "색감이 예술이에요"},
                    {"name": "스토리라인", "ratio": 25, "sample": "스토리가 있어요"},
                    {"name": "세트/의상", "ratio": 20, "sample": "의상이 너무 예뻐요"},
                    {"name": "CG/특수효과", "ratio": 15, "sample": "CG가 대박이에요"},
                    {"name": "촬영 기법", "ratio": 10, "sample": "카메라워크 미쳤다"},
                ]
            },
            "멤버별 반응": {
                "subtopics": [
                    {"name": "파트 분배", "ratio": 45, "sample": "OO 파트가 짧아요"},
                    {"name": "개인 활약", "ratio": 30, "sample": "OO 미모 실화?"},
                    {"name": "성장 칭찬", "ratio": 15, "sample": "많이 늘었어요"},
                    {"name": "케미스트리", "ratio": 10, "sample": "케미가 좋아요"},
                ]
            },
            "기타": {
                "subtopics": [
                    {"name": "팬덤 반응", "ratio": 35, "sample": "1억뷰 가즈아"},
                    {"name": "컴백 축하", "ratio": 30, "sample": "컴백 축하해요"},
                    {"name": "앨범 구매", "ratio": 20, "sample": "앨범 샀어요"},
                    {"name": "콘서트 기대", "ratio": 15, "sample": "콘서트 언제해요"},
                ]
            },
        },
        "urgent_issue": {"level": "yellow", "message": "멤버 파트 분배 관련 의견 증가 중"},
        "comments": [
            {"text": "중독성 미쳤다ㅋㅋㅋ 벌써 100번 들었어요!", "sentiment": "positive", "topic": "음악/멜로디", "likes": 15234},
            {"text": "안무 누가 짰어요? 역대급인데?! 특히 2절 포인트 안무 최고", "sentiment": "positive", "topic": "안무/퍼포먼스", "likes": 12456},
            {"text": "뮤비 색감이랑 스토리라인 진짜 예술이다...", "sentiment": "positive", "topic": "뮤직비디오/영상미", "likes": 8934},
            {"text": "OO 파트가 너무 짧아요ㅠㅠ 다음엔 더 늘려주세요!", "sentiment": "negative", "topic": "멤버별 반응", "likes": 6721},
            {"text": "전작보다 멜로디가 좀 약한 것 같아요. 개인적인 의견입니다.", "sentiment": "negative", "topic": "음악/멜로디", "likes": 3421},
            {"text": "브릿지 부분에서 소름 돋았어요. 작곡가 천재인 듯", "sentiment": "positive", "topic": "음악/멜로디", "likes": 9876},
            {"text": "조명이랑 무대 세트 퀄리티가 영화급이네요", "sentiment": "positive", "topic": "뮤직비디오/영상미", "likes": 7654},
            {"text": "ㅈㄴ 좋아 미친거 아니야? 최고다 진짜", "sentiment": "positive", "topic": "기타", "likes": 5432},
        ],
        "summary": [
            "신곡에 대한 반응은 전반적으로 매우 긍정적이며, 특히 음악의 중독성과 안무의 완성도에 대한 호평이 압도적입니다.",
            "뮤직비디오의 영상미와 스토리텔링에 대한 찬사가 이어지고 있으며, 팬덤의 열정적인 참여가 돋보입니다.",
            "일부 멤버의 파트 분배에 대한 아쉬움이 제기되고 있어, 향후 활동에서 고려가 필요합니다."
        ],
        "priorities": [
            {"task": "멤버별 파트 분배 균형 검토", "desc": "특정 멤버의 파트가 짧다는 피드백이 지속적으로 제기되고 있습니다. 다음 컴백에서는 멤버별 파트 시간을 분석하여 보다 균형 잡힌 분배를 검토해 주세요.", "urgency": "중간", "frequency": 156, "impact": 7.2},
            {"task": "중독성 있는 훅 파트 강화", "desc": "이번 곡의 훅이 큰 호응을 얻고 있습니다. 이 강점을 다음 앨범에도 유지하면서 더욱 발전시킬 수 있도록 프로듀싱 방향을 검토해 주세요.", "urgency": "낮음", "frequency": 45, "impact": 5.8},
            {"task": "팬 소통 채널 강화", "desc": "팬들의 다양한 피드백을 수렴할 수 있는 공식 채널을 확대하여, 앨범 제작 과정에서 팬 의견을 반영하는 것을 권장합니다.", "urgency": "낮음", "frequency": 34, "impact": 5.2},
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

def get_sentiment_counts(comments):
    counts = {"positive": 0, "negative": 0, "neutral": 0}
    for c in comments:
        counts[c["sentiment"]] = counts.get(c["sentiment"], 0) + 1
    return counts

def simulate_loading():
    progress_messages = [
        "소스 분석 중...",
        "텍스트 추출 중...",
        "감정 분류 중...",
        "주제 분류 중...",
        "인사이트 생성 중..."
    ]
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, msg in enumerate(progress_messages):
        status_text.text(msg)
        progress_bar.progress((i + 1) / len(progress_messages))
        time.sleep(0.2)
    
    status_text.empty()
    progress_bar.empty()

def render_sidebar():
    with st.sidebar:
        st.markdown(f'''
        <div class="brand-header">
            <div class="brand-logo">{ICONS["logo"]}</div>
            <div>
                <div class="brand-name">OpiniQ</div>
                <div class="brand-tagline">오피니큐</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown(f'<div class="sidebar-section"><span class="icon-wrapper">{ICONS["history"]}</span> 분석 내역</div>', unsafe_allow_html=True)
        
        if 'analysis_history' not in st.session_state:
            st.session_state.analysis_history = []
        if 'show_all_history' not in st.session_state:
            st.session_state.show_all_history = False
        
        if st.session_state.analysis_history:
            reversed_history = list(reversed(st.session_state.analysis_history))
            
            if st.session_state.show_all_history:
                display_history = reversed_history[:10]
            else:
                display_history = reversed_history[:5]
            
            for i, item in enumerate(display_history):
                st.markdown(f'''
                <div class="history-card">
                    <div class="history-card-title"><span class="icon-wrapper">{ICONS["document"]}</span> {item["name"]}</div>
                    <div class="history-card-meta">{item["count"]}개 분석 완료</div>
                </div>
                ''', unsafe_allow_html=True)
            
            if len(reversed_history) > 5 and not st.session_state.show_all_history:
                if st.button(f"더보기 ({len(reversed_history) - 5}개)", key="show_more_history", use_container_width=True):
                    st.session_state.show_all_history = True
                    st.rerun()
            elif st.session_state.show_all_history and len(reversed_history) > 5:
                if st.button("접기", key="show_less_history", use_container_width=True):
                    st.session_state.show_all_history = False
                    st.rerun()
        else:
            st.markdown('''
            <div style="color: #9ca3af; font-size: 0.8rem; padding: 0.75rem 0;">
                분석 내역이 없습니다
            </div>
            ''', unsafe_allow_html=True)
        
        if st.button("+ 새로운 분석", key="new_analysis_btn", use_container_width=True):
            st.session_state.analysis_done = False
            st.session_state.selected_data = None
            st.session_state.user_context = ""
            st.session_state.current_view = "input"
            st.session_state.input_mode = None
            st.session_state.selected_topic = None
            st.rerun()
        
        st.markdown("---")
        
        st.markdown(f'<div class="sidebar-section"><span class="icon-wrapper">{ICONS["test"]}</span> 테스트 모드</div>', unsafe_allow_html=True)
        
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
    st.markdown(f'''
    <div class="main-brand">
        <div class="brand-logo">{ICONS["logo"]}</div>
        <div class="main-brand-name">OpiniQ</div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('<p class="main-subheader">여론(Opinion)에 지능(IQ)과 단서(Cue)를 더하다</p>', unsafe_allow_html=True)
    
    if 'active_input' not in st.session_state:
        st.session_state.active_input = None
    if 'user_context' not in st.session_state:
        st.session_state.user_context = ""
    
    uploaded_file = None
    url_input = ""
    text_input = ""
    
    st.markdown('''
    <div class="drop-zone">
        <div class="drop-zone-text">분석할 데이터를 추가하세요</div>
        <div class="drop-zone-subtext">파일을 끌어다 놓거나 아래에서 입력 방식을 선택하세요</div>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button(f"📁 파일 업로드", key="btn_file", use_container_width=True, 
                    type="primary" if st.session_state.active_input == "file" else "secondary"):
            st.session_state.active_input = "file" if st.session_state.active_input != "file" else None
            st.rerun()
    
    with col2:
        if st.button(f"🔗 웹사이트", key="btn_url", use_container_width=True,
                    type="primary" if st.session_state.active_input == "url" else "secondary"):
            st.session_state.active_input = "url" if st.session_state.active_input != "url" else None
            st.rerun()
    
    with col3:
        if st.button(f"🖼️ 이미지", key="btn_image", use_container_width=True,
                    type="primary" if st.session_state.active_input == "image" else "secondary"):
            st.session_state.active_input = "image" if st.session_state.active_input != "image" else None
            st.rerun()
    
    with col4:
        if st.button(f"📝 텍스트", key="btn_text", use_container_width=True,
                    type="primary" if st.session_state.active_input == "text" else "secondary"):
            st.session_state.active_input = "text" if st.session_state.active_input != "text" else None
            st.rerun()
    
    if st.session_state.active_input == "file":
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("PDF, DOCX, CSV, Excel 파일을 업로드하세요", 
                                         type=['pdf', 'docx', 'csv', 'xlsx', 'xls'], 
                                         key="file_upload", 
                                         label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.active_input == "url":
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        url_input = st.text_input("웹사이트 URL을 입력하세요", 
                                  placeholder="https://example.com/reviews", 
                                  key="url_input", 
                                  label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.active_input == "image":
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("이미지 파일을 업로드하세요 (스크린샷, 캡처 등)", 
                                         type=['png', 'jpg', 'jpeg', 'gif', 'webp'], 
                                         key="image_upload", 
                                         label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.active_input == "text":
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        text_input = st.text_area("분석할 텍스트를 입력하세요", 
                                  placeholder="리뷰나 댓글을 여기에 붙여넣으세요...", 
                                  height=150, 
                                  key="text_input", 
                                  label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="context-input">
        <div class="context-label"><span class="icon-wrapper">{ICONS["context"]}</span> 맥락(Context) 추가 (선택 사항)</div>
    </div>
    ''', unsafe_allow_html=True)
    
    user_context = st.text_area(
        "분석에 참고할 맥락 정보를 입력하세요",
        placeholder="예: 이 제품은 20-30대 여성을 타겟으로 한 여름 신상품입니다. 최근 배송 지연 이슈가 있었습니다.",
        height=80,
        key="context_input",
        label_visibility="collapsed"
    )
    
    if user_context:
        st.session_state.user_context = user_context
    
    return uploaded_file, url_input, text_input

def render_results(data):
    st.markdown(f'''
    <div class="main-brand">
        <div class="brand-logo">{ICONS["logo"]}</div>
        <div class="main-brand-name">OpiniQ</div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown(f'<h2 class="main-header">{data["product_name"]} 분석 결과</h2>', unsafe_allow_html=True)
    
    issue = data.get("urgent_issue", {"level": "green", "message": "현재 특별한 이슈가 없습니다"})
    alert_class = f"alert-{issue['level']}"
    signal_icon = ICONS[f"signal_{issue['level']}"]
    
    st.markdown(f'''
    <div class="alert-card {alert_class}">
        <span class="icon-wrapper">{signal_icon}</span>
        <span class="alert-text">{issue['message']}</span>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="result-section">
        <div class="result-card-header"><span class="icon-wrapper">{ICONS["summary"]}</span> AI 요약</div>
        <div class="result-card-content">
    ''', unsafe_allow_html=True)
    
    for summary in data['summary']:
        st.markdown(f'<p class="summary-text">• {summary}</p>', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'''
        <div class="result-section">
            <div class="result-card-header"><span class="icon-wrapper">{ICONS["sentiment"]}</span> 감정 기상도</div>
            <div class="result-card-content">
        ''', unsafe_allow_html=True)
        
        sentiment_counts = get_sentiment_counts(data['comments'])
        total = sum(sentiment_counts.values())
        
        sentiment_df = pd.DataFrame({
            '감정': ['긍정', '부정', '중립'],
            '수': [sentiment_counts['positive'], sentiment_counts['negative'], sentiment_counts['neutral']],
            '비율': [
                round(sentiment_counts['positive']/total*100) if total > 0 else 0,
                round(sentiment_counts['negative']/total*100) if total > 0 else 0,
                round(sentiment_counts['neutral']/total*100) if total > 0 else 0,
            ]
        })
        
        fig = px.pie(
            sentiment_df, 
            values='수', 
            names='감정',
            color='감정',
            color_discrete_map={'긍정': '#10b981', '부정': '#ef4444', '중립': '#9ca3af'},
            hole=0.45
        )
        fig.update_traces(textposition='outside', textinfo='percent+label', textfont_size=12)
        fig.update_layout(
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20),
            height=240,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", size=12)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="result-section">
            <div class="result-card-header"><span class="icon-wrapper">{ICONS["chart"]}</span> 주제별 분포</div>
            <div class="result-card-content">
        ''', unsafe_allow_html=True)
        
        sorted_topics = dict(sorted(data['topics'].items(), key=lambda x: x[1], reverse=True))
        
        topics_df = pd.DataFrame({
            '주제': list(sorted_topics.keys()),
            '비율': list(sorted_topics.values())
        })
        
        fig = px.pie(
            topics_df, 
            values='비율', 
            names='주제',
            color_discrete_sequence=['#ef4444', '#3b82f6', '#9ca3af', '#f59e0b', '#10b981', '#8b5cf6'],
            hole=0.45
        )
        fig.update_traces(textposition='outside', textinfo='percent+label', textfont_size=12)
        fig.update_layout(
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20),
            height=240,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", size=12)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="result-section">
        <div class="result-card-header"><span class="icon-wrapper">{ICONS["detail"]}</span> 주제별 상세 분석</div>
        <div class="result-card-content">
            <p style="font-size: 0.85rem; color: #6b7280; margin-bottom: 1rem;">주제를 클릭하면 세부 항목을 볼 수 있습니다</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    sorted_topics_list = list(sorted(data['topics'].items(), key=lambda x: x[1], reverse=True))
    
    if "기타" not in [t[0] for t in sorted_topics_list]:
        sorted_topics_list.append(("기타", 0))
    
    if 'selected_topic' not in st.session_state or st.session_state.selected_topic is None:
        st.session_state.selected_topic = sorted_topics_list[0][0]
    
    for topic_name, ratio in sorted_topics_list:
        is_selected = st.session_state.selected_topic == topic_name
        
        topic_col1, topic_col2 = st.columns([6, 1])
        with topic_col1:
            header_class = "active" if is_selected else ""
            if st.button(f"{topic_name} ({ratio}%)", key=f"topic_header_{topic_name}", use_container_width=True,
                        type="primary" if is_selected else "secondary"):
                if st.session_state.selected_topic == topic_name:
                    st.session_state.selected_topic = None
                else:
                    st.session_state.selected_topic = topic_name
                st.rerun()
        
        if is_selected and topic_name in data.get('topic_details', {}):
            topic_detail = data['topic_details'][topic_name]
            
            st.markdown('<div class="micro-view">', unsafe_allow_html=True)
            
            for subtopic in topic_detail['subtopics']:
                st.markdown(f'''
                <div class="sub-topic-item">
                    <div>
                        <div class="sub-topic-name">{subtopic['name']}</div>
                        <div class="sub-topic-sample">"{subtopic['sample']}"</div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <div class="sub-topic-bar">
                            <div class="sub-topic-fill" style="width: {subtopic['ratio']}%"></div>
                        </div>
                        <span style="font-size: 0.8rem; font-weight: 600; color: #374151; min-width: 35px;">{subtopic['ratio']}%</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="result-section">
        <div class="result-card-header"><span class="icon-wrapper">{ICONS["priority"]}</span> 시급한 개선 과제</div>
        <div class="result-card-content">
    ''', unsafe_allow_html=True)
    
    for i, priority in enumerate(data['priorities']):
        urgency_class = get_urgency_class(priority['urgency'])
        st.markdown(f'''
        <div class="task-item">
            <div class="task-title">
                <span class="insight-chip {urgency_class}">{i+1}순위</span>
                <span style="font-weight: 600;">{priority['task']}</span>
            </div>
            <div class="task-desc">{priority.get('desc', '')}</div>
            <div class="task-meta">언급 {priority['frequency']}회 · 영향도 {priority['impact']}/10 · 우선순위: {priority['urgency']}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="result-section">
        <div class="result-card-header"><span class="icon-wrapper">{ICONS["comment"]}</span> 대표 의견</div>
        <div class="result-card-content">
    ''', unsafe_allow_html=True)
    
    positive_comments = sorted([c for c in data['comments'] if c['sentiment'] == 'positive'], key=lambda x: x['likes'], reverse=True)
    negative_comments = sorted([c for c in data['comments'] if c['sentiment'] == 'negative'], key=lambda x: x['likes'], reverse=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'<div class="section-label"><span class="icon-wrapper">{ICONS["check"]}</span> 긍정 리뷰</div>', unsafe_allow_html=True)
        if positive_comments:
            best = positive_comments[0]
            filtered_text, was_modified = filter_profanity(best['text'])
            badge = '<span class="modified-badge">수정됨</span>' if was_modified else ''
            st.markdown(f'''
            <div class="review-card review-positive">
                <div class="review-text">"{filtered_text}"{badge}</div>
                <div class="review-meta">{best['topic']} · {ICONS["thumbsup"]} {best['likes']:,}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="section-label"><span class="icon-wrapper">{ICONS["x"]}</span> 개선 필요</div>', unsafe_allow_html=True)
        if negative_comments:
            worst = negative_comments[0]
            filtered_text, was_modified = filter_profanity(worst['text'])
            badge = '<span class="modified-badge">수정됨</span>' if was_modified else ''
            st.markdown(f'''
            <div class="review-card review-negative">
                <div class="review-text">"{filtered_text}"{badge}</div>
                <div class="review-meta">{worst['topic']} · {ICONS["thumbsup"]} {worst['likes']:,}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    with st.expander("📋 전체 댓글 보기"):
        comments_df = pd.DataFrame(data['comments'])
        
        filtered_texts = []
        for text in comments_df['text']:
            filtered, was_modified = filter_profanity(text)
            if was_modified:
                filtered_texts.append(f"{filtered} [수정됨]")
            else:
                filtered_texts.append(filtered)
        
        comments_df['댓글'] = filtered_texts
        comments_df['감정'] = comments_df['sentiment'].map({
            'positive': '긍정',
            'negative': '부정',
            'neutral': '중립'
        })
        comments_df = comments_df.rename(columns={
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
        <div style="font-size: 0.85rem; color: #9ca3af;">소스를 추가하고 분석을 시작해주세요</div>
    </div>
    ''', unsafe_allow_html=True)

def main():
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
    if 'selected_data' not in st.session_state:
        st.session_state.selected_data = None
    if 'current_view' not in st.session_state:
        st.session_state.current_view = "input"
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    if 'input_mode' not in st.session_state:
        st.session_state.input_mode = None
    if 'selected_topic' not in st.session_state:
        st.session_state.selected_topic = None
    
    use_demo, demo_option = render_sidebar()
    
    if st.session_state.current_view == "input" or not st.session_state.analysis_done:
        uploaded_file, url_input, text_input = render_input_section()
        
        st.markdown('<div class="start-btn-wrapper">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("✨ 분석 시작", type="primary", use_container_width=True):
                has_input = uploaded_file or url_input or text_input or use_demo
                
                if not has_input:
                    st.warning("분석할 데이터를 입력하거나 데모 데이터를 선택해주세요.")
                else:
                    simulate_loading()
                    
                    if use_demo:
                        st.session_state.selected_data = MOCK_DATA_SETS[demo_option]
                    else:
                        st.session_state.selected_data = MOCK_DATA_SETS["tumbler"]
                    
                    st.session_state.analysis_history.append({
                        "name": st.session_state.selected_data["product_name"],
                        "count": len(st.session_state.selected_data["comments"])
                    })
                    
                    st.session_state.analysis_done = True
                    st.session_state.current_view = "results"
                    st.session_state.selected_topic = None
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        if st.session_state.selected_data:
            render_results(st.session_state.selected_data)
        else:
            render_empty_state()

if __name__ == "__main__":
    main()
