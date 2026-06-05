import streamlit as st

def apply():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=Unbounded:wght@300;400;600;700;900&display=swap');

    /* BASE */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #06080d !important;
        color: #c8d4e0 !important;
    }
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse 80% 50% at 10% -10%, rgba(0,255,170,0.04) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 90% 110%, rgba(0,170,255,0.04) 0%, transparent 60%),
            #06080d;
    }
    [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stToolbar"] { display: none !important; }
    section.main > div { padding-top: 0 !important; }

    /* =====================================================
       SIDEBAR — always open, no collapse button
    ===================================================== */

    /* Force sidebar always visible */
    [data-testid="stSidebar"] {
        background: #04070c !important;
        border-right: 1px solid #0f2535 !important;
        min-width: 240px !important;
        max-width: 240px !important;
        display: block !important;
        visibility: visible !important;
        transform: translateX(0px) !important;
    }

    /* Hide the collapse/expand arrow */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Sidebar top brand label */
    [data-testid="stSidebarContent"]::before {
        content: "DIGITVISION";
        display: block;
        font-family: 'Unbounded', sans-serif;
        font-size: 0.6rem;
        font-weight: 700;
        letter-spacing: 0.35em;
        color: #00ffaa;
        padding: 1.4rem 1.4rem 1.2rem;
        border-bottom: 1px solid #0f2535;
        margin-bottom: 0.8rem;
    }

    /* Nav links container */
    [data-testid="stSidebarNavItems"] {
        padding: 0 0.5rem !important;
        gap: 0.15rem !important;
        display: flex !important;
        flex-direction: column !important;
    }

    /* Individual nav link */
    [data-testid="stSidebarNavLink"] {
        border-radius: 8px !important;
        padding: 0.7rem 1rem !important;
        margin: 0.1rem 0 !important;
        border: 1px solid transparent !important;
        transition: all 0.18s ease !important;
        display: flex !important;
        align-items: center !important;
        text-decoration: none !important;
    }

    /* Nav link text */
    [data-testid="stSidebarNavLink"] span,
    [data-testid="stSidebarNavLink"] p,
    [data-testid="stSidebarNavLink"] div {
        font-family: 'DM Mono', monospace !important;
        font-size: 0.78rem !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        color: #4a7a9b !important;
        font-weight: 400 !important;
    }

    /* Hover */
    [data-testid="stSidebarNavLink"]:hover {
        background: rgba(0,255,170,0.05) !important;
        border-color: rgba(0,255,170,0.15) !important;
    }
    [data-testid="stSidebarNavLink"]:hover span,
    [data-testid="stSidebarNavLink"]:hover p,
    [data-testid="stSidebarNavLink"]:hover div {
        color: #a0d4c0 !important;
    }

    /* Active / current page */
    [data-testid="stSidebarNavLink"][aria-current="page"] {
        background: rgba(0,255,170,0.08) !important;
        border-color: rgba(0,255,170,0.2) !important;
        border-left: 3px solid #00ffaa !important;
    }
    [data-testid="stSidebarNavLink"][aria-current="page"] span,
    [data-testid="stSidebarNavLink"][aria-current="page"] p,
    [data-testid="stSidebarNavLink"][aria-current="page"] div {
        color: #00ffaa !important;
        font-weight: 500 !important;
    }

    /* TYPOGRAPHY */
    * { font-family: 'DM Mono', monospace !important; }

    .dv-display {
        font-family: 'Unbounded', sans-serif !important;
        font-weight: 900;
        letter-spacing: -0.04em;
        line-height: 0.95;
        background: linear-gradient(135deg, #ffffff 0%, #7af8cc 50%, #00aaff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .dv-mono {
        font-family: 'DM Mono', monospace !important;
        font-size: 0.7rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #2a5a7a;
    }

    /* CARDS */
    .dv-card {
        background: linear-gradient(135deg, #0a1420 0%, #080e18 100%);
        border: 1px solid #0f2535;
        border-radius: 16px;
        padding: 1.6rem 1.8rem;
        position: relative;
        overflow: hidden;
        transition: border-color 0.25s, transform 0.2s;
    }
    .dv-card::after {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(0,255,170,0.03), transparent 50%);
        pointer-events: none;
    }
    .dv-card:hover { border-color: #1a4a6a; transform: translateY(-3px); }
    .dv-card-accent {
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #00ffaa44, transparent);
    }

    .dv-stat-label {
        font-size: 0.58rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #2a5a7a;
        margin-bottom: 0.5rem;
    }
    .dv-stat-value {
        font-family: 'Unbounded', sans-serif !important;
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1;
    }
    .dv-stat-sub {
        font-size: 0.65rem;
        color: #2a5a7a;
        margin-top: 0.3rem;
    }

    /* SECTION TAGS */
    .dv-tag {
        display: inline-block;
        font-size: 0.6rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: #00ffaa;
        background: rgba(0,255,170,0.07);
        border: 1px solid rgba(0,255,170,0.18);
        padding: 0.2rem 0.65rem;
        border-radius: 3px;
        margin-bottom: 0.6rem;
    }

    .dv-section-title {
        font-family: 'Unbounded', sans-serif !important;
        font-size: 1.3rem;
        font-weight: 600;
        color: #ffffff;
        letter-spacing: -0.02em;
        margin-bottom: 1.2rem;
    }

    /* DIVIDER */
    .dv-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #0f2535 30%, #0f2535 70%, transparent);
        margin: 2rem 0;
    }

    /* PREDICTION BOX */
    .dv-pred-box {
        background: linear-gradient(135deg, #0a1e2e 0%, #06080d 100%);
        border: 1px solid #0f2535;
        border-radius: 16px;
        padding: 2.5rem 2rem;
        text-align: center;
    }
    .dv-pred-box.live {
        border-color: #00ffaa;
        box-shadow: 0 0 60px rgba(0,255,170,0.06), inset 0 0 60px rgba(0,255,170,0.02);
    }

    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, #004433, #006644) !important;
        color: #00ffaa !important;
        border: 1px solid #00ffaa44 !important;
        border-radius: 8px !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        padding: 0.65rem 1.5rem !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #005544, #008855) !important;
        border-color: #00ffaa88 !important;
        box-shadow: 0 0 20px rgba(0,255,170,0.15) !important;
        transform: translateY(-1px) !important;
    }

    /* CHECKBOX */
    .stCheckbox label { color: #4a7a9b !important; font-size: 0.78rem !important; }

    /* INFO / WARNING / SUCCESS */
    [data-testid="stInfo"] {
        background: rgba(0,170,255,0.05) !important;
        border-color: rgba(0,170,255,0.2) !important;
        color: #4a8aab !important;
        font-size: 0.78rem !important;
    }
    [data-testid="stSuccess"] {
        background: rgba(0,255,170,0.05) !important;
        border-color: rgba(0,255,170,0.2) !important;
        color: #00cc88 !important;
        font-size: 0.78rem !important;
    }

    /* PROGRESS BAR */
    .stProgress > div > div {
        background: linear-gradient(90deg, #004433, #00ffaa) !important;
    }
    .stProgress > div {
        background: #0a1a25 !important;
        border-radius: 4px !important;
    }

    /* HIDE BRANDING */
    #MainMenu, footer { visibility: hidden !important; }

    hr {
        border: none !important;
        border-top: 1px solid #0f2535 !important;
        margin: 1.5rem 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def page_header(tag, title, subtitle=None):
    sub_html = f'<div class="dv-mono" style="color:#4a7a9b;margin-top:0.6rem;">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div style="padding:2.5rem 0 1.5rem;">
        <div class="dv-tag">{tag}</div>
        <div class="dv-display" style="font-size:clamp(2.5rem,5vw,4rem);">{title}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def divider():
    st.markdown('<div class="dv-divider"></div>', unsafe_allow_html=True)


def stat_card(label, value, sub=None):
    sub_html = f'<div class="dv-stat-sub">{sub}</div>' if sub else ""
    return f"""
    <div class="dv-card">
        <div class="dv-card-accent"></div>
        <div class="dv-stat-label">{label}</div>
        <div class="dv-stat-value">{value}</div>
        {sub_html}
    </div>
    """