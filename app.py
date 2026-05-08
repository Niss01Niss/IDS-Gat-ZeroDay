
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json, os, random, time, math

st.set_page_config(
    page_title="IDS SIEM — Zero-Day Detection Platform",
    page_icon="🛡️", layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════
# THEME TOGGLE — Dark / Light Mode
# ═══════════════════════════════════════════════════════════
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def T(dark_val, light_val):
    return dark_val if st.session_state.theme == "dark" else light_val

# ═══════════════════════════════════════════════════════════
# CSS PREMIUM — DYNAMIC THEME
# ═══════════════════════════════════════════════════════════
_bg       = T("#0b0e14", "#f0f2f6")
_bg2      = T("#0d1117", "#ffffff")
_panel    = T("#161b22", "#f8f9fb")
_text     = T("#d4d9e3", "#1a1a2e")
_sub      = T("#8b949e", "#6b7280")
_border   = T("rgba(0,191,179,0.15)", "rgba(0,50,80,0.12)")
_accent   = T("#00bfb3", "#0077b6")
_accent2  = T("#58a6ff", "#0096c7")
_green    = T("#3fb950", "#2d9d3a")
_red      = T("#f85149", "#e63946")
_gold     = T("#d29922", "#e6a817")
_purple   = T("#bc8cff", "#7209b7")
_sidebar  = T("linear-gradient(160deg, #07090f 0%, #0d1117 60%, #0a1020 100%)",
              "linear-gradient(160deg, #e8ecf1 0%, #f0f2f6 60%, #e4e8ee 100%)")
_card_bg  = T("linear-gradient(145deg, #0d1117, #161b22)",
              "linear-gradient(145deg, #ffffff, #f3f4f6)")
_glow     = T("rgba(0,191,179,0.08)", "rgba(0,119,182,0.06)")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Orbitron:wght@600;700;800&display=swap');

.stApp {{
    background: {_bg};
    color: {_text};
    font-family: 'Inter', sans-serif;
}}

/* Animated grid background */
.stApp::before {{
    content: '';
    position: fixed; top:0; left:0; width:100%; height:100%;
    background-image:
        linear-gradient({T("rgba(0,191,179,0.03)","rgba(0,119,182,0.02)")} 1px, transparent 1px),
        linear-gradient(90deg, {T("rgba(0,191,179,0.03)","rgba(0,119,182,0.02)")} 1px, transparent 1px);
    background-size: 60px 60px;
    animation: gridMove 20s linear infinite;
    pointer-events: none; z-index: -1;
}}
@keyframes gridMove {{
    0% {{ background-position: 0 0; }}
    100% {{ background-position: 60px 60px; }}
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: {_sidebar};
    border-right: 1px solid {_border};
}}
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{ color: {T("#c9d1d9","#374151")}; }}
[data-testid="stSidebar"] .stRadio label:hover {{ color: {_accent} !important; }}

/* Sidebar buttons fix */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"] {{
    z-index: 99999 !important; opacity: 1 !important; visibility: visible !important;
    background-color: {T("rgba(13,17,23,0.6)","rgba(240,242,246,0.8)")} !important;
    border-radius: 6px;
}}
[data-testid="collapsedControl"] svg,
[data-testid="stSidebarCollapseButton"] svg {{
    width: 28px !important; height: 28px !important;
    color: {_accent} !important; fill: {_accent} !important;
    display: block !important; opacity: 1 !important;
}}

/* Hero title with animated gradient */
.hero-title {{
    font-family: 'Orbitron', sans-serif;
    font-size: 32px; font-weight: 800;
    background: linear-gradient(135deg, {_accent} 0%, {_accent2} 50%, {_accent} 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: gradShift 4s ease infinite;
    letter-spacing: 2px;
}}
@keyframes gradShift {{
    0%,100%{{ background-position:0% 50% }}
    50%{{ background-position:100% 50% }}
}}

/* Live badge pulse */
.live-badge {{
    display: inline-flex; align-items: center; gap: 8px;
    background: {T("rgba(248,81,73,0.12)","rgba(230,57,70,0.08)")};
    border: 1px solid {T("rgba(248,81,73,0.4)","rgba(230,57,70,0.3)")};
    border-radius: 20px; padding: 5px 14px;
    font-family: 'JetBrains Mono'; font-size: 12px; font-weight: 600;
    color: {_red}; letter-spacing: 1px;
    animation: pulseBorder 2s ease infinite;
}}
.live-dot {{
    width: 8px; height: 8px; border-radius: 50%;
    background: {_red}; animation: pulseRed 1.2s ease infinite;
}}
@keyframes pulseRed {{
    0%,100%{{ opacity:1; transform:scale(1); }}
    50%{{ opacity:0.4; transform:scale(0.7); }}
}}
@keyframes pulseBorder {{
    0%,100%{{ box-shadow:0 0 0 0 rgba(248,81,73,0.3); }}
    50%{{ box-shadow:0 0 12px 3px rgba(248,81,73,0.15); }}
}}

/* KPI Card — glassmorphism */
.kpi-card {{
    background: {_card_bg};
    border: 1px solid {_border};
    border-radius: 16px; padding: 22px 18px; text-align: center;
    position: relative; overflow: hidden;
    backdrop-filter: blur(10px);
    transition: all 0.4s cubic-bezier(.25,.8,.25,1);
}}
.kpi-card::before {{
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
    background: linear-gradient(90deg, transparent, {_accent}, transparent);
    background-size: 200% 100%;
    animation: shimmer 3s ease infinite;
}}
@keyframes shimmer {{
    0%{{ background-position:-200% 0 }}
    100%{{ background-position:200% 0 }}
}}
.kpi-card:hover {{
    border-color: {T("rgba(0,191,179,0.5)","rgba(0,119,182,0.4)")};
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 16px 40px {_glow};
}}
.kpi-icon {{ font-size:28px; margin-bottom:8px; filter: drop-shadow(0 0 8px {_glow}); }}
.kpi-lbl {{
    font-size:10px; font-weight:600; letter-spacing:2px;
    text-transform:uppercase; color:{_sub}; margin-bottom:6px;
}}
.kpi-val {{
    font-family:'JetBrains Mono'; font-size:30px; font-weight:700; line-height:1.1;
}}
.kpi-val.cyan  {{ color: {_accent}; }}
.kpi-val.green {{ color: {_green}; }}
.kpi-val.red   {{ color: {_red}; }}
.kpi-val.gold  {{ color: {_gold}; }}
.kpi-sub {{ font-size:11px; color:{_sub}; margin-top:5px; font-family:'JetBrains Mono'; }}

/* Alert rows */
.alert-row {{
    background: {_bg2}; border-left: 3px solid;
    border-radius: 0 12px 12px 0; padding: 12px 16px; margin: 6px 0;
    font-family: 'JetBrains Mono'; font-size: 12px;
    display: flex; align-items: center; gap: 12px;
    animation: slideIn 0.4s ease;
    transition: background 0.2s ease;
}}
.alert-row:hover {{ background: {T("rgba(0,191,179,0.04)","rgba(0,119,182,0.04)")}; }}
@keyframes slideIn {{
    from{{ opacity:0; transform:translateX(-15px); }}
    to{{ opacity:1; transform:translateX(0); }}
}}
.alert-critical {{ border-color: {_red}; }}
.alert-high     {{ border-color: {_gold}; }}
.alert-medium   {{ border-color: {_accent2}; }}
.alert-low      {{ border-color: {_green}; }}

/* Section header */
.sec-hdr {{
    border-left: 3px solid {_accent};
    padding: 12px 20px; margin: 28px 0 18px;
    background: linear-gradient(90deg, {_glow}, transparent);
    border-radius: 0 10px 10px 0;
}}
.sec-hdr h3 {{ margin:0; color:{T("#e0e6f0","#1a1a2e")}; font-size:18px; font-weight:700; }}
.sec-hdr p  {{ margin:3px 0 0; color:{_sub}; font-size:12px; }}

/* Incident card */
.incident-card {{
    background: {_bg2}; border: 1px solid {T("rgba(248,81,73,0.3)","rgba(230,57,70,0.2)")};
    border-radius: 16px; padding: 0; overflow: hidden; margin: 16px 0;
    box-shadow: 0 4px 20px {T("rgba(248,81,73,0.08)","rgba(230,57,70,0.05)")};
}}
.incident-header {{
    background: linear-gradient(90deg, {T("rgba(248,81,73,0.15)","rgba(230,57,70,0.08)")},
                {T("rgba(248,81,73,0.05)","rgba(230,57,70,0.02)")});
    padding: 16px 20px; border-bottom: 1px solid {T("rgba(248,81,73,0.2)","rgba(230,57,70,0.15)")};
}}
.incident-body {{ padding: 20px; }}

/* Dark table */
.dark-table {{
    width: 100%; border-collapse: collapse; font-size: 13px; font-family: 'Inter';
}}
.dark-table th {{
    background: {_panel}; color: {_sub}; font-size: 11px;
    font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase;
    padding: 12px 14px; text-align: left;
    border-bottom: 1px solid {T("#21262d","#e5e7eb")};
}}
.dark-table td {{
    padding: 12px 14px; color: {T("#c9d1d9","#374151")};
    border-bottom: 1px solid {T("#161b22","#f3f4f6")};
}}
.dark-table tr:hover td {{ background: {_glow}; }}

/* Badges */
.badge {{
    display:inline-block; padding:3px 10px; border-radius:20px;
    font-size:11px; font-weight:600; letter-spacing:0.5px;
}}
.b-red   {{ background:{T("rgba(248,81,73,0.15)","rgba(230,57,70,0.1)")}; color:{_red}; border:1px solid {T("rgba(248,81,73,0.3)","rgba(230,57,70,0.2)")}; }}
.b-green {{ background:{T("rgba(63,185,80,0.15)","rgba(45,157,58,0.1)")}; color:{_green}; border:1px solid {T("rgba(63,185,80,0.3)","rgba(45,157,58,0.2)")}; }}
.b-gold  {{ background:{T("rgba(210,153,34,0.15)","rgba(230,168,23,0.1)")}; color:{_gold}; border:1px solid {T("rgba(210,153,34,0.3)","rgba(230,168,23,0.2)")}; }}
.b-cyan  {{ background:{T("rgba(0,191,179,0.15)","rgba(0,119,182,0.1)")}; color:{_accent}; border:1px solid {T("rgba(0,191,179,0.3)","rgba(0,119,182,0.2)")}; }}
.b-blue  {{ background:{T("rgba(88,166,255,0.15)","rgba(0,150,199,0.1)")}; color:{_accent2}; border:1px solid {T("rgba(88,166,255,0.3)","rgba(0,150,199,0.2)")}; }}

/* Verdict boxes */
.verdict-ok {{
    background: linear-gradient(135deg, {T("rgba(63,185,80,0.08)","rgba(45,157,58,0.06)")},
                {T("rgba(0,191,179,0.05)","rgba(0,119,182,0.04)")});
    border: 1px solid {T("rgba(63,185,80,0.3)","rgba(45,157,58,0.25)")}; border-radius: 14px; padding: 20px; margin: 12px 0;
}}
.verdict-fail {{
    background: {T("rgba(248,81,73,0.06)","rgba(230,57,70,0.04)")};
    border: 1px solid {T("rgba(248,81,73,0.25)","rgba(230,57,70,0.2)")};
    border-radius: 14px; padding: 20px; margin: 12px 0;
}}

/* Glow card */
.glow-card {{
    background: {_card_bg};
    border: 1px solid {_border}; border-radius: 16px; padding: 24px;
    position: relative; overflow: hidden;
    transition: all 0.4s ease;
}}
.glow-card:hover {{
    box-shadow: 0 0 30px {_glow}, 0 0 60px {T("rgba(0,191,179,0.04)","rgba(0,119,182,0.03)")};
    transform: translateY(-2px);
}}

/* Info banner */
.info-banner {{
    background: {T("rgba(88,166,255,0.08)","rgba(0,150,199,0.06)")};
    border: 1px solid {T("rgba(88,166,255,0.25)","rgba(0,150,199,0.2)")};
    border-radius: 10px; padding: 14px 18px; font-size: 13px;
    color: {T("#79c0ff","#0077b6")}; margin-bottom: 20px;
}}

#MainMenu {{ display: none !important; }}
footer    {{ visibility: hidden !important; }}

/* Responsive */
@media (max-width: 768px) {{
    .hero-title {{ font-size: 20px !important; letter-spacing: 1px !important; }}
    .kpi-card {{ padding: 14px 10px !important; }}
    .kpi-val {{ font-size: 22px !important; }}
    .kpi-lbl {{ font-size: 9px !important; }}
    [data-testid="column"] {{ width: 100% !important; flex: 1 1 45% !important; min-width: 140px !important; }}
    .dark-table {{ display: block !important; overflow-x: auto !important; font-size: 11px !important; }}
    .alert-row {{ font-size: 10px !important; padding: 8px 10px !important; flex-wrap: wrap !important; }}
    .sec-hdr h3 {{ font-size: 14px !important; }}
    .badge {{ font-size: 9px !important; padding: 2px 7px !important; }}
}}
@media (max-width: 480px) {{
    .hero-title {{ font-size: 16px !important; }}
    .kpi-val    {{ font-size: 18px !important; }}
    [data-testid="column"] {{ flex: 1 1 100% !important; min-width: 100% !important; }}
}}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════
@st.cache_data
def load():
    df   = pd.read_csv("dashboard_data.csv") if os.path.exists("dashboard_data.csv") else pd.DataFrame()
    meta = json.load(open("dashboard_meta.json")) if os.path.exists("dashboard_meta.json") else {}
    soc  = json.load(open("dashboard_soc_alert.json","r",encoding="utf-8")) \
           if os.path.exists("dashboard_soc_alert.json") else {}
    return df, meta, soc

df, meta, soc = load()
bench   = meta.get('benchmark', {})
zd_info = meta.get('zd_info', {})

PLOTLY = dict(
    template="plotly_dark" if st.session_state.theme == "dark" else "plotly_white",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor=T("rgba(13,17,18,0.9)", "rgba(248,249,251,0.9)"),
    font=dict(family="Inter", color=T("#c9d1d9","#374151")),
    margin=dict(l=40, r=30, t=50, b=40),
)

# ═══════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════
def kpi(icon, label, value, cls="cyan", sub=""):
    return f"""<div class="kpi-card">
    <div class="kpi-icon">{icon}</div>
    <div class="kpi-lbl">{label}</div>
    <div class="kpi-val {cls}">{value}</div>
    {"<div class='kpi-sub'>"+sub+"</div>" if sub else ""}
    </div>"""

def sec(title, sub=""):
    st.markdown(f'<div class="sec-hdr"><h3>{title}</h3>{"<p>"+sub+"</p>" if sub else ""}</div>',
                unsafe_allow_html=True)

def img(path, cap=""):
    if os.path.exists(path): st.image(path, caption=cap, use_container_width=True)
    else: st.info(f"Image absente : {path}")

def gauge(val, title, color, max_v=100, suffix="%"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=val, title={"text": title, "font": {"size": 14, "color": T("#c9d1d9","#374151")}},
        number={"suffix": suffix, "font": {"size": 28, "color": color}},
        gauge={"axis": {"range": [0, max_v], "tickcolor": T("#30363d","#d1d5db")},
               "bar": {"color": color, "thickness": 0.7},
               "bgcolor": T("#161b22","#f3f4f6"),
               "borderwidth": 0,
               "steps": [{"range": [0, max_v*0.5], "color": T("rgba(63,185,80,0.08)","rgba(45,157,58,0.05)")},
                         {"range": [max_v*0.5, max_v*0.8], "color": T("rgba(210,153,34,0.08)","rgba(230,168,23,0.05)")},
                         {"range": [max_v*0.8, max_v], "color": T("rgba(248,81,73,0.08)","rgba(230,57,70,0.05)")}],
               "threshold": {"line": {"color": color, "width": 3}, "thickness": 0.8, "value": val}}))
    fig.update_layout(**{k:v for k,v in PLOTLY.items() if k!='margin'}, height=220, margin=dict(l=30,r=30,t=60,b=10))
    return fig

# ═══════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f'<div class="hero-title" style="font-size:18px;">🛡 IDS SIEM</div>',
                unsafe_allow_html=True)
    st.markdown(f'<div style="color:{_sub};font-size:11px;margin-bottom:12px;">Zero-Day Detection Platform</div>',
                unsafe_allow_html=True)

    # Theme toggle
    is_light = st.toggle("☀️ Light Mode", value=(st.session_state.theme == "light"), key="theme_toggle")
    new_theme = "light" if is_light else "dark"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

    st.markdown("---")

    page = st.radio("Navigation", [
        "🔴 SOC Live",
        "📊 Benchmark",
        "⚡ Latence Temps-Réel",
        "🎯 Cas Zero-Day",
        "🧠 Pourquoi le GAT ?",
        "🔬 XAI Avancé",
        "🛡️ Analyse SOC",
        "🌐 Généralisation",
        "🏗️ Architecture",
    ], label_visibility="collapsed")

    st.markdown("---")
    n_cls   = zd_info.get('n_classes', 5)
    n_train = zd_info.get('n_train', 0)
    n_test  = zd_info.get('n_test_total', 0)
    st.markdown(f"""
    <div style="font-size:11px; color:{_sub}; line-height:1.9;">
    📁 <b style="color:{T('#c9d1d9','#1a1a2e')};">Dataset</b> CICIDS2017 Wed<br>
    🏷️ <b style="color:{T('#c9d1d9','#1a1a2e')};">Classes connues</b> {n_cls}<br>
    🔴 <b style="color:{_red};">Zero-Day</b> DoS Slowhttptest<br>
    🏋️ <b style="color:{T('#c9d1d9','#1a1a2e')};">Train</b> {n_train:,} flux<br>
    🧪 <b style="color:{T('#c9d1d9','#1a1a2e')};">Test</b> {n_test:,} flux
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f'<div style="text-align:center;color:{_sub};font-size:10px;">PFE 2026 · Cybersécurité<br>IDS + Graph Neural Networks + XAI</div>',
                unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE 1 — SOC LIVE
# ═══════════════════════════════════════════════════════════
if page == "🔴 SOC Live":

    st.markdown(f"""
    <div style="text-align:center;padding:30px 0 8px;">
        <div class="hero-title">🛡️ IDS SIEM — ZERO-DAY DETECTION PLATFORM</div>
        <div style="color:{_sub};font-size:14px;margin:10px 0 18px;">
            Système de détection d'intrusions · RF / XGBoost / MLP / GAT
        </div>
        <div class="live-badge">
            <div class="live-dot"></div> SYSTÈME ACTIF — SURVEILLANCE EN COURS
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if bench:
        _gat_cns_key = next((k for k in bench if 'consensus' in k.lower() or '+cns' in k.lower()), None)
        _gat_key = next((k for k in bench if 'GAT' in k and 'consensus' not in k and '+cns' not in k), None)
        _ref_key = _gat_cns_key or _gat_key
        _ref     = bench.get(_ref_key, {}) if _ref_key else {}
        best_f1 = max(v['f1_known'] for v in bench.values())
        _zd_val = _ref.get('zd_recall', 0)
        _fp_val = _ref.get('fp_day',    0)
        _fb_val = _ref.get('fbeta2',    0)
        _lbl    = 'GAT+consensus' if _gat_cns_key else ('GAT' if _gat_key else 'Best')

        c1,c2,c3,c4 = st.columns(4)
        with c1: st.markdown(kpi("🎯","F1 Macro — Connus",f"{best_f1:.1f}%","green","Classification attaques connues"),unsafe_allow_html=True)
        with c2: st.markdown(kpi("🔴","Recall Zero-Day",f"{_zd_val:.1f}%","red",f"{_lbl} · Zero-Day recall"),unsafe_allow_html=True)
        with c3: st.markdown(kpi("⚡","Faux Positifs/jour",f"{_fp_val:,}","gold",f"{_lbl} · sur 1M flux/jour"),unsafe_allow_html=True)
        with c4: st.markdown(kpi("📐","Fβ(2) Score",f"{_fb_val:.1f}%","cyan",f"{_lbl} · priorité recall"),unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:{T('rgba(63,185,80,0.08)','rgba(45,157,58,0.06)')};border:1px solid {T('rgba(63,185,80,0.25)','rgba(45,157,58,0.2)')};
                    border-radius:10px;padding:10px 16px;margin:12px 0 8px;font-size:12px;">
        <b style="color:{_green};">📌 Chiffres affichés :</b>
        <span style="color:{T('#c9d1d9','#374151')};">Configuration <b>{_lbl}</b>
        — F1 Connus {best_f1:.1f}% · Recall ZD {_zd_val:.1f}% · FP/jour {_fp_val:,} · Fβ(2) {_fb_val:.1f}%</span><br>
        <span style="color:{_sub};font-size:11px;">Les 4 métriques proviennent du même modèle pour une comparaison cohérente.</span>
        </div>""", unsafe_allow_html=True)

    # Real-time scatter simulation
    st.markdown("<br>", unsafe_allow_html=True)
    sec("📡 Flux Réseau — Simulation Temps Réel", "Visualisation scatter : BENIGN (vert) vs Anomalies (rouge)")

    np.random.seed(42)
    n_pts = 200
    _benign_x = np.random.normal(50, 15, int(n_pts*0.85))
    _benign_y = np.random.normal(40, 12, int(n_pts*0.85))
    _atk_x = np.random.normal(85, 8, int(n_pts*0.10))
    _atk_y = np.random.normal(80, 10, int(n_pts*0.10))
    _zd_x = np.random.normal(30, 5, int(n_pts*0.05))
    _zd_y = np.random.normal(85, 5, int(n_pts*0.05))

    _all_x = np.concatenate([_benign_x, _atk_x, _zd_x])
    _all_y = np.concatenate([_benign_y, _atk_y, _zd_y])
    _labels = (["BENIGN"]*len(_benign_x) + ["Attaque Connue"]*len(_atk_x) + ["⚠️ ZERO-DAY"]*len(_zd_x))
    _colors_map = {"BENIGN": _green, "Attaque Connue": _gold, "⚠️ ZERO-DAY": _red}

    _sdf = pd.DataFrame({"Entropie OOD": _all_x, "Distance KNN": _all_y, "Type": _labels})
    fig_sc = px.scatter(_sdf, x="Entropie OOD", y="Distance KNN", color="Type",
                        color_discrete_map=_colors_map, opacity=0.75)
    fig_sc.update_traces(marker=dict(size=8, line=dict(width=1, color="rgba(255,255,255,0.15)")))
    fig_sc.update_layout(**PLOTLY, height=380,
        title="Distribution des flux — Espace Entropie × Distance KNN",
        legend=dict(bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig_sc, use_container_width=True)

    sec("🚨 Timeline des alertes récentes", "Simulation d'un flux d'incidents en production")

    _FAKE_ALERTS = [
        ("CRITIQUE","🔴","192.168.10.50 → 192.168.10.3:80","DoS Slowhttptest détecté (GAT OOD)","alert-critical","2017-07-05 14:32:07","GAT ✅ XGB ❌"),
        ("ÉLEVÉ","🟠","192.168.10.51 → 192.168.10.3:80","DoS GoldenEye — flux haute fréquence","alert-high","2017-07-05 14:31:44","GAT ✅ XGB ✅"),
        ("ÉLEVÉ","🟠","192.168.10.47 → 192.168.10.5:80","DoS Hulk — saturation bande passante","alert-high","2017-07-05 14:31:12","GAT ✅ XGB ✅"),
        ("MOYEN","🔵","192.168.10.8  → 192.168.10.3:443","Flux atypique — entropie élevée","alert-medium","2017-07-05 14:30:55","GAT ⚠️ XGB ⚠️"),
        ("FAIBLE","🟢","192.168.10.12 → 8.8.8.8:53","DNS query — trafic légitime","alert-low","2017-07-05 14:30:30","Tous ✅"),
        ("FAIBLE","🟢","192.168.10.22 → 185.199.108.133:443","HTTPS — trafic légitime","alert-low","2017-07-05 14:30:15","Tous ✅"),
    ]
    for lvl,ic,src_dst,desc,cls,ts,models in _FAKE_ALERTS:
        st.markdown(f"""
        <div class="alert-row {cls}">
            <div style="min-width:70px;color:{_sub};font-size:11px;">{ts[-8:]}</div>
            <div style="font-size:14px;">{ic}</div>
            <div style="min-width:90px;"><span class="badge {'b-red' if 'CRITIQUE' in lvl else 'b-gold' if 'ÉLEVÉ' in lvl else 'b-blue' if 'MOYEN' in lvl else 'b-green'}">{lvl}</span></div>
            <div style="flex:1;color:{T('#e0e6f0','#1a1a2e')};">{src_dst}</div>
            <div style="flex:2;color:{_sub};">{desc}</div>
            <div style="min-width:130px;text-align:right;color:{_sub};">{models}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sec("📊 Résumé benchmark en un coup d'œil")
    if not df.empty:
        cols = ['Modele','f1_known','zd_recall','fp_day','fbeta2']
        avail = [c for c in cols if c in df.columns]
        tdf = df[avail].copy().rename(columns={
            'f1_known':'F1 Connus (%)','zd_recall':'Recall ZD (%)','fp_day':'FP/jour','fbeta2':'Fβ(2) (%)'})
        st.dataframe(tdf, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════
# PAGE 2 — BENCHMARK
# ═══════════════════════════════════════════════════════════
elif page == "📊 Benchmark":
    sec("📊 Benchmark Comparatif","Performance des 5 configurations — jeu de test CICIDS2017")

    if not df.empty and 'Model_short' in df.columns:
        # Gauge charts for best GAT metrics
        _gat_rows = df[df['Model_short'].str.contains('GAT', case=False, na=False)]
        if not _gat_rows.empty:
            _best_gat = _gat_rows.iloc[_gat_rows['zd_recall'].argmax()]
            sec("🎛️ Jauges OOD — Métriques clés du GAT", "Entropie et Distance KNN : les capteurs d'anomalie")
            g1, g2, g3 = st.columns(3)
            with g1:
                st.plotly_chart(gauge(float(_best_gat['zd_recall']), "Recall Zero-Day", _red), use_container_width=True)
            with g2:
                st.plotly_chart(gauge(float(_best_gat['fbeta2']), "Fβ(2) Score", _accent), use_container_width=True)
            with g3:
                _fp_score = max(0, 100 - float(_best_gat['fp_day'])/10000*100)
                st.plotly_chart(gauge(_fp_score, "Score Anti-FP", _green), use_container_width=True)

        c1,c2 = st.columns(2)
        with c1:
            fig = go.Figure(go.Bar(
                x=df['Model_short'], y=df['f1_known'],
                marker=dict(color=[_green]*len(df), line=dict(color='rgba(0,0,0,0)')),
                text=df['f1_known'].round(1).astype(str)+'%', textposition='outside'))
            fig.update_layout(**PLOTLY,title="F1 Macro — Classes Connues",
                yaxis=dict(range=[90,102],title="F1 (%)"),showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            cols_c = [_red if v<10 else _gold if v<50 else _green for v in df['zd_recall']]
            fig = go.Figure(go.Bar(
                x=df['Model_short'], y=df['zd_recall'],
                marker=dict(color=cols_c, line=dict(color='rgba(255,255,255,0.1)',width=1)),
                text=df['zd_recall'].round(1).astype(str)+'%', textposition='outside'))
            fig.update_layout(**PLOTLY,title="🔴 Recall Zero-Day (DoS Slowhttptest)",
                yaxis=dict(range=[0,max(df['zd_recall'].max()*1.35,15)],title="Recall (%)"), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        sec("⚖️ Compromis Faux Positifs vs Recall ZD","Le coin idéal = haut + à gauche")
        fig = px.scatter(df, x='fp_day', y='zd_recall', size='fbeta2',
            color='Model_short', text='Model_short',
            color_discrete_sequence=[_accent,_green,_gold,_red,_purple],
            hover_data={'f1_known':True,'fbeta2':True})
        fig.update_traces(textposition='top center',
            marker=dict(sizemin=12,line=dict(width=1,color='rgba(255,255,255,0.15)')))
        fig.update_layout(**PLOTLY,
            title="FP/jour ↓ vs Recall ZD ↑  |  Taille = Fβ(2)",
            xaxis=dict(autorange='reversed',title="Faux Positifs / jour (↓ mieux)"),
            yaxis_title="Recall Zero-Day % (↑ mieux)")
        st.plotly_chart(fig, use_container_width=True)

        sec("🕸️ Radar Multi-Critères")
        cats = ['F1 Connus','Recall ZD','Fβ(2)','FP Score (inv.)']
        fig = go.Figure()
        palette = [_accent,_green,_gold,_red,_purple]
        for i,(_, row) in enumerate(df.iterrows()):
            fp_i = max(0,100-row['fp_day']/max(df['fp_day'].max(),1)*100)
            v = [row['f1_known'],row['zd_recall'],row['fbeta2'],fp_i]
            name = row.get('Model_short', row['Modele'])
            fig.add_trace(go.Scatterpolar(r=v+[v[0]],theta=cats+[cats[0]],
                name=name,fill='toself',opacity=0.55,
                line=dict(color=palette[i%len(palette)],width=2)))
        fig.update_layout(**PLOTLY,
            polar=dict(bgcolor=T('rgba(13,17,18,0.8)','rgba(248,249,251,0.8)'),
                       radialaxis=dict(visible=True,range=[0,100],
                                       gridcolor=T('rgba(48,54,61,0.5)','rgba(209,213,219,0.5)'),
                                       tickfont=dict(size=8)),
                       angularaxis=dict(gridcolor=T('rgba(48,54,61,0.5)','rgba(209,213,219,0.5)'))),
            title="Profil multi-critères par modèle",
            legend=dict(bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("dashboard_data.csv non disponible.")

# ═══════════════════════════════════════════════════════════
# PAGE 3 — LATENCE
# ═══════════════════════════════════════════════════════════
elif page == "⚡ Latence Temps-Réel":
    sec("⚡ Latence Temps-Réel (Throughput)","Vitesse de détection en flux par seconde — Prêt pour la Production ?")

    st.markdown(f"""
    <div class="info-banner">
    ℹ️ <b>Contexte SOC (Security Operations Center) :</b><br>
    Un modèle qui détecte tout mais qui traite 10 flux par seconde va créer un <b>goulot d'étranglement</b>.
    L'inférence doit être ultra-rapide (faible latence) pour du traitement en temps réel (streaming).
    </div>""", unsafe_allow_html=True)

    if bench and any('flows_per_sec' in v for v in bench.values()):
        _speed_data = [(mn, kv['flows_per_sec']) for mn, kv in bench.items()
                       if 'flows_per_sec' in kv and kv['flows_per_sec'] > 0]

        if _speed_data:
            _speed_data.sort(key=lambda x: x[1], reverse=True)
            names = [x[0] for x in _speed_data]
            speeds = [x[1] for x in _speed_data]

            # Gauge for fastest and GAT
            g1, g2 = st.columns(2)
            with g1:
                _max_spd = max(speeds)
                fig_g = go.Figure(go.Indicator(
                    mode="gauge+number", value=_max_spd,
                    title={"text": f"⚡ Plus rapide : {names[0]}", "font": {"size": 13, "color": T("#c9d1d9","#374151")}},
                    number={"font": {"size": 32, "color": _accent2}, "suffix": " f/s"},
                    gauge={"axis": {"range": [0, _max_spd*1.2]}, "bar": {"color": _accent2},
                           "bgcolor": T("#161b22","#f3f4f6"), "borderwidth": 0}))
                fig_g.update_layout(**{k:v for k,v in PLOTLY.items() if k!='margin'}, height=250, margin=dict(l=30,r=30,t=60,b=10))
                st.plotly_chart(fig_g, use_container_width=True)
            with g2:
                _gat_names = [n for n in names if 'GAT' in n]
                _gat_spd = dict(_speed_data).get(_gat_names[0], 0) if _gat_names else 0
                fig_g2 = go.Figure(go.Indicator(
                    mode="gauge+number", value=_gat_spd,
                    title={"text": "🕸️ GAT Hybrid", "font": {"size": 13, "color": T("#c9d1d9","#374151")}},
                    number={"font": {"size": 32, "color": _green}, "suffix": " f/s"},
                    gauge={"axis": {"range": [0, _max_spd*1.2]}, "bar": {"color": _green},
                           "bgcolor": T("#161b22","#f3f4f6"), "borderwidth": 0}))
                fig_g2.update_layout(**{k:v for k,v in PLOTLY.items() if k!='margin'}, height=250, margin=dict(l=30,r=30,t=60,b=10))
                st.plotly_chart(fig_g2, use_container_width=True)

            fig = go.Figure(go.Bar(
                x=names, y=speeds,
                marker=dict(color=[_accent2 if 'GAT' not in n else _green for n in names],
                            line=dict(color='rgba(255,255,255,0.1)',width=1)),
                text=[f"{v:,} f/s" for v in speeds], textposition='auto'))
            fig.update_layout(**PLOTLY,title="🚀 Débit d'inférence (Flux réseau analysés / seconde)",
                yaxis=dict(title="Vitesse (↑ mieux)"), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

            sec("🏆 Analyse des performances de production")
            fastest = speeds[0]
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div class="verdict-ok">
                    <div style="font-size:16px;font-weight:700;color:{_green};margin-bottom:10px;">
                        ⚡ Vitesse Maximale : {names[0]}
                    </div>
                    <div style="font-family:'JetBrains Mono';font-size:13px;color:{T('#c9d1d9','#374151')};line-height:2;">
                        Débit : <b style="color:{_green};">{fastest:,} flux/sec</b><br>
                        Idéal pour : Réseaux Gigabit, sans état (stateless).
                    </div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="glow-card">
                    <div style="font-size:16px;font-weight:700;color:{_accent};margin-bottom:10px;">
                        🕸️ Vitesse du GAT Hybrid
                    </div>
                    <div style="font-family:'JetBrains Mono';font-size:13px;color:{T('#c9d1d9','#374151')};line-height:2;">
                        Débit : <b style="color:{_accent};">{_gat_spd:,} flux/sec</b><br>
                        Compromis : Tolérable pour les réseaux d'entreprise moyens.
                    </div>
                </div>""", unsafe_allow_html=True)
    else:
        st.info("Aucune donnée de vitesse trouvée.")


# ═══════════════════════════════════════════════════════════
# PAGE 4 — CAS ZERO-DAY
# ═══════════════════════════════════════════════════════════
elif page == "🎯 Cas Zero-Day":
    sec("🎯 Cas Zero-Day — DoS Slowhttptest","Rapport d'incident complet style ticket SIEM")

    alert  = soc.get('alert',  {'alert_id':'IDS-2017-004821','timestamp':'2017-07-05 14:32:07','src_ip':'192.168.10.50','dst_ip':'192.168.10.3','dst_port':80,'protocol':'HTTP/TCP'})
    verdict= soc.get('verdict', {'xgb_pred':'BENIGN','xgb_conf':0.98,'gat_ood':True,'true_class':'DoS Slowhttptest'})
    mitre  = soc.get('mitre',  {'id':'T1499.002','name':'Service Exhaustion Flood','tactic':'Impact'})
    indics = soc.get('indicators', [])

    st.markdown(f"""
    <div class="incident-card">
        <div class="incident-header">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <span style="font-family:'Orbitron';font-size:15px;color:{_red};font-weight:700;">
                        🚨 ALERTE CRITIQUE — ATTAQUE ZERO-DAY DÉTECTÉE
                    </span>
                    <div style="font-family:'JetBrains Mono';font-size:11px;color:{_sub};margin-top:5px;">
                        ID : {alert.get('alert_id','')}  ·  {alert.get('timestamp','')}
                    </div>
                </div>
                <span class="badge b-red" style="font-size:13px;padding:6px 16px;">CRITIQUE</span>
            </div>
        </div>
        <div class="incident-body">
            <table class="dark-table">
                <tr><th>Champ</th><th>Valeur</th><th>Statut</th></tr>
                <tr><td>IP Source</td><td><code style="color:{_accent};">{alert.get('src_ip','')}</code></td>
                    <td><span class="badge b-red">🔴 BLOQUÉE</span></td></tr>
                <tr><td>IP Destination</td><td><code style="color:{T('#c9d1d9','#374151')};">{alert.get('dst_ip','')}:{alert.get('dst_port',80)}</code></td>
                    <td><span class="badge b-cyan">Victime protégée</span></td></tr>
                <tr><td>Protocole</td><td>{alert.get('protocol','')}</td><td></td></tr>
                <tr><td>Vraie nature</td><td><b style="color:{_red};">{verdict.get('true_class','')}</b></td>
                    <td><span class="badge b-gold">Zero-Day</span></td></tr>
                <tr><td>MITRE ATT&CK</td><td><b style="color:{_gold};">{mitre.get('id','')}</b> — {mitre.get('name','')}</td>
                    <td><span class="badge b-gold">{mitre.get('tactic','')}</span></td></tr>
            </table>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    xgb_c = verdict.get('xgb_conf', 0.98)
    with c1:
        st.markdown(f"""
        <div class="verdict-fail">
            <div style="font-size:16px;font-weight:700;color:{_red};margin-bottom:10px;">
                ❌ XGBoost — Diagnostic ERRONÉ
            </div>
            <div style="font-family:'JetBrains Mono';font-size:13px;color:{T('#c9d1d9','#374151')};line-height:2;">
                Prédiction : <b style="color:{_red};">{verdict.get('xgb_pred','BENIGN')}</b><br>
                Confiance  : <b style="color:{_red};">{xgb_c:.1%}</b> ← fausse certitude<br>
                Raison     : Volume faible → ressemble à du trafic normal<br>
                Résultat   : Attaque non détectée (Recall ZD ≈ 0%)
            </div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="verdict-ok">
            <div style="font-size:16px;font-weight:700;color:{_green};margin-bottom:10px;">
                ✅ GAT — Détection correcte (OOD)
            </div>
            <div style="font-family:'JetBrains Mono';font-size:13px;color:{T('#c9d1d9','#374151')};line-height:2;">
                Signal     : <b style="color:{_accent};">Out-of-Distribution</b><br>
                Mécanisme  : Pas de voisins typiques dans le graphe<br>
                Attention  : Diffuse → incertitude topologique<br>
                Résultat   : Attaque détectée → alerte SOC L2
            </div>
        </div>""", unsafe_allow_html=True)

    # Confidence comparison gauge
    sec("📊 Comparaison de Confiance", "XGBoost vs GAT — Qui a raison ?")
    gc1, gc2 = st.columns(2)
    with gc1:
        fig_xgb = go.Figure(go.Indicator(
            mode="gauge+number", value=xgb_c*100,
            title={"text": "❌ XGBoost Confiance (ERRONÉ)", "font": {"size": 12, "color": _red}},
            number={"suffix": "%", "font": {"size": 28, "color": _red}},
            gauge={"axis": {"range": [0, 100]}, "bar": {"color": _red},
                   "bgcolor": T("#161b22","#f3f4f6"), "borderwidth": 0}))
        fig_xgb.update_layout(**{k:v for k,v in PLOTLY.items() if k!='margin'}, height=220, margin=dict(l=30,r=30,t=60,b=10))
        st.plotly_chart(fig_xgb, use_container_width=True)
    with gc2:
        fig_gat = go.Figure(go.Indicator(
            mode="gauge+number", value=95.8,
            title={"text": "✅ GAT OOD Score", "font": {"size": 12, "color": _green}},
            number={"suffix": "%", "font": {"size": 28, "color": _green}},
            gauge={"axis": {"range": [0, 100]}, "bar": {"color": _green},
                   "bgcolor": T("#161b22","#f3f4f6"), "borderwidth": 0}))
        fig_gat.update_layout(**{k:v for k,v in PLOTLY.items() if k!='margin'}, height=220, margin=dict(l=30,r=30,t=60,b=10))
        st.plotly_chart(fig_gat, use_container_width=True)

    if indics:
        sec("🔍 Indicateurs réseau suspects","Analyse comportementale du flux")
        rows = ""
        for ind in indics:
            lvl = ind.get('level','')
            bc  = 'b-red' if '🔴' in lvl else 'b-gold' if '🟠' in lvl else 'b-blue' if '🟡' in lvl else 'b-green'
            rows += f"""<tr>
                <td>{ind.get('label','')}</td>
                <td><code style="color:{_accent};">{ind.get('value','')}</code></td>
                <td><code style="color:{_sub};">{ind.get('reference','')}</code></td>
                <td><span class="badge {bc}">{ind.get('level','')[:12].strip()}</span></td>
                <td style="color:{_sub};font-size:11px;">{ind.get('interpretation','')}</td>
            </tr>"""
        st.markdown(f"""
        <table class="dark-table">
            <tr><th>Indicateur réseau</th><th>Ce flux</th><th>Réf. normal</th><th>Niveau alerte</th><th>Interprétation SOC</th></tr>
            {rows}
        </table>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sec("🛠️ Actions recommandées")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="glow-card">
            <div style="color:{_red};font-weight:700;margin-bottom:12px;">⚡ Réponse immédiate (L1)</div>
            <ul style="color:{T('#c9d1d9','#374151')};font-size:13px;line-height:2;margin:0;">
                <li>Bloquer IP source <code style="color:{_accent};">192.168.10.50</code></li>
                <li>Escalader ticket vers analyste L2</li>
                <li>Capturer PCAP du flux (Wireshark)</li>
                <li>Documenter l'incident (JIRA/ServiceNow)</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="glow-card">
            <div style="color:{_gold};font-weight:700;margin-bottom:12px;">🔬 Investigation (L2)</div>
            <ul style="color:{T('#c9d1d9','#374151')};font-size:13px;line-height:2;margin:0;">
                <li>Analyser PCAP avec <code>tcp.window_size</code> dans Wireshark</li>
                <li>Scanner segment <code>192.168.10.0/24</code></li>
                <li>Créer règle Snort : Win TCP &gt; 60000 + durée &gt; 60s</li>
                <li>Ajouter IOC dans le SIEM (IP + signature TCP)</li>
            </ul>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE 5 — POURQUOI LE GAT
# ═══════════════════════════════════════════════════════════
elif page == "🧠 Pourquoi le GAT ?":
    sec("🧠 Pourquoi le GAT détecte ce que les autres ratent ?","Explication intuitive de la topologie de graphe")

    st.markdown(f"""
    <div class="glow-card" style="margin:16px 0;">
        <div style="font-family:'JetBrains Mono';font-size:13px;color:{T('#c9d1d9','#374151')};line-height:2.2;">
        <b style="color:{_accent};">Modèles classiques (RF, XGB, MLP)</b><br>
        → Analysent chaque flux <b>de façon isolée</b><br>
        → Regardent uniquement : volume ? débit ? taille des paquets ?<br>
        → Pour le Slowhttptest : volume faible + petits paquets = <b style="color:{_red};">ressemble à du BENIGN → ÉCHO</b><br><br>
        <b style="color:{_green};">GAT (Graph Attention Network)</b><br>
        → Représente chaque flux comme un <b>nœud dans un graphe</b><br>
        → Chaque nœud regarde ses <b>K=4 voisins les plus similaires</b><br>
        → Un flux Zero-Day : ses voisins ne se ressemblent pas → <b style="color:{_accent};">attention diffuse</b><br>
        → Signal : "Je ne ressemble à aucune classe connue" = <b style="color:{_gold};">OOD → ALERTE</b>
        </div>
    </div>""", unsafe_allow_html=True)

    # Network topology simulation with Plotly
    sec("🕸️ Topologie du Graphe KNN", "Visualisation interactive : Trafic bénin (dense) vs Zero-Day (isolé)")

    np.random.seed(123)
    # Generate cluster positions
    n_benign, n_atk, n_zd = 40, 12, 6
    bx = np.random.normal(0, 1.2, n_benign)
    by = np.random.normal(0, 1.2, n_benign)
    ax = np.random.normal(3.5, 0.6, n_atk)
    ay = np.random.normal(0.5, 0.6, n_atk)
    zx = np.random.normal(-2, 0.3, n_zd)
    zy = np.random.normal(3.5, 0.3, n_zd)

    all_x = np.concatenate([bx, ax, zx])
    all_y = np.concatenate([by, ay, zy])
    node_types = ["BENIGN"]*n_benign + ["Attaque Connue"]*n_atk + ["ZERO-DAY"]*n_zd
    node_colors = [_green]*n_benign + [_gold]*n_atk + [_red]*n_zd
    node_sizes = [10]*n_benign + [14]*n_atk + [18]*n_zd

    # Generate edges (KNN-style within clusters)
    edge_x, edge_y = [], []
    for i in range(len(all_x)):
        dists = np.sqrt((all_x - all_x[i])**2 + (all_y - all_y[i])**2)
        dists[i] = 999
        neighbors = np.argsort(dists)[:4]
        for j in neighbors:
            if dists[j] < 2.5:
                edge_x += [all_x[i], all_x[j], None]
                edge_y += [all_y[i], all_y[j], None]

    fig_net = go.Figure()
    fig_net.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines',
        line=dict(width=0.5, color=T('rgba(0,191,179,0.15)','rgba(0,119,182,0.12)')),
        hoverinfo='none'))

    for ntype, color, size in [("BENIGN", _green, 10), ("Attaque Connue", _gold, 14), ("ZERO-DAY", _red, 18)]:
        mask = [t == ntype for t in node_types]
        fig_net.add_trace(go.Scatter(
            x=all_x[mask], y=all_y[mask], mode='markers',
            marker=dict(size=size, color=color, line=dict(width=1.5, color='rgba(255,255,255,0.3)'),
                        symbol='circle'),
            name=ntype, hovertemplate=f"{ntype}<br>x: %{{x:.2f}}<br>y: %{{y:.2f}}<extra></extra>"))
    fig_net.update_layout(**PLOTLY, height=450,
        title="Graphe KNN — Clusters de Flux Réseau",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        legend=dict(bgcolor='rgba(0,0,0,0)'))
    # Add annotations
    fig_net.add_annotation(x=0, y=-2.5, text="Cluster BENIGN<br>(dense, bien connecté)",
        font=dict(color=_green, size=11), showarrow=False)
    fig_net.add_annotation(x=3.5, y=-1.2, text="Cluster Attaque<br>(séparé mais connecté)",
        font=dict(color=_gold, size=11), showarrow=False)
    fig_net.add_annotation(x=-2, y=4.8, text="⚠️ ZERO-DAY<br>(isolé, peu de voisins)",
        font=dict(color=_red, size=11), showarrow=False)
    st.plotly_chart(fig_net, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="kpi-card" style="text-align:left;padding:20px;">
            <div style="font-size:20px;margin-bottom:10px;">📐</div>
            <div style="color:{_accent};font-weight:700;margin-bottom:8px;">Construction du graphe</div>
            <div style="font-size:12px;color:{_sub};line-height:1.8;">
                • PCA → espace 15D<br>• KNN → K=4 voisins<br>• Seuil distance (médiane)<br>• Graphe : Train + Test
            </div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card" style="text-align:left;padding:20px;">
            <div style="font-size:20px;margin-bottom:10px;">👁️</div>
            <div style="color:{_green};font-weight:700;margin-bottom:8px;">Mécanisme d'attention</div>
            <div style="font-size:12px;color:{_sub};line-height:1.8;">
                • Chaque voisin reçoit un poids (0→1)<br>• Voisin similaire → poids élevé<br>• ZD : distribution atypique<br>• Signal OOD naturel
            </div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card" style="text-align:left;padding:20px;">
            <div style="font-size:20px;margin-bottom:10px;">📊</div>
            <div style="color:{_gold};font-weight:700;margin-bottom:8px;">Preuve expérimentale</div>
            <div style="font-size:12px;color:{_sub};line-height:1.8;">
                • MLP = mêmes neurones que GAT<br>• MLP sans graphe → Recall ZD ≈ 0%<br>• GAT avec graphe → Recall ZD &gt; 50%<br>• Δ = topologie
            </div>
        </div>""", unsafe_allow_html=True)

    if bench:
        sec("Preuve chiffrée : MLP vs GAT")
        mlp_zd = bench.get('MLP (No Graph)', {}).get('zd_recall', 0)
        gat_vals = [(k,v['zd_recall']) for k,v in bench.items() if 'GAT' in k or 'gat' in k.lower()]
        gat_zd = max(v for _,v in gat_vals) if gat_vals else 0
        delta = gat_zd - mlp_zd
        st.markdown(f"""
        <div class="glow-card" style="font-family:'JetBrains Mono';font-size:14px;line-height:2.2;">
        🧪 MLP (sans graphe)  : Recall ZD = <b style="color:{_red};">{mlp_zd:.1f}%</b><br>
        🕸️ GAT (avec graphe)  : Recall ZD = <b style="color:{_green};">{gat_zd:.1f}%</b><br>
        ──────────────────────────────────<br>
        📈 Gain pur du graphe : <b style="color:{_accent};">+{delta:.1f}%</b>
        {"→ La topologie contribue significativement ✅" if delta > 5 else "→ Contribution modérée ⚠️"}
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE 6 — XAI AVANCÉ
# ═══════════════════════════════════════════════════════════
elif page == "🔬 XAI Avancé":
    sec("🔬 XAI Avancé — Pour Data Scientists","SHAP, Attention GAT, Comparaison XGB vs GAT")

    tab1,tab2,tab3,tab4 = st.tabs(["📊 SHAP Global RF","📊 SHAP Global XGB","🔎 Waterfall Local","🕸️ Attention & Comparaison"])

    with tab1:
        st.markdown("#### Random Forest — Importance globale des features")
        st.markdown(f"""<div class="info-banner">
            📘 Le beeswarm montre l'impact de chaque feature sur la prédiction.
            La couleur = valeur de la feature (rouge = élevé). Les features liées au trafic retour (Backward) dominent.
            </div>""", unsafe_allow_html=True)
        img("xai_shap_rf.png", "SHAP Global RF")

    with tab2:
        st.markdown("#### XGBoost — Importance globale des features")
        st.markdown(f"""<div class="info-banner">
            📘 XGBoost utilise les features volumétriques ET protocolaires (Fenêtre TCP initiale, IAT).
            C'est cette combinaison qui lui permet d'atteindre 99.8% de F1 sur les classes connues.
            </div>""", unsafe_allow_html=True)
        img("xai_shap_xgb.png", "SHAP Global XGB")

    with tab3:
        c1,c2 = st.columns(2)
        with c1:
            st.markdown("##### 🔴 Flux Zero-Day")
            st.markdown(f"""<div style="background:{T('rgba(248,81,73,0.08)','rgba(230,57,70,0.06)')};border:1px solid {T('rgba(248,81,73,0.25)','rgba(230,57,70,0.2)')};
                border-radius:8px;padding:10px 14px;font-size:12px;color:{_red};margin-bottom:12px;">
                ⚠️ XGBoost prédit BENIGN à 98% de confiance. Les features "faible volume" poussent vers BENIGN.
                </div>""", unsafe_allow_html=True)
            img("xai_shap_xgb_local_zd.png","Waterfall — Flux Zero-Day")
        with c2:
            st.markdown("##### ✅ Flux connu (attaque)")
            st.markdown(f"""<div style="background:{T('rgba(63,185,80,0.08)','rgba(45,157,58,0.06)')};border:1px solid {T('rgba(63,185,80,0.25)','rgba(45,157,58,0.2)')};
                border-radius:8px;padding:10px 14px;font-size:12px;color:{_green};margin-bottom:12px;">
                ✅ Contributions SHAP cohérentes → confiance maximale, diagnostic correct.
                </div>""", unsafe_allow_html=True)
            img("xai_shap_xgb_local_known.png","Waterfall — Flux Connu")

    with tab4:
        c1,c2 = st.columns(2)
        with c1:
            st.markdown("##### 🕸️ Distribution d'attention GAT")
            st.markdown(f"""<div style="background:{T('rgba(210,153,34,0.08)','rgba(230,168,23,0.06)')};border:1px solid {T('rgba(210,153,34,0.25)','rgba(230,168,23,0.2)')};
                border-radius:8px;padding:10px 14px;font-size:12px;color:{_gold};margin-bottom:12px;">
                ⚠️ Le Zero-Day a une attention très diffuse — pas de correspondance franche.
                C'est ce signal d'incertitude topologique qui déclenche le flag OOD.
                </div>""", unsafe_allow_html=True)
            img("xai_gat_attention.png","Attention Weights GAT")
        with c2:
            st.markdown("##### 📈 Comparaison XGB vs GAT sur 10 ZD")
            st.markdown(f"""<div class="info-banner">
                🔵 XGB : confiance élevée même sur ZD (entropie basse = aveugle).
                GAT : entropie typiquement plus élevée sur ZD → meilleur signal OOD.
                </div>""", unsafe_allow_html=True)
            img("xai_comparison_zd.png","Heatmap XGB vs GAT — 10 ZD")

        # Simulated attention heatmap
        sec("🔥 Heatmap Attention GAT — Simulation", "Distribution des poids d'attention par classe voisine")
        np.random.seed(77)
        classes = ["BENIGN","DoS Hulk","DoS GoldenEye","Heartbleed","PortScan"]
        data_hm = np.random.dirichlet(np.ones(5)*0.5, size=8)
        fig_hm = go.Figure(go.Heatmap(
            z=data_hm, x=classes, y=[f"Flux #{i}" for i in range(8)],
            colorscale=T("Viridis","Blues"), text=np.round(data_hm,3), texttemplate="%{text:.3f}"))
        fig_hm.update_layout(**PLOTLY, height=320, title="Poids d'attention conv1 (simulé)")
        st.plotly_chart(fig_hm, use_container_width=True)

# ═══════════════════════════════════════════════════════════
# PAGE 7 — ANALYSE SOC
# ═══════════════════════════════════════════════════════════
elif page == "🛡️ Analyse SOC":
    sec("🛡️ Analyse SOC — Profil de trafic & Radar de menace","Visualisations pour analyste réseau")

    st.markdown(f"""<div style="background:{T('rgba(210,153,34,0.08)','rgba(230,168,23,0.06)')};border:1px solid {T('rgba(210,153,34,0.25)','rgba(230,168,23,0.2)')};
        border-radius:8px;padding:14px 18px;font-size:13px;color:{_gold};margin-bottom:12px;">
    ⚠️ <b>Pourquoi le Zero-Day est invisible pour XGBoost ?</b><br>
    Le Slowhttptest envoie de <b>très petits paquets</b> à <b>très faible débit</b> — signature similaire au trafic légitime.
    Seules la <b>durée anormalement longue</b> et la <b>fenêtre TCP atypique</b> trahissent l'attaque.
    </div>""", unsafe_allow_html=True)
    img("xai_traffic_profile.png","Profil de trafic — Normal vs Attaque connue vs Zero-Day")

    st.markdown("### 🕸️ SOC Threat Radar — Dangerosité par axe de menace")
    st.markdown(f"""<div class="info-banner">
    📡 <b>Lecture du radar :</b><br>
    • <b>Volume</b> : ZD bas → pas volumétrique · <b>Débit</b> : ZD faible → furtive<br>
    • <b>Temporalité</b> : ZD élevé → connexion longue ← <b>signal principal</b><br>
    • <b>Protocole TCP</b> : ZD élevé → fenêtre anormale ← <b>signature outil</b>
    </div>""", unsafe_allow_html=True)
    img("xai_threat_radar.png","SOC Threat Radar")

    # Simulated threat radar
    sec("📡 Radar de Menace — Simulation Interactive")
    cats_r = ["Volume","Débit","Temporalité","Protocole TCP","Régularité"]
    fig_r = go.Figure()
    fig_r.add_trace(go.Scatterpolar(r=[20,15,85,90,55,20], theta=cats_r+[cats_r[0]],
        fill='toself', name='Zero-Day', line=dict(color=_red,width=2), opacity=0.6))
    fig_r.add_trace(go.Scatterpolar(r=[90,85,30,40,70,90], theta=cats_r+[cats_r[0]],
        fill='toself', name='DoS Hulk (connu)', line=dict(color=_gold,width=2), opacity=0.5))
    fig_r.add_trace(go.Scatterpolar(r=[10,10,15,20,10,10], theta=cats_r+[cats_r[0]],
        fill='toself', name='BENIGN', line=dict(color=_green,width=2), opacity=0.4))
    fig_r.update_layout(**PLOTLY, height=400, title="Profil de menace multi-axes",
        polar=dict(bgcolor=T('rgba(13,17,18,0.8)','rgba(248,249,251,0.8)'),
                   radialaxis=dict(visible=True,range=[0,100])),
        legend=dict(bgcolor='rgba(0,0,0,0)'))
    st.plotly_chart(fig_r, use_container_width=True)

    sec("🏷️ Mapping MITRE ATT&CK")
    mitre = soc.get('mitre', {'id':'T1499.002','name':'Service Exhaustion Flood','tactic':'Impact'})
    st.markdown(f"""
    <table class="dark-table">
        <tr><th>Technique ID</th><th>Nom</th><th>Tactique</th><th>Outil</th><th>Plateforme</th></tr>
        <tr>
            <td><b style="color:{_gold};">{mitre.get('id','')}</b></td>
            <td>{mitre.get('name','')}</td>
            <td><span class="badge b-red">{mitre.get('tactic','')}</span></td>
            <td>Slowhttptest, Slowloris, R-U-Dead-Yet</td>
            <td>Windows, Linux, macOS</td>
        </tr>
    </table>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE 8 — GÉNÉRALISATION
# ═══════════════════════════════════════════════════════════
elif page == "🌐 Généralisation":
    st.markdown(f'<div class="hero-title" style="font-size:26px">🌐 Test de Généralisation Multi-Jour</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:{_sub};font-size:14px;margin-bottom:24px;">Entraîné sur Wednesday (DoS) · Testé sur Thursday & Friday (attaques jamais vues)</div>', unsafe_allow_html=True)

    _gen_file = "generalisation_results.json"
    if not os.path.exists(_gen_file):
        st.warning("⚠️ Résultats de généralisation non trouvés. Exécutez le volet Généralisation dans le notebook.")
    else:
        _gen_data = json.load(open(_gen_file))

        st.markdown(f"""
        <div class="glow-card" style="margin-bottom:20px;">
        <b style="color:{_accent};">🎯 Objectif :</b>
        <span style="color:{T('#c9d1d9','#374151')};">Le modèle est entraîné uniquement sur Wednesday (DoS).
        On l'expose à des attaques de familles différentes pour mesurer sa capacité de généralisation.</span><br><br>
        <b style="color:{_accent2};">Rappel OSI :</b>
        <span style="color:{_sub};">
        Thursday = Web Attacks (Layer 7) · Zone WAF |
        Friday = DDoS / PortScan (Layer 3-4) · Zone GAT
        </span>
        </div>""", unsafe_allow_html=True)

        _days_avail = list(_gen_data.keys())
        _day_sel = st.selectbox("Sélectionner le jour", [d.capitalize() for d in _days_avail], key="gen_day")
        _day_key = _day_sel.lower()
        _day_info = _gen_data[_day_key]
        _modeles  = _day_info["modeles"]
        _classes  = _day_info.get("classes", [])
        _n_atk    = _day_info.get("n_attaques", 0)
        _n_ben    = _day_info.get("n_benign", 0)
        _atk_types = [c for c in _classes if c.upper() != "BENIGN"]
        _atk_join  = ", ".join(_atk_types[:2])
        _osi_layer = "Layer 7 (WAF)" if _day_key == "thursday" else "Layer 3-4 (IDS)"
        _osi_sub   = "Hors perimetre GAT" if _day_key == "thursday" else "Perimetre GAT"

        k1,k2,k3,k4 = st.columns(4)
        with k1: st.markdown(kpi("🚨","Attaques inedites",f"{_n_atk:,}","red","jamais vues"), unsafe_allow_html=True)
        with k2: st.markdown(kpi("✅","Trafic BENIGN",f"{_n_ben:,}","green","reference FP"), unsafe_allow_html=True)
        with k3: st.markdown(kpi("🏷️","Types d attaques",f"{len(_atk_types)}","cyan",_atk_join), unsafe_allow_html=True)
        with k4: st.markdown(kpi("⚠️","Couche OSI",_osi_layer,"gold",_osi_sub), unsafe_allow_html=True)

        st.markdown("---")
        sec("📋 Tableau de Performance SOC")
        _mdl_order = ["RF", "XGB", "MLP", "GAT+cns", "GAT+dist(P97)"]
        _mdl_info  = {
            "RF": ("RF","Entropie accidentelle",_accent2),
            "XGB": ("XGB","Entropie accidentelle",_gold),
            "MLP": ("MLP","Surconfiant / aveugle",_purple),
            "GAT+cns": ("GAT+consensus","OOD Intentionnel ✅",_green),
            "GAT+dist(P97)": ("GAT+distance","Adaptatif cross-domaine ✅","#a371f7"),
        }

        def _badge(v, metric):
            pct = f"{v:.1f}%"
            if metric == "det":
                if v >= 70: return '<span class="badge b-green">BON ' + pct + '</span>'
                if v >= 40: return '<span class="badge b-gold">MOYEN ' + pct + '</span>'
                return '<span class="badge b-red">FAIBLE ' + pct + '</span>'
            elif metric == "fp":
                if v <= 3:  return '<span class="badge b-green">OK ' + pct + '</span>'
                if v <= 10: return '<span class="badge b-gold">ATTENTION ' + pct + '</span>'
                return '<span class="badge b-red">ELEVE ' + pct + '</span>'
            elif metric == "prec":
                if v >= 80: return '<span class="badge b-green">FIABLE ' + pct + '</span>'
                if v >= 60: return '<span class="badge b-gold">PARTIEL ' + pct + '</span>'
                return '<span class="badge b-red">NON FIABLE ' + pct + '</span>'
            return pct

        _tbl = f"""<table class="dark-table"><thead><tr style="background:{_glow};">
          <th>Modele</th><th>Type Detection</th><th style="text-align:center;">Recall</th>
          <th style="text-align:center;">FP BENIGN</th><th style="text-align:center;">Precision</th>
        </tr></thead><tbody>"""
        for _mn in _mdl_order:
            if _mn not in _modeles: continue
            _d=_modeles[_mn].get("detection",0); _fp=_modeles[_mn].get("fp",0); _pr=_modeles[_mn].get("precision",0)
            _lbl,_type,_col = _mdl_info.get(_mn,(_mn,"","#fff"))
            _rbg = T("rgba(63,185,80,0.04)","rgba(45,157,58,0.04)") if "GAT" in _mn else "transparent"
            _tbl += (f'<tr style="border-bottom:1px solid {T("#21262d","#e5e7eb")};background:{_rbg};">'
                f'<td><b style="color:{_col};">{_lbl}</b></td><td style="color:{_sub};font-size:12px;">{_type}</td>'
                f'<td style="text-align:center;">{_badge(_d,"det")}</td>'
                f'<td style="text-align:center;">{_badge(_fp,"fp")}</td>'
                f'<td style="text-align:center;">{_badge(_pr,"prec")}</td></tr>')
        _tbl += "</tbody></table>"
        st.markdown(_tbl, unsafe_allow_html=True)

        st.markdown("---")
        sec("📈 Analyse Visuelle Comparative")
        _lp,_dp,_fpp,_prp,_cp = [],[],[],[],[]
        _cm = {"RF":_accent2,"XGB":_gold,"MLP":_purple,"GAT+cns":_green,"GAT+dist(P97)":"#a371f7"}
        for _mn in _mdl_order:
            if _mn not in _modeles: continue
            _lp.append(_mdl_info.get(_mn,(_mn,))[0])
            _dp.append(_modeles[_mn].get("detection",0)); _fpp.append(_modeles[_mn].get("fp",0))
            _prp.append(_modeles[_mn].get("precision",0)); _cp.append(_cm.get(_mn,"#fff"))
        c1,c2,c3 = st.columns(3)
        with c1:
            f1=go.Figure(go.Bar(x=_dp,y=_lp,orientation="h",marker_color=_cp,text=[f"{v:.1f}%" for v in _dp],textposition="outside"))
            f1.update_layout(**PLOTLY,title="Recall",xaxis_range=[0,120],height=280)
            st.plotly_chart(f1,use_container_width=True)
        with c2:
            f2=go.Figure(go.Bar(x=_fpp,y=_lp,orientation="h",marker_color=_cp,text=[f"{v:.1f}%" for v in _fpp],textposition="outside"))
            f2.update_layout(**PLOTLY,title="Faux Positifs",xaxis_range=[0,40],height=280)
            st.plotly_chart(f2,use_container_width=True)
        with c3:
            f3=go.Figure(go.Bar(x=_prp,y=_lp,orientation="h",marker_color=_cp,text=[f"{v:.1f}%" for v in _prp],textposition="outside"))
            f3.update_layout(**PLOTLY,title="Précision Alertes",xaxis_range=[0,120],height=280)
            st.plotly_chart(f3,use_container_width=True)

        st.markdown("---")
        sec("🧠 Interprétation SOC Automatique")
        if _day_key == "thursday":
            st.markdown(f"""
            <div class="verdict-fail">
            <b style="color:{_red};">⚠️ Hors périmètre IDS réseau</b><br><br>
            Les attaques Thursday (XSS, SQL Injection) opèrent au <b>Layer 7</b>.
            Elles nécessitent un <b style="color:{_gold};">WAF</b>. Ce n'est pas un échec du GAT.
            </div>
            <div class="verdict-ok">
            <b style="color:{_green};">✅ Architecture recommandée</b><br><br>
            <b>IDS GAT</b> → couches 3-4 | <b>WAF</b> → couche 7 | <b>SIEM</b> → corrélation
            </div>""", unsafe_allow_html=True)
        elif _day_key == "friday":
            _gat_d = _modeles.get("GAT+cns",{}).get("detection",0)
            _rf_d = _modeles.get("RF",{}).get("detection",0)
            _delta = _gat_d - _rf_d
            _vc = "verdict-ok" if _gat_d >= 70 else "verdict-fail"
            _vi = "✅" if _gat_d >= 70 else "⚠️"
            _vcol = _green if _gat_d >= 70 else _gold
            st.markdown(f"""
            <div class="{_vc}">
            <b style="color:{_vcol};">{_vi} Verdict Friday (DDoS / PortScan)</b><br><br>
            GAT+consensus : <b>{_gat_d:.1f}%</b> recall ({'+' if _delta>0 else ''}{_delta:.1f}% vs RF).
            </div>
            <div class="info-banner">
            <b style="color:{_accent2};">📌 Rappel :</b> Sur Wednesday (DoS Slowhttptest), le GAT atteint <b style="color:{_green};">~96% recall</b>.
            </div>""", unsafe_allow_html=True)

        if os.path.exists("generalisation_soc_dashboard.png"):
            st.markdown("---")
            sec("🖼️ Rapport Graphique Complet")
            st.image("generalisation_soc_dashboard.png", caption="Dashboard SOC — Généralisation Multi-Jour", use_container_width=True)

# ═══════════════════════════════════════════════════════════
# PAGE 9 — ARCHITECTURE
# ═══════════════════════════════════════════════════════════
elif page == "🏗️ Architecture":
    sec("🏗️ Architecture du Pipeline IDS","Vue d'ensemble du système de bout en bout")

    st.markdown(f"""
    <div class="glow-card" style="font-family:'JetBrains Mono';font-size:13px;line-height:2.3;color:{T('#c9d1d9','#374151')};">
    <span style="color:{_accent};font-weight:700;">① DONNÉES</span>  CICIDS2017 (Mercredi) — 80+ features réseau<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    <span style="color:{_green};font-weight:700;">② NETTOYAGE</span> 8 étapes : NaN, Inf, doublons, VarianceThreshold, StandardScaler<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    <span style="color:{_gold};font-weight:700;">③ SPLIT</span>  Train 60% / Val 20% / Test 20% — stratifié par classe<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓ <span style="color:{_red};">← Zero-Day retiré du Train</span><br>
    <span style="color:{_purple};font-weight:700;">④ PCA + KNN</span> PCA 15D → graphe KNN K=4<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    <span style="color:{_accent};font-weight:700;">⑤ ENTRAÎNEMENT</span><br>
    &nbsp;&nbsp;&nbsp;├── 🌲 Random Forest (200 arbres)<br>
    &nbsp;&nbsp;&nbsp;├── ⚡ XGBoost (300 estimateurs)<br>
    &nbsp;&nbsp;&nbsp;├── 🧠 MLP sans graphe (128 units)<br>
    &nbsp;&nbsp;&nbsp;└── <b style="color:{_green};">🕸️ GAT V5 Hybrid</b> (2 couches, skip, BatchNorm)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    <span style="color:{_gold};font-weight:700;">⑥ CALIBRATION OOD</span>  Seuils sur VAL<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    <span style="color:{_red};font-weight:700;">⑦ ÉVALUATION TEST</span>  F1 + Recall ZD + FP/jour + Fβ(2)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    <span style="color:{_purple};font-weight:700;">⑧ XAI</span>  SHAP + Attention GAT + Rapport SOC
    </div>""", unsafe_allow_html=True)

    # Architecture flow chart with Plotly
    sec("📐 Diagramme de Flux", "Pipeline de bout en bout visualisé")
    stages = ["Données<br>CICIDS2017","Nettoyage<br>8 étapes","Split<br>Train/Val/Test",
              "PCA+KNN<br>Graphe","Entraînement<br>4 Modèles","Calibration<br>OOD",
              "Évaluation<br>Test Final","XAI<br>SHAP+Attn"]
    stage_colors = [_accent, _green, _gold, _purple, _accent, _gold, _red, _purple]
    fig_flow = go.Figure()
    for i, (s, c) in enumerate(zip(stages, stage_colors)):
        fig_flow.add_trace(go.Scatter(
            x=[i], y=[0], mode='markers+text', text=[s], textposition='top center',
            marker=dict(size=40, color=c, line=dict(width=2, color='rgba(255,255,255,0.3)')),
            textfont=dict(size=10, color=T('#c9d1d9','#374151')), showlegend=False))
        if i < len(stages)-1:
            fig_flow.add_annotation(x=i+0.5, y=0, text="→", font=dict(size=20, color=_sub), showarrow=False)
    fig_flow.update_layout(**PLOTLY, height=200, title="Pipeline IDS — Flux de données",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, len(stages)-0.5]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.8, 1.2]))
    st.plotly_chart(fig_flow, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        sec("🌲 Modèles Tabulaires")
        st.markdown(f"""
        <div class="glow-card" style="font-size:13px;line-height:2;color:{T('#c9d1d9','#374151')};">
        <b style="color:{_accent2};">Random Forest :</b> 200 experts, vote majoritaire<br>
        → Robuste, interprétable, rapide<br>
        → Aveugle au contexte<br><br>
        <b style="color:{_accent2};">XGBoost :</b> Correcteurs successifs<br>
        → Meilleur F1 (≈99.8%)<br>
        → Sur-confiant face au ZD<br><br>
        <b style="color:{_accent2};">MLP :</b> Réseau de neurones <i>sans</i> graphe<br>
        → Preuve que les neurones seuls ne suffisent pas
        </div>""", unsafe_allow_html=True)
    with c2:
        sec("🕸️ GAT (Graph Attention Network)")
        st.markdown(f"""
        <div class="glow-card" style="font-size:13px;line-height:2;color:{T('#c9d1d9','#374151')};">
        <b style="color:{_accent};">Innovation :</b> Chaque flux = nœud dans un graphe KNN<br>
        → Le GAT agrège les voisins avec des <i>poids d'attention</i><br><br>
        <b style="color:{_accent};">Zero-Day :</b><br>
        → Voisins hétérogènes → attention diffuse<br>
        → Entropie élevée → Seuil OOD franchi → 🚨 ALERTE<br><br>
        <b style="color:{_accent};">+ Consensus RF/XGB :</b><br>
        → Réduit les faux positifs sans perte de ZD
        </div>""", unsafe_allow_html=True)


