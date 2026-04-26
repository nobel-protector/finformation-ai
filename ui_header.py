
# ui_header.py — CSS styles and header

import streamlit as st

def render_css():
    st.markdown("""
<style>
@import url("https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap");
* { font-family: "DM Sans", sans-serif; }
.main { background-color: #f4f6f9; }
.header-box { background: linear-gradient(135deg, #0d1b2a 0%, #1a3a5c 100%); padding: 32px 40px; border-radius: 16px; margin-bottom: 24px; }
.header-title { font-family: "DM Serif Display", serif; font-size: 36px; color: white; margin-bottom: 8px; }
.header-subtitle { color: rgba(255,255,255,0.65); font-size: 15px; }
.header-badge { display: inline-block; background: rgba(232,160,32,0.15); border: 1px solid rgba(232,160,32,0.3); color: #e8a020; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; margin-bottom: 12px; }
.track-card { background: white; border-radius: 12px; padding: 16px; border: 1px solid #dde3ec; margin-bottom: 12px; }
.risk-red { background: rgba(192,57,43,0.08); border: 2px solid #c0392b; border-radius: 16px; padding: 24px; text-align: center; }
.risk-amber { background: rgba(217,119,6,0.08); border: 2px solid #d97706; border-radius: 16px; padding: 24px; text-align: center; }
.risk-green { background: rgba(26,140,78,0.08); border: 2px solid #1a8c4e; border-radius: 16px; padding: 24px; text-align: center; }
.edu-box { background: linear-gradient(135deg, #1a2f50 0%, #0d1b2a 100%); border-radius: 14px; padding: 20px; color: white; margin-top: 16px; }
.red-flag { background: rgba(192,57,43,0.06); border-left: 3px solid #c0392b; padding: 6px 12px; margin: 4px 0; border-radius: 4px; font-size: 13px; }
.key-fact { background: rgba(42,125,225,0.06); border-left: 3px solid #2a7de1; padding: 6px 12px; margin: 4px 0; border-radius: 4px; font-size: 13px; }
.verify-step { background: rgba(26,140,78,0.06); border-left: 3px solid #1a8c4e; padding: 6px 12px; margin: 4px 0; border-radius: 4px; font-size: 13px; }
.case-box { background: rgba(192,57,43,0.04); border: 1px solid rgba(192,57,43,0.2); border-radius: 10px; padding: 14px; margin: 12px 0; font-size: 13px; }
.quiz-correct { background: rgba(26,140,78,0.1); border: 2px solid #1a8c4e; border-radius: 8px; padding: 10px; color: #1a8c4e; font-weight: 600; margin: 4px 0; }
.quiz-wrong { background: rgba(192,57,43,0.1); border: 2px solid #c0392b; border-radius: 8px; padding: 10px; color: #c0392b; margin: 4px 0; }
.footer-box { background: #0d1b2a; color: rgba(255,255,255,0.4); text-align: center; padding: 16px; border-radius: 10px; font-size: 12px; margin-top: 32px; }
.score-box { background: linear-gradient(135deg, #1a3a5c, #0d1b2a); border-radius: 12px; padding: 16px; text-align: center; color: white; margin-top: 16px; }
.feedback-box { background: white; border-radius: 12px; padding: 20px; border: 1px solid #dde3ec; margin-top: 16px; }
.module-card { background: white; border-radius: 12px; padding: 20px; border: 1px solid #dde3ec; margin-bottom: 16px; }
</style>
""", unsafe_allow_html=True)


def render_header():
    st.markdown("""
<div class="header-box">
    <div class="header-badge">🇮🇳 IOSCO TechSprint 2026 · SEBI</div>
    <div class="header-title">🛡️ Finformation.ai</div>
    <div class="header-subtitle">AI-powered investor protection · Detect fraud before you invest · Commercial AI + RAG Architecture</div>
</div>
""", unsafe_allow_html=True)


def render_footer():
    st.markdown("""<div class="footer-box">
    <strong style="color:rgba(255,255,255,0.7)">Finformation.ai</strong> ·
    IOSCO TechSprint 2026 · SEBI · Commercial AI + RAG Architecture ·
    Decision-support tool only — not a legal conclusion · SEBI Helpline: 1800 266 7575
</div>""", unsafe_allow_html=True)
