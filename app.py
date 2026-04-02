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

    # ── Header banner (dark, like app) ──
    pdf.set_fill_color(*BG_HEADER)
    pdf.rect(8, 8, 194, 32, 'F')

    pdf.set_xy(10, 13)
    pdf.set_text_color(201, 168, 76)
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 10, "  VedicTrade - Astro Finance Report", ln=True, align="L")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(200, 190, 170)
    pdf.cell(0, 6, f"  Generated: {datetime.date.today().strftime('%d %B %Y')}   |   Trader: {user_data.get('name','Trader')}   |   For spiritual guidance only", ln=True, align="L")

    pdf.ln(8)

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

    return bytes(pdf.output())

def get_pdf_download_link(pdf_bytes, filename="VedicTrade_Report.pdf"):
    b64 = base64.b64encode(pdf_bytes).decode()
    return f'<a href="data:application/pdf;base64,{b64}" download="{filename}" style="text-decoration:none;"><button style="background:linear-gradient(135deg,#8B6914,#C9A84C);color:#0A0A0A;border:none;padding:0.6rem 1.5rem;border-radius:8px;font-family:Cinzel,serif;font-weight:700;cursor:pointer;letter-spacing:1px;font-size:0.9rem;">📥 Download PDF Report</button></a>'

# ─────────────────────────────────────────────
#  GROQ AI
# ─────────────────────────────────────────────

def get_groq_analysis(user_data: dict, analysis_data: dict, question: str = None) -> str:
    api_key = st.session_state.get("groq_api_key", "")
    if not api_key:
        return "⚠️ Please enter your Groq API key in the sidebar to enable AI analysis."
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

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────

def sidebar():
    with st.sidebar:
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
        st.markdown('<div class="sec-head">🤖 Groq AI Key</div>', unsafe_allow_html=True)
        groq_key = st.text_input("Groq API Key", type="password",
                                  placeholder="gsk_...",
                                  help="Get free key at console.groq.com")
        if groq_key:
            st.session_state["groq_api_key"] = groq_key
            st.markdown('<span class="pill-good">✓ API Key Set</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="pill-warn">⚠ No API Key</span>', unsafe_allow_html=True)

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
  <div style="display:flex;gap:0.8rem;flex-wrap:wrap;">
    <span class="pill-neut">🌙 {today_nak}</span>
    <span class="pill-neut">📅 {tithi} {paksha}</span>
    <span class="pill-neut">⭐ {vara.split('(')[0].strip()}</span>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── TABS ──
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🕐 Muhurta Timer",
        "🪐 Dasha Profile",
        "📊 Sector Map",
        "🤖 VedicAI Chat",
        "📥 PDF Report"
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
