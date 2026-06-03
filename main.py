import os
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Cena Dashboard — Bank XYZ CX",
    page_icon="CD",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLORS = {
    "page_bg": "#EEF3F8",
    "app_bg": "#FFFFFF",
    "sidebar_bg": "#F3F7FD",
    "sidebar_active": "#DCEBFF",
    "sidebar_hover": "#EAF2FF",
    "card_bg": "#FFFFFF",
    "card_soft": "#F8FAFD",
    "border": "#E3E8EF",
    "border_dark": "#CBD5E1",
    "text_primary": "#1F2933",
    "text_secondary": "#5F6B7A",
    "text_muted": "#8A97A8",
    "accent_blue": "#2F80ED",
    "accent_navy": "#1F3A5F",
    "accent_orange": "#F26A2E",
    "accent_gold": "#F3C76B",
    "accent_purple": "#CDA7F7",
    "accent_teal": "#48BFB7",
    "positive": "#3DBE7A",
    "warning": "#E5B84A",
    "danger": "#D95F5F",
    "chart_bg": "rgba(0,0,0,0)",
}

LOCAL_DOWNLOADS_DIR = Path.home() / "Downloads"
PROJECT_DATA_DIR = Path(__file__).parent / "data"
DATA_FILES = {
    "ind": "bank_dashboard_final_clean.csv",
    "cab": "bank_dashboard_cabang_summary.csv",
    "nas": "bank_dashboard_nasional_summary.csv",
}


def resolve_data_path(filename):
    project_path = PROJECT_DATA_DIR / filename
    downloads_path = LOCAL_DOWNLOADS_DIR / filename

    if project_path.exists():
        return project_path
    if downloads_path.exists():
        return downloads_path

    return project_path

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, .stApp, .block-container {
    font-family: 'Poppins', sans-serif;
}

p, div, span, label, input, textarea, button {
    font-family: 'Poppins', sans-serif;
}

button[kind="header"] span,
button[data-testid="collapsedControl"] span,
[data-testid="collapsedControl"] span,
[data-testid="stSidebarCollapseButton"] span {
    font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
    font-size: 20px !important;
    line-height: 1 !important;
}

.stApp {
    background: #EEF3F8;
    color: #1F2933;
}

.block-container {
    padding-top: 3.4rem;
    padding-bottom: 2rem;
    max-width: 1320px;
}

section[data-testid="stSidebar"] {
    background: #F3F7FD;
    border-right: 1px solid #E3E8EF;
}

section[data-testid="stSidebar"] * {
    font-family: 'Poppins', sans-serif;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #1F2933;
}

.brand-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px 0 26px 0;
}

.brand-icon {
    width: 78px;
    height: 78px;
    border-radius: 24px;
    background:
        radial-gradient(circle at 25% 20%, rgba(255,255,255,0.95), rgba(255,255,255,0) 34%),
        linear-gradient(145deg, #DCEBFF 0%, #F8FBFF 52%, #CFE2FF 100%);
    border: 1px solid #C8DCF5;
    color: #1F3A5F;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 28px;
    letter-spacing: -2px;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.85),
        0 10px 24px rgba(31, 58, 95, 0.08);
    position: relative;
}

.brand-icon::after {
    content: "";
    position: absolute;
    width: 28px;
    height: 3px;
    border-radius: 999px;
    background: #F26A2E;
    bottom: 17px;
    left: 25px;
    opacity: 0.9;
}

.brand-text,
.brand-title,
.brand-subtitle {
    display: none;
}

.sidebar-count {
    background: #FFFFFF;
    border: 1px solid #E3E8EF;
    border-radius: 14px;
    padding: 14px 14px;
    margin-top: 14px;
}

.sidebar-count-value {
    font-size: 22px;
    font-weight: 600;
    color: #1F2933;
    line-height: 1.1;
}

.sidebar-count-label {
    font-size: 12px;
    color: #8A97A8;
    margin-top: 4px;
}

.cx-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 24px;
    margin-bottom: 22px;
}

.cx-title {
    font-size: 31px;
    font-weight: 700;
    color: #1F2933;
    margin: 0;
    letter-spacing: -0.9px;
}

.cx-subtitle {
    color: #5F6B7A;
    font-size: 14px;
    margin-top: 7px;
}

.header-pills {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: flex-end;
}

.header-pill {
    background: #FFFFFF;
    border: 1px solid #E3E8EF;
    color: #5F6B7A;
    border-radius: 999px;
    padding: 8px 12px;
    font-size: 12px;
    font-weight: 500;
    white-space: nowrap;
}

.kpi-card {
    background: #FFFFFF;
    border: 1px solid #E3E8EF;
    border-radius: 14px;
    padding: 22px 22px 20px 22px;
    min-height: 154px;
    box-shadow: 0 8px 24px rgba(15, 25, 35, 0.04);
    position: relative;
    overflow: hidden;
}

.kpi-card::before {
    content: "";
    position: absolute;
    left: 0;
    top: 18px;
    bottom: 18px;
    width: 4px;
    border-radius: 0 999px 999px 0;
    background: var(--stripe-color, #2F80ED);
}

.kpi-top {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    margin-bottom: 14px;
}

.kpi-icon {
    display: none;
}

.kpi-icon-orange,
.kpi-icon-blue,
.kpi-icon-purple,
.kpi-icon-teal {
    background: transparent;
    color: inherit;
}

.kpi-label {
    font-size: 13px;
    color: #5F6B7A;
    font-weight: 400;
    margin-bottom: 6px;
}

.kpi-value {
    font-size: 2rem;
    line-height: 1.1;
    font-weight: 600;
    color: #1F2933;
    letter-spacing: -1px;
}

.kpi-caption {
    color: #8A97A8;
    font-size: 12px;
    margin-top: 8px;
}

.status-pill {
    border-radius: 0;
    padding: 0 0 3px 0;
    font-size: 12px;
    font-weight: 600;
    border: none;
    background: transparent !important;
    letter-spacing: -0.2px;
    line-height: 1.1;
}

.status-good {
    color: #247A4D;
    border-bottom: 2px solid #3DBE7A;
}

.status-warning {
    color: #8A6412;
    border-bottom: 2px solid #E5B84A;
}

.status-danger {
    color: #A64242;
    border-bottom: 2px solid #D95F5F;
}

.chart-card, .summary-box {
    background: #FFFFFF;
    border: 1px solid #E3E8EF;
    border-radius: 14px;
    padding: 18px 18px 8px 18px;
    box-shadow: 0 8px 24px rgba(15, 25, 35, 0.04);
    margin-bottom: 18px;
}

.summary-box {
    padding-bottom: 18px;
}

.section-title {
    font-size: 16px;
    font-weight: 600;
    color: #1F2933;
    margin-bottom: 12px;
    padding-left: 10px;
    border-left: 3px solid #F26A2E;
    text-transform: none;
    letter-spacing: -0.3px;
}

.gauge-card {
    padding: 18px 18px 2px 18px;
}

.small-muted {
    color: #8A97A8;
    font-size: 12px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background: #FFFFFF;
    border: 1px solid #E3E8EF;
    border-radius: 999px;
    padding: 8px 18px;
    color: #5F6B7A;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background: #DCEBFF !important;
    color: #1F3A5F !important;
    border-color: #C4DAF7 !important;
}

div[data-testid="stMetricValue"] {
    color: #1F2933;
}

.stButton > button {
    background: #2F80ED;
    color: white;
    border: 0;
    border-radius: 12px;
    padding: 0.65rem 1rem;
    font-weight: 600;
}

.stButton > button:hover {
    background: #1F6FD1;
    color: white;
}

/* Dataframe header emphasis */
[data-testid="stDataFrame"] [role="columnheader"],
[data-testid="stDataFrame"] [data-testid="stTableHeader"] {
    font-weight: 700 !important;
    color: #1F2933 !important;
}

[data-testid="stDataFrame"] div[role="columnheader"] p,
[data-testid="stDataFrame"] div[role="columnheader"] span {
    font-weight: 700 !important;
    color: #1F2933 !important;
}

/* Styled HTML tables, used because Streamlit dataframe headers are canvas-rendered and resist normal CSS like an emotionally unavailable spreadsheet */
.styled-table-wrap {
    background: #FFFFFF;
    border: 1px solid #E3E8EF;
    border-radius: 14px;
    overflow: hidden;
    margin-top: 12px;
    margin-bottom: 18px;
}

.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    color: #1F2933;
}

.styled-table thead th {
    background: #F7FAFE;
    color: #1F2933;
    font-weight: 700 !important;
    text-align: left;
    padding: 12px 14px;
    border-bottom: 1px solid #E3E8EF;
    border-right: 1px solid #E3E8EF;
}

.styled-table tbody td {
    padding: 11px 14px;
    border-bottom: 1px solid #EEF2F6;
    border-right: 1px solid #EEF2F6;
    color: #374151;
    font-weight: 500;
}

.styled-table tbody tr:nth-child(even) {
    background: #FBFCFE;
}

.styled-table tbody tr:hover {
    background: #F3F7FD;
}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    paths = {key: resolve_data_path(filename) for key, filename in DATA_FILES.items()}
    missing = [str(path) for path in paths.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing CSV file(s): " + ", ".join(missing))

    ind = pd.read_csv(paths["ind"])
    cab = pd.read_csv(paths["cab"])
    nas = pd.read_csv(paths["nas"]).iloc[0]
    return ind, cab, nas


try:
    df_ind, df_cab, national = load_data()
except Exception as exc:
    st.error(str(exc))
    st.info(
        "Put these files in either the project data/ folder or ~/Downloads: "
        "bank_dashboard_final_clean.csv, "
        "bank_dashboard_cabang_summary.csv, "
        "bank_dashboard_nasional_summary.csv"
    )
    st.stop()


required_cols = {
    "PROV",
    "CABANG",
    "gender",
    "usia_kategori",
    "CSI",
    "Loyalty",
    "NPS_kategori",
    "touch_operasional",
    "touch_parkir",
    "touch_banking_hall",
    "touch_toilet",
}
missing_cols = sorted(required_cols - set(df_ind.columns))
if missing_cols:
    st.error(f"Missing required columns in bank_dashboard_final_clean.csv: {missing_cols}")
    st.stop()


def nps_category(value):
    if value < 0:
        return "Critical", "status-danger"
    if value < 30:
        return "Needs Work", "status-warning"
    if value < 70:
        return "Good", "status-warning"
    return "Excellent", "status-good"


def safe_score(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:.2f} / 6.0"


def base_layout(height=340, margin=None, showlegend=True):
    if margin is None:
        margin = dict(l=24, r=24, t=36, b=24)

    return dict(
        height=height,
        margin=margin,
        paper_bgcolor=COLORS["chart_bg"],
        plot_bgcolor=COLORS["chart_bg"],
        font=dict(family="Poppins, sans-serif", color=COLORS["text_primary"], size=12),
        showlegend=showlegend,
        xaxis=dict(showgrid=True, gridcolor="#EEF2F6", zeroline=False, linecolor=COLORS["border"]),
        yaxis=dict(showgrid=False, zeroline=False, linecolor=COLORS["border"]),
    )



def kpi_card(icon, icon_class, label, value, caption, status_label, status_class):
    stripe_map = {
        "kpi-icon-orange": "#F26A2E",
        "kpi-icon-blue": "#2F80ED",
        "kpi-icon-purple": "#8C52D6",
        "kpi-icon-teal": "#48BFB7",
    }
    stripe_color = stripe_map.get(icon_class, "#2F80ED")

    st.markdown(
        f"""
        <div class="kpi-card" style="--stripe-color: {stripe_color};">
            <div class="kpi-top">
                <div class="status-pill {status_class}">{status_label}</div>
            </div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Helper to render styled HTML table instead of Streamlit dataframe
def render_html_table(dataframe, max_rows=40):
    display_df = dataframe.head(max_rows).copy()
    html_table = display_df.to_html(index=False, escape=False, classes="styled-table")
    st.markdown(
        f"""
        <div class="styled-table-wrap">
            {html_table}
        </div>
        """,
        unsafe_allow_html=True,
    )


# --- AI Helper Functions ---
def get_anthropic_api_key():
    env_key = os.getenv("ANTHROPIC_API_KEY")
    if env_key:
        return env_key

    try:
        return st.secrets.get("ANTHROPIC_API_KEY", None)
    except Exception:
        return None


def local_insight_response(question, n, nps_val, csi_val, loyal_val, ease_val, pct_p, pct_pa, pct_d, sel_prov, sel_branch, sel_gender):
    question_clean = (question or "").strip()
    scope_prov = ", ".join(sel_prov) if sel_prov else "all provinces"
    scope_branch = ", ".join(sel_branch[:6]) + ("..." if len(sel_branch) > 6 else "") if sel_branch else "all branches"
    loyalty_text = "N/A" if pd.isna(loyal_val) else f"{loyal_val:.2f} / 6.0"
    csi_text = "N/A" if pd.isna(csi_val) else f"{csi_val:.2f} / 6.0"
    ease_text = "N/A" if pd.isna(ease_val) else f"{ease_val:.2f} / 6.0"

    q_lower = question_clean.lower()
    if "passive" in q_lower:
        focus = (
            f"Passive customers are respondents who gave an NPS score of 7 or 8. In this filtered data, "
            f"Passive is {pct_pa:.1f}%, meaning about {round(n * pct_pa / 100):,} out of {n:,} respondents are satisfied enough not to complain, "
            f"but not enthusiastic enough to be classified as Promoters."
        )
    elif "promoter" in q_lower:
        focus = (
            f"Promoters are respondents who gave an NPS score of 9 or 10. In this filtered data, "
            f"Promoters account for {pct_p:.1f}%, or about {round(n * pct_p / 100):,} respondents. "
            f"This is the main reason the NPS reaches {nps_val:.1f}."
        )
    elif "detractor" in q_lower:
        focus = (
            f"Detractors are respondents who gave an NPS score from 0 to 6. In this filtered data, "
            f"Detractors account for {pct_d:.1f}%, or about {round(n * pct_d / 100):,} respondents. "
            f"This group directly reduces NPS because NPS equals Promoter percentage minus Detractor percentage."
        )
    elif "nps" in q_lower:
        focus = (
            f"The current NPS is {nps_val:.1f}. This is calculated as Promoters ({pct_p:.1f}%) minus "
            f"Detractors ({pct_d:.1f}%). A score above 70 is generally interpreted as excellent advocacy."
        )
    else:
        focus = (
            f"For the current filter scope, the dashboard shows {n:,} respondents, NPS of {nps_val:.1f}, "
            f"CSI of {csi_text}, Loyalty of {loyalty_text}, and Service Ease of {ease_text}. "
            f"Promoters dominate at {pct_p:.1f}%, while Passive customers are {pct_pa:.1f}% and Detractors are {pct_d:.1f}%."
        )

    return f"""
**Local Insight Mode**

API key is not configured, so this response is generated from the dashboard metrics directly.

- {focus}
- Current scope: {scope_prov}; {scope_branch}; gender filter: {sel_gender}.
- CSI is {csi_text}, which indicates very high satisfaction on the 1 to 6 scale.
- Service Ease is {ease_text}, so operational touchpoints appear strong in the current filtered view.
- Interpretation note: this does not test statistical significance. It summarizes the filtered dashboard values only.
""".strip()


with st.sidebar:
    st.markdown(
        """
        <div class="brand-wrap">
            <div class="brand-icon">CD</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>Filters</div>", unsafe_allow_html=True)

    provinces = sorted(df_ind["PROV"].dropna().unique())
    sel_prov = st.multiselect("Province", provinces, default=[])

    if sel_prov:
        branch_pool = sorted(df_ind[df_ind["PROV"].isin(sel_prov)]["CABANG"].dropna().unique())
    else:
        branch_pool = sorted(df_ind["CABANG"].dropna().unique())

    sel_branch = st.multiselect("Branch", branch_pool, default=[])
    sel_gender = st.radio("Gender", ["All", "Pria", "Wanita"])


# Apply filters to individual data
filtered = df_ind.copy()
if sel_prov:
    filtered = filtered[filtered["PROV"].isin(sel_prov)]
if sel_branch:
    filtered = filtered[filtered["CABANG"].isin(sel_branch)]
if sel_gender != "All":
    filtered = filtered[filtered["gender"] == sel_gender]

# Apply same province/branch filters to cabang summary
filtered_cabang = df_cab.copy()
if sel_prov:
    filtered_cabang = filtered_cabang[filtered_cabang["PROV"].isin(sel_prov)]
if sel_branch:
    filtered_cabang = filtered_cabang[filtered_cabang["CABANG"].isin(sel_branch)]

n = len(filtered)
nps_val = round(
    (filtered["NPS_kategori"].eq("Promoter").sum() / n * 100)
    - (filtered["NPS_kategori"].eq("Detractor").sum() / n * 100),
    1,
) if n > 0 else 0.0
csi_val = round(filtered["CSI"].dropna().mean(), 2) if n > 0 else np.nan
loyal_val = round(filtered["Loyalty"].dropna().mean(), 2) if n > 0 and len(filtered["Loyalty"].dropna()) > 0 else np.nan
ease_val = round(filtered["touch_operasional"].dropna().mean(), 2) if n > 0 else np.nan
pct_p = round(filtered["NPS_kategori"].eq("Promoter").sum() / n * 100, 1) if n > 0 else 0.0
pct_pa = round(filtered["NPS_kategori"].eq("Passive").sum() / n * 100, 1) if n > 0 else 0.0
pct_d = round(filtered["NPS_kategori"].eq("Detractor").sum() / n * 100, 1) if n > 0 else 0.0

with st.sidebar:
    st.markdown(
        f"""
        <div class="sidebar-count">
            <div class="sidebar-count-value">{n:,}</div>
            <div class="sidebar-count-label">respondents after filtering</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    f"""
    <div class="cx-header">
        <div>
            <h1 class="cx-title">Bank XYZ Customer Experience</h1>
            <div class="cx-subtitle">Executive overview of satisfaction, loyalty, NPS, and service touchpoints</div>
        </div>
        <div class="header-pills">
            <div class="header-pill">{int(national.get('total_responden', len(df_ind))):,} respondents</div>
            <div class="header-pill">{df_cab['CABANG'].nunique():,} branches</div>
            <div class="header-pill">{df_ind['PROV'].nunique():,} provinces</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if n == 0:
    st.warning("No data available for the selected filters.")

nps_label, nps_class = nps_category(nps_val)

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("N", "kpi-icon-orange", "NPS", f"{nps_val:.1f}", "Customer advocacy score", nps_label, nps_class)
with k2:
    kpi_card("C", "kpi-icon-blue", "CSI", safe_score(csi_val), "Average satisfaction score", "Score", "status-good")
with k3:
    kpi_card("L", "kpi-icon-purple", "Loyalty", safe_score(loyal_val), "Indicative only, high missing rate", "Indicative", "status-warning")
with k4:
    kpi_card("E", "kpi-icon-teal", "Service Ease", safe_score(ease_val), "Operational touchpoint proxy", "Proxy", "status-good")

st.write("")

overview_tab, branch_tab, province_tab, ai_tab = st.tabs(["Overview", "Branch Analysis", "Province Analysis", "AI Insights"])

touch_cols = {
    "touch_operasional": "Operational",
    "touch_parkir": "Parking",
    "touch_banking_hall": "Banking Hall",
    "touch_toilet": "Toilet",
}

with overview_tab:
    col_left, col_right = st.columns([1.25, 1])

    with col_left:
        st.markdown("<div class='chart-card gauge-card'><div class='section-title'>NPS Gauge</div>", unsafe_allow_html=True)
        gauge_color = COLORS["positive"] if nps_val >= 70 else COLORS["warning"] if nps_val >= 30 else COLORS["danger"]
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=nps_val,
                domain={"x": [0.06, 0.94], "y": [0.02, 0.96]},
                number={
                    "font": {"size": 44, "family": "Poppins", "color": COLORS["text_primary"]},
                    "valueformat": ".1f",
                },
                gauge={
                    "shape": "angular",
                    "axis": {
                        "range": [-100, 100],
                        "tickmode": "array",
                        "tickvals": [-100, -50, 0, 50, 100],
                        "ticktext": ["-100", "-50", "0", "50", "100"],
                        "tickwidth": 1,
                        "tickcolor": COLORS["border_dark"],
                    },
                    "bar": {"color": gauge_color, "thickness": 0.18},
                    "bgcolor": "rgba(255,255,255,0)",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [-100, 0], "color": "#FBEAEA"},
                        {"range": [0, 30], "color": "#FFF3D0"},
                        {"range": [30, 70], "color": "#E4F0FF"},
                        {"range": [70, 100], "color": "#E5F6ED"},
                    ],
                },
            )
        )
        fig.update_layout(
            **base_layout(height=390, margin=dict(l=54, r=54, t=8, b=8), showlegend=False)
        )
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        st.plotly_chart(fig, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("<div class='chart-card'><div class='section-title'>Customer Mix</div>", unsafe_allow_html=True)
        fig = go.Figure(
            go.Pie(
                labels=["Promoter", "Passive", "Detractor"],
                values=[pct_p, pct_pa, pct_d],
                hole=0.62,
                marker=dict(colors=[COLORS["positive"], COLORS["warning"], COLORS["danger"]]),
                textinfo="label+percent",
            )
        )
        fig.update_layout(**base_layout(height=320, margin=dict(l=20, r=20, t=16, b=8)))
        st.plotly_chart(fig, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1.2, 1])

    with col_a:
        st.markdown("<div class='chart-card'><div class='section-title'>Touchpoint Score</div>", unsafe_allow_html=True)
        touch_values = filtered[list(touch_cols.keys())].mean().rename(index=touch_cols).dropna() if n > 0 else pd.Series(dtype=float)
        bar_colors = [
            COLORS["danger"] if value < 4.5 else COLORS["warning"] if value <= 5.0 else COLORS["positive"]
            for value in touch_values.values
        ]
        fig = go.Figure(go.Bar(x=touch_values.values, y=touch_values.index, orientation="h", marker_color=bar_colors))
        fig.update_layout(**base_layout(height=340, showlegend=False))
        fig.update_xaxes(range=[0, 6])
        st.plotly_chart(fig, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("<div class='chart-card'><div class='section-title'>Gender Distribution</div>", unsafe_allow_html=True)
        gender_counts = filtered["gender"].value_counts() if n > 0 else pd.Series(dtype=int)
        fig = go.Figure(
            go.Pie(
                labels=gender_counts.index,
                values=gender_counts.values,
                hole=0.52,
                marker=dict(colors=[COLORS["accent_blue"], COLORS["accent_orange"]]),
            )
        )
        fig.update_layout(**base_layout(height=340, margin=dict(l=20, r=20, t=16, b=8)))
        st.plotly_chart(fig, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='chart-card'><div class='section-title'>Age Group</div>", unsafe_allow_html=True)
    age_counts = filtered["usia_kategori"].value_counts().sort_index() if n > 0 else pd.Series(dtype=int)
    fig = go.Figure(go.Bar(x=age_counts.index, y=age_counts.values, marker_color=COLORS["accent_blue"]))
    fig.update_layout(**base_layout(height=340, showlegend=False))
    st.plotly_chart(fig, width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)

with branch_tab:
    top_bottom = filtered_cabang.dropna(subset=["NPS"]).copy()
    top15 = top_bottom.sort_values("NPS", ascending=False).head(15)
    bottom15 = top_bottom.sort_values("NPS", ascending=True).head(15)

    col_top, col_bottom = st.columns(2)
    with col_top:
        st.markdown("<div class='chart-card'><div class='section-title'>Top 15 Branches by NPS</div>", unsafe_allow_html=True)
        fig = go.Figure(go.Bar(x=top15["NPS"], y=top15["CABANG"], orientation="h", marker_color=COLORS["positive"]))
        fig.update_layout(**base_layout(height=480, showlegend=False))
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_bottom:
        st.markdown("<div class='chart-card'><div class='section-title'>Bottom 15 Branches by NPS</div>", unsafe_allow_html=True)
        fig = go.Figure(go.Bar(x=bottom15["NPS"], y=bottom15["CABANG"], orientation="h", marker_color=COLORS["accent_orange"]))
        fig.update_layout(**base_layout(height=480, showlegend=False))
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    search_branch = st.text_input("Search branch", "")
    branch_table = filtered_cabang.rename(columns={"CABANG": "Branch", "PROV": "Province"})[
        ["Branch", "Province", "n", "NPS", "CSI", "Loyalty"]
    ].copy()
    if search_branch:
        branch_table = branch_table[branch_table["Branch"].str.contains(search_branch, case=False, na=False)]
    branch_table["Loyalty"] = branch_table["Loyalty"].apply(lambda x: "N/A" if pd.isna(x) else f"{x:.2f}")
    for col in ["NPS", "CSI"]:
        branch_table[col] = branch_table[col].apply(lambda x: "N/A" if pd.isna(x) else f"{float(x):.2f}")
    branch_table["n"] = branch_table["n"].astype(int).astype(str)
    branch_table = branch_table.astype(str)
    render_html_table(branch_table, max_rows=128)

with province_tab:
    if n > 0:
        prov_summary = (
            filtered.groupby("PROV")
            .agg(
                n=("SERIAL", "count"),
                CSI=("CSI", "mean"),
                Loyalty=("Loyalty", lambda x: x.dropna().mean()),
                Operational=("touch_operasional", "mean"),
                Parking=("touch_parkir", "mean"),
                **{"Banking Hall": ("touch_banking_hall", "mean"), "Toilet": ("touch_toilet", "mean")},
            )
            .reset_index()
        )
        nps_by_prov = filtered.groupby("PROV")["NPS_kategori"].apply(
            lambda x: round(x.eq("Promoter").sum() / len(x) * 100 - x.eq("Detractor").sum() / len(x) * 100, 2)
        )
        prov_summary["NPS"] = prov_summary["PROV"].map(nps_by_prov)
    else:
        prov_summary = pd.DataFrame(columns=["PROV", "n", "CSI", "Loyalty", "Operational", "Parking", "Banking Hall", "Toilet", "NPS"])

    st.markdown("<div class='chart-card'><div class='section-title'>NPS by Province</div>", unsafe_allow_html=True)
    prov_plot = prov_summary.sort_values("NPS", ascending=True)
    bar_colors = [COLORS["positive"] if v >= 70 else COLORS["warning"] if v >= 30 else COLORS["danger"] for v in prov_plot["NPS"]]
    fig = go.Figure(go.Bar(x=prov_plot["NPS"], y=prov_plot["PROV"], orientation="h", marker_color=bar_colors))
    fig.update_layout(**base_layout(height=430, showlegend=False))
    st.plotly_chart(fig, width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='chart-card'><div class='section-title'>Province Touchpoint Heatmap</div>", unsafe_allow_html=True)
    heat_data = prov_summary.set_index("PROV")[["Operational", "Parking", "Banking Hall", "Toilet"]] if not prov_summary.empty else pd.DataFrame()
    fig = go.Figure(
        go.Heatmap(
            z=heat_data.values,
            x=heat_data.columns,
            y=heat_data.index,
            zmin=5,
            zmax=6,
            xgap=3,
            ygap=3,
            colorscale=[
                [0.00, "#F4C542"],
                [0.20, "#BFD95A"],
                [0.40, "#78C86A"],
                [0.60, "#2EB67D"],
                [0.80, "#159A7A"],
                [1.00, "#0B6E69"],
            ],
            colorbar=dict(
                title="Score",
                tickmode="array",
                tickvals=[5.0, 5.2, 5.4, 5.6, 5.8, 6.0],
                ticktext=["5.0", "5.2", "5.4", "5.6", "5.8", "6.0"],
            ),
            hovertemplate="<b>%{y}</b><br>%{x}: %{z:.2f}<extra></extra>",
        )
    )
    fig.update_layout(
        **base_layout(height=520, margin=dict(l=95, r=35, t=20, b=55), showlegend=False)
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="#FFFFFF",
        gridwidth=3,
        tickfont=dict(size=12, color=COLORS["text_secondary"]),
        side="bottom",
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#FFFFFF",
        gridwidth=3,
        tickfont=dict(size=12, color=COLORS["text_secondary"]),
    )
    st.plotly_chart(fig, width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)

    table = prov_summary.rename(columns={"PROV": "Province"})[
        ["Province", "n", "NPS", "CSI", "Loyalty", "Operational", "Parking", "Banking Hall", "Toilet"]
    ].copy()
    for col in ["NPS", "CSI", "Operational", "Parking", "Banking Hall", "Toilet"]:
        table[col] = table[col].round(2)
    table["Loyalty"] = table["Loyalty"].apply(lambda x: "N/A" if pd.isna(x) else f"{x:.2f}")
    for col in ["NPS", "CSI", "Operational", "Parking", "Banking Hall", "Toilet"]:
        table[col] = table[col].apply(lambda x: "N/A" if pd.isna(x) else f"{float(x):.2f}")
    table["n"] = table["n"].astype(int).astype(str)
    table = table.sort_values("NPS", ascending=False).astype(str)
    render_html_table(table, max_rows=30)

with ai_tab:
    selected_provinces = ", ".join(sel_prov) if sel_prov else "All provinces"
    selected_branches = ", ".join(sel_branch[:8]) + ("..." if len(sel_branch) > 8 else "") if sel_branch else "All branches"

    summary_text = f"""
Respondents: {n:,}
NPS: {nps_val:.1f}
CSI: {safe_score(csi_val)}
Loyalty: {safe_score(loyal_val)}
Service Ease: {safe_score(ease_val)}
Promoter: {pct_p:.1f}%
Passive: {pct_pa:.1f}%
Detractor: {pct_d:.1f}%
Selected provinces: {selected_provinces}
Selected branches: {selected_branches}
Selected gender: {sel_gender}
""".strip()

    st.markdown("<div class='summary-box'><div class='section-title'>Current Filtered Data Summary</div>", unsafe_allow_html=True)
    st.code(summary_text, language="text")
    st.markdown("</div>", unsafe_allow_html=True)

    question = st.text_area("Ask a question about the current filtered data", height=130)

    if st.button("Generate Insights"):
        api_key = get_anthropic_api_key()

        if not api_key:
            st.warning(
                "ANTHROPIC_API_KEY is not configured. Showing local metric-based insight instead. "
                "For full AI answers, add the key to .streamlit/secrets.toml or set it as an environment variable."
            )
            st.markdown(
                local_insight_response(
                    question,
                    n,
                    nps_val,
                    csi_val,
                    loyal_val,
                    ease_val,
                    pct_p,
                    pct_pa,
                    pct_d,
                    sel_prov,
                    sel_branch,
                    sel_gender,
                )
            )
        else:
            try:
                from anthropic import Anthropic

                client = Anthropic(api_key=api_key)
                response = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1000,
                    system=(
                        "You are a senior CX consultant for an Indonesian bank. "
                        "Answer in English. Give concise, data-driven insights with specific numbers. "
                        "Use bullet points when helpful. Max 400 words. "
                        "Only use the provided dashboard summary. Do not invent extra data."
                    ),
                    messages=[
                        {
                            "role": "user",
                            "content": f"Dashboard summary:\n{summary_text}\n\nUser question:\n{question or 'Give executive insights.'}",
                        }
                    ],
                )
                st.markdown(response.content[0].text)
            except Exception as exc:
                st.error(f"AI insight generation failed: {exc}")
                st.markdown(
                    local_insight_response(
                        question,
                        n,
                        nps_val,
                        csi_val,
                        loyal_val,
                        ease_val,
                        pct_p,
                        pct_pa,
                        pct_d,
                        sel_prov,
                        sel_branch,
                        sel_gender,
                    )
                )

# Deployment:
# Local:
#   pip install streamlit pandas plotly anthropic numpy
#   streamlit run main.py
#
# Streamlit Cloud:
#   1. Push this project to GitHub with the CSV files inside data/.
#   2. Create a new app on Streamlit Cloud.
#   3. Main file path: main.py
#   4. Add ANTHROPIC_API_KEY in App Settings > Secrets if using AI Insights.
#   5. Do not commit .streamlit/secrets.toml to GitHub.
