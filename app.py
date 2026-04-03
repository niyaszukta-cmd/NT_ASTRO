import streamlit as st
import datetime
import math
import pytz
from groq import Groq
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF
import base64
import io
import os
from PIL import Image

# ─────────────────────────────────────────────
#  LOGO HELPER
# ─────────────────────────────────────────────
# ── Logo embedded as base64 — no external file needed ──
LOGO_B64 = "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"
LOGO_B64_PDF = "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"  # smaller version for PDF embedding
LOGO_PATH = None  # not used — logo is embedded

def get_logo_base64(path=None):
    return LOGO_B64

def get_logo_html(width="160px", style=""):
    return f'<img src="data:image/jpeg;base64,{LOGO_B64}" width="{width}" style="border-radius:8px;{style}" alt="NyzTrade Logo"/>'


# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="VedicTrade · Astro Finance Dashboard",
    page_icon="🔱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  THEME & CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700;900&family=Cinzel:wght@400;600;700&family=Raleway:wght@300;400;500;600&display=swap');

:root {
  --gold:        #C9A84C;
  --gold-light:  #E8C97A;
  --gold-dark:   #8B6914;
  --deep:        #0A0A14;
  --deep2:       #0F0F1E;
  --panel:       #13132A;
  --panel2:      #1A1A35;
  --accent:      #6B3FA0;
  --accent2:     #8B5CF6;
  --saffron:     #FF6B00;
  --crimson:     #C0392B;
  --teal:        #1ABC9C;
  --text:        #E8E0D0;
  --muted:       #8A8090;
}

/* ── Global reset ── */
html, body, [class*="css"] {
  background-color: var(--deep) !important;
  color: var(--text) !important;
  font-family: 'Raleway', sans-serif !important;
}
.stApp { background: var(--deep) !important; }

/* ── Hide default Streamlit elements ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0D0D20 0%, #110B2D 100%) !important;
  border-right: 1px solid var(--gold-dark) !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stTextInput label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
  color: var(--gold-light) !important;
  font-family: 'Cinzel', serif !important;
}

/* ── Gold divider ── */
.gold-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
  margin: 1.5rem 0;
}

/* ── Section cards ── */
.astro-card {
  background: linear-gradient(135deg, var(--panel) 0%, var(--panel2) 100%);
  border: 1px solid var(--gold-dark);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(201,168,76,0.1);
}

/* ── Metric chips ── */
.metric-chip {
  display: inline-block;
  background: var(--panel2);
  border: 1px solid var(--gold-dark);
  border-radius: 8px;
  padding: 0.5rem 1rem;
  margin: 0.3rem;
  font-family: 'Cinzel', serif;
  font-size: 0.85rem;
}
.metric-chip .val { color: var(--gold-light); font-size: 1.1rem; font-weight: 700; }
.metric-chip .lbl { color: var(--muted); font-size: 0.7rem; display: block; }

/* ── Status pills ── */
.pill-good  { background:#1A3A2A; border:1px solid #27AE60; color:#2ECC71; border-radius:20px; padding:0.2rem 0.8rem; font-size:0.8rem; }
.pill-bad   { background:#3A1A1A; border:1px solid #C0392B; color:#E74C3C; border-radius:20px; padding:0.2rem 0.8rem; font-size:0.8rem; }
.pill-warn  { background:#3A2A0A; border:1px solid #E67E22; color:#F39C12; border-radius:20px; padding:0.2rem 0.8rem; font-size:0.8rem; }
.pill-neut  { background:#1A1A3A; border:1px solid #7B68EE; color:#9B84EE; border-radius:20px; padding:0.2rem 0.8rem; font-size:0.8rem; }

/* ── Section heading ── */
.sec-head {
  font-family: 'Cinzel', serif;
  font-size: 1.1rem;
  color: var(--gold);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 0.8rem;
}

/* ── AI response box ── */
.ai-box {
  background: linear-gradient(135deg, #0D0D25, #160B2E);
  border: 1px solid var(--accent);
  border-left: 4px solid var(--gold);
  border-radius: 10px;
  padding: 1.2rem 1.5rem;
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--text);
}

/* ── Choghadiya time blocks ── */
.chog-block {
  border-radius: 8px;
  padding: 0.6rem 1rem;
  margin: 0.3rem 0;
  font-family: 'Cinzel', serif;
  font-size: 0.82rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.chog-amrit  { background:#0F2A1A; border:1px solid #27AE60; }
.chog-shubh  { background:#1A2A0F; border:1px solid #82E048; }
.chog-labh   { background:#0F1A2A; border:1px solid #3498DB; }
.chog-char   { background:#1A1A0A; border:1px solid #F1C40F; }
.chog-kal    { background:#2A0F0F; border:1px solid #C0392B; }
.chog-udveg  { background:#2A1F0F; border:1px solid #E67E22; }
.chog-rog    { background:#2A0F2A; border:1px solid #8E44AD; }

/* ── Buttons ── */
.stButton > button {
  background: linear-gradient(135deg, var(--gold-dark), var(--gold)) !important;
  color: #0A0A0A !important;
  border: none !important;
  font-family: 'Cinzel', serif !important;
  font-weight: 700 !important;
  border-radius: 8px !important;
  letter-spacing: 1px !important;
  transition: all 0.3s ease !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(201,168,76,0.4) !important;
}

/* ── Inputs ── */
.stTextInput input, .stNumberInput input, .stSelectbox select,
.stDateInput input, .stTimeInput input {
  background: var(--panel2) !important;
  border: 1px solid var(--gold-dark) !important;
  color: var(--text) !important;
  border-radius: 8px !important;
  font-family: 'Raleway', sans-serif !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--panel) !important;
  border-radius: 10px !important;
  padding: 4px !important;
  border: 1px solid var(--gold-dark) !important;
}
.stTabs [data-baseweb="tab"] {
  color: var(--muted) !important;
  font-family: 'Cinzel', serif !important;
  font-size: 0.82rem !important;
  letter-spacing: 1px !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--gold-dark), var(--gold)) !important;
  color: #0A0A0A !important;
  border-radius: 8px !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--gold) !important; }

/* ── Progress ── */
.stProgress > div > div { background: linear-gradient(90deg, var(--gold-dark), var(--gold)) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  VEDIC DATA TABLES
# ─────────────────────────────────────────────

WEEKDAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

# Choghadiya order for Day (sunrise to sunset) — starting period varies by weekday
# Format: (name, quality)  — 8 periods per day
CHOG_DAY_ORDER = {
    "Monday":    ["Amrit","Kaal","Shubh","Rog","Udveg","Char","Labh","Amrit"],
    "Tuesday":   ["Rog","Udveg","Char","Labh","Amrit","Kaal","Shubh","Rog"],
    "Wednesday": ["Labh","Amrit","Kaal","Shubh","Rog","Udveg","Char","Labh"],
    "Thursday":  ["Shubh","Rog","Udveg","Char","Labh","Amrit","Kaal","Shubh"],
    "Friday":    ["Char","Labh","Amrit","Kaal","Shubh","Rog","Udveg","Char"],
    "Saturday":  ["Kaal","Shubh","Rog","Udveg","Char","Labh","Amrit","Kaal"],
    "Sunday":    ["Udveg","Char","Labh","Amrit","Kaal","Shubh","Rog","Udveg"],
}
CHOG_NIGHT_ORDER = {
    "Monday":    ["Shubh","Amrit","Char","Rog","Kaal","Labh","Udveg","Shubh"],
    "Tuesday":   ["Char","Rog","Kaal","Labh","Udveg","Shubh","Amrit","Char"],
    "Wednesday": ["Kaal","Labh","Udveg","Shubh","Amrit","Char","Rog","Kaal"],
    "Thursday":  ["Amrit","Char","Rog","Kaal","Labh","Udveg","Shubh","Amrit"],
    "Friday":    ["Rog","Kaal","Labh","Udveg","Shubh","Amrit","Char","Rog"],
    "Saturday":  ["Udveg","Shubh","Amrit","Char","Rog","Kaal","Labh","Udveg"],
    "Sunday":    ["Labh","Udveg","Shubh","Amrit","Char","Rog","Kaal","Labh"],
}
CHOG_QUALITY = {
    "Amrit": ("🟢","Highly Auspicious","Best for entry/exit","#27AE60","chog-amrit"),
    "Shubh": ("🟩","Auspicious","Good for trading","#82E048","chog-shubh"),
    "Labh":  ("🔵","Beneficial","Favourable gains","#3498DB","chog-labh"),
    "Char":  ("🟡","Neutral","Moderate trading","#F1C40F","chog-char"),
    "Kaal":  ("🔴","Inauspicious","Avoid new positions","#C0392B","chog-kal"),
    "Udveg": ("🟠","Unfavourable","High risk period","#E67E22","chog-udveg"),
    "Rog":   ("🟣","Malefic","Best to avoid","#8E44AD","chog-rog"),
}

RAHU_KALAM = {
    "Monday":    (7,5),   # 7th slot of day (1.5hr slots from sunrise)
    "Tuesday":   (6,5),
    "Wednesday": (5,5),
    "Thursday":  (6,5),
    "Friday":    (4,5),
    "Saturday":  (3,5),
    "Sunday":    (8,5),
}
RAHU_KALAM_SLOTS = {
    "Monday":    (15,16.5),
    "Tuesday":   (7.5,9),
    "Wednesday": (12,13.5),
    "Thursday":  (13.5,15),
    "Friday":    (10.5,12),
    "Saturday":  (9,10.5),
    "Sunday":    (16.5,18),
}

NAKSHATRAS = [
    "Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu",
    "Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta",
    "Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula","Purva Ashadha",
    "Uttara Ashadha","Shravana","Dhanishtha","Shatabhisha","Purva Bhadrapada",
    "Uttara Bhadrapada","Revati"
]

RASI = ["Mesha (Aries)","Vrishabha (Taurus)","Mithuna (Gemini)","Karka (Cancer)",
        "Simha (Leo)","Kanya (Virgo)","Tula (Libra)","Vrishchika (Scorpio)",
        "Dhanu (Sagittarius)","Makara (Capricorn)","Kumbha (Aquarius)","Meena (Pisces)"]

PLANETS = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"]

MAHADASHA_YEARS = {
    "Sun":7,"Moon":10,"Mars":7,"Rahu":18,"Jupiter":16,
    "Saturn":19,"Mercury":17,"Ketu":7,"Venus":20
}

SECTOR_PLANET = {
    "Sun":    ["Power","Govt Stocks","Healthcare","Gold"],
    "Moon":   ["FMCG","Dairy","Retail","Consumer Goods"],
    "Mars":   ["Real Estate","Defence","Metals","Engineering"],
    "Mercury":["IT","Telecom","Media","Logistics"],
    "Jupiter":["Banking","Finance","Education","Insurance"],
    "Venus":  ["Luxury","Auto","Entertainment","FMCG"],
    "Saturn": ["Oil & Gas","Mining","Infrastructure","Chemicals"],
    "Rahu":   ["Tech Startups","Aviation","Pharma","Crypto"],
    "Ketu":   ["Spirituality","Chemicals","Research","Ayurveda"],
}

TITHI_NAMES = [
    "Pratipada","Dwitiya","Tritiya","Chaturthi","Panchami",
    "Shashthi","Saptami","Ashtami","Navami","Dashami",
    "Ekadashi","Dwadashi","Trayodashi","Chaturdashi","Purnima/Amavasya"
]

# ─────────────────────────────────────────────
#  CALCULATION HELPERS
# ─────────────────────────────────────────────

def get_choghadiya(date: datetime.date, sunrise_hour=6.25, sunset_hour=18.25):
    """Return list of (name, start_time_str, end_time_str, quality_tuple)"""
    wd = date.strftime("%A")
    day_dur   = sunset_hour - sunrise_hour
    night_dur = 24 - day_dur
    slot_day  = day_dur / 8
    slot_night= night_dur / 8

    def hm(fh):
        h = int(fh) % 24
        m = int((fh - int(fh)) * 60)
        return f"{h:02d}:{m:02d}"

    periods = []
    day_chog = CHOG_DAY_ORDER.get(wd, CHOG_DAY_ORDER["Monday"])
    for i, name in enumerate(day_chog):
        s = sunrise_hour + i * slot_day
        e = s + slot_day
        periods.append((name, hm(s), hm(e), "day"))

    night_chog = CHOG_NIGHT_ORDER.get(wd, CHOG_NIGHT_ORDER["Monday"])
    for i, name in enumerate(night_chog):
        s = sunset_hour + i * slot_night
        e = s + slot_night
        if s >= 24: s -= 24
        if e >= 24: e -= 24
        periods.append((name, hm(s), hm(e), "night"))

    return periods

def get_rahu_kalam(date: datetime.date, sunrise_hour=6.25):
    wd = date.strftime("%A")
    slot = (18.25 - sunrise_hour) / 8
    offsets = {
        "Monday":7,"Tuesday":2,"Wednesday":5,
        "Thursday":6,"Friday":4,"Saturday":3,"Sunday":8
    }
    n = offsets.get(wd, 1)
    start = sunrise_hour + (n-1)*slot
    end   = start + slot
    def hm(fh):
        h = int(fh)%24; m=int((fh-int(fh))*60)
        return f"{h:02d}:{m:02d}"
    return hm(start), hm(end)

def get_abhijit(date: datetime.date, sunrise_hour=6.25, sunset_hour=18.25):
    mid = (sunrise_hour + sunset_hour) / 2
    start = mid - 0.4
    end   = mid + 0.4
    def hm(fh):
        h=int(fh)%24; m=int((fh-int(fh))*60)
        return f"{h:02d}:{m:02d}"
    return hm(start), hm(end)

def get_tithi(date: datetime.date):
    # Simplified tithi approximation
    ref = datetime.date(2000,1,6)  # known new moon
    days = (date - ref).days
    tithi_num = int((days % 29.53) / 29.53 * 30) % 30
    if tithi_num == 0: tithi_num = 30
    idx = min(tithi_num - 1, 14)
    paksha = "Shukla" if tithi_num <= 15 else "Krishna"
    return TITHI_NAMES[idx], paksha, tithi_num

def get_nakshatra(date: datetime.date):
    ref = datetime.date(2000,1,1)
    days = (date - ref).days
    idx = int((days * 13.176) % 27)
    return NAKSHATRAS[idx]

def get_vara(date: datetime.date):
    vara_names = {
        0:"Soma Vara (Monday)","1":"Mangala Vara (Tuesday)",
        "2":"Budha Vara (Wednesday)","3":"Guru Vara (Thursday)",
        "4":"Shukra Vara (Friday)","5":"Shani Vara (Saturday)",
        "6":"Ravi Vara (Sunday)"
    }
    wd = date.weekday()  # 0=Mon
    names_list = [
        "Soma Vara (Monday)","Mangala Vara (Tuesday)","Budha Vara (Wednesday)",
        "Guru Vara (Thursday)","Shukra Vara (Friday)","Shani Vara (Saturday)",
        "Ravi Vara (Sunday)"
    ]
    rulers = ["Moon","Mars","Mercury","Jupiter","Venus","Saturn","Sun"]
    return names_list[wd], rulers[wd]

def mahadasha_from_birth(dob: datetime.date, birth_nakshatra: str):
    # Simplified dasha sequence starting from birth nakshatra lord
    nak_idx = NAKSHATRAS.index(birth_nakshatra) if birth_nakshatra in NAKSHATRAS else 0
    lords_cycle = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]
    start_lord_idx = nak_idx % 9
    sequence = lords_cycle[start_lord_idx:] + lords_cycle[:start_lord_idx]
    today = datetime.date.today()
    age_years = (today - dob).days / 365.25
    cum = 0
    for lord in sequence:
        yrs = MAHADASHA_YEARS[lord]
        if cum + yrs > age_years:
            elapsed = age_years - cum
            remaining = yrs - elapsed
            return lord, round(elapsed,1), round(remaining,1), yrs
        cum += yrs
    return sequence[0], 0, MAHADASHA_YEARS[sequence[0]], MAHADASHA_YEARS[sequence[0]]

def get_antardasha(mahadasha_lord: str, elapsed_in_dasha: float):
    lords_cycle = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]
    total = MAHADASHA_YEARS[mahadasha_lord]
    idx = lords_cycle.index(mahadasha_lord)
    sequence = lords_cycle[idx:] + lords_cycle[:idx]
    cum = 0
    for lord in sequence:
        portion = (MAHADASHA_YEARS[lord] / 120) * total
        if cum + portion > elapsed_in_dasha:
            return lord
        cum += portion
    return sequence[0]

def rasi_from_dob(dob: datetime.date):
    # Rough moon sign from DOB (simplified)
    days = (dob - datetime.date(2000,1,1)).days
    idx = int((days / 27.32) % 12)
    return RASI[idx]

def lucky_sectors(mahadasha_lord, antardasha_lord):
    s1 = SECTOR_PLANET.get(mahadasha_lord, [])
    s2 = SECTOR_PLANET.get(antardasha_lord, [])
    combined = list(dict.fromkeys(s1 + s2))
    fallback = ["Banking","IT","FMCG","Metals","Auto","Energy"]
    for f in fallback:
        if f not in combined:
            combined.append(f)
        if len(combined) >= 6:
            break
    return combined[:6]

def wealth_score(dob: datetime.date, birth_nak: str):
    """Simplified wealth potential score 0-100"""
    nak_idx = NAKSHATRAS.index(birth_nak) if birth_nak in NAKSHATRAS else 0
    base = (nak_idx * 37 + dob.day * 13 + dob.month * 7) % 101
    return max(30, min(95, base))

def trading_strength_this_month(dob: datetime.date, birth_nak: str):
    today = datetime.date.today()
    score = (dob.day + today.month * 3 + today.day) % 10
    labels = ["Very Weak","Weak","Below Avg","Average","Average",
              "Above Avg","Good","Strong","Very Strong","Excellent"]
    return labels[score], score * 10

# ─────────────────────────────────────────────
#  CHARTS
# ─────────────────────────────────────────────

def choghadiya_chart(periods_day):
    """Gantt-style Choghadiya timeline for market hours"""
    color_map = {
        "Amrit":"#27AE60","Shubh":"#82E048","Labh":"#3498DB",
        "Char":"#F1C40F","Kaal":"#C0392B","Udveg":"#E67E22","Rog":"#8E44AD"
    }
    fig = go.Figure()
    market_periods = [p for p in periods_day if p[3]=="day"][:8]
    for i, (name, st, et, _) in enumerate(market_periods):
        color = color_map.get(name,"#888")
        fig.add_trace(go.Bar(
            x=[1], y=[name+" "+st],
            orientation='h',
            marker_color=color,
            name=name,
            showlegend=False,
            text=f"{name} ({st}–{et})",
            textposition="inside",
            insidetextanchor="middle",
            hoverinfo="text"
        ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E8E0D0",
        margin=dict(l=10,r=10,t=10,b=10),
        height=280,
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(tickfont=dict(family="Cinzel",size=10,color="#C9A84C")),
        barmode='stack',
    )
    return fig

def dasha_donut(elapsed, remaining, total, lord):
    color_map = {
        "Sun":"#FF6B35","Moon":"#C0C0FF","Mars":"#FF4444",
        "Mercury":"#44FF44","Jupiter":"#FFD700","Venus":"#FF88CC",
        "Saturn":"#8888AA","Rahu":"#8B5CF6","Ketu":"#8B6914"
    }
    c = color_map.get(lord,"#C9A84C")
    fig = go.Figure(go.Pie(
        values=[elapsed, remaining],
        labels=["Elapsed","Remaining"],
        hole=0.65,
        marker_colors=[c,"#1A1A35"],
        textinfo="none",
        hoverinfo="label+value"
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E8E0D0",
        showlegend=False,
        margin=dict(l=10,r=10,t=10,b=10),
        height=200,
        annotations=[dict(
            text=f"<b>{lord}</b><br>{round(remaining,1)}y left",
            font=dict(family="Cinzel",size=12,color="#C9A84C"),
            showarrow=False
        )]
    )
    return fig

def wealth_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        gauge=dict(
            axis=dict(range=[0,100], tickcolor="#C9A84C",
                      tickfont=dict(color="#C9A84C",family="Cinzel")),
            bar=dict(color="#C9A84C"),
            bgcolor="#13132A",
            bordercolor="#8B6914",
            steps=[
                dict(range=[0,40],color="#2A0F0F"),
                dict(range=[40,70],color="#1A1A0A"),
                dict(range=[70,100],color="#0F2A1A"),
            ],
            threshold=dict(line=dict(color="#E8C97A",width=3),
                          thickness=0.75,value=score)
        ),
        number=dict(font=dict(family="Cinzel",color="#C9A84C",size=28)),
        title=dict(text="Wealth Potential",
                   font=dict(family="Cinzel",color="#8A8090",size=12))
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#E8E0D0",
        height=220,
        margin=dict(l=20,r=20,t=30,b=10)
    )
    return fig

def hex_to_rgba(hex_color, alpha=0.2):
    """Convert hex color to rgba string for Plotly"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

def sector_radar(sectors, lord):
    color_map = {
        "Sun":"#FF6B35","Moon":"#C0C0FF","Mars":"#FF4444",
        "Mercury":"#44CC44","Jupiter":"#FFD700","Venus":"#FF88CC",
        "Saturn":"#8888AA","Rahu":"#8B5CF6","Ketu":"#8B6914"
    }
    c = color_map.get(lord,"#C9A84C")
    # Ensure we have enough sectors
    if not sectors:
        sectors = ["Banking","IT","Metals","FMCG","Energy","Auto"]
    vals = [85,70,60,75,55,80][:len(sectors)]
    while len(vals)<len(sectors): vals.append(50)
    # Close the polygon
    theta = sectors + [sectors[0]]
    r_vals = vals + [vals[0]]
    fig = go.Figure(go.Scatterpolar(
        r=r_vals,
        theta=theta,
        fill='toself',
        fillcolor=hex_to_rgba(c, 0.2),
        line=dict(color=c, width=2),
        marker=dict(color=c, size=6)
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True,range=[0,100],
                           tickfont=dict(color="#8A8090",size=8),
                           gridcolor="#2A2A4A"),
            angularaxis=dict(tickfont=dict(family="Cinzel",color="#C9A84C",size=9),
                            gridcolor="#2A2A4A"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#E8E0D0",
        showlegend=False,
        height=280,
        margin=dict(l=40,r=40,t=20,b=20)
    )
    return fig

def monthly_trading_calendar(dob, birth_nak):
    today = datetime.date.today()
    start = today.replace(day=1)
    import calendar
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    scores = []
    day_labels = []
    for d in range(1, days_in_month+1):
        dt = today.replace(day=d)
        s = (dob.day + dt.day * 3 + dt.month + NAKSHATRAS.index(birth_nak) if birth_nak in NAKSHATRAS else 0) % 10
        scores.append(s*10)
        day_labels.append(f"{d}")
    colors = ["#27AE60" if s>=70 else "#F1C40F" if s>=40 else "#C0392B" for s in scores]
    fig = go.Figure(go.Bar(
        x=day_labels, y=scores,
        marker_color=colors,
        text=[f"{s}%" for s in scores],
        textposition="outside",
        textfont=dict(size=7,color="#8A8090")
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E8E0D0",
        xaxis=dict(tickfont=dict(family="Cinzel",size=8,color="#C9A84C"),
                   gridcolor="#1A1A35"),
        yaxis=dict(range=[0,120],tickfont=dict(size=8,color="#8A8090"),
                   gridcolor="#1A1A35"),
        height=220,
        margin=dict(l=10,r=10,t=10,b=10),
        title=dict(text=f"Trading Score — {today.strftime('%B %Y')}",
                   font=dict(family="Cinzel",color="#C9A84C",size=12))
    )
    return fig

# ─────────────────────────────────────────────
#  PDF GENERATION
# ─────────────────────────────────────────────

def generate_pdf(user_data: dict, analysis_data: dict, ai_text: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── Color palette for WHITE background ──
    # All text must be dark and readable on white paper
    GOLD_DARK   = (139, 105, 20)   # dark gold — headings only
    BLACK       = (20, 20, 20)     # near-black — body text
    DARK_GREY   = (60, 60, 60)     # labels
    MID_GREY    = (100, 100, 100)  # secondary text
    RED_DARK    = (160, 30, 30)    # Rahu Kalam warning
    GREEN_DARK  = (30, 120, 60)    # Abhijit Muhurta
    GOLD_LINE   = (180, 140, 40)   # divider lines
    BG_HEADER   = (25, 25, 45)     # dark header banner
    BG_SECTION  = (248, 245, 238)  # very light cream section bg

    def section_heading(text):
        """Dark gold bold heading with cream background strip"""
        pdf.set_fill_color(*BG_SECTION)
        pdf.set_text_color(*GOLD_DARK)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 9, "  " + text, ln=True, fill=True)
        pdf.set_draw_color(*GOLD_LINE)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(3)

    def body_row(label, value, label_w=65):
        """Label in dark grey, value in near-black"""
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(label_w, 6, label + ":", ln=False)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*BLACK)
        pdf.cell(0, 6, str(value), ln=True)

    # ── Page border ──
    pdf.set_draw_color(*GOLD_LINE)
    pdf.rect(8, 8, 194, 281)

    # ── Header banner (dark, like app) — taller to fit logo ──
    pdf.set_fill_color(*BG_HEADER)
    pdf.rect(8, 8, 194, 38, 'F')

    # Logo on the RIGHT side of header — from embedded base64
    try:
        import tempfile
        _logo_bytes = base64.b64decode(LOGO_B64_PDF)
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as _tmp:
            _tmp.write(_logo_bytes)
            _tmp_path = _tmp.name
        pdf.image(_tmp_path, x=148, y=10, w=50, h=0)
        os.unlink(_tmp_path)
    except Exception:
        pass

    # Title text on LEFT
    pdf.set_xy(10, 12)
    pdf.set_text_color(201, 168, 76)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(130, 9, "  VedicTrade", ln=False, align="L")
    pdf.ln()

    pdf.set_xy(10, 22)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(200, 190, 170)
    pdf.cell(130, 5, "  Astro Finance Report", ln=False, align="L")
    pdf.ln()

    pdf.set_xy(10, 29)
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(160, 150, 130)
    pdf.cell(130, 5, f"  Powered by NyzTrade Financial Solutions", ln=False, align="L")
    pdf.ln()

    pdf.set_xy(10, 36)
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(140, 130, 110)
    pdf.cell(130, 4, f"  {datetime.date.today().strftime('%d %B %Y')}  |  Trader: {user_data.get('name','Trader')}  |  Spiritual guidance only", ln=True, align="L")

    pdf.ln(12)

    # ── SECTION 1: Birth Details ──
    section_heading("BIRTH DETAILS & PANCHANGA")

    details = [
        ("Date of Birth",       str(user_data.get('dob',''))),
        ("Birth Nakshatra",     user_data.get('nakshatra','')),
        ("Moon Sign (Rasi)",    analysis_data.get('rasi','')),
        ("Today's Nakshatra",   analysis_data.get('today_nak','')),
        ("Today's Tithi",       f"{analysis_data.get('tithi','')} ({analysis_data.get('paksha','')})"),
        ("Vara (Weekday)",      analysis_data.get('vara','')),
    ]
    for label, val in details:
        body_row(label, val)

    pdf.ln(4)

    # ── SECTION 2: Dasha Analysis ──
    section_heading("PLANETARY DASHA ANALYSIS")

    maha      = analysis_data.get('mahadasha','')
    antar     = analysis_data.get('antardasha','')
    remaining = analysis_data.get('maha_remaining', 0)

    dasha_items = [
        ("Mahadasha Lord",              maha),
        ("Antardasha Lord",             antar),
        ("Remaining in Mahadasha",      f"{remaining} years"),
        ("Wealth Potential Score",      f"{analysis_data.get('wealth_score',0)} / 100"),
        ("Trading Strength This Month", analysis_data.get('trade_strength','')),
    ]
    for label, val in dasha_items:
        body_row(label, val, label_w=75)

    pdf.ln(4)

    # ── SECTION 3: Favourable Sectors ──
    section_heading("FAVOURABLE SECTORS (Based on Planetary Lords)")

    sectors = analysis_data.get('sectors', [])
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*BLACK)
    # Two-column layout
    col_w = 85
    for i in range(0, len(sectors), 2):
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*GOLD_DARK)
        pdf.cell(8, 6, f"{i+1}.", ln=False)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*BLACK)
        pdf.cell(col_w - 8, 6, sectors[i], ln=False)
        if i+1 < len(sectors):
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(*GOLD_DARK)
            pdf.cell(8, 6, f"{i+2}.", ln=False)
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(*BLACK)
            pdf.cell(0, 6, sectors[i+1], ln=True)
        else:
            pdf.ln()

    pdf.ln(4)

    # ── SECTION 4: Choghadiya ──
    section_heading("TODAY'S CHOGHADIYA - MARKET HOURS")

    chog = analysis_data.get('choghadiya', [])
    day_chogs = [(n,s,e,p) for n,s,e,p in chog if p=="day"]

    # Table header
    pdf.set_fill_color(230, 222, 200)
    pdf.set_text_color(*DARK_GREY)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(40, 6, "Time Window", border=0, ln=False, fill=True)
    pdf.cell(30, 6, "Choghadiya", border=0, ln=False, fill=True)
    pdf.cell(30, 6, "Quality", border=0, ln=False, fill=True)
    pdf.cell(0,  6, "Advice", border=0, ln=True, fill=True)

    chog_colors = {
        "Amrit":  (20, 100, 50),
        "Shubh":  (40, 130, 40),
        "Labh":   (20, 80, 150),
        "Char":   (100, 80, 20),
        "Kaal":   (150, 30, 30),
        "Udveg":  (150, 80, 20),
        "Rog":    (100, 30, 100),
    }

    pdf.set_font("Helvetica", "", 8)
    for i, (name_c, st, et, _) in enumerate(day_chogs):
        q = CHOG_QUALITY.get(name_c, ("","","Neutral","#888",""))
        txt_color = chog_colors.get(name_c, BLACK)
        fill = (248, 248, 248) if i % 2 == 0 else (255, 255, 255)
        pdf.set_fill_color(*fill)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(40, 5, f"{st} - {et}", border=0, ln=False, fill=True)
        pdf.set_text_color(*txt_color)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(30, 5, name_c, border=0, ln=False, fill=True)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*DARK_GREY)
        pdf.cell(30, 5, q[1] if len(q)>1 else "", border=0, ln=False, fill=True)
        pdf.set_text_color(*BLACK)
        pdf.cell(0,  5, q[2] if len(q)>2 else "", border=0, ln=True, fill=True)

    pdf.ln(4)

    # ── SECTION 5: Muhurtas ──
    section_heading("RAHU KALAM & ABHIJIT MUHURTA")

    rk  = analysis_data.get('rahu_kalam', ('--','--'))
    abh = analysis_data.get('abhijit', ('--','--'))

    # Rahu Kalam box
    pdf.set_fill_color(255, 235, 235)
    pdf.set_text_color(*RED_DARK)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 7, f"  RAHU KALAM (AVOID NEW POSITIONS): {rk[0]} - {rk[1]}", ln=True, fill=True)
    pdf.ln(1)

    # Abhijit box
    pdf.set_fill_color(235, 255, 240)
    pdf.set_text_color(*GREEN_DARK)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 7, f"  ABHIJIT MUHURTA (MOST AUSPICIOUS): {abh[0]} - {abh[1]}", ln=True, fill=True)

    pdf.ln(5)

    # ── SECTION 6: AI Analysis ──
    section_heading("AI VEDIC ANALYSIS")

    clean_text = (ai_text
                  .replace("*", "")
                  .replace("#", "")
                  .replace("\u2013", "-")
                  .replace("\u2014", "-")
                  .replace("\u2018", "'")
                  .replace("\u2019", "'")
                  .replace("\u201c", '"')
                  .replace("\u201d", '"'))

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*BLACK)
    # Split into paragraphs for better formatting
    paragraphs = [p.strip() for p in clean_text.split('\n') if p.strip()]
    for para in paragraphs:
        try:
            pdf.multi_cell(0, 5, para)
            pdf.ln(2)
        except Exception:
            pass

    pdf.ln(4)

    # ── Footer disclaimer ──
    pdf.set_draw_color(*GOLD_LINE)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(3)
    pdf.set_fill_color(255, 248, 230)
    pdf.set_text_color(120, 60, 20)
    pdf.set_font("Helvetica", "I", 7.5)
    pdf.multi_cell(0, 4,
        "DISCLAIMER: This report is for spiritual and cultural guidance only, based on Vedic astrology traditions. "
        "It is NOT SEBI-registered investment advice. The creators of VedicTrade are not responsible for any financial "
        "decisions made based on this report. Always consult a SEBI-registered financial advisor before investing. "
        "Past astrological alignments do not guarantee future market performance.",
        fill=True
    )

    pdf.ln(5)

    # ── PDF Footer — Powered by NyzTrade ──
    pdf.set_draw_color(*GOLD_LINE)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(3)

    # Footer: logo left + text right
    try:
        import tempfile
        _logo_bytes2 = base64.b64decode(LOGO_B64_PDF)
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as _tmp2:
            _tmp2.write(_logo_bytes2)
            _tmp2_path = _tmp2.name
        footer_y = pdf.get_y()
        pdf.image(_tmp2_path, x=15, y=footer_y, w=35, h=0)
        os.unlink(_tmp2_path)
        pdf.set_xy(55, footer_y + 2)
    except Exception:
        pdf.set_xy(15, pdf.get_y())

    pdf.set_text_color(*GOLD_DARK)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(0, 4, "Powered by NyzTrade Financial Solutions", ln=True, align="L")

    pdf.set_xy(55, pdf.get_y())
    pdf.set_text_color(*MID_GREY)
    pdf.set_font("Helvetica", "", 7)
    pdf.cell(0, 4, "nyztrade.com  |  VedicTrade Astro Dashboard  |  " + datetime.date.today().strftime("%d %B %Y"), ln=True, align="L")

    return bytes(pdf.output())

def get_pdf_download_link(pdf_bytes, filename="VedicTrade_Report.pdf"):
    b64 = base64.b64encode(pdf_bytes).decode()
    return f'<a href="data:application/pdf;base64,{b64}" download="{filename}" style="text-decoration:none;"><button style="background:linear-gradient(135deg,#8B6914,#C9A84C);color:#0A0A0A;border:none;padding:0.6rem 1.5rem;border-radius:8px;font-family:Cinzel,serif;font-weight:700;cursor:pointer;letter-spacing:1px;font-size:0.9rem;">📥 Download PDF Report</button></a>'

# ─────────────────────────────────────────────
#  GROQ AI
# ─────────────────────────────────────────────

def get_groq_analysis(user_data: dict, analysis_data: dict, question: str = None) -> str:
    # Read from Streamlit secrets (secrets.toml) — never exposed to users
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        return "⚠️ GROQ_API_KEY not found in secrets.toml. Please add it to your Streamlit secrets."
    if not api_key:
        return "⚠️ GROQ_API_KEY is empty in secrets.toml."
    try:
        client = Groq(api_key=api_key)
        context = f"""
You are VedicAI, an expert in Vedic astrology applied to Indian stock markets.
Provide spiritual guidance on trading timing and wealth building.
Always remind users this is NOT financial advice.

User Profile:
- Name: {user_data.get('name','Trader')}
- DOB: {user_data.get('dob','')}
- Birth Nakshatra: {user_data.get('nakshatra','')}
- Moon Sign: {analysis_data.get('rasi','')}
- Mahadasha: {analysis_data.get('mahadasha','')} ({analysis_data.get('maha_remaining',0)} years remaining)
- Antardasha: {analysis_data.get('antardasha','')}
- Wealth Score: {analysis_data.get('wealth_score',0)}/100
- Trading Strength This Month: {analysis_data.get('trade_strength','')}
- Favourable Sectors: {', '.join(analysis_data.get('sectors',[]))}
- Today's Nakshatra: {analysis_data.get('today_nak','')}
- Today's Tithi: {analysis_data.get('tithi','')} {analysis_data.get('paksha','')}
- Rahu Kalam Today: {analysis_data.get('rahu_kalam',('',''))[0]} to {analysis_data.get('rahu_kalam',('',''))[1]}
- Abhijit Muhurta: {analysis_data.get('abhijit',('',''))[0]} to {analysis_data.get('abhijit',('',''))[1]}
"""
        if question:
            prompt = f"{context}\n\nUser Question: {question}\n\nProvide a thoughtful Vedic astrology based response about trading/investments. Keep it practical and under 250 words."
        else:
            prompt = f"{context}\n\nGenerate a comprehensive Vedic trading analysis for today. Include:\n1. Overall energy for trading today based on Panchanga\n2. Dasha analysis and what it means for wealth\n3. Best time windows for trading today\n4. Sectors to focus on\n5. One specific Vedic mantra or practice for financial prosperity\n\nKeep response under 350 words. Be insightful and practical."

        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"user","content":prompt}],
            max_tokens=500,
            temperature=0.7
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"

# ─────────────────────────────────────────────
#  LANDING PAGE
# ─────────────────────────────────────────────

def show_landing():
    st.markdown("""
<style>
.landing-hero {
  text-align: center;
  padding: 3rem 1rem 2rem;
  position: relative;
}
.om-symbol {
  font-size: 5rem;
  line-height: 1;
  background: linear-gradient(135deg, #8B6914, #C9A84C, #E8C97A, #C9A84C, #8B6914);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: block;
  margin-bottom: 1rem;
  animation: pulse 3s ease-in-out infinite;
  filter: drop-shadow(0 0 20px rgba(201,168,76,0.5));
}
@keyframes pulse {
  0%,100% { filter: drop-shadow(0 0 10px rgba(201,168,76,0.3)); }
  50%      { filter: drop-shadow(0 0 30px rgba(201,168,76,0.8)); }
}
.hero-title {
  font-family: 'Cinzel Decorative', serif;
  font-size: 2.8rem;
  font-weight: 900;
  background: linear-gradient(135deg, #8B6914, #C9A84C, #E8C97A);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.2;
  margin-bottom: 0.5rem;
}
.hero-sub {
  font-family: 'Cinzel', serif;
  font-size: 1rem;
  color: #8A8090;
  letter-spacing: 4px;
  text-transform: uppercase;
  margin-bottom: 1.5rem;
}
.hero-desc {
  font-family: 'Raleway', sans-serif;
  font-size: 1.05rem;
  color: #B8B0C0;
  max-width: 640px;
  margin: 0 auto 2rem;
  line-height: 1.7;
}
.mandala-ring {
  position: absolute;
  width: 300px; height: 300px;
  border-radius: 50%;
  border: 1px solid rgba(201,168,76,0.15);
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  animation: rotate 30s linear infinite;
  pointer-events: none;
}
.mandala-ring:nth-child(2) {
  width:400px; height:400px;
  border-color: rgba(201,168,76,0.08);
  animation-duration: 50s;
  animation-direction: reverse;
}
@keyframes rotate { to { transform: translate(-50%,-50%) rotate(360deg); } }

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.2rem;
  margin: 2rem 0;
}
.feature-card {
  background: linear-gradient(135deg, #13132A, #1A1A35);
  border: 1px solid #3A2A0A;
  border-top: 2px solid #C9A84C;
  border-radius: 12px;
  padding: 1.5rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(201,168,76,0.2);
}
.feature-icon { font-size: 2.2rem; margin-bottom: 0.8rem; }
.feature-title {
  font-family: 'Cinzel', serif;
  font-size: 0.95rem;
  color: #C9A84C;
  letter-spacing: 1px;
  margin-bottom: 0.5rem;
}
.feature-desc { font-size: 0.88rem; color: #8A8090; line-height: 1.6; }

.planet-strip {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  margin: 1.5rem 0;
}
.planet-badge {
  background: var(--panel);
  border: 1px solid #3A2A0A;
  border-radius: 20px;
  padding: 0.3rem 0.9rem;
  font-family: 'Cinzel', serif;
  font-size: 0.78rem;
  color: #C9A84C;
  letter-spacing: 1px;
}
.disclaimer-box {
  background: #130A0A;
  border: 1px solid #3A1A1A;
  border-left: 3px solid #C0392B;
  border-radius: 8px;
  padding: 1rem 1.2rem;
  font-size: 0.8rem;
  color: #8A8090;
  margin: 1.5rem 0;
}
.cta-strip {
  text-align: center;
  padding: 1.5rem;
  background: linear-gradient(135deg, #0D0D20, #160B2E);
  border: 1px solid #3A2A0A;
  border-radius: 12px;
  margin: 1.5rem 0;
}
.cta-text {
  font-family: 'Cinzel', serif;
  font-size: 1.1rem;
  color: #C9A84C;
  margin-bottom: 0.5rem;
}
</style>

<div class="landing-hero">
  <div class="mandala-ring"></div>
  <div class="mandala-ring"></div>
  <span class="om-symbol">ॐ</span>
  <div class="hero-title">VedicTrade</div>
  <div class="hero-sub">Astro · Finance · Dashboard</div>
  <div class="hero-desc">
    Ancient Vedic wisdom meets modern Indian markets. Discover your personal trading muhurta,
    planetary dasha analysis, and AI-powered astro insights — all in one sacred dashboard.
  </div>
</div>

<div class="planet-strip">
  <span class="planet-badge">☀️ Surya</span>
  <span class="planet-badge">🌙 Chandra</span>
  <span class="planet-badge">♂ Mangala</span>
  <span class="planet-badge">☿ Budha</span>
  <span class="planet-badge">♃ Guru</span>
  <span class="planet-badge">♀ Shukra</span>
  <span class="planet-badge">♄ Shani</span>
  <span class="planet-badge">☊ Rahu</span>
  <span class="planet-badge">☋ Ketu</span>
</div>

<div class="gold-divider"></div>

<div class="feature-grid">
  <div class="feature-card">
    <div class="feature-icon">🕐</div>
    <div class="feature-title">Muhurta Trading Timer</div>
    <div class="feature-desc">Real-time Choghadiya periods, Rahu Kalam alerts, and Abhijit Muhurta windows tailored for NSE/BSE market hours.</div>
  </div>
  <div class="feature-card">
    <div class="feature-icon">🪐</div>
    <div class="feature-title">Personal Dasha Analysis</div>
    <div class="feature-desc">Your Mahadasha & Antardasha decoded for wealth — know when planets favour financial growth in your birth chart.</div>
  </div>
  <div class="feature-card">
    <div class="feature-icon">📊</div>
    <div class="feature-title">Sector Astrology Map</div>
    <div class="feature-desc">Discover which Nifty sectors align with your planetary lords — from IT to Defence, Banking to Gold.</div>
  </div>
  <div class="feature-card">
    <div class="feature-icon">🤖</div>
    <div class="feature-title">VedicAI Analysis</div>
    <div class="feature-desc">Powered by Groq LLaMA — ask questions about your trading destiny, get personalised Vedic market insights instantly.</div>
  </div>
  <div class="feature-card">
    <div class="feature-icon">📅</div>
    <div class="feature-title">Monthly Trading Calendar</div>
    <div class="feature-desc">Your personalised auspicious and inauspicious trading days for the entire month — colour coded for clarity.</div>
  </div>
  <div class="feature-card">
    <div class="feature-icon">📥</div>
    <div class="feature-title">PDF Report Download</div>
    <div class="feature-desc">Download your complete Vedic trading report — Panchanga, Dasha, sector map, Choghadiya and AI analysis in one PDF.</div>
  </div>
</div>

<div class="disclaimer-box">
  ⚠️ <strong>Important Disclaimer:</strong> VedicTrade provides spiritual and cultural guidance based on Vedic astrology traditions. 
  This is NOT SEBI-registered investment advice. All trading decisions should be made independently with a certified financial advisor. 
  Past astrological alignments do not guarantee future market performance.
</div>

<div class="cta-strip">
  <div class="cta-text">🔱 Enter your birth details in the sidebar to begin your Vedic journey</div>
  <div style="color:#8A8090;font-size:0.85rem;font-family:Raleway,sans-serif;">
    Your data is never stored · Calculations happen locally · Free to use
  </div>
</div>
""", unsafe_allow_html=True)

    # Powered by logo at bottom of landing
    logo_b64 = get_logo_base64()
    if logo_b64:
        st.markdown(f"""
<div style="text-align:center;margin-top:1.5rem;padding:1rem;
            background:linear-gradient(135deg,#0D0D20,#110B2D);
            border:1px solid #2A1A0A;border-radius:12px;">
  <div style="font-size:0.65rem;color:#8A8090;letter-spacing:3px;
              font-family:'Cinzel',serif;margin-bottom:0.6rem;">
    POWERED BY
  </div>
  <img src="data:image/jpeg;base64,{logo_b64}" width="220"
       style="border-radius:10px;box-shadow:0 4px 20px rgba(201,168,76,0.25);"
       alt="NyzTrade Financial Solutions"/>
  <div style="font-size:0.72rem;color:#8A8090;font-family:'Cinzel',serif;
              margin-top:0.6rem;letter-spacing:1px;">
    nyztrade.com · Financial Solutions
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────

def sidebar():
    with st.sidebar:
        # Logo
        logo_b64 = get_logo_base64()
        if logo_b64:
            st.markdown(f"""
<div style="text-align:center;padding:1rem 0 0.3rem;">
  <div style="font-size:0.6rem;color:#8A8090;letter-spacing:3px;font-family:'Cinzel',serif;margin-bottom:0.4rem;">
    POWERED BY
  </div>
  <img src="data:image/jpeg;base64,{logo_b64}" width="180"
       style="border-radius:10px;box-shadow:0 4px 16px rgba(201,168,76,0.3);"
       alt="NyzTrade Logo"/>
  <div style="font-size:2rem;margin-top:0.6rem;background:linear-gradient(135deg,#8B6914,#C9A84C,#E8C97A);
              -webkit-background-clip:text;-webkit-text-fill-color:transparent;
              background-clip:text;font-family:'Cinzel Decorative',serif;font-weight:900;">
    🔱 VedicTrade
  </div>
  <div style="font-size:0.65rem;color:#8A8090;letter-spacing:3px;font-family:'Cinzel',serif;">
    ASTRO FINANCE DASHBOARD
  </div>
</div>
<div class="gold-divider"></div>
""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div style="text-align:center;padding:1rem 0 0.5rem;">
  <div style="font-size:2.5rem;background:linear-gradient(135deg,#8B6914,#C9A84C,#E8C97A);
              -webkit-background-clip:text;-webkit-text-fill-color:transparent;
              background-clip:text;font-family:'Cinzel Decorative',serif;font-weight:900;">
    🔱 VedicTrade
  </div>
  <div style="font-size:0.7rem;color:#8A8090;letter-spacing:3px;font-family:'Cinzel',serif;">
    ASTRO FINANCE DASHBOARD
  </div>
</div>
<div class="gold-divider"></div>
""", unsafe_allow_html=True)

        st.markdown('<div class="sec-head">📋 Your Profile</div>', unsafe_allow_html=True)
        name = st.text_input("Your Name", placeholder="e.g. Arjun Menon")
        dob  = st.date_input("Date of Birth",
                             value=datetime.date(1990,1,1),
                             min_value=datetime.date(1940,1,1),
                             max_value=datetime.date(2005,12,31))
        nakshatra = st.selectbox("Birth Nakshatra (Janam Nakshatra)", NAKSHATRAS)
        sunrise   = st.slider("Sunrise Time (Hour)", 5.5, 7.5, 6.25, 0.25,
                              help="Approximate sunrise for your city")
        sunset    = st.slider("Sunset Time (Hour)", 17.5, 19.5, 18.25, 0.25)

        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        # Check if Groq secret is configured — show status only, no input
        try:
            _key = st.secrets["GROQ_API_KEY"]
            _ai_status = '<span class="pill-good">🤖 VedicAI Ready</span>'
        except Exception:
            _ai_status = '<span class="pill-warn">⚠ VedicAI Offline — Add GROQ_API_KEY to secrets.toml</span>'
        st.markdown(_ai_status, unsafe_allow_html=True)

        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        generate = st.button("🔱 Generate My Dashboard", use_container_width=True)

        st.markdown("""
<div style="margin-top:2rem;padding:0.8rem;background:#0D0D20;border-radius:8px;
            border:1px solid #2A2A4A;text-align:center;">
  <div style="font-size:0.7rem;color:#8A8090;font-family:'Cinzel',serif;letter-spacing:2px;">
    नमस्ते · NAMASTE<br/>
    <span style="color:#C9A84C;">सर्वे भवन्तु सुखिनः</span><br/>
    <span style="font-size:0.65rem;">May all beings be prosperous</span>
  </div>
</div>
""", unsafe_allow_html=True)

        return name, dob, nakshatra, sunrise, sunset, generate
# ─────────────────────────────────────────────
#  MAIN DASHBOARD
# ─────────────────────────────────────────────

def show_dashboard(name, dob, nakshatra, sunrise, sunset):
    today = datetime.date.today()

    # ── Compute everything ──
    tithi, paksha, tithi_num = get_tithi(today)
    today_nak   = get_nakshatra(today)
    vara, vara_ruler = get_vara(today)
    rk          = get_rahu_kalam(today, sunrise)
    abh         = get_abhijit(today, sunrise, sunset)
    chog        = get_choghadiya(today, sunrise, sunset)
    maha_lord, maha_elapsed, maha_remain, maha_total = mahadasha_from_birth(dob, nakshatra)
    antar_lord  = get_antardasha(maha_lord, maha_elapsed)
    rasi        = rasi_from_dob(dob)
    sectors     = lucky_sectors(maha_lord, antar_lord)
    w_score     = wealth_score(dob, nakshatra)
    trade_str, trade_score = trading_strength_this_month(dob, nakshatra)

    analysis_data = {
        "tithi": tithi, "paksha": paksha, "today_nak": today_nak,
        "vara": vara, "vara_ruler": vara_ruler,
        "rahu_kalam": rk, "abhijit": abh, "choghadiya": chog,
        "mahadasha": maha_lord, "antardasha": antar_lord,
        "maha_elapsed": maha_elapsed, "maha_remaining": maha_remain,
        "rasi": rasi, "sectors": sectors,
        "wealth_score": w_score, "trade_strength": trade_str,
    }
    user_data = {"name": name, "dob": str(dob), "nakshatra": nakshatra}

    # ── Hero strip ──
    _logo_b64 = get_logo_base64()
    _logo_tag  = f'<img src="data:image/jpeg;base64,{_logo_b64}" height="38" style="border-radius:6px;vertical-align:middle;" alt="NyzTrade"/>' if _logo_b64 else ""
    _powered   = f'<span style="font-size:0.6rem;color:#8A8090;font-family:Cinzel,serif;letter-spacing:2px;vertical-align:middle;margin-right:0.4rem;">POWERED BY</span>{_logo_tag}' if _logo_tag else ""
    st.markdown(f"""
<div style="background:linear-gradient(135deg,#0D0D20,#160B2E);
            border:1px solid #3A2A0A;border-radius:12px;
            padding:1.2rem 1.5rem;margin-bottom:1rem;
            display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
  <div>
    <div style="font-family:'Cinzel Decorative',serif;font-size:1.5rem;
                background:linear-gradient(135deg,#8B6914,#C9A84C,#E8C97A);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
      🔱 VedicTrade Dashboard
    </div>
    <div style="font-family:'Cinzel',serif;font-size:0.8rem;color:#8A8090;letter-spacing:2px;">
      {name.upper() if name else 'TRADER'} · {today.strftime('%d %B %Y')}
    </div>
  </div>
  <div style="display:flex;flex-direction:column;align-items:flex-end;gap:0.5rem;">
    <div style="display:flex;gap:0.8rem;flex-wrap:wrap;">
      <span class="pill-neut">🌙 {today_nak}</span>
      <span class="pill-neut">📅 {tithi} {paksha}</span>
      <span class="pill-neut">⭐ {vara.split("(")[0].strip()}</span>
    </div>
    <div style="display:flex;align-items:center;">{_powered}</div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── TABS ──
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🕐 Muhurta Timer",
        "🪐 Dasha Profile",
        "📊 Sector Map",
        "🤖 VedicAI Chat",
        "📥 PDF Report",
        "🥇 Metals & Buying"
    ])

    # ─── TAB 1: MUHURTA ───
    with tab1:
        col1, col2 = st.columns([1.4, 1])

        with col1:
            st.markdown('<div class="sec-head">📿 Today\'s Choghadiya</div>', unsafe_allow_html=True)
            st.markdown('<div class="astro-card">', unsafe_allow_html=True)

            now = datetime.datetime.now()
            current_time_str = now.strftime("%H:%M")

            for name_c, st_t, et_t, period in chog:
                if period == "day":
                    q = CHOG_QUALITY.get(name_c, ("","","","#888","chog-char"))
                    emoji, quality, advice, color, css = q
                    # Check if current
                    is_current = st_t <= current_time_str <= et_t
                    border = f"border:2px solid {color};" if is_current else ""
                    st.markdown(f"""
<div class="chog-block {css}" style="{border}">
  <span style="font-family:'Cinzel',serif;color:{color};">{emoji} {name_c}</span>
  <span style="color:#8A8090;font-size:0.78rem;">{st_t} – {et_t}</span>
  <span style="color:{color};font-size:0.75rem;">{advice}</span>
  {"<span style='background:#C9A84C;color:#0A0A0A;border-radius:4px;padding:0.1rem 0.4rem;font-size:0.7rem;font-family:Cinzel,serif;'>NOW</span>" if is_current else ""}
</div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="sec-head">⚡ Key Muhurtas</div>', unsafe_allow_html=True)
            st.markdown(f"""
<div class="astro-card">
  <div style="margin-bottom:1rem;">
    <div style="font-family:'Cinzel',serif;font-size:0.75rem;color:#8A8090;letter-spacing:1px;margin-bottom:0.3rem;">RAHU KALAM — AVOID</div>
    <div style="background:#2A0F0F;border:1px solid #C0392B;border-radius:8px;padding:0.7rem 1rem;">
      <span style="font-size:1.2rem;color:#E74C3C;font-family:'Cinzel',serif;">🔴 {rk[0]} – {rk[1]}</span>
      <div style="font-size:0.75rem;color:#8A8090;margin-top:0.2rem;">Avoid new entries/exits</div>
    </div>
  </div>
  <div style="margin-bottom:1rem;">
    <div style="font-family:'Cinzel',serif;font-size:0.75rem;color:#8A8090;letter-spacing:1px;margin-bottom:0.3rem;">ABHIJIT MUHURTA — BEST</div>
    <div style="background:#0F2A1A;border:1px solid #27AE60;border-radius:8px;padding:0.7rem 1rem;">
      <span style="font-size:1.2rem;color:#2ECC71;font-family:'Cinzel',serif;">🟢 {abh[0]} – {abh[1]}</span>
      <div style="font-size:0.75rem;color:#8A8090;margin-top:0.2rem;">Most auspicious window</div>
    </div>
  </div>
  <div>
    <div style="font-family:'Cinzel',serif;font-size:0.75rem;color:#8A8090;letter-spacing:1px;margin-bottom:0.3rem;">TODAY'S PANCHANGA</div>
    <div style="font-size:0.82rem;line-height:2;color:#E8E0D0;">
      <span style="color:#8A8090;">Vara:</span> {vara_ruler}<br/>
      <span style="color:#8A8090;">Tithi:</span> {tithi} ({paksha})<br/>
      <span style="color:#8A8090;">Nakshatra:</span> {today_nak}<br/>
      <span style="color:#8A8090;">Tithi No:</span> {tithi_num}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

            st.markdown('<div class="sec-head" style="margin-top:1rem;">📖 Choghadiya Guide</div>', unsafe_allow_html=True)
            st.markdown('<div class="astro-card">', unsafe_allow_html=True)
            for n, (emoji, quality, advice, color, _) in CHOG_QUALITY.items():
                st.markdown(f'<div style="font-size:0.8rem;margin:0.3rem 0;"><span style="color:{color};">{emoji} <b>{n}</b></span> <span style="color:#8A8090;">— {advice}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ─── TAB 2: DASHA ───
    with tab2:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
<div class="astro-card" style="text-align:center;">
  <div style="font-family:'Cinzel',serif;font-size:0.75rem;color:#8A8090;letter-spacing:2px;margin-bottom:0.5rem;">MOON SIGN (RASI)</div>
  <div style="font-size:1.4rem;color:#C9A84C;font-family:'Cinzel',serif;">{rasi}</div>
</div>""", unsafe_allow_html=True)
            st.markdown(f"""
<div class="astro-card" style="text-align:center;">
  <div style="font-family:'Cinzel',serif;font-size:0.75rem;color:#8A8090;letter-spacing:2px;margin-bottom:0.5rem;">BIRTH NAKSHATRA</div>
  <div style="font-size:1.3rem;color:#C9A84C;font-family:'Cinzel',serif;">{nakshatra}</div>
</div>""", unsafe_allow_html=True)
            st.plotly_chart(dasha_donut(maha_elapsed, maha_remain, maha_total, maha_lord),
                           use_container_width=True)

        with col2:
            st.markdown(f"""
<div class="astro-card">
  <div class="sec-head">🪐 Mahadasha</div>
  <div style="font-size:2rem;color:#C9A84C;font-family:'Cinzel Decorative',serif;margin-bottom:0.5rem;">{maha_lord}</div>
  <div style="font-size:0.85rem;color:#8A8090;margin-bottom:1rem;">
    {round(maha_elapsed,1)} years elapsed · {round(maha_remain,1)} years remaining
  </div>
  <div style="font-size:0.82rem;line-height:1.8;color:#E8E0D0;">
    <span style="color:#8A8090;">Antardasha:</span> {antar_lord}<br/>
    <span style="color:#8A8090;">Sectors:</span> {', '.join(SECTOR_PLANET.get(maha_lord,[])[:2])}<br/>
    <span style="color:#8A8090;">Nature:</span> {"Benefic 🟢" if maha_lord in ["Jupiter","Venus","Moon","Mercury"] else "Malefic 🔴" if maha_lord in ["Saturn","Mars","Rahu","Ketu"] else "Mixed 🟡"}
  </div>
</div>
<div class="astro-card">
  <div class="sec-head">📅 Trading Strength</div>
  <div style="font-size:1.5rem;color:{'#27AE60' if trade_score>=70 else '#F1C40F' if trade_score>=40 else '#C0392B'};font-family:'Cinzel',serif;">{trade_str}</div>
  <div style="margin-top:0.5rem;">
""", unsafe_allow_html=True)
            st.progress(trade_score / 100)
            st.markdown('</div></div>', unsafe_allow_html=True)

        with col3:
            st.plotly_chart(wealth_gauge(w_score), use_container_width=True)
            st.markdown(f"""
<div class="astro-card">
  <div class="sec-head">💰 Wealth Indicators</div>
  <div style="font-size:0.82rem;line-height:2;color:#E8E0D0;">
    <span style="color:#8A8090;">Dhan Bhava Lord:</span> {maha_lord}<br/>
    <span style="color:#8A8090;">Labha Bhava:</span> {antar_lord}<br/>
    <span style="color:#8A8090;">Wealth Score:</span> <span style="color:#C9A84C;font-size:1.1rem;">{w_score}/100</span><br/>
    <span style="color:#8A8090;">Best Period:</span> {"Now 🟢" if w_score > 70 else "Building 🟡" if w_score > 50 else "Caution 🔴"}
  </div>
</div>""", unsafe_allow_html=True)

        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-head">📅 Monthly Trading Auspiciousness</div>', unsafe_allow_html=True)
        st.plotly_chart(monthly_trading_calendar(dob, nakshatra), use_container_width=True)

    # ─── TAB 3: SECTORS ───
    with tab3:
        col1, col2 = st.columns([1, 1.2])
        with col1:
            st.markdown('<div class="sec-head">🎯 Your Lucky Sectors</div>', unsafe_allow_html=True)
            st.markdown('<div class="astro-card">', unsafe_allow_html=True)
            for i, s in enumerate(sectors):
                bar = "█" * int((7-i)*2) + "░" * (i*2)
                pct = int(90 - i*8)
                color = "#27AE60" if i<2 else "#F1C40F" if i<4 else "#E67E22"
                st.markdown(f"""
<div style="margin-bottom:0.8rem;">
  <div style="display:flex;justify-content:space-between;margin-bottom:0.2rem;">
    <span style="font-family:'Cinzel',serif;font-size:0.85rem;color:#E8E0D0;">{'⭐ ' if i<2 else ''}{s}</span>
    <span style="color:{color};font-size:0.8rem;">{pct}%</span>
  </div>
  <div style="background:#1A1A35;border-radius:4px;height:6px;overflow:hidden;">
    <div style="width:{pct}%;height:100%;background:linear-gradient(90deg,{color}88,{color});border-radius:4px;"></div>
  </div>
</div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="sec-head">🪐 Planet → Sector Map</div>', unsafe_allow_html=True)
            st.markdown('<div class="astro-card">', unsafe_allow_html=True)
            highlight = [maha_lord, antar_lord]
            for planet, sects in SECTOR_PLANET.items():
                is_hl = planet in highlight
                color = "#C9A84C" if is_hl else "#8A8090"
                bg = "background:#1A1A2A;" if is_hl else ""
                st.markdown(f"""
<div style="padding:0.3rem 0.5rem;margin:0.2rem 0;border-radius:6px;{bg}">
  <span style="color:{color};font-family:'Cinzel',serif;font-size:0.78rem;">{'★ ' if is_hl else ''}{planet}:</span>
  <span style="color:#8A8090;font-size:0.75rem;"> {', '.join(sects)}</span>
</div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="sec-head">🕸️ Sector Strength Radar</div>', unsafe_allow_html=True)
            st.plotly_chart(sector_radar(sectors[:6], maha_lord), use_container_width=True)

            st.markdown(f"""
<div class="astro-card">
  <div class="sec-head">💡 Trading Guidance</div>
  <div style="font-size:0.85rem;line-height:1.8;color:#E8E0D0;">
    Your <span style="color:#C9A84C;">{maha_lord} Mahadasha</span> with 
    <span style="color:#C9A84C;">{antar_lord} Antardasha</span> creates 
    {'a powerful wealth combination. Focus on long-term positions in your favoured sectors.' if maha_lord in ['Jupiter','Venus'] else 
     'a volatile but opportunity-rich period. Use strict stop-losses and shorter timeframes.' if maha_lord in ['Mars','Rahu'] else
     'a structured, disciplined approach. Systematic investment works best now.' if maha_lord == 'Saturn' else
     'an information-driven edge. Research-heavy positions in your favoured sectors.' if maha_lord == 'Mercury' else
     'an intuitive trading period. Trust your gut on market timing.'}
    <br/><br/>
    <span style="color:#8A8090;font-size:0.8rem;">
    ⚠️ This is Vedic guidance, not financial advice. Always use proper risk management.
    </span>
  </div>
</div>""", unsafe_allow_html=True)

    # ─── TAB 4: AI CHAT ───
    with tab4:
        st.markdown('<div class="sec-head">🤖 VedicAI — Ask Your Trading Questions</div>', unsafe_allow_html=True)

        if "ai_daily" not in st.session_state:
            st.session_state.ai_daily = ""
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("🔮 Generate Today's Full Analysis", use_container_width=True):
                with st.spinner("Consulting the stars..."):
                    st.session_state.ai_daily = get_groq_analysis(user_data, analysis_data)

        with col2:
            if st.button("🔄 Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.ai_daily = ""

        if st.session_state.ai_daily:
            st.markdown(f'<div class="ai-box">✨ <b style="color:#C9A84C;font-family:Cinzel,serif;">VedicAI Daily Analysis</b><br/><br/>{st.session_state.ai_daily}</div>', unsafe_allow_html=True)

        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-head">💬 Ask VedicAI</div>', unsafe_allow_html=True)

        # Chat history
        for msg in st.session_state.chat_history:
            role_color = "#C9A84C" if msg["role"]=="assistant" else "#8B5CF6"
            role_label = "🔱 VedicAI" if msg["role"]=="assistant" else "👤 You"
            st.markdown(f'<div class="ai-box" style="margin-bottom:0.8rem;border-left-color:{role_color};"><b style="color:{role_color};font-family:Cinzel,serif;">{role_label}</b><br/>{msg["content"]}</div>', unsafe_allow_html=True)

        q_col, btn_col = st.columns([4,1])
        with q_col:
            user_q = st.text_input("", placeholder="e.g. Is this week good for buying IT stocks? Which sectors should I avoid?", label_visibility="collapsed")
        with btn_col:
            ask_btn = st.button("Ask 🔮", use_container_width=True)

        if ask_btn and user_q:
            st.session_state.chat_history.append({"role":"user","content":user_q})
            with st.spinner("VedicAI is consulting planetary positions..."):
                answer = get_groq_analysis(user_data, analysis_data, user_q)
            st.session_state.chat_history.append({"role":"assistant","content":answer})
            st.rerun()

        st.markdown("""
<div style="margin-top:1rem;">
  <div style="font-family:'Cinzel',serif;font-size:0.75rem;color:#8A8090;margin-bottom:0.5rem;letter-spacing:1px;">SUGGESTED QUESTIONS</div>
  <div style="display:flex;gap:0.5rem;flex-wrap:wrap;">
""", unsafe_allow_html=True)
        suggestions = [
            "Is today good for F&O trading?",
            "What sectors should I focus on this month?",
            "How is my Dasha affecting my wealth?",
            "When is the next auspicious period for big investments?",
        ]
        for s in suggestions:
            st.markdown(f'<span style="background:#1A1A35;border:1px solid #3A2A5A;border-radius:20px;padding:0.3rem 0.8rem;font-size:0.78rem;color:#8A8090;cursor:pointer;">{s}</span>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # ─── TAB 5: PDF ───
    with tab5:
        st.markdown('<div class="sec-head">📥 Download Your Vedic Trading Report</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="astro-card">
  <div style="font-size:0.9rem;color:#E8E0D0;line-height:1.8;margin-bottom:1rem;">
    Your personalised PDF report includes:
    <ul style="color:#8A8090;margin-top:0.5rem;">
      <li>Complete Panchanga for today</li>
      <li>Your Mahadasha & Antardasha analysis</li>
      <li>Wealth potential score & indicators</li>
      <li>Favourable sectors based on planetary lords</li>
      <li>Today's Choghadiya with market timings</li>
      <li>Rahu Kalam & Abhijit Muhurta</li>
      <li>AI-generated Vedic trading insights</li>
    </ul>
  </div>
</div>""", unsafe_allow_html=True)

        ai_for_pdf = st.session_state.get("ai_daily","")

        col1, col2 = st.columns(2)
        with col1:
            if not ai_for_pdf:
                st.markdown('<span class="pill-warn">⚠ Generate AI analysis first for complete report</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="pill-good">✓ AI Analysis ready for PDF</span>', unsafe_allow_html=True)

        with col2:
            if st.button("📄 Generate PDF Now", use_container_width=True):
                with st.spinner("Preparing your sacred report..."):
                    if not ai_for_pdf:
                        ai_for_pdf = get_groq_analysis(user_data, analysis_data)
                        st.session_state.ai_daily = ai_for_pdf
                    pdf_bytes = generate_pdf(user_data, analysis_data, ai_for_pdf)
                    fname = f"VedicTrade_{name.replace(' ','_') if name else 'Report'}_{today.strftime('%Y%m%d')}.pdf"
                    st.markdown(get_pdf_download_link(pdf_bytes, fname), unsafe_allow_html=True)
                    st.success("✅ Your Vedic Trading Report is ready!")

        st.markdown("""
<div class="disclaimer-box" style="margin-top:1.5rem;">
  📜 <strong>Legal Disclaimer:</strong> This PDF report is generated for spiritual and cultural guidance purposes only, based on Vedic astrology traditions followed by the Hindu community. It is NOT registered financial or investment advice under SEBI regulations. The creators of VedicTrade are not responsible for any financial decisions made based on this report. Always consult a SEBI-registered financial advisor for investment decisions.
</div>""", unsafe_allow_html=True)

    # ─── TAB 6: METALS & BUYING ───
    with tab6:
        st.markdown('<div class="sec-head">🥇 Vedic Metals & Auspicious Buying Guide</div>', unsafe_allow_html=True)

        # ── Intro card ──
        st.markdown(f"""
<div class="astro-card">
  <div style="font-size:0.88rem;color:#E8E0D0;line-height:1.8;">
    In Vedic tradition, each metal is governed by a planet. Buying metals on the <span style="color:#C9A84C;">day ruled by their governing planet</span>
    during an auspicious Choghadiya window is believed to multiply prosperity.
    Based on your <span style="color:#C9A84C;">{maha_lord} Mahadasha</span>, your most favoured metals are highlighted below.
  </div>
</div>""", unsafe_allow_html=True)

        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

        # ── Metal data ──
        metals = [
            {
                "name": "Gold",
                "symbol": "🥇",
                "planet": "Sun",
                "best_day": "Sunday (Ravi Vara)",
                "best_time": "Abhijit Muhurta / Amrit/Labh Choghadiya",
                "avoid": "Rahu Kalam, Amavasya (New Moon)",
                "best_tithi": "Akshaya Tritiya, Dhanteras, Purnima",
                "purpose": "Wealth, authority, health, father's blessings",
                "tips": "Buy gold in odd weight (e.g., 10g, 21g). Never gift empty wallets.",
                "nse_symbol": "GOLDBEES / Sovereign Gold Bond",
                "color": "#FFD700",
                "bg": "#2A2000",
            },
            {
                "name": "Silver",
                "symbol": "🥈",
                "planet": "Moon",
                "best_day": "Monday (Soma Vara)",
                "best_time": "Morning Amrit Choghadiya",
                "avoid": "Rahu Kalam, Krishna Paksha Ashtami",
                "best_tithi": "Purnima (Full Moon), Ekadashi, Chaturthi",
                "purpose": "Peace, emotions, mother's blessings, fertility",
                "tips": "Silver coins, idols of Lakshmi/Ganesha are best. Avoid broken/dented silver.",
                "nse_symbol": "SILVERBEES / Silver ETF",
                "color": "#C0C0C0",
                "bg": "#1A1A2A",
            },
            {
                "name": "Copper",
                "symbol": "🔶",
                "planet": "Venus / Mars",
                "best_day": "Friday (Shukra Vara) or Tuesday (Mangala Vara)",
                "best_time": "Labh or Shubh Choghadiya",
                "avoid": "Rahu Kalam, Saturdays",
                "best_tithi": "Navami, Tritiya",
                "purpose": "Health, relationships, vitality, Mars energy",
                "tips": "Copper water vessels (lota) and copper coins are traditional. Clean with lemon.",
                "nse_symbol": "COPPERETF / Copper MCX Futures",
                "color": "#B87333",
                "bg": "#2A1A00",
            },
            {
                "name": "Platinum",
                "symbol": "⬜",
                "planet": "Saturn / Venus",
                "best_day": "Saturday (Shani Vara) or Friday",
                "best_time": "Char or Labh Choghadiya",
                "avoid": "Rahu Kalam, Ashtami",
                "best_tithi": "Chaturdashi, Purnima",
                "purpose": "Discipline, longevity, career stability",
                "tips": "Newer metal in Vedic context — treat as Saturn metal. Best for long-term holding.",
                "nse_symbol": "Platinum ETF / MCX Platinum",
                "color": "#E5E4E2",
                "bg": "#1A1A1A",
            },
            {
                "name": "Lead / Iron",
                "symbol": "⚙️",
                "planet": "Saturn",
                "best_day": "Saturday (Shani Vara)",
                "best_time": "Afternoon Char Choghadiya",
                "avoid": "Sunrise hour, Sundays",
                "best_tithi": "Amavasya, Chaturdashi",
                "purpose": "Protection, warding off negative energy, Saturn remedies",
                "tips": "Iron horseshoe, iron ring on middle finger. Donate iron on Saturdays for Saturn relief.",
                "nse_symbol": "STEELETF / Iron & Steel sector",
                "color": "#708090",
                "bg": "#111118",
            },
            {
                "name": "Brass (Pital)",
                "symbol": "🟡",
                "planet": "Jupiter",
                "best_day": "Thursday (Guru Vara)",
                "best_time": "Morning Amrit or Shubh Choghadiya",
                "avoid": "Rahu Kalam, Amavasya",
                "best_tithi": "Purnima, Ekadashi, Panchami",
                "purpose": "Knowledge, prosperity, Jupiter blessings, temple use",
                "tips": "Brass vessels, bells, and idols are auspicious. Never use cracked brass in puja.",
                "nse_symbol": "Zinc/Copper MCX — Brass alloy exposure",
                "color": "#CFB53B",
                "bg": "#1A1800",
            },
        ]

        # ── Display metal cards in 2 columns ──
        for i in range(0, len(metals), 2):
            col_a, col_b = st.columns(2)
            for col, idx in [(col_a, i), (col_b, i+1)]:
                if idx >= len(metals):
                    break
                m = metals[idx]
                is_favoured = m["planet"].split("/")[0].strip() in [maha_lord, antar_lord]
                border_style = f"border:2px solid {m['color']};" if is_favoured else f"border:1px solid {m['color']}44;"
                star = "⭐ FAVOURED FOR YOUR DASHA · " if is_favoured else ""
                with col:
                    st.markdown(f"""
<div class="astro-card" style="{border_style}background:linear-gradient(135deg,{m['bg']},{m['bg']}CC);">
  <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.8rem;">
    <span style="font-size:1.8rem;">{m['symbol']}</span>
    <div>
      <div style="font-family:'Cinzel',serif;font-size:1rem;color:{m['color']};font-weight:700;">{m['name']}</div>
      <div style="font-size:0.65rem;color:{m['color']}AA;letter-spacing:2px;">{star}Planet: {m['planet']}</div>
    </div>
  </div>
  <div style="font-size:0.78rem;line-height:1.9;color:#E8E0D0;">
    <span style="color:#8A8090;">📅 Best Day:</span> {m['best_day']}<br/>
    <span style="color:#8A8090;">⏰ Best Time:</span> {m['best_time']}<br/>
    <span style="color:#8A8090;">🚫 Avoid:</span> {m['avoid']}<br/>
    <span style="color:#8A8090;">🌙 Best Tithi:</span> {m['best_tithi']}<br/>
    <span style="color:#8A8090;">🎯 Purpose:</span> {m['purpose']}<br/>
    <span style="color:#8A8090;">💡 Tip:</span> {m['tips']}<br/>
    <span style="color:{m['color']}99;font-size:0.72rem;">📈 Market:</span>
    <span style="color:{m['color']}99;font-size:0.72rem;"> {m['nse_symbol']}</span>
  </div>
</div>""", unsafe_allow_html=True)

        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

        # ── Today's buying verdict ──
        st.markdown('<div class="sec-head">📅 Today\'s Metal Buying Verdict</div>', unsafe_allow_html=True)

        today_wd = today.strftime("%A")
        day_metal_map = {
            "Sunday":    ("Gold", "🥇", "#FFD700"),
            "Monday":    ("Silver", "🥈", "#C0C0C0"),
            "Tuesday":   ("Copper/Iron", "🔶", "#B87333"),
            "Wednesday": ("Mixed Alloys", "⚙️", "#88AA88"),
            "Thursday":  ("Brass/Gold", "🟡", "#CFB53B"),
            "Friday":    ("Silver/Platinum", "⬜", "#E5E4E2"),
            "Saturday":  ("Iron/Lead", "⚫", "#708090"),
        }
        today_metal, today_metal_icon, today_metal_color = day_metal_map.get(today_wd, ("Any", "✨", "#C9A84C"))
        rk_start, rk_end = rk

        st.markdown(f"""
<div class="astro-card">
  <div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-start;">
    <div style="flex:1;min-width:200px;">
      <div style="font-family:'Cinzel',serif;font-size:0.75rem;color:#8A8090;letter-spacing:2px;margin-bottom:0.4rem;">TODAY — {today_wd.upper()}</div>
      <div style="font-size:1.6rem;color:{today_metal_color};font-family:'Cinzel',serif;font-weight:700;">
        {today_metal_icon} {today_metal}
      </div>
      <div style="font-size:0.8rem;color:#8A8090;margin-top:0.3rem;">Most auspicious metal to buy today</div>
    </div>
    <div style="flex:1;min-width:200px;">
      <div style="font-family:'Cinzel',serif;font-size:0.75rem;color:#8A8090;letter-spacing:2px;margin-bottom:0.4rem;">BEST WINDOW</div>
      <div style="background:#0F2A1A;border:1px solid #27AE60;border-radius:8px;padding:0.5rem 0.8rem;">
        <span style="color:#2ECC71;font-family:'Cinzel',serif;">🟢 {abh[0]} – {abh[1]}</span>
        <div style="font-size:0.7rem;color:#8A8090;">Abhijit Muhurta</div>
      </div>
    </div>
    <div style="flex:1;min-width:200px;">
      <div style="font-family:'Cinzel',serif;font-size:0.75rem;color:#8A8090;letter-spacing:2px;margin-bottom:0.4rem;">AVOID BUYING</div>
      <div style="background:#2A0F0F;border:1px solid #C0392B;border-radius:8px;padding:0.5rem 0.8rem;">
        <span style="color:#E74C3C;font-family:'Cinzel',serif;">🔴 {rk_start} – {rk_end}</span>
        <div style="font-size:0.7rem;color:#8A8090;">Rahu Kalam</div>
      </div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

        # ── Akshaya Tritiya countdown ──
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-head">🌟 Auspicious Metal Buying Festivals</div>', unsafe_allow_html=True)

        festivals = [
            ("Akshaya Tritiya",    "Most auspicious day for buying Gold — whatever you buy grows endlessly", "🥇 Gold, Silver"),
            ("Dhanteras",          "Buy metals & new items — Lakshmi enters homes with new purchases", "🥇 Gold, 🥈 Silver, ⚙️ Iron"),
            ("Diwali (Lakshmi Puja)","Puja with gold/silver idols — attracts Lakshmi for the year", "🥇 Gold coins, 🥈 Silver Lakshmi"),
            ("Purnima (Full Moon)", "Every full moon is auspicious for silver — Moon's energy peaks", "🥈 Silver"),
            ("Guruvayur Ekadashi",  "Sacred day for brass and gold donations — Jupiter blessings", "🟡 Brass, 🥇 Gold"),
            ("Navratri",           "9 days — copper and gold offerings to Devi — increases shakti", "🔶 Copper, 🥇 Gold"),
        ]

        for fest, desc, metals_rec in festivals:
            st.markdown(f"""
<div style="background:linear-gradient(135deg,#13132A,#1A1A35);border:1px solid #3A2A0A;
            border-left:3px solid #C9A84C;border-radius:8px;padding:0.7rem 1rem;margin:0.4rem 0;
            display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;">
  <div>
    <div style="font-family:'Cinzel',serif;font-size:0.88rem;color:#C9A84C;">{fest}</div>
    <div style="font-size:0.75rem;color:#8A8090;margin-top:0.2rem;">{desc}</div>
  </div>
  <div style="font-size:0.75rem;color:#E8E0D0;background:#2A2A4A;padding:0.3rem 0.7rem;border-radius:6px;">{metals_rec}</div>
</div>""", unsafe_allow_html=True)

        st.markdown("""
<div class="disclaimer-box" style="margin-top:1rem;">
  ⚠️ Metal buying recommendations are based on Vedic astrology traditions for spiritual and cultural purposes only.
  Investment in gold/silver ETFs or physical metals should be based on financial advice from a SEBI-registered advisor.
  Prices of metals fluctuate and past performance does not guarantee returns.
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    name, dob, nakshatra, sunrise, sunset, generate = sidebar()

    if generate and name:
        st.session_state["dashboard_active"] = True
        st.session_state["user_name"]  = name
        st.session_state["user_dob"]   = dob
        st.session_state["user_nak"]   = nakshatra
        st.session_state["sunrise"]    = sunrise
        st.session_state["sunset"]     = sunset
        st.session_state.pop("ai_daily", None)
        st.session_state.pop("chat_history", None)

    if st.session_state.get("dashboard_active"):
        show_dashboard(
            st.session_state["user_name"],
            st.session_state["user_dob"],
            st.session_state["user_nak"],
            st.session_state["sunrise"],
            st.session_state["sunset"],
        )
    else:
        show_landing()

if __name__ == "__main__":
    main()
