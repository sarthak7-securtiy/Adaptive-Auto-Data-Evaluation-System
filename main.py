import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os, time, math

os.environ["JOBLIB_START_METHOD"] = "spawn"
os.environ["OMP_NUM_THREADS"] = "1"

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="AADES · Intelligent Data Platform",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded",
)

# ╔══════════════════════════════════════════════════════════╗
#  DESIGN SYSTEM — WORLD-CLASS PREMIUM CSS
# ╚══════════════════════════════════════════════════════════╝
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=JetBrains+Mono:wght@300;400;500;600&family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
/* ───────────────────────────────────────────────────────
   DESIGN TOKENS
─────────────────────────────────────────────────────── */
:root {
  /* Surfaces */
  --s0: #020409;
  --s1: #060b14;
  --s2: #0a1022;
  --s3: #0f1830;
  --s4: #152040;

  /* Borders */
  --b0: rgba(255,255,255,0.04);
  --b1: rgba(255,255,255,0.08);
  --b2: rgba(255,255,255,0.14);
  --b3: rgba(99,179,255,0.30);

  /* Text */
  --t1: #e8f0fe;
  --t2: #7e9ab8;
  --t3: #3a5070;

  /* Accent palette */
  --cyan:    #22d3ee;
  --cyan-d:  #0891b2;
  --blue:    #818cf8;
  --blue-d:  #4f46e5;
  --violet:  #c084fc;
  --violet-d:#9333ea;
  --emerald: #34d399;
  --amber:   #fbbf24;
  --rose:    #fb7185;
  --orange:  #fb923c;

  /* Glow */
  --glow-c: rgba(34,211,238,0.18);
  --glow-b: rgba(129,140,248,0.18);
  --glow-v: rgba(192,132,252,0.14);
  --glow-e: rgba(52,211,153,0.18);

  /* Radii */
  --r-xs: 6px;
  --r-sm: 10px;
  --r-md: 16px;
  --r-lg: 22px;
  --r-xl: 32px;
  --r-pill: 999px;

  /* Motion */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.45, 0, 0.55, 1);
  --dur-fast: 180ms;
  --dur-base: 320ms;
  --dur-slow: 600ms;
}

/* ───────────────────────────────────────────────────────
   RESET
─────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, body, [class*="css"] {
  font-family: 'Inter', system-ui, sans-serif !important;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

/* ───────────────────────────────────────────────────────
   APP SHELL — ANIMATED MESH BACKGROUND
─────────────────────────────────────────────────────── */
.stApp {
  background-color: var(--s0) !important;
  background-image:
    radial-gradient(ellipse 140% 70%  at  5% -5%,  rgba(34,211,238,0.09)  0%, transparent 65%),
    radial-gradient(ellipse 100% 60%  at 95%  110%, rgba(129,140,248,0.10) 0%, transparent 65%),
    radial-gradient(ellipse 80%  50%  at 50%  50%,  rgba(192,132,252,0.04) 0%, transparent 65%),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40'%3E%3Ccircle cx='1' cy='1' r='0.8' fill='rgba(255,255,255,0.035)'/%3E%3C/svg%3E") !important;
  min-height: 100vh;
}

.main .block-container {
  padding: 0 2.5rem 5rem !important;
  max-width: 1380px !important;
}

/* ───────────────────────────────────────────────────────
   HIDE CHROME
─────────────────────────────────────────────────────── */
#MainMenu, .stDeployButton, footer, header { visibility: hidden !important; }
[data-testid="stToolbar"]                  { display: none !important; }

/* ───────────────────────────────────────────────────────
   SIDEBAR
─────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #040810 0%, #060c1a 60%, #040810 100%) !important;
  border-right: 1px solid var(--b0) !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
[data-testid="stSidebar"] .stMarkdown p { color: var(--t2) !important; font-size: 0.8rem !important; }

/* Sidebar brand */
.sb-brand {
  padding: 1.6rem 1rem 1.4rem;
  text-align: center;
  border-bottom: 1px solid var(--b0);
  position: relative;
  overflow: hidden;
}
.sb-brand::after {
  content: '';
  position: absolute;
  bottom: 0; left: 10%; right: 10%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--cyan), var(--blue), transparent);
}
.sb-logo-ring {
  width: 64px; height: 64px;
  border-radius: 50%;
  margin: 0 auto 0.85rem;
  position: relative;
  display: flex; align-items: center; justify-content: center;
  background: radial-gradient(circle at 40% 35%, rgba(34,211,238,0.2), rgba(129,140,248,0.1));
  border: 1.5px solid rgba(34,211,238,0.25);
  box-shadow: 0 0 40px rgba(34,211,238,0.12), 0 0 80px rgba(129,140,248,0.06);
}
.sb-logo-ring::before {
  content: '';
  position: absolute; inset: -4px;
  border-radius: 50%;
  border: 1px solid transparent;
  border-top-color: var(--cyan);
  border-right-color: var(--blue);
  animation: spin-ring 6s linear infinite;
}
@keyframes spin-ring {
  to { transform: rotate(360deg); }
}
.sb-logo-text {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  background: linear-gradient(135deg, var(--cyan), var(--blue));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.sb-wordmark {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, var(--cyan) 0%, var(--blue) 55%, var(--violet) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 0.2rem;
}
.sb-descriptor {
  font-size: 0.58rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--t3) !important;
  font-weight: 500;
  line-height: 1.4;
}
.sb-version {
  display: inline-flex; align-items: center; gap: 4px;
  margin-top: 0.65rem;
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 2px 9px 2px 7px;
  border-radius: var(--r-pill);
  background: rgba(34,211,238,0.08);
  border: 1px solid rgba(34,211,238,0.18);
  color: var(--cyan) !important;
}
.sb-version::before {
  content: '';
  width: 5px; height: 5px;
  border-radius: 50%;
  background: var(--emerald);
  box-shadow: 0 0 6px var(--emerald);
  animation: pulse-live 2s infinite;
}
@keyframes pulse-live {
  0%,100% { opacity:1; transform:scale(1); }
  50%      { opacity:0.4; transform:scale(0.7); }
}

/* Sidebar section labels */
.sb-section {
  font-size: 0.58rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  font-weight: 700;
  color: var(--t3) !important;
  padding: 1rem 0 0.35rem;
  display: flex; align-items: center; gap: 6px;
}
.sb-section::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--b1);
}

/* Sidebar status rows */
.sb-status {
  display: flex; align-items: center; gap: 8px;
  font-size: 0.72rem; font-weight: 500;
  color: var(--t2) !important;
  padding: 7px 10px;
  border-radius: var(--r-sm);
  background: rgba(255,255,255,0.02);
  border: 1px solid var(--b0);
  margin-bottom: 5px;
  transition: border-color var(--dur-fast) var(--ease-out);
}
.sb-status:hover { border-color: var(--b1); }
.sb-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}
.sb-dot.on  { background: var(--emerald); box-shadow: 0 0 8px var(--emerald); animation: pulse-live 2.5s infinite; }
.sb-dot.off { background: var(--t3); }

/* Sidebar tech stack */
.sb-stack {
  display: flex; flex-wrap: wrap; gap: 4px;
  margin-top: 0.5rem;
}
.sb-pill {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.57rem; font-weight: 500;
  padding: 3px 7px;
  border-radius: var(--r-xs);
  background: rgba(255,255,255,0.025);
  border: 1px solid var(--b1);
  color: var(--t3) !important;
  transition: all var(--dur-fast) var(--ease-out);
}
.sb-pill:hover { color: var(--t2) !important; border-color: var(--b2); }

/* File uploader */
[data-testid="stFileUploader"] section {
  background: rgba(34,211,238,0.03) !important;
  border: 1.5px dashed rgba(34,211,238,0.2) !important;
  border-radius: var(--r-md) !important;
  transition: all var(--dur-base) var(--ease-out);
}
[data-testid="stFileUploader"] section:hover {
  border-color: rgba(34,211,238,0.5) !important;
  background: rgba(34,211,238,0.06) !important;
}
[data-testid="stFileUploader"] small { color: var(--t3) !important; font-size: 0.7rem !important; }

/* ───────────────────────────────────────────────────────
   TOP NAVBAR STRIP
─────────────────────────────────────────────────────── */
.navbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.1rem 0 0.6rem;
  border-bottom: 1px solid var(--b0);
  margin-bottom: 0;
}
.nav-left { display: flex; align-items: center; gap: 10px; }
.nav-wordmark {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.9rem; font-weight: 700;
  letter-spacing: 0.04em;
  background: linear-gradient(90deg, var(--cyan), var(--blue));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.nav-slash { color: var(--b2); font-weight: 300; font-size: 1rem; }
.nav-page { font-size: 0.78rem; font-weight: 500; color: var(--t2); }
.nav-right { display: flex; align-items: center; gap: 8px; }
.nav-badge {
  font-size: 0.6rem; font-weight: 700;
  letter-spacing: 0.1em; text-transform: uppercase;
  padding: 3px 9px; border-radius: var(--r-pill);
  border: 1px solid;
}
.nav-badge.cyan   { color: var(--cyan);    border-color: rgba(34,211,238,0.25);   background: rgba(34,211,238,0.07);  }
.nav-badge.blue   { color: var(--blue);    border-color: rgba(129,140,248,0.25);  background: rgba(129,140,248,0.07); }
.nav-badge.emerald{ color: var(--emerald); border-color: rgba(52,211,153,0.25);   background: rgba(52,211,153,0.07);  }

/* ───────────────────────────────────────────────────────
   HERO
─────────────────────────────────────────────────────── */
.hero {
  padding: 3.5rem 0 2rem;
  position: relative;
}
.hero::before {
  content: '';
  position: absolute;
  top: 0; left: -2.5rem; right: -2.5rem; bottom: 0;
  background: radial-gradient(ellipse 60% 100% at 50% 0%, rgba(34,211,238,0.05) 0%, transparent 70%);
  pointer-events: none;
}
.hero-eyebrow {
  display: inline-flex; align-items: center; gap: 7px;
  font-size: 0.63rem; font-weight: 700;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--cyan);
  background: rgba(34,211,238,0.07);
  border: 1px solid rgba(34,211,238,0.18);
  padding: 4px 12px 4px 8px;
  border-radius: var(--r-pill);
  margin-bottom: 1.4rem;
}
.hero-eyebrow-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--cyan);
  box-shadow: 0 0 10px var(--cyan);
  animation: pulse-live 2s infinite;
}
.hero-h1 {
  font-family: 'Space Grotesk', sans-serif !important;
  font-size: clamp(2.6rem, 5vw, 4.2rem) !important;
  font-weight: 700 !important;
  line-height: 1.08 !important;
  letter-spacing: -0.04em !important;
  color: var(--t1) !important;
  margin-bottom: 0.2rem !important;
}
.hero-h1-line2 {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(2.6rem, 5vw, 4.2rem);
  font-weight: 700;
  line-height: 1.08;
  letter-spacing: -0.04em;
  background: linear-gradient(135deg, var(--cyan) 0%, var(--blue) 45%, var(--violet) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: block;
  margin-bottom: 1.2rem;
}
.hero-sub {
  font-size: 1rem;
  line-height: 1.7;
  color: var(--t2);
  max-width: 500px;
  font-weight: 400;
  margin-bottom: 2rem;
}
.hero-cta-row {
  display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;
  margin-bottom: 0;
}
.hero-chip {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 0.7rem; font-weight: 600;
  padding: 5px 12px;
  border-radius: var(--r-pill);
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--b1);
  color: var(--t2);
  transition: all var(--dur-fast) var(--ease-out);
}
.hero-chip:hover { border-color: var(--b2); color: var(--t1); }

.hero-rule {
  height: 1px;
  background: linear-gradient(90deg, transparent 0%, var(--b2) 25%, var(--b2) 75%, transparent 100%);
  margin: 2.5rem 0;
  position: relative;
}
.hero-rule::after {
  content: '◆';
  position: absolute;
  left: 50%; top: 50%;
  transform: translate(-50%,-50%);
  font-size: 0.4rem;
  color: var(--t3);
  background: var(--s0);
  padding: 0 6px;
}

/* ───────────────────────────────────────────────────────
   METRIC STRIP
─────────────────────────────────────────────────────── */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 2rem;
}
@media (max-width: 900px) { .kpi-grid { grid-template-columns: repeat(2,1fr); } }

.kpi-card {
  position: relative;
  border-radius: var(--r-lg);
  padding: 1.5rem 1.4rem 1.3rem;
  overflow: hidden;
  cursor: default;
  transition: transform var(--dur-base) var(--ease-out),
              box-shadow var(--dur-base) var(--ease-out),
              border-color var(--dur-base) var(--ease-out);
  /* Glass surface */
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
.kpi-card::before {
  content: '';
  position: absolute; inset: 0;
  border-radius: inherit;
  background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%);
  pointer-events: none;
}
/* Top shimmer */
.kpi-card::after {
  content: '';
  position: absolute;
  top: 0; left: 15%; right: 15%;
  height: 1px;
  border-radius: var(--r-pill);
  transition: opacity var(--dur-base);
  opacity: 0;
}
.kpi-card:hover { transform: translateY(-5px); }
.kpi-card:hover::after { opacity: 1; }

/* Per-color themes */
.kpi-c {
  background: linear-gradient(135deg, rgba(34,211,238,0.09) 0%, rgba(8,145,178,0.04) 100%);
  border: 1px solid rgba(34,211,238,0.15);
  box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 0 0 1px rgba(34,211,238,0.05);
}
.kpi-c:hover { box-shadow: 0 16px 48px rgba(34,211,238,0.14), inset 0 0 0 1px rgba(34,211,238,0.1); border-color: rgba(34,211,238,0.35); }
.kpi-c::after { background: linear-gradient(90deg, transparent, var(--cyan), transparent); }

.kpi-b {
  background: linear-gradient(135deg, rgba(129,140,248,0.09) 0%, rgba(79,70,229,0.04) 100%);
  border: 1px solid rgba(129,140,248,0.15);
  box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 0 0 1px rgba(129,140,248,0.05);
}
.kpi-b:hover { box-shadow: 0 16px 48px rgba(129,140,248,0.14), inset 0 0 0 1px rgba(129,140,248,0.1); border-color: rgba(129,140,248,0.35); }
.kpi-b::after { background: linear-gradient(90deg, transparent, var(--blue), transparent); }

.kpi-v {
  background: linear-gradient(135deg, rgba(192,132,252,0.09) 0%, rgba(147,51,234,0.04) 100%);
  border: 1px solid rgba(192,132,252,0.15);
  box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 0 0 1px rgba(192,132,252,0.05);
}
.kpi-v:hover { box-shadow: 0 16px 48px rgba(192,132,252,0.14), inset 0 0 0 1px rgba(192,132,252,0.1); border-color: rgba(192,132,252,0.35); }
.kpi-v::after { background: linear-gradient(90deg, transparent, var(--violet), transparent); }

.kpi-e {
  background: linear-gradient(135deg, rgba(52,211,153,0.09) 0%, rgba(16,185,129,0.04) 100%);
  border: 1px solid rgba(52,211,153,0.15);
  box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 0 0 1px rgba(52,211,153,0.05);
}
.kpi-e:hover { box-shadow: 0 16px 48px rgba(52,211,153,0.14), inset 0 0 0 1px rgba(52,211,153,0.1); border-color: rgba(52,211,153,0.35); }
.kpi-e::after { background: linear-gradient(90deg, transparent, var(--emerald), transparent); }

/* KPI internals */
.kpi-top { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 1rem; }
.kpi-icon {
  width: 38px; height: 38px;
  border-radius: var(--r-sm);
  display: flex; align-items: center; justify-content: center;
  font-size: 1rem;
}
.kpi-icon-c { background: rgba(34,211,238,0.12);  border: 1px solid rgba(34,211,238,0.2); }
.kpi-icon-b { background: rgba(129,140,248,0.12); border: 1px solid rgba(129,140,248,0.2); }
.kpi-icon-v { background: rgba(192,132,252,0.12); border: 1px solid rgba(192,132,252,0.2); }
.kpi-icon-e { background: rgba(52,211,153,0.12);  border: 1px solid rgba(52,211,153,0.2);  }

.kpi-tag {
  font-size: 0.52rem; font-weight: 700;
  letter-spacing: 0.12em; text-transform: uppercase;
  padding: 2px 7px; border-radius: var(--r-pill);
}
.kpi-tag-c { color: var(--cyan);    background: rgba(34,211,238,0.08);  border: 1px solid rgba(34,211,238,0.15); }
.kpi-tag-b { color: var(--blue);    background: rgba(129,140,248,0.08); border: 1px solid rgba(129,140,248,0.15); }
.kpi-tag-v { color: var(--violet);  background: rgba(192,132,252,0.08); border: 1px solid rgba(192,132,252,0.15); }
.kpi-tag-e { color: var(--emerald); background: rgba(52,211,153,0.08);  border: 1px solid rgba(52,211,153,0.15);  }

.kpi-val {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 2.4rem; font-weight: 700;
  letter-spacing: -0.05em;
  color: var(--t1);
  line-height: 1;
  margin-bottom: 0.2rem;
  font-variant-numeric: tabular-nums;
}
.kpi-lbl {
  font-size: 0.72rem; font-weight: 500;
  color: var(--t2);
  letter-spacing: 0.02em;
  margin-bottom: 0.9rem;
}
/* Progress bar */
.kpi-bar-track {
  height: 3px;
  border-radius: var(--r-pill);
  background: rgba(255,255,255,0.06);
  overflow: hidden;
}
.kpi-bar-fill {
  height: 100%;
  border-radius: var(--r-pill);
  animation: fill-bar 1.4s var(--ease-out) forwards;
  transform-origin: left;
}
@keyframes fill-bar { from { width: 0%; } }
.kpi-bar-c { background: linear-gradient(90deg, var(--cyan-d), var(--cyan)); }
.kpi-bar-b { background: linear-gradient(90deg, var(--blue-d), var(--blue)); }
.kpi-bar-v { background: linear-gradient(90deg, var(--violet-d), var(--violet)); }
.kpi-bar-e { background: linear-gradient(90deg, #059669, var(--emerald)); }

/* ───────────────────────────────────────────────────────
   TABS
─────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  gap: 3px !important;
  background: rgba(255,255,255,0.025) !important;
  border: 1px solid var(--b1) !important;
  border-radius: var(--r-xl) !important;
  padding: 4px !important;
  width: fit-content !important;
  margin-bottom: 2rem !important;
  backdrop-filter: blur(8px) !important;
}
.stTabs [data-baseweb="tab"] {
  height: 36px !important;
  border-radius: 20px !important;
  padding: 0 20px !important;
  color: var(--t2) !important;
  font-weight: 600 !important;
  font-size: 0.78rem !important;
  letter-spacing: 0.02em !important;
  background: transparent !important;
  border: none !important;
  transition: all var(--dur-fast) var(--ease-out) !important;
  font-family: 'Inter', sans-serif !important;
  white-space: nowrap !important;
}
.stTabs [data-baseweb="tab"]:hover {
  color: var(--t1) !important;
  background: rgba(255,255,255,0.05) !important;
}
.stTabs [aria-selected="true"] {
  color: #000 !important;
  font-weight: 700 !important;
  background: linear-gradient(135deg, var(--cyan) 0%, #38bdf8 40%, var(--blue) 100%) !important;
  box-shadow: 0 2px 20px rgba(34,211,238,0.4), 0 0 0 1px rgba(34,211,238,0.3) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ───────────────────────────────────────────────────────
   SECTION HEADERS
─────────────────────────────────────────────────────── */
.sec-head {
  display: flex; align-items: center; gap: 10px;
  margin: 1.8rem 0 1rem;
}
.sec-icon {
  width: 30px; height: 30px;
  border-radius: var(--r-xs);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.8rem; flex-shrink: 0;
  background: rgba(34,211,238,0.08);
  border: 1px solid rgba(34,211,238,0.15);
}
.sec-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.88rem; font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--t1);
}
.sec-badge {
  font-size: 0.55rem; font-weight: 700;
  letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--t3);
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--b0);
  padding: 2px 8px;
  border-radius: var(--r-pill);
}

/* ───────────────────────────────────────────────────────
   CHART CARD WRAPPER
─────────────────────────────────────────────────────── */
.chart-card {
  background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
  border: 1px solid var(--b1);
  border-radius: var(--r-lg);
  padding: 1.4rem 1.2rem 0.6rem;
  transition: border-color var(--dur-base) var(--ease-out),
              box-shadow var(--dur-base) var(--ease-out);
  backdrop-filter: blur(4px);
  position: relative;
  overflow: hidden;
}
.chart-card::before {
  content: '';
  position: absolute;
  top: 0; left: 20%; right: 20%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent);
}
.chart-card:hover {
  border-color: rgba(34,211,238,0.25);
  box-shadow: 0 8px 40px rgba(34,211,238,0.07);
}
.chart-title {
  font-size: 0.68rem; font-weight: 700;
  letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--t3);
  margin-bottom: 0.8rem;
}

/* ───────────────────────────────────────────────────────
   DATA TABLE
─────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
  background: var(--s2) !important;
  border-radius: var(--r-lg) !important;
  border: 1px solid var(--b1) !important;
  overflow: hidden !important;
}
[data-testid="stDataFrame"] > div { border-radius: var(--r-lg) !important; }

/* ───────────────────────────────────────────────────────
   BUTTONS
─────────────────────────────────────────────────────── */
.stButton > button {
  font-family: 'Inter', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.78rem !important;
  letter-spacing: 0.05em !important;
  text-transform: uppercase !important;
  border: none !important;
  border-radius: var(--r-md) !important;
  padding: 0.65rem 1.8rem !important;
  transition: all var(--dur-base) var(--ease-out) !important;
  position: relative !important;
  overflow: hidden !important;
  background: linear-gradient(135deg, var(--cyan) 0%, #38bdf8 50%, var(--blue) 100%) !important;
  color: #050a14 !important;
  box-shadow: 0 4px 24px rgba(34,211,238,0.28), 0 1px 0 rgba(255,255,255,0.15) inset !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 36px rgba(34,211,238,0.42), 0 1px 0 rgba(255,255,255,0.2) inset !important;
  filter: brightness(1.06) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

[data-testid="stDownloadButton"] > button {
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.75rem !important;
  letter-spacing: 0.04em !important;
  background: rgba(34,211,238,0.07) !important;
  color: var(--cyan) !important;
  border: 1px solid rgba(34,211,238,0.22) !important;
  border-radius: var(--r-md) !important;
  padding: 0.55rem 1.3rem !important;
  transition: all var(--dur-base) var(--ease-out) !important;
  box-shadow: none !important;
}
[data-testid="stDownloadButton"] > button:hover {
  background: rgba(34,211,238,0.13) !important;
  border-color: rgba(34,211,238,0.45) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 16px rgba(34,211,238,0.15) !important;
}

/* ───────────────────────────────────────────────────────
   INPUTS & CONTROLS
─────────────────────────────────────────────────────── */
[data-testid="stSelectbox"] [data-baseweb="select"] {
  background: var(--s2) !important;
  border: 1px solid var(--b2) !important;
  border-radius: var(--r-md) !important;
  color: var(--t1) !important;
  transition: border-color var(--dur-fast) !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"]:hover { border-color: rgba(34,211,238,0.3) !important; }

.stSlider [data-baseweb="slider"] [role="slider"] {
  background: linear-gradient(135deg, var(--cyan), var(--blue)) !important;
  border: 2px solid rgba(255,255,255,0.2) !important;
  box-shadow: 0 0 16px rgba(34,211,238,0.6) !important;
}
.stSlider [data-baseweb="slider"] > div > div:first-child {
  background: linear-gradient(90deg, var(--cyan), var(--blue)) !important;
}

.stRadio [role="radiogroup"] {
  background: var(--s2) !important;
  border: 1px solid var(--b1) !important;
  border-radius: var(--r-lg) !important;
  padding: 4px !important;
  gap: 3px !important;
  display: flex !important;
}

.stCheckbox [data-testid="stWidgetLabel"] {
  color: var(--t2) !important;
  font-size: 0.75rem !important;
  font-weight: 500 !important;
}

/* ───────────────────────────────────────────────────────
   ALERTS
─────────────────────────────────────────────────────── */
.stSuccess, .stWarning, .stError, .stInfo {
  border-radius: var(--r-md) !important;
  font-size: 0.82rem !important;
}

/* ───────────────────────────────────────────────────────
   EMPTY STATE — ORBITAL RING SYSTEM
─────────────────────────────────────────────────────── */
.empty-wrap {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  min-height: 62vh;
  text-align: center; padding: 3rem 2rem;
}
.orbit-system {
  position: relative;
  width: 160px; height: 160px;
  margin: 0 auto 2.4rem;
}
.orbit-core {
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
}
.orbit-core-inner {
  width: 56px; height: 56px;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 35%, rgba(34,211,238,0.5), rgba(129,140,248,0.2));
  border: 1.5px solid rgba(34,211,238,0.3);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.6rem;
  box-shadow: 0 0 40px rgba(34,211,238,0.2), 0 0 80px rgba(129,140,248,0.1);
  animation: orbit-breathe 3s ease-in-out infinite;
}
@keyframes orbit-breathe {
  0%,100% { transform: scale(1);    box-shadow: 0 0 40px rgba(34,211,238,0.2), 0 0 80px rgba(129,140,248,0.1); }
  50%      { transform: scale(1.06); box-shadow: 0 0 60px rgba(34,211,238,0.35), 0 0 100px rgba(129,140,248,0.15); }
}
.orbit-ring {
  position: absolute; inset: 0;
  border-radius: 50%;
  border: 1px solid transparent;
}
.orbit-ring-1 {
  border-color: rgba(34,211,238,0.15);
  animation: spin-cw 8s linear infinite;
}
.orbit-ring-1::before {
  content: '';
  position: absolute; top: -3px; left: 50%;
  width: 6px; height: 6px; margin-left: -3px;
  border-radius: 50%;
  background: var(--cyan);
  box-shadow: 0 0 10px var(--cyan);
}
.orbit-ring-2 {
  inset: 12px;
  border-color: rgba(192,132,252,0.12);
  animation: spin-ccw 12s linear infinite;
}
.orbit-ring-2::before {
  content: '';
  position: absolute; bottom: -3px; right: 20%;
  width: 5px; height: 5px;
  border-radius: 50%;
  background: var(--violet);
  box-shadow: 0 0 8px var(--violet);
}
.orbit-ring-3 {
  inset: -14px;
  border-color: rgba(129,140,248,0.08);
  animation: spin-cw 20s linear infinite;
}
.orbit-ring-3::before {
  content: '';
  position: absolute; top: 20%; right: -3px;
  width: 4px; height: 4px;
  border-radius: 50%;
  background: var(--blue);
  box-shadow: 0 0 8px var(--blue);
}
@keyframes spin-cw  { to { transform: rotate(360deg); } }
@keyframes spin-ccw { to { transform: rotate(-360deg); } }

.empty-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.8rem; font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--t1);
  margin-bottom: 0.6rem;
}
.empty-sub {
  font-size: 0.88rem;
  color: var(--t2);
  line-height: 1.7;
  max-width: 360px;
  margin-bottom: 2rem;
}
.empty-chips {
  display: flex; flex-wrap: wrap;
  justify-content: center; gap: 6px;
  max-width: 520px;
}
.empty-chip {
  font-size: 0.68rem; font-weight: 600;
  letter-spacing: 0.04em;
  padding: 5px 13px;
  border-radius: var(--r-pill);
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--b1);
  color: var(--t2);
  transition: all var(--dur-fast) var(--ease-out);
}
.empty-chip:hover { border-color: rgba(34,211,238,0.25); color: var(--cyan); }

/* ───────────────────────────────────────────────────────
   ML RESULT CARD
─────────────────────────────────────────────────────── */
.score-card {
  position: relative;
  background: linear-gradient(135deg, rgba(34,211,238,0.07) 0%, rgba(129,140,248,0.05) 100%);
  border: 1px solid rgba(34,211,238,0.18);
  border-radius: var(--r-lg);
  padding: 2rem;
  text-align: center;
  overflow: hidden;
  margin-bottom: 1.5rem;
}
.score-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--cyan), var(--blue), var(--violet));
}
.score-card::after {
  content: '';
  position: absolute; inset: 0;
  background: radial-gradient(ellipse 60% 80% at 50% 0%, rgba(34,211,238,0.08) 0%, transparent 70%);
  pointer-events: none;
}
.score-num {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 4.5rem; font-weight: 700;
  letter-spacing: -0.06em;
  background: linear-gradient(135deg, var(--cyan), var(--blue));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 0.3rem;
}
.score-lbl {
  font-size: 0.65rem; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--t3);
}

/* ───────────────────────────────────────────────────────
   ML INFO PANEL
─────────────────────────────────────────────────────── */
.algo-panel {
  border-radius: var(--r-md);
  padding: 1.1rem 1.2rem;
  margin-top: 2.2rem;
}
.algo-panel-c { background: rgba(34,211,238,0.05);  border: 1px solid rgba(34,211,238,0.13); }
.algo-panel-b { background: rgba(129,140,248,0.05); border: 1px solid rgba(129,140,248,0.13); }
.algo-kw {
  font-size: 0.58rem; letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--t3); margin-bottom: 0.35rem; font-weight: 700;
}
.algo-name {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.95rem; font-weight: 700;
  color: var(--t1); margin-bottom: 0.2rem;
}
.algo-desc { font-size: 0.68rem; color: var(--t2); line-height: 1.5; }

/* ───────────────────────────────────────────────────────
   MISC
─────────────────────────────────────────────────────── */
hr { border-color: var(--b0) !important; }
[data-testid="stSpinner"] svg { stroke: var(--cyan) !important; }
</style>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════╗
#  HELPERS
# ╚══════════════════════════════════════════════════════════╝
PALETTE = ['#22d3ee', '#818cf8', '#c084fc', '#34d399', '#fbbf24', '#fb7185', '#fb923c']

def hex_to_rgba(hex_color: str, alpha: float = 0.12) -> str:
    """Convert #RRGGBB hex to rgba(r,g,b,alpha) string."""
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f'rgba({r},{g},{b},{alpha})'

def chart_theme(fig, title="", height=340):
    fig.update_layout(
        height=height,
        title=dict(
            text=title,
            font=dict(family="Space Grotesk, Inter", size=12, color="#7e9ab8"),
            x=0, xanchor='left', pad=dict(l=0, b=8)
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", color="#7e9ab8", size=10),
        margin=dict(l=4, r=4, t=36 if title else 8, b=4),
        legend=dict(
            font=dict(size=9, color="#7e9ab8"),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            orientation='h',
            yanchor='bottom', y=1.02, xanchor='right', x=1
        ),
        xaxis=dict(
            showgrid=False, zeroline=False,
            color="#3a5070", tickfont=dict(size=9),
            linecolor='rgba(255,255,255,0.04)'
        ),
        yaxis=dict(
            showgrid=True, gridcolor='rgba(255,255,255,0.04)',
            zeroline=False, color="#3a5070", tickfont=dict(size=9)
        ),
        coloraxis_colorbar=dict(
            thickness=10, len=0.6,
            tickfont=dict(size=8, color="#7e9ab8"),
            outlinewidth=0
        )
    )
    return fig

def sec(icon, title, badge=""):
    badge_html = f'<span class="sec-badge">{badge}</span>' if badge else ''
    return f"""<div class="sec-head">
      <div class="sec-icon">{icon}</div>
      <span class="sec-title">{title}</span>
      {badge_html}
    </div>"""

def chart_wrap(content_fn, *args, **kwargs):
    """Render a chart inside a styled card."""
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    content_fn(*args, **kwargs)
    st.markdown('</div>', unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════╗
#  SIDEBAR
# ╚══════════════════════════════════════════════════════════╝
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
      <div class="sb-logo-ring">
        <span class="sb-logo-text">⚡</span>
      </div>
      <div class="sb-wordmark">AADES</div>
      <div class="sb-descriptor">Adaptive Auto Data<br>Evaluation System</div>
      <span class="sb-version">v2.0 · Live</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-section">System Status</div>
    <div class="sb-status"><div class="sb-dot on"></div>Analytics Engine &nbsp;·&nbsp; Online</div>
    <div class="sb-status"><div class="sb-dot on"></div>ML Pipeline &nbsp;·&nbsp; Ready</div>
    <div class="sb-status"><div class="sb-dot on"></div>Viz Layer &nbsp;·&nbsp; Loaded</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Data Source</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload dataset", type=['csv', 'xlsx', 'xls', 'json'],
        label_visibility="collapsed",
        help="CSV · Excel (.xlsx/.xls) · JSON"
    )

    st.markdown('<div class="sb-section">Display</div>', unsafe_allow_html=True)
    if 'dark_mode' not in st.session_state:
        st.session_state['dark_mode'] = True
    st.checkbox("Dark Mode", value=st.session_state['dark_mode'], key='dark_mode_toggle')

    st.markdown("""
    <div class="sb-section">Stack</div>
    <div class="sb-stack">
      <span class="sb-pill">Python 3.11</span>
      <span class="sb-pill">Streamlit</span>
      <span class="sb-pill">Pandas</span>
      <span class="sb-pill">NumPy</span>
      <span class="sb-pill">scikit-learn</span>
      <span class="sb-pill">Plotly</span>
    </div>
    """, unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════╗
#  NAVBAR
# ╚══════════════════════════════════════════════════════════╝
st.markdown("""
<div class="navbar">
  <div class="nav-left">
    <span class="nav-wordmark">AADES</span>
    <span class="nav-slash">/</span>
    <span class="nav-page">Intelligent Data Platform</span>
  </div>
  <div class="nav-right">
    <span class="nav-badge cyan">ML-Powered</span>
    <span class="nav-badge blue">v2.0</span>
    <span class="nav-badge emerald">● Live</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════╗
#  HERO
# ╚══════════════════════════════════════════════════════════╝
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">
    <span class="hero-eyebrow-dot"></span>
    Adaptive Auto Data Evaluation System
  </div>
  <h1 class="hero-h1">Turn Raw Data Into</h1>
  <span class="hero-h1-line2">Actionable Intelligence</span>
  <p class="hero-sub">
    Upload any CSV, Excel, or JSON dataset and instantly unlock 
    automated descriptive stats, correlation heatmaps, pattern clustering,
    and regression analysis — zero code required.
  </p>
  <div class="hero-cta-row">
    <span class="hero-chip">📊 Descriptive Stats</span>
    <span class="hero-chip">🔥 Correlation Matrix</span>
    <span class="hero-chip">🤖 K-Means Clustering</span>
    <span class="hero-chip">📈 OLS Regression</span>
    <span class="hero-chip">💾 CSV Export</span>
  </div>
</div>
<div class="hero-rule"></div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════╗
#  EMPTY STATE
# ╚══════════════════════════════════════════════════════════╝
if uploaded_file is None:
    st.markdown("""
    <div class="empty-wrap">
      <div class="orbit-system">
        <div class="orbit-ring orbit-ring-3"></div>
        <div class="orbit-ring orbit-ring-1"></div>
        <div class="orbit-ring orbit-ring-2"></div>
        <div class="orbit-core">
          <div class="orbit-core-inner">⚡</div>
        </div>
      </div>
      <div class="empty-title">Ready to Ignite</div>
      <p class="empty-sub">
        Drop a dataset in the sidebar panel to activate the full 
        analytics and machine learning pipeline.
      </p>
      <div class="empty-chips">
        <span class="empty-chip">🗂 CSV / Excel / JSON</span>
        <span class="empty-chip">⚡ Instant processing</span>
        <span class="empty-chip">🤖 Auto ML config</span>
        <span class="empty-chip">📊 Interactive charts</span>
        <span class="empty-chip">🔍 Schema inspector</span>
        <span class="empty-chip">💾 One-click export</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ╔══════════════════════════════════════════════════════════╗
#  LOAD DATA
# ╚══════════════════════════════════════════════════════════╝
try:
    fname = uploaded_file.name
    if fname.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif fname.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(uploaded_file)
    elif fname.endswith('.json'):
        df = pd.read_json(uploaded_file)
    else:
        st.error("⚠️ Unsupported format — please upload CSV, Excel, or JSON.")
        st.stop()
    st.toast(f"⚡ **{fname}** loaded — {df.shape[0]:,} rows × {df.shape[1]} cols", icon="✅")
except Exception as e:
    st.error(f"Failed to parse `{fname}`: {e}")
    st.stop()

num_df     = df.select_dtypes(include=[np.number]).dropna()
missing    = int(df.isnull().sum().sum())
complete   = round((1 - missing / max(df.size, 1)) * 100, 1)
n_num      = len(num_df.columns)
bar_n_num  = min(100, round(n_num / max(df.shape[1], 1) * 100))
bar_compl  = min(100, complete)


# ╔══════════════════════════════════════════════════════════╗
#  KPI STRIP
# ╚══════════════════════════════════════════════════════════╝
st.markdown(f"""
<div class="kpi-grid">

  <div class="kpi-card kpi-c">
    <div class="kpi-top">
      <div class="kpi-icon kpi-icon-c">📊</div>
      <span class="kpi-tag kpi-tag-c">Records</span>
    </div>
    <div class="kpi-val">{df.shape[0]:,}</div>
    <div class="kpi-lbl">Total Rows Loaded</div>
    <div class="kpi-bar-track"><div class="kpi-bar-fill kpi-bar-c" style="width:72%"></div></div>
  </div>

  <div class="kpi-card kpi-b">
    <div class="kpi-top">
      <div class="kpi-icon kpi-icon-b">🧩</div>
      <span class="kpi-tag kpi-tag-b">Features</span>
    </div>
    <div class="kpi-val">{df.shape[1]}</div>
    <div class="kpi-lbl">Columns Detected</div>
    <div class="kpi-bar-track"><div class="kpi-bar-fill kpi-bar-b" style="width:60%"></div></div>
  </div>

  <div class="kpi-card kpi-v">
    <div class="kpi-top">
      <div class="kpi-icon kpi-icon-v">🔢</div>
      <span class="kpi-tag kpi-tag-v">Numeric</span>
    </div>
    <div class="kpi-val">{n_num}</div>
    <div class="kpi-lbl">Numeric Features</div>
    <div class="kpi-bar-track"><div class="kpi-bar-fill kpi-bar-v" style="width:{bar_n_num}%"></div></div>
  </div>

  <div class="kpi-card kpi-e">
    <div class="kpi-top">
      <div class="kpi-icon kpi-icon-e">✅</div>
      <span class="kpi-tag kpi-tag-e">Quality</span>
    </div>
    <div class="kpi-val">{complete}%</div>
    <div class="kpi-lbl">Data Completeness</div>
    <div class="kpi-bar-track"><div class="kpi-bar-fill kpi-bar-e" style="width:{bar_compl}%"></div></div>
  </div>

</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════╗
#  TABS
# ╚══════════════════════════════════════════════════════════╝
t_overview, t_analysis, t_ml = st.tabs([
    "  📋  Overview  ",
    "  📈  Analysis  ",
    "  🤖  ML Engine  ",
])


# ══════════════════════════════════════════
#  TAB 1 · OVERVIEW
# ══════════════════════════════════════════
with t_overview:

    # Action bar
    c_dl, c_sp = st.columns([1, 4])
    with c_dl:
        st.download_button(
            "⬇  Export CSV",
            data=df.to_csv(index=False).encode(),
            file_name=f"{fname.rsplit('.',1)[0]}_aades.csv",
            mime="text/csv",
            use_container_width=True
        )

    # Data preview
    st.markdown(sec("👁", "Data Preview", f"First 15 of {df.shape[0]:,} rows"), unsafe_allow_html=True)
    st.dataframe(df.head(15), use_container_width=True, height=340)

    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)

    # Schema + Stats side by side
    c_schema, c_stats = st.columns(2, gap="large")

    with c_schema:
        st.markdown(sec("🗂", "Schema Inspector"), unsafe_allow_html=True)
        info_df = pd.DataFrame({
            'Dtype':    df.dtypes.astype(str),
            'Missing':  df.isnull().sum(),
            'Missing%': (df.isnull().sum() / len(df) * 100).round(1).astype(str) + '%',
            'Unique':   df.nunique(),
            'Sample':   [str(df[c].dropna().iloc[0]) if len(df[c].dropna()) else "—" for c in df.columns]
        })
        st.dataframe(info_df, use_container_width=True, height=300)

    with c_stats:
        st.markdown(sec("📐", "Descriptive Statistics", "Numeric cols"), unsafe_allow_html=True)
        if not num_df.empty:
            st.dataframe(num_df.describe().T.round(3), use_container_width=True, height=300)
        else:
            st.warning("No numeric columns found.")


# ══════════════════════════════════════════
#  TAB 2 · ANALYSIS
# ══════════════════════════════════════════
with t_analysis:

    if num_df.empty:
        st.warning("No numeric features detected in your dataset. Please upload data with numeric columns.")
    else:
        # Row 1: Histogram + Heatmap
        c_hist, c_heat = st.columns(2, gap="large")

        with c_hist:
            st.markdown(sec("📊", "Feature Distribution", "Histogram + box"), unsafe_allow_html=True)
            feat = st.selectbox("Column", options=num_df.columns, label_visibility="collapsed")
            fig_h = px.histogram(num_df, x=feat, marginal="box", color_discrete_sequence=['#22d3ee'])
            fig_h.update_traces(
                marker_line_color='rgba(34,211,238,0.25)',
                marker_line_width=0.4,
                opacity=0.85
            )
            fig_h.data[1].marker.color = '#818cf8'  # box trace
            chart_theme(fig_h)
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(fig_h, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

        with c_heat:
            st.markdown(sec("🔥", "Correlation Matrix", "Pearson r"), unsafe_allow_html=True)
            corr = num_df.corr()
            fig_c = px.imshow(
                corr, text_auto=".2f", aspect="auto",
                color_continuous_scale=[
                    [0.00, '#4f46e5'], [0.25, '#0a1022'],
                    [0.50, '#0a1022'], [0.75, '#0a1022'],
                    [1.00, '#22d3ee']
                ],
                zmin=-1, zmax=1
            )
            fig_c.update_traces(textfont=dict(size=8, color="#e8f0fe"))
            chart_theme(fig_c)
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(fig_c, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

        # Row 2: Box plots
        st.markdown(sec("📦", "Distribution Spread", "Box + whisker per feature"), unsafe_allow_html=True)
        cols_bp = list(num_df.columns[:min(10, len(num_df.columns))])
        fig_bp = go.Figure()
        for i, col in enumerate(cols_bp):
            c = PALETTE[i % len(PALETTE)]
            fig_bp.add_trace(go.Box(
                y=num_df[col], name=col,
                marker_color=c, line_color=c,
                line_width=1.5,
                boxmean='sd',
                fillcolor=hex_to_rgba(c, 0.10),
                marker=dict(size=3, opacity=0.5)
            ))
        chart_theme(fig_bp, height=300)
        fig_bp.update_layout(showlegend=False)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_bp, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

        # Row 3: Scatter matrix (if ≤6 numeric cols)
        if 2 <= len(num_df.columns) <= 6:
            st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
            st.markdown(sec("🔗", "Pairwise Scatter Matrix", "All numeric pairs"), unsafe_allow_html=True)
            fig_sp = px.scatter_matrix(
                num_df,
                dimensions=list(num_df.columns),
                color_discrete_sequence=['#22d3ee']
            )
            fig_sp.update_traces(
                diagonal_visible=False,
                marker=dict(size=3, opacity=0.55, color='#22d3ee'),
                selected=dict(marker=dict(color='#c084fc')),
            )
            chart_theme(fig_sp, height=420)
            fig_sp.update_layout(
                font_color="#7e9ab8",
                xaxis_showgrid=False, yaxis_showgrid=False,
            )
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.plotly_chart(fig_sp, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════
#  TAB 3 · ML ENGINE
# ══════════════════════════════════════════
with t_ml:

    if num_df.empty:
        st.warning("ML pipeline requires at least one numeric column.")
        st.stop()

    st.markdown(sec("🤖", "Machine Learning Engine", "Auto-configured"), unsafe_allow_html=True)

    algo = st.radio(
        "Algorithm",
        ["  🔵  K-Means Clustering  ", "  📈  Linear Regression  "],
        horizontal=True,
        label_visibility="collapsed"
    )
    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)

    # ── K-MEANS ─────────────────────────────────────
    if "K-Means" in algo:
        if len(num_df) < 2:
            st.warning("Need at least 2 rows for clustering.")
        else:
            c_cfg, c_info = st.columns([3, 1], gap="large")
            with c_cfg:
                st.markdown(sec("⚙", "Configuration"), unsafe_allow_html=True)
                k = st.slider("Number of Clusters (K)", 2, 10, 3)

            with c_info:
                st.markdown(f"""
                <div class="algo-panel algo-panel-c">
                  <div class="algo-kw">Algorithm</div>
                  <div class="algo-name">K-Means++</div>
                  <div class="algo-desc">
                    StandardScaler preprocessing<br>
                    n_init=auto · seed 42<br>
                    K = {k} clusters
                  </div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

            if st.button("⚡  Run Clustering Engine"):
                with st.spinner("Fitting K-Means model…"):
                    time.sleep(0.25)
                    sc   = StandardScaler()
                    X_sc = sc.fit_transform(num_df)
                    km   = KMeans(n_clusters=k, random_state=42, n_init='auto').fit(X_sc)
                    cdf  = num_df.copy()
                    cdf['Cluster'] = [f"Cluster {i+1}" for i in km.labels_]

                st.toast(f"✅ {k} clusters identified!", icon="🎉")

                c1, c2 = st.columns(2, gap="large")

                with c1:
                    st.markdown(sec("🍩", "Cluster Distribution"), unsafe_allow_html=True)
                    cc = cdf['Cluster'].value_counts().reset_index()
                    cc.columns = ['Cluster', 'Count']
                    fig_pie = px.pie(
                        cc, names='Cluster', values='Count', hole=0.65,
                        color_discrete_sequence=PALETTE
                    )
                    fig_pie.update_traces(
                        textfont=dict(size=9, color="#e8f0fe"),
                        marker=dict(line=dict(color='rgba(0,0,0,0.4)', width=2)),
                        pull=[0.04] + [0] * (k - 1)
                    )
                    chart_theme(fig_pie, height=320)
                    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                    st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
                    st.markdown('</div>', unsafe_allow_html=True)

                with c2:
                    if len(num_df.columns) >= 2:
                        x0, y0 = num_df.columns[0], num_df.columns[1]
                        st.markdown(sec("💠", f"{x0} vs {y0}", "2D cluster view"), unsafe_allow_html=True)
                        fig_sc = px.scatter(
                            cdf, x=x0, y=y0, color='Cluster',
                            color_discrete_sequence=PALETTE, opacity=0.82
                        )
                        fig_sc.update_traces(
                            marker=dict(size=7, line=dict(width=0.6, color='rgba(0,0,0,0.4)'))
                        )
                        chart_theme(fig_sc, height=320)
                        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                        st.plotly_chart(fig_sc, use_container_width=True, config={'displayModeBar': False})
                        st.markdown('</div>', unsafe_allow_html=True)

                # Inertia bar
                st.markdown(sec("📉", "Cluster Inertia"), unsafe_allow_html=True)
                inertias = []
                for ki in range(2, min(k + 4, len(num_df))):
                    km_i = KMeans(n_clusters=ki, random_state=42, n_init='auto').fit(X_sc)
                    inertias.append({'K': ki, 'Inertia': km_i.inertia_})
                idf = pd.DataFrame(inertias)
                fig_elbow = px.line(
                    idf, x='K', y='Inertia',
                    markers=True, color_discrete_sequence=['#22d3ee']
                )
                fig_elbow.update_traces(
                    line=dict(width=2.5),
                    marker=dict(size=8, color='#22d3ee',
                                line=dict(color='rgba(34,211,238,0.4)', width=4))
                )
                fig_elbow.add_vline(x=k, line_dash="dash", line_color="rgba(192,132,252,0.5)", line_width=1.5)
                chart_theme(fig_elbow, height=260)
                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                st.plotly_chart(fig_elbow, use_container_width=True, config={'displayModeBar': False})
                st.markdown('</div>', unsafe_allow_html=True)

    # ── LINEAR REGRESSION ──────────────────────────────
    else:
        if len(num_df) < 5 or num_df.shape[1] < 2:
            st.warning("Need ≥ 5 rows and ≥ 2 numeric columns for regression.")
        else:
            c_cfg2, c_info2 = st.columns([3, 1], gap="large")
            with c_cfg2:
                st.markdown(sec("🎯", "Model Configuration"), unsafe_allow_html=True)
                target = st.selectbox("Target Variable (Y)", options=num_df.columns,
                                      index=len(num_df.columns) - 1)
                feats = [c for c in num_df.columns if c != target]

            with c_info2:
                st.markdown(f"""
                <div class="algo-panel algo-panel-b">
                  <div class="algo-kw">Algorithm</div>
                  <div class="algo-name">OLS Regression</div>
                  <div class="algo-desc">
                    scikit-learn LinearRegression<br>
                    {len(feats)} predictor{'s' if len(feats) != 1 else ''}<br>
                    Target: <strong style="color:#c084fc">{target}</strong>
                  </div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

            if st.button("🚀  Train Predictive Model"):
                with st.spinner("Training OLS model…"):
                    time.sleep(0.25)
                    X  = num_df[feats].values
                    y  = num_df[target].values
                    mdl = LinearRegression().fit(X, y)
                    r2  = mdl.score(X, y)
                    yh  = mdl.predict(X)

                st.toast(f"🤖 R² = {r2:.4f}", icon="✅")

                # Score hero card
                quality = "Excellent" if r2 > 0.8 else "Good" if r2 > 0.5 else "Moderate"
                st.markdown(f"""
                <div class="score-card">
                  <div class="score-num">{r2:.4f}</div>
                  <div class="score-lbl">R² · Coefficient of Determination &nbsp;·&nbsp; {quality} Fit</div>
                </div>""", unsafe_allow_html=True)

                # Actual vs Predicted
                n = min(100, len(y))
                st.markdown(sec("📈", f"Actual vs Predicted — {target}", f"First {n} samples"), unsafe_allow_html=True)
                fig_ap = go.Figure()
                idx = list(range(n))
                fig_ap.add_trace(go.Scatter(
                    x=idx, y=y[:n], name='Actual',
                    mode='lines',
                    line=dict(color='#c084fc', width=2.5),
                    fill='tozeroy', fillcolor='rgba(192,132,252,0.06)'
                ))
                fig_ap.add_trace(go.Scatter(
                    x=idx, y=yh[:n], name='Predicted',
                    mode='lines',
                    line=dict(color='#22d3ee', width=2, dash='dot')
                ))
                chart_theme(fig_ap, height=320)
                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                st.plotly_chart(fig_ap, use_container_width=True, config={'displayModeBar': False})
                st.markdown('</div>', unsafe_allow_html=True)

                # Residuals
                c_res, c_coef = st.columns(2, gap="large")
                with c_res:
                    st.markdown(sec("🎯", "Residuals", "Actual − Predicted"), unsafe_allow_html=True)
                    residuals = y[:n] - yh[:n]
                    fig_res = go.Figure()
                    fig_res.add_trace(go.Scatter(
                        x=idx, y=residuals,
                        mode='markers',
                        marker=dict(
                            color=residuals, colorscale=[[0,'#818cf8'],[0.5,'#7e9ab8'],[1,'#22d3ee']],
                            size=6, opacity=0.75,
                            line=dict(width=0.4, color='rgba(0,0,0,0.5)')
                        ),
                        name='Residual'
                    ))
                    fig_res.add_hline(y=0, line_color='rgba(255,255,255,0.12)', line_width=1, line_dash='dash')
                    chart_theme(fig_res, height=280)
                    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                    st.plotly_chart(fig_res, use_container_width=True, config={'displayModeBar': False})
                    st.markdown('</div>', unsafe_allow_html=True)

                with c_coef:
                    st.markdown(sec("🏋", "Feature Coefficients", "Sorted by |magnitude|"), unsafe_allow_html=True)
                    coef_df = pd.DataFrame({'Feature': feats, 'Coefficient': mdl.coef_})
                    coef_df = coef_df.assign(Abs=coef_df['Coefficient'].abs()).sort_values('Abs')
                    colors = ['#fb7185' if v < 0 else '#22d3ee' for v in coef_df['Coefficient']]
                    fig_coef = go.Figure(go.Bar(
                        x=coef_df['Coefficient'], y=coef_df['Feature'],
                        orientation='h',
                        marker=dict(color=colors, opacity=0.85,
                                    line=dict(color='rgba(0,0,0,0.3)', width=0.5)),
                    ))
                    chart_theme(fig_coef, height=280)
                    fig_coef.update_layout(showlegend=False)
                    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                    st.plotly_chart(fig_coef, use_container_width=True, config={'displayModeBar': False})
                    st.markdown('</div>', unsafe_allow_html=True)
