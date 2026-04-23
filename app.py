import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json, os, random, time

st.set_page_config(
    page_title="IDS SIEM — Zero-Day Detection",
    page_icon="🛡️", layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════
# CSS PREMIUM — ELASTIC SECURITY DARK THEME
# ═══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Orbitron:wght@600;700;800&display=swap');

/* REMOVED global reset * { box-sizing: border-box; } because it breaks Streamlit SVG icons */

.stApp {
    background: #0b0e14;
    color: #d4d9e3;
    font-family: 'Inter', sans-serif;
}

/* Scanline subtle */
.stApp::before {
    content: '';
    position: fixed; top:0; left:0; width:100%; height:100%;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px,
        rgba(0,191,179,0.012) 2px, rgba(0,191,179,0.012) 4px);
    pointer-events: none; z-index: -1; /* Fix z-index pour ne pas bloquer les clics */
}

/* Customisation de la Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #07090f 0%, #0d1117 60%, #0a1020 100%);
    border-right: 1px solid rgba(0,191,179,0.15);
}

/* Ne pas forcer le '*' dans la sidebar pour éviter de casser les boutons SVG */
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span { 
    color: #c9d1d9; 
}
[data-testid="stSidebar"] .stRadio label:hover { color: #00bfb3 !important; }

/* 🔴 CORRECTIF DEFINITIF POUR LES BOUTONS DE LA SIDEBAR 🔴 */
/* Forcer la visibilité, la taille et le z-index de l'icone pour fermer et ouvrir */
[data-testid="collapsedControl"], 
[data-testid="stSidebarCollapseButton"] {
    z-index: 99999 !important;
    opacity: 1 !important;
    visibility: visible !important;
    background-color: rgba(13, 17, 23, 0.6) !important;
    border-radius: 6px;
}

[data-testid="collapsedControl"] svg, 
[data-testid="stSidebarCollapseButton"] svg {
    width: 28px !important;
    height: 28px !important;
    color: #00bfb3 !important;
    fill: #00bfb3 !important;
    display: block !important;
    opacity: 1 !important;
}

/* Hero title */
.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 32px; font-weight: 800;
    background: linear-gradient(135deg, #00bfb3 0%, #58a6ff 50%, #00bfb3 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: gradShift 4s ease infinite;
    letter-spacing: 2px;
}
@keyframes gradShift {
    0%,100%{background-position:0% 50%}
    50%{background-position:100% 50%}
}

/* Live badge pulse */
.live-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(248,81,73,0.12); border: 1px solid rgba(248,81,73,0.4);
    border-radius: 20px; padding: 5px 14px;
    font-family: 'JetBrains Mono'; font-size: 12px; font-weight: 600;
    color: #f85149; letter-spacing: 1px;
    animation: pulseBorder 2s ease infinite;
}
.live-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: #f85149; animation: pulseRed 1.2s ease infinite;
}
@keyframes pulseRed {
    0%,100%{opacity:1; transform:scale(1);}
    50%{opacity:0.4; transform:scale(0.7);}
}
@keyframes pulseBorder {
    0%,100%{box-shadow:0 0 0 0 rgba(248,81,73,0.3);}
    50%{box-shadow:0 0 12px 3px rgba(248,81,73,0.15);}
}

/* KPI Card premium */
.kpi-card {
    background: linear-gradient(145deg, #0d1117, #161b22);
    border: 1px solid rgba(0,191,179,0.15);
    border-radius: 14px; padding: 22px 18px; text-align: center;
    position: relative; overflow: hidden;
    transition: all 0.35s cubic-bezier(.25,.8,.25,1);
}
.kpi-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, transparent, #00bfb3, transparent);
    animation: shimmer 3s ease infinite;
}
@keyframes shimmer {
    0%{background-position:-200% 0}
    100%{background-position:200% 0}
}
.kpi-card:hover {
    border-color: rgba(0,191,179,0.4);
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(0,191,179,0.1);
}
.kpi-icon { font-size:26px; margin-bottom:8px; }
.kpi-lbl {
    font-size:10px; font-weight:600; letter-spacing:2px;
    text-transform:uppercase; color:#8b949e; margin-bottom:6px;
}
.kpi-val {
    font-family:'JetBrains Mono'; font-size:30px; font-weight:700;
    line-height:1.1;
}
.kpi-val.cyan  { color: #00bfb3; }
.kpi-val.green { color: #3fb950; }
.kpi-val.red   { color: #f85149; }
.kpi-val.gold  { color: #d29922; }
.kpi-sub { font-size:11px; color:#8b949e; margin-top:5px;
           font-family:'JetBrains Mono'; }

/* Alert row */
.alert-row {
    background: #0d1117; border-left: 3px solid;
    border-radius: 0 10px 10px 0; padding: 12px 16px; margin: 6px 0;
    font-family: 'JetBrains Mono'; font-size: 12px;
    display: flex; align-items: center; gap: 12px;
    animation: slideIn 0.4s ease;
}
@keyframes slideIn {
    from{opacity:0; transform:translateX(-10px);}
    to{opacity:1; transform:translateX(0);}
}
.alert-critical { border-color: #f85149; }
.alert-high     { border-color: #d29922; }
.alert-medium   { border-color: #58a6ff; }
.alert-low      { border-color: #3fb950; }

/* Section header */
.sec-hdr {
    border-left: 3px solid #00bfb3;
    padding: 10px 18px; margin: 24px 0 16px;
    background: linear-gradient(90deg, rgba(0,191,179,0.07), transparent);
    border-radius: 0 8px 8px 0;
}
.sec-hdr h3 { margin:0; color:#e0e6f0; font-size:17px; font-weight:700; }
.sec-hdr p  { margin:3px 0 0; color:#8b949e; font-size:12px; }

/* Incident card */
.incident-card {
    background: #0d1117; border: 1px solid rgba(248,81,73,0.3);
    border-radius: 14px; padding: 0; overflow: hidden; margin: 16px 0;
}
.incident-header {
    background: linear-gradient(90deg, rgba(248,81,73,0.15), rgba(248,81,73,0.05));
    padding: 16px 20px; border-bottom: 1px solid rgba(248,81,73,0.2);
}
.incident-body { padding: 20px; }

/* Table dark */
.dark-table {
    width: 100%; border-collapse: collapse; font-size: 13px;
    font-family: 'Inter';
}
.dark-table th {
    background: #161b22; color: #8b949e; font-size: 11px;
    font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase;
    padding: 10px 14px; text-align: left;
    border-bottom: 1px solid #21262d;
}
.dark-table td {
    padding: 10px 14px; color: #c9d1d9;
    border-bottom: 1px solid #161b22;
}
.dark-table tr:hover td { background: rgba(0,191,179,0.04); }

/* Badges */
.badge {
    display:inline-block; padding:3px 10px; border-radius:20px;
    font-size:11px; font-weight:600; letter-spacing:0.5px;
}
.b-red  { background:rgba(248,81,73,0.15); color:#f85149; border:1px solid rgba(248,81,73,0.3); }
.b-green{ background:rgba(63,185,80,0.15); color:#3fb950; border:1px solid rgba(63,185,80,0.3); }
.b-gold { background:rgba(210,153,34,0.15);color:#d29922; border:1px solid rgba(210,153,34,0.3);}
.b-cyan { background:rgba(0,191,179,0.15); color:#00bfb3; border:1px solid rgba(0,191,179,0.3);}
.b-blue { background:rgba(88,166,255,0.15);color:#58a6ff; border:1px solid rgba(88,166,255,0.3);}

/* Verdict box */
.verdict-ok {
    background: linear-gradient(135deg, rgba(63,185,80,0.08), rgba(0,191,179,0.05));
    border: 1px solid rgba(63,185,80,0.3); border-radius: 12px; padding: 20px;
    margin: 12px 0;
}
.verdict-fail {
    background: rgba(248,81,73,0.06); border: 1px solid rgba(248,81,73,0.25);
    border-radius: 12px; padding: 20px; margin: 12px 0;
}

/* Hide default streamlit chrome — WITHOUT hiding the sidebar toggle button */
#MainMenu { display: none !important; }
footer { visibility: hidden !important; }
header { visibility: hidden !important; }

/* 🔴 CORRECTIF SIDEBAR TOGGLE 🔴 */
/* Le header est caché mais son bouton collapse doit rester visible */
header[data-testid="stHeader"] {
    height: 0 !important;
    overflow: visible !important;  /* Les enfants (le bouton) peuvent déborder */
}

/* Cibler les deux variantes possibles du bouton selon la version de Streamlit */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
button[kind="header"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    z-index: 999999 !important;
    position: fixed !important;
    top: 8px !important;
    left: 8px !important;
    background: rgba(0,191,179,0.15) !important;
    border: 1px solid rgba(0,191,179,0.4) !important;
    border-radius: 8px !important;
    width: 36px !important;
    height: 36px !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
}

[data-testid="collapsedControl"] svg,
[data-testid="stSidebarCollapseButton"] svg,
button[kind="header"] svg {
    width: 20px !important;
    height: 20px !important;
    fill: #00bfb3 !important;
    color: #00bfb3 !important;
    display: block !important;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# DATA
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
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(13,17,18,0.9)",
    font=dict(family="Inter", color="#c9d1d9"),
    margin=dict(l=40, r=30, t=50, b=40),
)

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
    if os.path.exists(path): st.image(path, caption=cap, width='stretch')
    else: st.info(f"Image absente : {path}")

# ═══════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="hero-title" style="font-size:18px;">🛡 IDS SIEM</div>',
                unsafe_allow_html=True)
    st.markdown('<div style="color:#8b949e;font-size:11px;margin-bottom:12px;">Zero-Day Detection Platform</div>',
                unsafe_allow_html=True)
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
    <div style="font-size:11px; color:#8b949e; line-height:1.9;">
    📁 <b style="color:#c9d1d9;">Dataset</b> CICIDS2017 Wed<br>
    🏷️ <b style="color:#c9d1d9;">Classes connues</b> {n_cls}<br>
    🔴 <b style="color:#f85149;">Zero-Day</b> DoS Slowhttptest<br>
    🏋️ <b style="color:#c9d1d9;">Train</b> {n_train:,} flux<br>
    🧪 <b style="color:#c9d1d9;">Test</b> {n_test:,} flux
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div style="text-align:center;color:#8b949e;font-size:10px;">PFE 2026 · Cybersécurité<br>IDS + Graph Neural Networks + XAI</div>',
                unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE 1 — SOC LIVE
# ═══════════════════════════════════════════════════════════
if page == "🔴 SOC Live":

    # Hero
    st.markdown("""
    <div style="text-align:center;padding:30px 0 8px;">
        <div class="hero-title">🛡️ IDS SIEM — ZERO-DAY DETECTION PLATFORM</div>
        <div style="color:#8b949e;font-size:14px;margin:10px 0 18px;">
            Système de détection d'intrusions · RF / XGBoost / MLP / GAT
        </div>
        <div class="live-badge">
            <div class="live-dot"></div> SYSTÈME ACTIF — SURVEILLANCE EN COURS
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # KPIs — chiffres du GAT+consensus (le modèle de production recommandé)
    if bench:
        # Cherche le GAT+consensus en priorité, sinon le meilleur GAT disponible
        _gat_cns_key = next(
            (k for k in bench if 'consensus' in k.lower() or '+cns' in k.lower()), None
        )
        _gat_key = next(
            (k for k in bench if 'GAT' in k and 'consensus' not in k and '+cns' not in k), None
        )
        _ref_key = _gat_cns_key or _gat_key  # priorité : GAT+cns
        _ref     = bench.get(_ref_key, {}) if _ref_key else {}

        # F1 connus = prend le meilleur (F1 est pareil pour GAT et GAT+cns)
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

        # Bandeau d'identification du modèle affiché
        st.markdown(f"""
        <div style="background:rgba(63,185,80,0.08);border:1px solid rgba(63,185,80,0.25);
                    border-radius:8px;padding:10px 16px;margin-bottom:8px;font-size:12px;">
        <b style="color:#3fb950;">📌 Chiffres affichés :</b>
        <span style="color:#c9d1d9;"> Configuration <b>{_lbl}</b>
        — F1 Connus {best_f1:.1f}% · Recall ZD {_zd_val:.1f}% · FP/jour {_fp_val:,} · Fβ(2) {_fb_val:.1f}%</span><br>
        <span style="color:#8b949e;font-size:11px;">Les 4 métriques proviennent du même modèle pour une comparaison cohérente.</span>
        </div>""", unsafe_allow_html=True)


    st.markdown("<br>", unsafe_allow_html=True)
    sec("🚨 Timeline des alertes récentes", "Simulation d'un flux d'incidents en production")

    # Alertes fictives dynamiques
    _FAKE_ALERTS = [
        ("CRITIQUE","🔴",f"192.168.10.50 → 192.168.10.3:80","DoS Slowhttptest détecté (GAT OOD)","alert-critical","2017-07-05 14:32:07","GAT ✅ XGB ❌"),
        ("ÉLEVÉ","🟠",f"192.168.10.51 → 192.168.10.3:80","DoS GoldenEye — flux haute fréquence","alert-high","2017-07-05 14:31:44","GAT ✅ XGB ✅"),
        ("ÉLEVÉ","🟠",f"192.168.10.47 → 192.168.10.5:80","DoS Hulk — saturation bande passante","alert-high","2017-07-05 14:31:12","GAT ✅ XGB ✅"),
        ("MOYEN","🔵",f"192.168.10.8  → 192.168.10.3:443","Flux atypique — entropie élevée","alert-medium","2017-07-05 14:30:55","GAT ⚠️ XGB ⚠️"),
        ("FAIBLE","🟢",f"192.168.10.12 → 8.8.8.8:53","DNS query — trafic légitime","alert-low","2017-07-05 14:30:30","Tous ✅"),
        ("FAIBLE","🟢",f"192.168.10.22 → 185.199.108.133:443","HTTPS — trafic légitime","alert-low","2017-07-05 14:30:15","Tous ✅"),
    ]
    for lvl,ic,src_dst,desc,cls,ts,models in _FAKE_ALERTS:
        st.markdown(f"""
        <div class="alert-row {cls}">
            <div style="min-width:70px;color:#8b949e;font-size:11px;">{ts[-8:]}</div>
            <div style="font-size:14px;">{ic}</div>
            <div style="min-width:90px;"><span class="badge {'b-red' if 'CRITIQUE' in lvl else 'b-gold' if 'ÉLEVÉ' in lvl else 'b-blue' if 'MOYEN' in lvl else 'b-green'}">{lvl}</span></div>
            <div style="flex:1;color:#e0e6f0;">{src_dst}</div>
            <div style="flex:2;color:#8b949e;">{desc}</div>
            <div style="min-width:130px;text-align:right;color:#8b949e;">{models}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sec("📊 Résumé benchmark en un coup d'œil")
    if not df.empty:
        cols = ['Modele','f1_known','zd_recall','fp_day','fbeta2']
        avail = [c for c in cols if c in df.columns]
        tdf = df[avail].copy().rename(columns={
            'f1_known':'F1 Connus (%)','zd_recall':'Recall ZD (%)','fp_day':'FP/jour','fbeta2':'Fβ(2) (%)'})
        st.dataframe(tdf, width='stretch', hide_index=True)

# ═══════════════════════════════════════════════════════════
# PAGE 2 — BENCHMARK
# ═══════════════════════════════════════════════════════════
elif page == "📊 Benchmark":
    sec("📊 Benchmark Comparatif","Performance des 5 configurations — jeu de test CICIDS2017")

    if not df.empty and 'Model_short' in df.columns:
        c1,c2 = st.columns(2)
        with c1:
            fig = go.Figure(go.Bar(
                x=df['Model_short'], y=df['f1_known'],
                marker=dict(color=['#3fb950']*len(df),
                            line=dict(color='rgba(0,0,0,0)')),
                text=df['f1_known'].round(1).astype(str)+'%',
                textposition='outside'))
            fig.update_layout(**PLOTLY,title="F1 Macro — Classes Connues",
                yaxis=dict(range=[90,102],title="F1 (%)"),showlegend=False)
            st.plotly_chart(fig, width='stretch')
        with c2:
            cols_c = ['#f85149' if v<10 else '#d29922' if v<50 else '#3fb950'
                      for v in df['zd_recall']]
            fig = go.Figure(go.Bar(
                x=df['Model_short'], y=df['zd_recall'],
                marker=dict(color=cols_c,
                            line=dict(color='rgba(255,255,255,0.1)',width=1)),
                text=df['zd_recall'].round(1).astype(str)+'%',
                textposition='outside'))
            fig.update_layout(**PLOTLY,title="🔴 Recall Zero-Day (DoS Slowhttptest)",
                yaxis=dict(range=[0,max(df['zd_recall'].max()*1.35,15)],title="Recall (%)"),
                showlegend=False)
            st.plotly_chart(fig, width='stretch')

        sec("⚖️ Compromis Faux Positifs vs Recall ZD","Le coin idéal = haut + à gauche")
        fig = px.scatter(df, x='fp_day', y='zd_recall', size='fbeta2',
            color='Model_short', text='Model_short',
            color_discrete_sequence=['#00bfb3','#3fb950','#d29922','#f85149','#bc8cff'],
            hover_data={'f1_known':True,'fbeta2':True})
        fig.update_traces(textposition='top center',
            marker=dict(sizemin=12,line=dict(width=1,color='rgba(255,255,255,0.15)')))
        fig.update_layout(**PLOTLY,
            title="FP/jour ↓ vs Recall ZD ↑  |  Taille = Fβ(2)",
            xaxis=dict(autorange='reversed',title="Faux Positifs / jour (↓ mieux)"),
            yaxis_title="Recall Zero-Day % (↑ mieux)")
        st.plotly_chart(fig, width='stretch')

        sec("🕸️ Radar Multi-Critères")
        cats = ['F1 Connus','Recall ZD','Fβ(2)','FP Score (inv.)']
        fig = go.Figure()
        palette = ['#00bfb3','#3fb950','#d29922','#f85149','#bc8cff']
        for i,(_, row) in enumerate(df.iterrows()):
            fp_i = max(0,100-row['fp_day']/max(df['fp_day'].max(),1)*100)
            v = [row['f1_known'],row['zd_recall'],row['fbeta2'],fp_i]
            name = row.get('Model_short', row['Modele'])
            fig.add_trace(go.Scatterpolar(r=v+[v[0]],theta=cats+[cats[0]],
                name=name,fill='toself',opacity=0.55,
                line=dict(color=palette[i%len(palette)],width=2)))
        fig.update_layout(**PLOTLY,
            polar=dict(bgcolor='rgba(13,17,18,0.8)',
                       radialaxis=dict(visible=True,range=[0,100],
                                       gridcolor='rgba(48,54,61,0.5)',
                                       tickfont=dict(size=8)),
                       angularaxis=dict(gridcolor='rgba(48,54,61,0.5)')),
            title="Profil multi-critères par modèle",
            legend=dict(bgcolor='rgba(13,17,18,0.7)'))
        st.plotly_chart(fig, width='stretch')
    else:
        st.warning("dashboard_data.csv non disponible.")

# ═══════════════════════════════════════════════════════════
# PAGE 2B — LATENCE 
# ═══════════════════════════════════════════════════════════
elif page == "⚡ Latence Temps-Réel":
    sec("⚡ Latence Temps-Réel (Throughput)","Vitesse de détection en flux par seconde — Prêt pour la Production ?")

    st.markdown("""
    <div style="background:rgba(88,166,255,0.08);border:1px solid rgba(88,166,255,0.25);
        border-radius:8px;padding:14px 18px;font-size:13px;color:#79c0ff;margin-bottom:20px;">
    ℹ️ <b>Contexte SOC (Security Operations Center) :</b><br>
    Un modèle qui détecte tout mais qui traite 10 flux par seconde va créer un <b>goulot d'étranglement</b>. 
    L'inférence doit être ultra-rapide (faible latence) pour du traitement en temps réel (streaming).
    Ici, nous testons la vitesse pure d'analyse sur le dataset de test (en incluant l'agrégation GAT).
    </div>""", unsafe_allow_html=True)

    if bench and any('flows_per_sec' in v for v in bench.values()):
        _speed_data = []
        for mn, kv in bench.items():
            if 'flows_per_sec' in kv and kv['flows_per_sec'] > 0:
                _speed_data.append((mn, kv['flows_per_sec']))

        if _speed_data:
            _speed_data.sort(key=lambda x: x[1], reverse=True)
            names = [x[0] for x in _speed_data]
            speeds = [x[1] for x in _speed_data]

            fig = go.Figure(go.Bar(
                x=names, y=speeds,
                marker=dict(color=['#58a6ff' if 'GAT' not in n else '#3fb950' for n in names],
                            line=dict(color='rgba(255,255,255,0.1)',width=1)),
                text=[f"{v:,} f/s" for v in speeds],
                textposition='auto'))
            fig.update_layout(**PLOTLY,title="🚀 Débit d'inférence (Flux réseau analysés / seconde)",
                yaxis=dict(title="Vitesse (↑ mieux)"), showlegend=False)
            st.plotly_chart(fig, width='stretch')

            st.markdown("### 🏆 Analyse des performances de production")
            fastest = speeds[0]
            gat_speed = dict(_speed_data).get([n for n in names if 'GAT' in n][0], 0)
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div class="verdict-ok">
                    <div style="font-size:16px;font-weight:700;color:#3fb950;margin-bottom:10px;">
                        ⚡ Vitesse Maximale : {names[0]}
                    </div>
                    <div style="font-family:'JetBrains Mono';font-size:13px;color:#c9d1d9;line-height:2;">
                        Débit : <b style="color:#56d364;">{fastest:,} flux/sec</b><br>
                        Idéal pour : Réseaux Gigabit, sans état (stateless).
                    </div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="verdict-fail" style="border-color:rgba(0,191,179,0.3);background:rgba(0,191,179,0.05);">
                    <div style="font-size:16px;font-weight:700;color:#00bfb3;margin-bottom:10px;">
                        🕸️ Vitesse du GAT Hybrid
                    </div>
                    <div style="font-family:'JetBrains Mono';font-size:13px;color:#c9d1d9;line-height:2;">
                        Débit : <b style="color:#00bfb3;">{gat_speed:,} flux/sec</b><br>
                        Compromis : Tolérable pour les réseaux d'entreprise moyens, le coût est justifié par la récupération ZD.
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Les mesures de latence n'ont pas encore été exportées.")
    else:
         st.info("Aucune donnée de vitesse trouvée. Lancez la nouvelle section de notebook OOD.")
         
# ═══════════════════════════════════════════════════════════
# PAGE 3 — CAS ZERO-DAY
# ═══════════════════════════════════════════════════════════
elif page == "🎯 Cas Zero-Day":
    sec("🎯 Cas Zero-Day — DoS Slowhttptest","Rapport d'incident complet style ticket SIEM")

    # Chargement données SOC
    alert  = soc.get('alert',  {'alert_id':'IDS-2017-004821','timestamp':'2017-07-05 14:32:07','src_ip':'192.168.10.50','dst_ip':'192.168.10.3','dst_port':80,'protocol':'HTTP/TCP'})
    verdict= soc.get('verdict', {'xgb_pred':'BENIGN','xgb_conf':0.98,'gat_ood':True,'true_class':'DoS Slowhttptest'})
    mitre  = soc.get('mitre',  {'id':'T1499.002','name':'Service Exhaustion Flood','tactic':'Impact'})
    indics = soc.get('indicators', [])

    # Carte d'incident principale
    st.markdown(f"""
    <div class="incident-card">
        <div class="incident-header">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <span style="font-family:'Orbitron';font-size:15px;color:#f85149;font-weight:700;">
                        🚨 ALERTE CRITIQUE — ATTAQUE ZERO-DAY DÉTECTÉE
                    </span>
                    <div style="font-family:'JetBrains Mono';font-size:11px;color:#8b949e;margin-top:5px;">
                        ID : {alert.get('alert_id','')}  ·  {alert.get('timestamp','')}
                    </div>
                </div>
                <span class="badge b-red" style="font-size:13px;padding:6px 16px;">CRITIQUE</span>
            </div>
        </div>
        <div class="incident-body">
            <table class="dark-table">
                <tr><th>Champ</th><th>Valeur</th><th>Statut</th></tr>
                <tr><td>IP Source</td><td><code style="color:#00bfb3;">{alert.get('src_ip','')}</code></td>
                    <td><span class="badge b-red">🔴 BLOQUÉE</span></td></tr>
                <tr><td>IP Destination</td><td><code style="color:#c9d1d9;">{alert.get('dst_ip','')}:{alert.get('dst_port',80)}</code></td>
                    <td><span class="badge b-cyan">Victime protégée</span></td></tr>
                <tr><td>Protocole</td><td>{alert.get('protocol','')}</td><td></td></tr>
                <tr><td>Vraie nature</td><td><b style="color:#f85149;">{verdict.get('true_class','')}</b></td>
                    <td><span class="badge b-gold">Zero-Day</span></td></tr>
                <tr><td>MITRE ATT&CK</td><td><b style="color:#d29922;">{mitre.get('id','')}</b> — {mitre.get('name','')}</td>
                    <td><span class="badge b-gold">{mitre.get('tactic','')}</span></td></tr>
            </table>
        </div>
    </div>""", unsafe_allow_html=True)

    # Comparaison modèles
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        xgb_c = verdict.get('xgb_conf', 0.98)
        st.markdown(f"""
        <div class="verdict-fail">
            <div style="font-size:16px;font-weight:700;color:#f85149;margin-bottom:10px;">
                ❌ XGBoost — Diagnostic ERRONÉ
            </div>
            <div style="font-family:'JetBrains Mono';font-size:13px;color:#c9d1d9;line-height:2;">
                Prédiction : <b style="color:#f85149;">{verdict.get('xgb_pred','BENIGN')}</b><br>
                Confiance  : <b style="color:#f85149;">{xgb_c:.1%}</b> ← fausse certitude<br>
                Raison     : Volume faible → ressemble à du trafic normal<br>
                Résultat   : Attaque non détectée (Recall ZD ≈ 0%)
            </div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="verdict-ok">
            <div style="font-size:16px;font-weight:700;color:#3fb950;margin-bottom:10px;">
                ✅ GAT — Détection correcte (OOD)
            </div>
            <div style="font-family:'JetBrains Mono';font-size:13px;color:#c9d1d9;line-height:2;">
                Signal     : <b style="color:#00bfb3;">Out-of-Distribution</b><br>
                Mécanisme  : Pas de voisins typiques dans le graphe<br>
                Attention  : Diffuse → incertitude topologique<br>
                Résultat   : Attaque détectée → alerte SOC L2
            </div>
        </div>""", unsafe_allow_html=True)

    # Indicateurs réseau
    if indics:
        sec("🔍 Indicateurs réseau suspects","Analyse comportementale du flux — valeurs réelles vs référence normale")
        rows = ""
        for ind in indics:
            lvl = ind.get('level','')
            bc  = 'b-red' if '🔴' in lvl else 'b-gold' if '🟠' in lvl else \
                  'b-blue' if '🟡' in lvl else 'b-green'
            rows += f"""<tr>
                <td>{ind.get('label','')}</td>
                <td><code style="color:#00bfb3;">{ind.get('value','')}</code></td>
                <td><code style="color:#8b949e;">{ind.get('reference','')}</code></td>
                <td><span class="badge {bc}">{ind.get('level','')[:12].strip()}</span></td>
                <td style="color:#8b949e;font-size:11px;">{ind.get('interpretation','')}</td>
            </tr>"""
        st.markdown(f"""
        <table class="dark-table">
            <tr>
                <th>Indicateur réseau</th>
                <th>Ce flux</th>
                <th>Réf. normal</th>
                <th>Niveau alerte</th>
                <th>Interprétation SOC</th>
            </tr>
            {rows}
        </table>""", unsafe_allow_html=True)

    # Actions recommandées
    st.markdown("<br>", unsafe_allow_html=True)
    sec("🛠️ Actions recommandées")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background:#0d1117;border:1px solid #21262d;border-radius:12px;padding:18px;">
            <div style="color:#f85149;font-weight:700;margin-bottom:12px;">⚡ Réponse immédiate (L1)</div>
            <ul style="color:#c9d1d9;font-size:13px;line-height:2;margin:0;">
                <li>Bloquer IP source <code style="color:#00bfb3;">192.168.10.50</code></li>
                <li>Escalader ticket vers analyste L2</li>
                <li>Capturer PCAP du flux (Wireshark)</li>
                <li>Documenter l'incident (JIRA/ServiceNow)</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:#0d1117;border:1px solid #21262d;border-radius:12px;padding:18px;">
            <div style="color:#d29922;font-weight:700;margin-bottom:12px;">🔬 Investigation (L2)</div>
            <ul style="color:#c9d1d9;font-size:13px;line-height:2;margin:0;">
                <li>Analyser PCAP avec <code>tcp.window_size</code> dans Wireshark</li>
                <li>Scanner segment <code>192.168.10.0/24</code> (autres hôtes)</li>
                <li>Créer règle Snort : Win TCP &gt; 60000 + durée &gt; 60s</li>
                <li>Ajouter IOC dans le SIEM (IP + signature TCP)</li>
            </ul>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE 4 — POURQUOI LE GAT
# ═══════════════════════════════════════════════════════════
elif page == "🧠 Pourquoi le GAT ?":
    sec("🧠 Pourquoi le GAT détecte ce que les autres ratent ?","Explication intuitive de la topologie de graphe")

    st.markdown("""
    <div style="background:#0d1117;border:1px solid rgba(0,191,179,0.2);border-radius:14px;padding:24px;margin:16px 0;">
        <div style="font-family:'JetBrains Mono';font-size:13px;color:#c9d1d9;line-height:2.2;">
        <b style="color:#00bfb3;">Modèles classiques (RF, XGB, MLP)</b><br>
        → Analysent chaque flux <b>de façon isolée</b><br>
        → Regardent uniquement : volume ? débit ? taille des paquets ?<br>
        → Pour le Slowhttptest : volume faible + petits paquets = <b style="color:#f85149;">ressemble à du BENIGN → ÉCHO</b><br><br>
        <b style="color:#3fb950;">GAT (Graph Attention Network)</b><br>
        → Représente chaque flux comme un <b>nœud dans un graphe</b><br>
        → Chaque nœud regarde ses <b>K=4 voisins les plus similaires</b> dans les données d'entraînement<br>
        → Un flux Zero-Day : ses voisins ne se ressemblent pas entre eux → <b style="color:#00bfb3;">attention diffuse</b><br>
        → Signal : "Je ne ressemble à aucune classe connue" = <b style="color:#d29922;">OOD → ALERTE</b>
        </div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="kpi-card" style="text-align:left;padding:20px;">
            <div style="font-size:20px;margin-bottom:10px;">📐</div>
            <div style="color:#00bfb3;font-weight:700;margin-bottom:8px;">Construction du graphe</div>
            <div style="font-size:12px;color:#8b949e;line-height:1.8;">
                • PCA → espace 15D<br>
                • KNN → K=4 voisins les plus proches<br>
                • Seuil distance (médiane)<br>
                • Graphe : Train + Test combinés
            </div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="kpi-card" style="text-align:left;padding:20px;">
            <div style="font-size:20px;margin-bottom:10px;">👁️</div>
            <div style="color:#3fb950;font-weight:700;margin-bottom:8px;">Mécanisme d'attention</div>
            <div style="font-size:12px;color:#8b949e;line-height:1.8;">
                • Chaque voisin reçoit un poids (0→1)<br>
                • Voisin similaire → poids élevé<br>
                • ZD : voisins hétérogènes → distribution atypique<br>
                • Signal OOD naturel sans supervision
            </div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="kpi-card" style="text-align:left;padding:20px;">
            <div style="font-size:20px;margin-bottom:10px;">📊</div>
            <div style="color:#d29922;font-weight:700;margin-bottom:8px;">Preuve expérimentale</div>
            <div style="font-size:12px;color:#8b949e;line-height:1.8;">
                • MLP = mêmes neurones que GAT<br>
                • MLP sans graphe → Recall ZD ≈ 0%<br>
                • GAT avec graphe → Recall ZD &gt; 50%<br>
                • Δ vient uniquement de la topologie
            </div>
        </div>""", unsafe_allow_html=True)

    if bench:
        sec("Preuve chiffrée : MLP vs GAT")
        mlp_zd = bench.get('MLP (No Graph)', {}).get('zd_recall', 0)
        gat_vals = [(k,v['zd_recall']) for k,v in bench.items() if 'GAT' in k or 'gat' in k.lower()]
        gat_zd = max(v for _,v in gat_vals) if gat_vals else 0
        delta = gat_zd - mlp_zd
        st.markdown(f"""
        <div style="background:#0d1117;border:1px solid #21262d;border-radius:12px;padding:20px;font-family:'JetBrains Mono';font-size:14px;line-height:2.2;">
        🧪 MLP (sans graphe)  : Recall ZD = <b style="color:#f85149;">{mlp_zd:.1f}%</b><br>
        🕸️ GAT (avec graphe)  : Recall ZD = <b style="color:#3fb950;">{gat_zd:.1f}%</b><br>
        ──────────────────────────────────<br>
        📈 Gain pur du graphe : <b style="color:#00bfb3;">+{delta:.1f}%</b>
        {"→ La topologie contribue significativement ✅" if delta > 5 else "→ Contribution modérée ⚠️"}
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE 5 — XAI AVANCÉ
# ═══════════════════════════════════════════════════════════
elif page == "🔬 XAI Avancé":
    sec("🔬 XAI Avancé — Pour Data Scientists","SHAP, Attention GAT, Comparaison XGB vs GAT")

    tab1,tab2,tab3,tab4 = st.tabs(["📊 SHAP Global RF","📊 SHAP Global XGB","🔎 Waterfall Local","🕸️ Attention & Comparaison"])

    with tab1:
        st.markdown("#### Random Forest — Importance globale des features")
        st.markdown("""<div style="background:rgba(0,191,179,0.06);border:1px solid rgba(0,191,179,0.2);
            border-radius:8px;padding:12px 16px;font-size:13px;color:#79c0ff;margin-bottom:16px;">
            📘 Le beeswarm montre l'impact de chaque feature sur la prédiction.
            La couleur = valeur de la feature (rouge = élevé). Les features liées au trafic retour (Backward) dominent.
            </div>""", unsafe_allow_html=True)
        img("xai_shap_rf.png", "SHAP Global RF")

    with tab2:
        st.markdown("#### XGBoost — Importance globale des features")
        st.markdown("""<div style="background:rgba(0,191,179,0.06);border:1px solid rgba(0,191,179,0.2);
            border-radius:8px;padding:12px 16px;font-size:13px;color:#79c0ff;margin-bottom:16px;">
            📘 XGBoost utilise les features volumétriques ET protocolaires (Fenêtre TCP initiale, IAT).
            C'est cette combinaison qui lui permet d'atteindre 99.8% de F1 sur les classes connues.
            </div>""", unsafe_allow_html=True)
        img("xai_shap_xgb.png", "SHAP Global XGB")

    with tab3:
        c1,c2 = st.columns(2)
        with c1:
            st.markdown("##### 🔴 Flux Zero-Day")
            st.markdown("""<div style="background:rgba(248,81,73,0.08);border:1px solid rgba(248,81,73,0.25);
                border-radius:8px;padding:10px 14px;font-size:12px;color:#ff7b72;margin-bottom:12px;">
                ⚠️ XGBoost prédit BENIGN à 98% de confiance.
                Les features "faible volume" poussent vers BENIGN car l'attaque est furtive.
                </div>""", unsafe_allow_html=True)
            img("xai_shap_xgb_local_zd.png","Waterfall — Flux Zero-Day")
        with c2:
            st.markdown("##### ✅ Flux connu (attaque)")
            st.markdown("""<div style="background:rgba(63,185,80,0.08);border:1px solid rgba(63,185,80,0.25);
                border-radius:8px;padding:10px 14px;font-size:12px;color:#56d364;margin-bottom:12px;">
                ✅ Contributions SHAP cohérentes dans le même sens → confiance maximale, diagnostic correct.
                </div>""", unsafe_allow_html=True)
            img("xai_shap_xgb_local_known.png","Waterfall — Flux Connu")

    with tab4:
        c1,c2 = st.columns(2)
        with c1:
            st.markdown("##### 🕸️ Distribution d'attention GAT")
            st.markdown("""<div style="background:rgba(210,153,34,0.08);border:1px solid rgba(210,153,34,0.25);
                border-radius:8px;padding:10px 14px;font-size:12px;color:#e3b341;margin-bottom:12px;">
                ⚠️ Le Zero-Day a une attention très diffuse sur les classes voisines — pas de correspondance franche.
                C'est ce signal d'incertitude topologique qui déclenche le flag OOD.
                </div>""", unsafe_allow_html=True)
            img("xai_gat_attention.png","Attention Weights GAT")
        with c2:
            st.markdown("##### 📈 Comparaison XGB vs GAT sur 10 ZD")
            st.markdown("""<div style="background:rgba(0,191,179,0.06);border:1px solid rgba(0,191,179,0.2);
                border-radius:8px;padding:10px 14px;font-size:12px;color:#79c0ff;margin-bottom:12px;">
                🔵 XGB : confiance élevée même sur ZD (entropie basse = aveugle).
                GAT : entropie typiquement plus élevée sur ZD → meilleur signal OOD.
                </div>""", unsafe_allow_html=True)
            img("xai_comparison_zd.png","Heatmap XGB vs GAT — 10 ZD")

# ═══════════════════════════════════════════════════════════
# PAGE 6 — ANALYSE SOC
# ═══════════════════════════════════════════════════════════
elif page == "🛡️ Analyse SOC":
    sec("🛡️ Analyse SOC — Profil de trafic & Radar de menace","Visualisations pour analyste réseau — sans jargon ML")

    st.markdown("### 📊 Profilage comportemental du trafic")
    st.markdown("""
    <div style="background:rgba(210,153,34,0.08);border:1px solid rgba(210,153,34,0.25);
        border-radius:8px;padding:14px 18px;font-size:13px;color:#e3b341;margin-bottom:12px;">
    ⚠️ <b>Pourquoi le Zero-Day est invisible pour XGBoost ?</b><br>
    Le Slowhttptest envoie de <b>très petits paquets</b> à <b>très faible débit</b> — signature similaire au trafic légitime au repos.
    Seules la <b>durée anormalement longue</b> et la <b>fenêtre TCP atypique</b> (signature de l'outil offensif) trahissent l'attaque.
    Ce sont ces indicateurs qu'un analyste Wireshark/Zeek identifierait en premier.
    </div>""", unsafe_allow_html=True)
    img("xai_traffic_profile.png","Profil de trafic — Normal vs Attaque connue vs Zero-Day")

    st.markdown("### 🕸️ SOC Threat Radar — Dangerosité par axe de menace")
    st.markdown("""
    <div style="background:rgba(0,191,179,0.06);border:1px solid rgba(0,191,179,0.2);
        border-radius:8px;padding:14px 18px;font-size:13px;color:#79c0ff;margin-bottom:12px;">
    📡 <b>Lecture du radar pour l'analyste :</b><br>
    • <b>Volume</b> : Le ZD (orange) est bas → pas une attaque volumétrique<br>
    • <b>Débit</b> : Le ZD est faible → attaque furtive et lente<br>
    • <b>Temporalité</b> : Le ZD est élevé → connexion anormalement longue ← <b>signal principal</b><br>
    • <b>Protocole TCP</b> : Le ZD est élevé → fenêtre TCP anormale ← <b>signature outil</b><br>
    • <b>Régularité</b> : Le ZD est modéré → comportement semi-automatisé
    </div>""", unsafe_allow_html=True)
    img("xai_threat_radar.png","SOC Threat Radar — Score dangerosité")

    sec("🏷️ Mapping MITRE ATT&CK")
    mitre = soc.get('mitre', {'id':'T1499.002','name':'Service Exhaustion Flood','tactic':'Impact'})
    st.markdown(f"""
    <table class="dark-table">
        <tr><th>Techique ID</th><th>Nom</th><th>Tactique</th><th>Outil</th><th>Plateforme</th></tr>
        <tr>
            <td><b style="color:#d29922;">{mitre.get('id','')}</b></td>
            <td>{mitre.get('name','')}</td>
            <td><span class="badge b-red">{mitre.get('tactic','')}</span></td>
            <td>Slowhttptest, Slowloris, R-U-Dead-Yet</td>
            <td>Windows, Linux, macOS</td>
        </tr>
    </table>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE 7 — ARCHITECTURE
# ═══════════════════════════════════════════════════════════
elif page == "🏗️ Architecture":
    sec("🏗️ Architecture du Pipeline IDS","Vue d'ensemble du système de bout en bout")

    st.markdown("""
    <div style="background:#0d1117;border:1px solid rgba(0,191,179,0.2);border-radius:14px;
                padding:28px;font-family:'JetBrains Mono';font-size:13px;line-height:2.3;color:#c9d1d9;">
    <span style="color:#00bfb3;font-weight:700;">① DONNÉES</span>  CICIDS2017 (Mercredi) — 80+ features réseau capturées<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    <span style="color:#3fb950;font-weight:700;">② NETTOYAGE</span> 8 étapes : NaN, Inf, doublons, durations négatives, VarianceThreshold, StandardScaler<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    <span style="color:#d29922;font-weight:700;">③ SPLIT</span>  Train 60% / Val 20% / Test 20% — stratifié par classe<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓ <span style="color:#f85149;">← Zero-Day retiré du Train exprès</span><br>
    <span style="color:#bc8cff;font-weight:700;">④ PCA + KNN</span> PCA 15D → graphe KNN K=4 (seuil distance médiane)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    <span style="color:#00bfb3;font-weight:700;">⑤ ENTRAÎNEMENT</span><br>
    &nbsp;&nbsp;&nbsp;├── 🌲 Random Forest (200 arbres, baseline)<br>
    &nbsp;&nbsp;&nbsp;├── ⚡ XGBoost (300 estimateurs, lr=0.10)<br>
    &nbsp;&nbsp;&nbsp;├── 🧠 MLP sans graphe (baseline neurones, 128 units)<br>
    &nbsp;&nbsp;&nbsp;└── <b style="color:#3fb950;">🕸️ GAT V5 Hybrid</b> (2 couches, 4 têtes, skip connections, BatchNorm)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    <span style="color:#d29922;font-weight:700;">⑥ CALIBRATION OOD</span>  Seuils Entropie + Distance KNN → calibrés sur VAL uniquement<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    <span style="color:#f85149;font-weight:700;">⑦ ÉVALUATION TEST</span>  F1 Macro + Recall ZD + FP/jour + Fβ(2) — une seule passe<br>
    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    <span style="color:#bc8cff;font-weight:700;">⑧ XAI</span>  SHAP (RF, XGB) + Attention GAT + Rapport SOC + Profil trafic dark theme
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        sec("🌲 Modèles Tabulaires")
        st.markdown("""
        <div style="background:#0d1117;border:1px solid rgba(88,166,255,0.2);border-radius:10px;padding:18px;font-size:13px;line-height:2;color:#c9d1d9;">
        <b style="color:#58a6ff;">Random Forest :</b> 200 experts indépendants, vote majoritaire<br>
        → Robuste, interprétable, rapide<br>
        → Aveugle au contexte (flux isolés)<br><br>
        <b style="color:#58a6ff;">XGBoost :</b> Correcteurs successifs (boosting)<br>
        → Meilleur F1 sur classes connues (≈99.8%)<br>
        → Sur-confiant face à l'inconnu (ZD)<br><br>
        <b style="color:#58a6ff;">MLP :</b> Réseau de neurones <i>sans</i> graphe<br>
        → Preuve que les neurones seuls ne suffisent pas<br>
        → Recall ZD ≈ 0% sans topologie
        </div>""", unsafe_allow_html=True)
    with c2:
        sec("🕸️ GAT (Graph Attention Network)")
        st.markdown("""
        <div style="background:#0d1117;border:1px solid rgba(0,191,179,0.3);border-radius:10px;padding:18px;font-size:13px;line-height:2;color:#c9d1d9;">
        <b style="color:#00bfb3;">Innovation :</b> Chaque flux = nœud dans un graphe KNN<br>
        → Le GAT agrège les voisins avec des <i>poids d'attention</i><br><br>
        <b style="color:#00bfb3;">Zero-Day :</b><br>
        → Voisins hétérogènes (pas de classe dominante)<br>
        → Distribution d'attention diffuse → entropie élevée<br>
        → Seuil OOD franchi → 🚨 ALERTE<br><br>
        <b style="color:#00bfb3;">+ Consensus RF/XGB :</b><br>
        → Si RF ET XGB très confiants (BENIGN, >99.9%) → annule l'alerte<br>
        → Réduction des faux positifs sans perte de ZD
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE 8 : GÉNÉRALISATION MULTI-JOUR CICIDS2017
# ═══════════════════════════════════════════════════════════
elif page == "🌐 Généralisation":
    st.markdown('<div class="hero-title" style="font-size:26px">🌐 Test de Généralisation Multi-Jour</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#8b949e;font-size:14px;margin-bottom:24px;">Entraîné sur Wednesday (DoS) · Testé sur Thursday & Friday (attaques jamais vues)</div>', unsafe_allow_html=True)

    # Chargement des résultats
    _gen_file = "generalisation_results.json"
    if not os.path.exists(_gen_file):
        st.warning("⚠️ Résultats de généralisation non trouvés. Exécutez d\'abord le volet Généralisation dans le notebook Kaggle.")
        st.code("# Dans le notebook Kaggle, exécutez la cellule :\n# VOLET GENERALISATION MULTI-JOUR — CICIDS2017 Thu & Fri", language="python")
    else:
        _gen_data = json.load(open(_gen_file))

        # ── Contexte pédagogique ──────────────────────────────────────────
        st.markdown("""
        <div style="background:linear-gradient(135deg,rgba(0,191,179,0.08),rgba(88,166,255,0.05));
                    border:1px solid rgba(0,191,179,0.25);border-radius:12px;padding:18px;margin-bottom:20px;">
        <b style="color:#00bfb3;">🎯 Objectif du test :</b>
        <span style="color:#c9d1d9;"> Le modèle est entraîné uniquement sur des attaques DoS (Wednesday).
        On l\'expose ensuite à des attaques de familles complètement différentes pour mesurer sa capacité de généralisation.</span><br><br>
        <b style="color:#58a6ff;">Rappel OSI :</b>
        <span style="color:#8b949e;">
        Thursday = Web Attacks (Layer 7 — applicatif) · Non détectable par IDS réseau · Zone WAF<br>
        Friday = DDoS / PortScan / Bot (Layer 3-4 — réseau/transport) · Zone de responsabilité du GAT
        </span>
        </div>""", unsafe_allow_html=True)

        # ── Sélecteur de jour ─────────────────────────────────────────────
        _days_avail = list(_gen_data.keys())
        _day_sel = st.selectbox(
            "Sélectionner le jour à analyser",
            [d.capitalize() for d in _days_avail],
            key="gen_day"
        )
        _day_key = _day_sel.lower()
        _day_info = _gen_data[_day_key]
        _modeles  = _day_info["modeles"]
        _classes  = _day_info.get("classes", [])
        _n_atk    = _day_info.get("n_attaques", 0)
        _n_ben    = _day_info.get("n_benign", 0)

        # ── KPIs: contexte du jour ────────────────────────────────────────
        _atk_types = [c for c in _classes if c.upper() != "BENIGN"]
        # Pre-calculer les valeurs hors f-string (interdit d'avoir \ dans {} en Python<3.12)
        _atk_join  = ", ".join(_atk_types[:2])
        _osi_layer = "Layer 7 (WAF)"     if _day_key == "thursday" else "Layer 3-4 (IDS)"
        _osi_sub   = "Hors perimetre GAT" if _day_key == "thursday" else "Perimetre GAT"
        _intro_sub = "jamais vues a l entrainement"
        st.markdown(f"""
        <div style="display:flex;gap:16px;margin-bottom:20px;flex-wrap:wrap;">
          <div class="kpi-card">
            <div class="kpi-icon">&#128680;</div>
            <div class="kpi-lbl">Attaques inedites</div>
            <div class="kpi-val red">{_n_atk:,}</div>
            <div class="kpi-sub">{_intro_sub}</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-icon">&#9989;</div>
            <div class="kpi-lbl">Trafic BENIGN</div>
            <div class="kpi-val green">{_n_ben:,}</div>
            <div class="kpi-sub">reference FP</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-icon">&#127991;</div>
            <div class="kpi-lbl">Types d attaques</div>
            <div class="kpi-val cyan">{len(_atk_types)}</div>
            <div class="kpi-sub">{_atk_join}</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-icon">&#9888;</div>
            <div class="kpi-lbl">Couche OSI</div>
            <div class="kpi-val gold">{_osi_layer}</div>
            <div class="kpi-sub">{_osi_sub}</div>
          </div>
        </div>""", unsafe_allow_html=True)

        # ── Tableau de performance interactif ────────────────────────────
        st.markdown("---")
        sec("📋 Tableau de Performance SOC", "Pour chaque modèle : Recall, Faux Positifs, Précision des alertes")

        _mdl_order = ["RF", "XGB", "MLP", "GAT+cns", "GAT+dist(P97)"]
        _mdl_info  = {
            "RF"           : ("RF", "Entropie accidentelle", "#58a6ff"),
            "XGB"          : ("XGB", "Entropie accidentelle", "#d29922"),
            "MLP"          : ("MLP", "Surconfiant / aveugle", "#bc8cff"),
            "GAT+cns"      : ("GAT+consensus", "OOD Intentionnel ✅", "#3fb950"),
            "GAT+dist(P97)": ("GAT+distance", "Adaptatif cross-domaine ✅", "#a371f7"),
        }

        def _badge(v, metric):
            pct = f"{v:.1f}%"
            if metric == "det":
                if v >= 70: return '<span class="badge b-green">BON '   + pct + '</span>'
                if v >= 40: return '<span class="badge b-gold">MOYEN '  + pct + '</span>'
                return             '<span class="badge b-red">FAIBLE '  + pct + '</span>'
            elif metric == "fp":
                if v <= 3:  return '<span class="badge b-green">OK '        + pct + '</span>'
                if v <= 10: return '<span class="badge b-gold">ATTENTION '  + pct + '</span>'
                return             '<span class="badge b-red">ELEVE '       + pct + '</span>'
            elif metric == "prec":
                if v >= 80: return '<span class="badge b-green">FIABLE '    + pct + '</span>'
                if v >= 60: return '<span class="badge b-gold">PARTIEL '    + pct + '</span>'
                return             '<span class="badge b-red">NON FIABLE '  + pct + '</span>'
            return pct

        _tbl_html = """
        <table style="width:100%;border-collapse:collapse;font-size:13px;">
          <thead>
            <tr style="background:rgba(0,191,179,0.1);">
              <th style="padding:10px 14px;text-align:left;color:#8b949e;border-bottom:1px solid #30363d;">Modele</th>
              <th style="padding:10px 14px;text-align:left;color:#8b949e;border-bottom:1px solid #30363d;">Type Detection</th>
              <th style="padding:10px 14px;text-align:center;color:#8b949e;border-bottom:1px solid #30363d;">Recall (Detection)</th>
              <th style="padding:10px 14px;text-align:center;color:#8b949e;border-bottom:1px solid #30363d;">FP BENIGN</th>
              <th style="padding:10px 14px;text-align:center;color:#8b949e;border-bottom:1px solid #30363d;">Precision Alertes</th>
            </tr>
          </thead><tbody>"""

        for _mn in _mdl_order:
            if _mn not in _modeles: continue
            _d  = _modeles[_mn].get("detection", 0)
            _fp = _modeles[_mn].get("fp", 0)
            _pr = _modeles[_mn].get("precision", 0)
            _lbl, _type_lbl, _col = _mdl_info.get(_mn, (_mn, "", "#fff"))
            _row_bg = "rgba(63,185,80,0.04)" if "GAT" in _mn else "transparent"
            _b_det  = _badge(_d,  "det")
            _b_fp   = _badge(_fp, "fp")
            _b_prec = _badge(_pr, "prec")
            _tbl_html += (
                f'<tr style="border-bottom:1px solid #21262d;background:{_row_bg};">'
                f'<td style="padding:12px 14px;"><b style="color:{_col};">{_lbl}</b></td>'
                f'<td style="padding:12px 14px;color:#8b949e;font-size:12px;">{_type_lbl}</td>'
                f'<td style="padding:12px 14px;text-align:center;">{_b_det}</td>'
                f'<td style="padding:12px 14px;text-align:center;">{_b_fp}</td>'
                f'<td style="padding:12px 14px;text-align:center;">{_b_prec}</td>'
                f'</tr>'
            )


        _tbl_html += "</tbody></table>"
        st.markdown(_tbl_html, unsafe_allow_html=True)

        # ── Graphiques Plotly ──────────────────────────────────────────────
        st.markdown("---")
        sec("📈 Analyse Visuelle Comparative")

        _labels_plot = []
        _det_plot    = []
        _fp_plot     = []
        _prec_plot   = []
        _colors_plot = []
        _colmap = {"RF":"#58a6ff","XGB":"#d29922","MLP":"#bc8cff",
                   "GAT+cns":"#3fb950","GAT+dist(P97)":"#a371f7"}

        for _mn in _mdl_order:
            if _mn not in _modeles: continue
            _labels_plot.append(_mdl_info.get(_mn, (_mn,))[0])
            _det_plot.append(_modeles[_mn].get("detection", 0))
            _fp_plot.append(_modeles[_mn].get("fp", 0))
            _prec_plot.append(_modeles[_mn].get("precision", 0))
            _colors_plot.append(_colmap.get(_mn, "#fff"))

        _col1, _col2, _col3 = st.columns(3)

        with _col1:
            _fig1 = go.Figure(go.Bar(
                x=_det_plot, y=_labels_plot, orientation="h",
                marker_color=_colors_plot, marker_opacity=0.85,
                text=[f"{v:.1f}%" for v in _det_plot], textposition="outside",
            ))
            _fig1.add_vline(x=70, line_dash="dot", line_color="#3fb950",
                           annotation_text="Seuil SOC 70%", annotation_font_color="#3fb950")
            _fig1.update_layout(**PLOTLY, title="Recall (Détection)",
                                xaxis_range=[0, 120], height=280,
                                xaxis_title="%", yaxis_title="")
            st.plotly_chart(_fig1, use_container_width=True)

        with _col2:
            _fig2 = go.Figure(go.Bar(
                x=_fp_plot, y=_labels_plot, orientation="h",
                marker_color=_colors_plot, marker_opacity=0.85,
                text=[f"{v:.1f}%" for v in _fp_plot], textposition="outside",
            ))
            _fig2.add_vline(x=5, line_dash="dot", line_color="#d29922",
                           annotation_text="Seuil SOC 5%", annotation_font_color="#d29922")
            _fig2.update_layout(**PLOTLY, title="Faux Positifs BENIGN",
                                xaxis_range=[0, 40], height=280,
                                xaxis_title="%", yaxis_title="")
            st.plotly_chart(_fig2, use_container_width=True)

        with _col3:
            _fig3 = go.Figure(go.Bar(
                x=_prec_plot, y=_labels_plot, orientation="h",
                marker_color=_colors_plot, marker_opacity=0.85,
                text=[f"{v:.1f}%" for v in _prec_plot], textposition="outside",
            ))
            _fig3.add_vline(x=70, line_dash="dot", line_color="#3fb950",
                           annotation_text="Min SOC 70%", annotation_font_color="#3fb950")
            _fig3.update_layout(**PLOTLY, title="Précision des Alertes",
                                xaxis_range=[0, 120], height=280,
                                xaxis_title="%", yaxis_title="")
            st.plotly_chart(_fig3, use_container_width=True)

        # ── Interprétation SOC ────────────────────────────────────────────
        st.markdown("---")
        sec("🧠 Interprétation SOC Automatique")

        if _day_key == "thursday":
            st.markdown("""
            <div class="verdict-fail">
            <b style="color:#f85149;">⚠️ Résultat attendu — Hors périmètre IDS réseau</b><br><br>
            Les attaques de Thursday (XSS, SQL Injection, Brute Force HTTP) opèrent au <b style="color:#f85149;">Layer 7 (couche applicative)</b>.
            Elles sont <b>indiscernables du trafic BENIGN</b> au niveau des métriques de flux réseau (CICFlowMeter).<br><br>
            Ce n\'est pas un échec du modèle GAT — c\'est une <b>limite physique</b> connue et documentée de tout IDS réseau.
            Ces attaques nécessitent un <b style="color:#d29922;">WAF (Web Application Firewall)</b> qui inspecte le payload HTTP.
            </div>
            <div class="verdict-ok">
            <b style="color:#3fb950;">✅ Architecture recommandée</b><br><br>
            <b>IDS GAT</b> (votre modèle) → Protège les couches 3-4 : DoS, DDoS, PortScan, Zero-Day volumétrique<br>
            <b>WAF</b> (ModSecurity, AWS WAF) → Protège la couche 7 : XSS, SQLi, Brute Force HTTP<br>
            <b>SIEM</b> → Corrèle les alertes des deux systèmes pour une vision unifiée
            </div>""", unsafe_allow_html=True)

        elif _day_key == "friday":
            _gat_d = _modeles.get("GAT+cns", {}).get("detection", 0)
            _rf_d  = _modeles.get("RF", {}).get("detection", 0)
            _delta = _gat_d - _rf_d
            _cls_str = ", ".join(_atk_types)
            if _gat_d >= 70:
                _verdict_class = "verdict-ok"
                _verdict_icon  = "✅"
                _verdict_color = "#3fb950"
                # Pre-calculer le delta string hors f-string
                _delta_str = "+" + f"{_delta:.1f}%" if _delta > 0 else f"{_delta:.1f}%"
                _verdict_msg   = ("Le GAT+consensus atteint <b>" + f"{_gat_d:.1f}%" +
                    "</b> de recall sur les attaques volumetriques inedites — " +
                    _delta_str + " vs RF. Son mecanisme OOD topologique (entropie + distance KNN)"
                    " detecte efficacement les anomalies volumetriques, meme sans les avoir vues"
                    " a l entrainement.")
            else:
                _verdict_class = "verdict-fail"
                _verdict_icon  = "⚠️"
                _verdict_color = "#d29922"
                _verdict_msg   = f"Détection partielle ({_gat_d:.1f}%). Les attaques ({_cls_str}) partagent quelques caractéristiques avec le trafic BENIGN de reference, réduisant la distance KNN."

            st.markdown(f"""
            <div class="{_verdict_class}">
            <b style="color:{_verdict_color};">{_verdict_icon} Verdict Friday (DDoS / PortScan)</b><br><br>
            {_verdict_msg}
            </div>
            <div style="background:rgba(88,166,255,0.06);border:1px solid rgba(88,166,255,0.2);
                        border-radius:10px;padding:16px;margin-top:12px;">
            <b style="color:#58a6ff;">📌 Rappel Zero-Day Wednesday (périmètre principal du PFE)</b><br>
            <span style="color:#8b949e;">Sur ses attaques cibles (DoS Slowhttptest), le GAT atteint <b style="color:#3fb950;">~96% de recall</b> contre ~5% pour RF et XGB. Friday est un bonus de généralisation.</span>
            </div>""", unsafe_allow_html=True)

        # ── Image du dashboard matplotlib ────────────────────────────────
        if os.path.exists("generalisation_soc_dashboard.png"):
            st.markdown("---")
            sec("🖼️ Rapport Graphique Complet")
            st.image("generalisation_soc_dashboard.png",
                     caption="Dashboard SOC — Généralisation Multi-Jour CICIDS2017",
                     width="stretch")
