import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
from datetime import timedelta

st.set_page_config(
    page_title="Stock Market Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

DARK_BG       = "#0a0e0d"
PRIMARY_GREEN = "#2d5f4f"
ACCENT_GREEN  = "#3d7f6f"
LIGHT_GREEN   = "#5f9f8f"
TEXT_WHITE    = "#ffffff"
TEXT_GRAY     = "#b0b0b0"
CARD_BG       = "#1a2520"
BORDER        = "rgba(45,95,79,0.25)"

PANEL_HEIGHT_PX = 620

if "active_filters" not in st.session_state:
    st.session_state.active_filters = set()

st.markdown(f"""
<style>

*, *::before, *::after {{ box-sizing: border-box; }}
.stApp {{ background-color: {DARK_BG}; }}

[data-testid="stHorizontalBlock"] {{
    align-items: stretch !important;
    flex-wrap: nowrap !important;
    gap: 1.25rem !important;
}}

[data-testid="column"] {{
    min-width: 0 !important;
}}

.stMetric {{
    background-color: {CARD_BG} !important;
    padding: 0.9rem 1rem !important;
    border-radius: 8px !important;
    border-left: 4px solid {PRIMARY_GREEN} !important;
    height: 100% !important;
    min-width: 0 !important;
    overflow: hidden !important;
}}

.stMetric label {{
    color: {TEXT_GRAY} !important;
    font-size: clamp(0.65rem, 0.85vw, 0.82rem) !important;
    font-weight: 500 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    display: block !important;
    line-height: 1.4 !important;
    margin-bottom: 0.2rem !important;
}}

.stMetric [data-testid="stMetricValue"] {{
    color: {TEXT_WHITE} !important;
    font-size: clamp(1rem, 1.8vw, 1.55rem) !important;
    font-weight: 700 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    line-height: 1.2 !important;
    display: block !important;
}}

.stMetric [data-testid="stMetricDelta"] {{
    color: {ACCENT_GREEN} !important;
    font-size: clamp(0.65rem, 0.8vw, 0.78rem) !important;
    white-space: nowrap !important;
    margin-top: 0.2rem !important;
    display: flex !important;
    align-items: center !important;
    gap: 2px !important;
}}

.stMetric [data-testid="stMetricDelta"] svg {{
    flex-shrink: 0 !important;
    width: 14px !important;
    height: 14px !important;
}}

[data-testid="stSidebar"] {{
    background-color: {CARD_BG};
    border-right: 1px solid {PRIMARY_GREEN};
}}
[data-testid="stSidebar"] label {{ color: {TEXT_WHITE} !important; font-weight: 500; }}
[data-testid="stSidebar"] input {{
    background-color: {DARK_BG} !important;
    color: {TEXT_WHITE} !important;
    border-color: {PRIMARY_GREEN} !important;
}}
[data-testid="stSidebar"] [data-baseweb="select"] {{
    background-color: {DARK_BG} !important;
    border-color: {PRIMARY_GREEN} !important;
    border-radius: 6px !important;
}}
[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {{
    max-height: 160px !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    scrollbar-width: thin;
    scrollbar-color: {PRIMARY_GREEN} {DARK_BG};
}}
[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child::-webkit-scrollbar {{ width: 4px; }}
[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child::-webkit-scrollbar-thumb {{
    background-color: {PRIMARY_GREEN}; border-radius: 2px;
}}
[data-testid="stSidebar"] [data-baseweb="tag"] {{
    background-color: {PRIMARY_GREEN} !important;
    color: {TEXT_WHITE} !important;
    border-radius: 4px !important;
    white-space: nowrap !important;
    max-width: 130px !important;
    overflow: hidden !important;
}}
[data-baseweb="popover"] [data-baseweb="menu"] {{
    background-color: {CARD_BG} !important;
    border: 1px solid {PRIMARY_GREEN} !important;
    border-radius: 6px !important;
    max-height: 240px !important;
    overflow-y: auto !important;
}}
[data-baseweb="popover"] [role="option"] {{
    background-color: {CARD_BG} !important;
    color: {TEXT_GRAY} !important;
    font-size: 0.88rem !important;
    padding: 8px 12px !important;
}}
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [aria-selected="true"] {{
    background-color: {PRIMARY_GREEN} !important;
    color: {TEXT_WHITE} !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 6px; background-color: {CARD_BG};
    padding: 0.4rem; border-radius: 8px;
    flex-wrap: nowrap !important; overflow-x: auto; scrollbar-width: none;
}}
.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {{ display: none; }}
.stTabs [data-baseweb="tab"] {{
    background-color: transparent; color: {TEXT_GRAY};
    border-radius: 6px; padding: 0.5rem 1.1rem;
    font-weight: 500; white-space: nowrap;
    flex-shrink: 0; font-size: clamp(0.78rem, 1vw, 0.9rem);
}}
.stTabs [aria-selected="true"] {{ background-color: {PRIMARY_GREEN}; color: {TEXT_WHITE}; }}

h1, h2, h3 {{ color: {TEXT_WHITE} !important; min-width: 0; overflow: hidden; text-overflow: ellipsis; }}

.js-plotly-plot, [class*="stPlotlyChart"] {{
    min-width: 0 !important; width: 100% !important; overflow: hidden !important;
}}

.stDataFrame {{ background-color: {CARD_BG}; }}
.stDataFrame table {{ width: 100%; table-layout: fixed; text-align: center; }}
.stDataFrame th, .stDataFrame td {{
    text-align: center !important; overflow: hidden !important;
    text-overflow: ellipsis !important; white-space: nowrap !important;
}}

::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {DARK_BG}; }}
::-webkit-scrollbar-thumb {{ background-color: {PRIMARY_GREEN}; border-radius: 3px; }}

hr {{ border-color: {PRIMARY_GREEN} !important; opacity: 0.3 !important; }}
.footer {{
    text-align: center; color: {TEXT_GRAY};
    padding: 2rem 0 1rem; border-top: 1px solid {PRIMARY_GREEN};
    margin-top: 2rem; font-size: 0.88rem;
}}

.filter-badge {{
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(61,127,111,0.12);
    border: 1px solid rgba(61,127,111,0.3);
    border-radius: 6px; padding: 2px 9px;
    font-size: 0.73rem; color: {ACCENT_GREEN};
    margin-left: 8px; vertical-align: middle;
}}

</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('data/stock_data_cleaned.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    summary = pd.read_csv('data/summary_stats.csv')
    return df, summary

def plotly_theme():
    return dict(
        plot_bgcolor='rgba(15,20,18,0.8)',
        paper_bgcolor='rgba(26,37,32,0.6)',
        font=dict(color=TEXT_WHITE, family="Inter, Arial, sans-serif", size=12),
        xaxis=dict(
            gridcolor="rgba(45,95,79,0.15)", linecolor="rgba(45,95,79,0.3)",
            zerolinecolor="rgba(45,95,79,0.3)", showgrid=True, gridwidth=0.5,
            tickfont=dict(size=11, color=TEXT_GRAY), automargin=True,
        ),
        yaxis=dict(
            gridcolor="rgba(45,95,79,0.15)", linecolor="rgba(45,95,79,0.3)",
            zerolinecolor="rgba(45,95,79,0.3)", showgrid=True, gridwidth=0.5,
            tickfont=dict(size=11, color=TEXT_GRAY), automargin=True,
        ),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='rgba(26,37,32,0.95)', font_color=TEXT_WHITE,
            bordercolor=PRIMARY_GREEN, font=dict(size=12),
        ),
        margin=dict(l=70, r=40, t=80, b=70),
    )


COLOR_PALETTE = [
    "#3d7f6f", "#4fc3f7", "#ffa726", "#ab47bc",
    "#ef5350", "#ffee58", "#66bb6a", "#ec407a",
]


def build_watchlist_html(
    stocks_data: list,
    active_filters: set,
) -> str:
    """
    Build a COMPLETE HTML document for the watchlist display panel.

    RENDERING RULE (enforced here):
      Cards are rendered for EVERY stock in stocks_data — never filtered by
      active_filters. active_filters only controls the visual state (active/dimmed).
      This guarantees: adding a stock to the left multiselect → card appears
      immediately. Removing from multiselect → card disappears immediately.
      No secondary state gate between the data and the rendering.

    VISUAL STATES:
      No active filters  → all cards at full opacity
      Filter active,  IN → .is-active: accent border + subtle background
      Filter active, OUT → .is-dimmed: 38% opacity (still visible, still clickable)

    CLICK INTERACTIVITY:
      Cards do NOT handle clicks here. The click is handled by native
      st.button() elements rendered below this iframe in the right_col.
      The iframe is display-only. This design avoids all postMessage complexity.
    """
    has_filter = len(active_filters) > 0
    cards_html = ""

    for stock in stocks_data:
        name   = stock['name']
        price  = stock['price']
        ret_1y = stock['ret_1y']
        ytd    = stock['ytd']
        vol    = stock['vol']

        in_filter  = name in active_filters
        state_cls  = ""
        if has_filter:
            state_cls = "is-active" if in_filter else "is-dimmed"

        ret_cls  = "pos" if ret_1y > 0 else ("neg" if ret_1y < 0 else "neu")
        ret_sign = "+" if ret_1y > 0 else ""
        ytd_cls  = "pos" if ytd >= 0 else "neg"
        ytd_sign = "+" if ytd >= 0 else ""

        safe_name = name.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')

        cards_html += f"""<div class="card {state_cls}" data-stock="{safe_name}">
  <div class="card-top">
    <span class="card-name" title="{safe_name}">{safe_name}</span>
    <span class="card-price">${price:,.2f}</span>
  </div>
  <div class="card-bottom">
    <span class="badge {ret_cls}">1Y {ret_sign}{ret_1y:.1f}%</span>
    <span class="badge {ytd_cls}">YTD {ytd_sign}{ytd:.1f}%</span>
    <span class="card-vol">\u03c3 {vol:.2f}%</span>
  </div>
</div>"""

    count = len(stocks_data)
    filter_text = ""
    if has_filter:
        n_active = sum(1 for s in stocks_data if s['name'] in active_filters)
        filter_text = f"Filtering: {n_active} of {count}"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
:root {{
  --dark:   {DARK_BG};
  --green:  {PRIMARY_GREEN};
  --accent: {ACCENT_GREEN};
  --light:  {LIGHT_GREEN};
  --white:  {TEXT_WHITE};
  --gray:   {TEXT_GRAY};
  --bg:     {CARD_BG};
  --border: rgba(45,95,79,0.25);
  --pos:    #4ade80;
  --neg:    #f87171;
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ height: 100%; }}
body {{
  height: 100%;
  overflow: hidden;
  background: var(--bg);
  font-family: Inter, -apple-system, Arial, sans-serif;
  color: var(--white);
  font-size: 13px;
}}

.wrapper {{
  height: 100%;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}}

.hdr {{
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px 9px;
  border-bottom: 1px solid var(--border);
  gap: 6px; min-width: 0;
}}
.hdr-title {{
  font-size: 0.8rem; font-weight: 600;
  letter-spacing: 0.4px; color: var(--white); white-space: nowrap;
}}
.hdr-right {{ display: flex; align-items: center; gap: 6px; flex-shrink: 0; }}
.badge-count {{
  font-size: 0.68rem; font-weight: 500; color: var(--light);
  background: rgba(45,95,79,0.28); border-radius: 10px;
  padding: 2px 7px; white-space: nowrap;
}}
.filter-status {{
  font-size: 0.66rem; color: var(--accent);
  background: rgba(61,127,111,0.12);
  border: 1px solid rgba(61,127,111,0.25);
  border-radius: 4px; padding: 2px 6px;
  white-space: nowrap;
  display: {"flex" if filter_text else "none"};
  align-items: center; gap: 4px;
}}
.filter-dot {{
  width: 5px; height: 5px; border-radius: 50%;
  background: var(--accent); flex-shrink: 0;
  animation: pulse 2s ease-in-out infinite;
}}
@keyframes pulse {{
  0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.35; }}
}}

.search-wrap {{
  flex-shrink: 0;
  padding: 7px 10px;
  border-bottom: 1px solid var(--border);
  position: relative;
}}
.search-icon {{
  position: absolute; left: 20px; top: 50%;
  transform: translateY(-50%);
  color: var(--gray); pointer-events: none;
  font-size: 0.8rem; opacity: 0.6; user-select: none;
}}
.search-input {{
  width: 100%;
  background: rgba(10,14,13,0.85);
  border: 1px solid var(--green);
  border-radius: 6px;
  padding: 6px 10px 6px 26px;
  color: var(--white); font-size: 0.77rem;
  outline: none; caret-color: var(--accent);
  transition: border-color 0.16s, box-shadow 0.16s;
}}
.search-input:focus {{
  border-color: var(--accent);
  box-shadow: 0 0 0 2px rgba(61,127,111,0.18);
}}
.search-input::placeholder {{ color: rgba(176,176,176,0.4); }}

.list {{
  flex: 1;            
  overflow-y: auto;  
  min-height: 0;     
  overflow-x: hidden;
  padding: 5px 0 4px;
  scrollbar-width: thin;
  scrollbar-color: var(--green) transparent;
}}
.list::-webkit-scrollbar {{ width: 4px; }}
.list::-webkit-scrollbar-thumb {{ background: var(--green); border-radius: 2px; }}

.no-results {{
  display: none;
  padding: 20px 12px;
  text-align: center;
  color: var(--gray);
  font-size: 0.77rem;
  opacity: 0.75;
}}

.card {{
  padding: 7px 11px;
  margin: 0 7px 4px;
  border-radius: 7px;
  background: rgba(10,14,13,0.45);
  border: 1px solid transparent;
  border-left: 3px solid transparent;
  overflow: hidden; min-width: 0;
  cursor: default;
  transition: background 0.14s, border-color 0.14s, opacity 0.14s;
}}

.card.is-active {{
  background: rgba(61,127,111,0.12);
  border-left-color: var(--accent);
  border-color: rgba(61,127,111,0.25);
}}

.card.is-dimmed {{ opacity: 0.35; }}

.card-top {{
  display: flex; align-items: center;
  justify-content: space-between;
  gap: 6px; min-width: 0; margin-bottom: 4px;
}}
.card-name {{
  font-size: 0.79rem; font-weight: 600; color: var(--white);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  flex: 1; min-width: 0;
}}
.card-price {{
  font-size: 0.79rem; font-weight: 700; color: var(--white);
  white-space: nowrap; flex-shrink: 0;
}}

.card-bottom {{
  display: flex; align-items: center;
  gap: 4px; min-width: 0; flex-wrap: nowrap;
}}

.badge {{
  font-size: 0.64rem; font-weight: 600;
  white-space: nowrap; padding: 1px 5px;
  border-radius: 4px; flex-shrink: 0;
}}

.pos {{ color: var(--pos); background: rgba(74,222,128,0.1); }}
.neg {{ color: var(--neg); background: rgba(248,113,113,0.1); }}
.neu {{ color: var(--gray); background: rgba(176,176,176,0.1); }}
.card-vol {{
  font-size: 0.62rem; color: var(--gray);
  white-space: nowrap; overflow: hidden;
  text-overflow: ellipsis; flex: 1; min-width: 0; opacity: 0.8;
}}
</style>
</head>
<body>

<div class="wrapper">

  <!-- HEADER -->
  <div class="hdr">
    <span class="hdr-title">Watchlist</span>
    <div class="hdr-right">
      <span class="badge-count" id="stockCount">{count} stock{'s' if count != 1 else ''}</span>
      <div class="filter-status" id="filterStatus">
        <div class="filter-dot"></div>
        <span>{filter_text}</span>
      </div>
    </div>
  </div>

  <!-- SEARCH: inline filter — JS toggles display:none on cards -->
  <!-- Does NOT use dropdown — no absolute positioning, no overflow conflict -->
  <div class="search-wrap">
    <i class="search-icon">&#x2315;</i>
    <input
      id="searchInput"
      class="search-input"
      type="text"
      placeholder="Search watchlist&#x2026;"
      oninput="applySearch(this.value)"
      autocomplete="off"
      spellcheck="false"
    />
  </div>

  <!-- CARD LIST — THE SCROLL CONTAINER                                    -->
  <!-- flex:1 + overflow-y:auto + min-height:0 = Three Laws satisfied      -->
  <!-- Cards are pre-rendered from Python — no JS protocol needed          -->
  <div class="list" id="cardList">
    {cards_html}
    <div class="no-results" id="noResults">No stocks match your search</div>
  </div>

</div>

<script>
// Search: toggle display on cards — no DOM removal (avoids parent reflow)
// data-stock is pre-lowercased at render time for O(1) comparison
function applySearch(query) {{
  var q = query.toLowerCase().trim();
  var cards = document.querySelectorAll('#cardList .card');
  var visible = 0;
  for (var i = 0; i < cards.length; i++) {{
    var name = (cards[i].getAttribute('data-stock') || '').toLowerCase();
    var show = !q || name.indexOf(q) !== -1;
    cards[i].style.display = show ? '' : 'none';
    if (show) visible++;
  }}
  document.getElementById('stockCount').textContent =
    visible + ' stock' + (visible !== 1 ? 's' : '');
  document.getElementById('noResults').style.display =
    visible === 0 ? 'block' : 'none';
}}
</script>

</body>
</html>"""






def main():
    df, summary = load_data()

    st.sidebar.markdown(f"""
        <div style='text-align:center;padding:2rem 0.5rem 1.5rem;margin-bottom:1.5rem;
                    border-bottom:1px solid rgba(45,95,79,0.3);'>
            <h2 style='color:{ACCENT_GREEN};margin:0;font-size:1.1rem;font-weight:600;
                       letter-spacing:2px;'>STOCK MARKET</h2>
            <p style='color:{LIGHT_GREEN};margin:0.3rem 0 0;font-size:0.75rem;
                      letter-spacing:1px;'>ANALYSIS DASHBOARD</p>
        </div>
    """, unsafe_allow_html=True)

    min_date = df['Date'].min()
    max_date = df['Date'].max()

    st.sidebar.markdown(
        f"<p style='color:{LIGHT_GREEN};font-size:0.85rem;font-weight:600;"
        "margin-bottom:0.5rem;'>Time Period</p>", unsafe_allow_html=True,
    )
    date_range = st.sidebar.date_input(
        "date_range",
        value=(max_date - timedelta(days=365), max_date),
        min_value=min_date, max_value=max_date,
        label_visibility="collapsed",
    )

    st.sidebar.markdown("<div style='margin:1.5rem 0 0.25rem;'></div>",
                        unsafe_allow_html=True)

    all_stocks = sorted(df['Company'].unique().tolist())

    st.sidebar.markdown(
        f"<p style='color:{LIGHT_GREEN};font-size:0.85rem;font-weight:600;"
        "margin-bottom:0.25rem;'>Choose Stocks to Watch</p>"
        f"<p style='color:#6a8f87;font-size:0.74rem;margin-bottom:0.4rem;'>"
        "Type to search • Click buttons below to filter charts</p>",
        unsafe_allow_html=True,
    )

    selected_stocks = st.sidebar.multiselect(
        "stocks",
        options=all_stocks,
        default=['Apple', 'Microsoft', 'NVIDIA', 'S&P 500'],
        label_visibility="collapsed",
        placeholder="Search stocks…",
    )

    if not selected_stocks:
        st.sidebar.warning("Select at least one stock to begin.")
        st.info("Use the sidebar to select stocks for analysis.")
        return

    st.session_state.active_filters = {
        f for f in st.session_state.active_filters
        if f in selected_stocks           
    }
    active_filters = st.session_state.active_filters  

    if active_filters:
        display_stocks = [s for s in selected_stocks if s in active_filters]
    else:
        display_stocks = list(selected_stocks)

    if len(date_range) == 2:
        mask = (
            (df['Date'] >= pd.to_datetime(date_range[0])) &
            (df['Date'] <= pd.to_datetime(date_range[1]))
        )
        filtered_df = df[mask]
    else:
        filtered_df = df

    all_selected_df = filtered_df[filtered_df['Company'].isin(selected_stocks)]
    display_df = filtered_df[filtered_df['Company'].isin(display_stocks)]

    filter_badge = ""
    if active_filters:
        filter_badge = (
            f"<span class='filter-badge'>"
            f"&#x25CF; Filtering: {len(active_filters)} of {len(selected_stocks)}"
            f"</span>"
        )

    st.markdown(
        f"<h3 style='margin:0 0 0.75rem;font-size:1.1rem;'>"
        f"Key Performance Indicators{filter_badge}</h3>",
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4 = st.columns(4, gap="medium")

    best = summary.nlargest(1, '1Y_Return_%').iloc[0]
    with k1:
        st.metric("Best Performer This Year",
                  best['Company'], f"{best['1Y_Return_%']:.2f}%")

    tech_avg = summary[summary['Ticker'] != '^GSPC']['1Y_Return_%'].mean()
    with k2:
        st.metric("Avg Tech Growth (1Y)", f"{tech_avg:.2f}%")

    sp500 = summary[summary['Ticker'] == '^GSPC']
    with k3:
        val = f"{sp500.iloc[0]['1Y_Return_%']:.2f}%" if not sp500.empty else "N/A"
        st.metric("S&P 500 Benchmark", val)

    most_vol = summary.nlargest(1, '30D_Volatility_%').iloc[0]
    with k4:
        st.metric("Highest Volatility (30D)",
                  most_vol['Company'], f"{most_vol['30D_Volatility_%']:.2f}%")

    st.markdown("---")


    left_col, right_col = st.columns([3, 1], gap="medium")


    with left_col:
        if active_filters:
            section_label = (
                f"<h3 style='margin:0 0 0.5rem;font-size:1.05rem;'>"
                f"Detailed Analysis "
                f"<span style='font-size:0.74rem;font-weight:400;color:{LIGHT_GREEN};'>"
                f"({len(display_stocks)} stock{'s' if len(display_stocks) != 1 else ''} shown)"
                f"</span></h3>"
            )
        else:
            section_label = "<h3 style='margin:0 0 0.5rem;font-size:1.05rem;'>Detailed Analysis</h3>"
        st.markdown(section_label, unsafe_allow_html=True)

        tab1, tab2, tab3, tab4 = st.tabs(
            ["Total Gains", "Price History", "Trading Activity", "Price Swings"]
        )

        with tab1:
            fig = go.Figure()
            for idx, company in enumerate(display_stocks):
                cdata = display_df[display_df['Company'] == company]
                clr = COLOR_PALETTE[idx % len(COLOR_PALETTE)]
                r, g, b = int(clr[1:3], 16), int(clr[3:5], 16), int(clr[5:7], 16)
                fig.add_trace(go.Scatter(
                    x=cdata['Date'], y=cdata['Cumulative_Return'],
                    mode='lines', name=company,
                    line=dict(width=2, color=clr),
                    fill='tonexty' if idx > 0 else 'tozeroy',
                    fillcolor=f"rgba({r},{g},{b},0.1)",
                    hovertemplate='<b>%{fullData.name}</b><br>%{y:.2f}%<extra></extra>',
                ))
            fig.update_layout(
                **plotly_theme(),
                title=dict(text="<b>Total Gains</b>",
                           font=dict(size=16, color=TEXT_WHITE), x=0.02),
                xaxis_title="", yaxis_title="Return (%)",
                height=480, showlegend=True,
                legend=dict(orientation="h", yanchor="top", y=-0.18,
                            xanchor="left", x=0, bgcolor='rgba(0,0,0,0)',
                            font=dict(size=11)),
            )
            fig.add_hline(y=0, line_dash="dash",
                          line_color="rgba(176,176,176,0.3)", line_width=1)
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.markdown(
                f"<p style='color:{TEXT_GRAY};font-size:0.88rem;margin-bottom:0.75rem;'>"
                "Select a stock for detailed technical analysis</p>",
                unsafe_allow_html=True,
            )
            sel_co = st.selectbox(
                "company_select", display_stocks, label_visibility="collapsed"
            )
            cdata = display_df[display_df['Company'] == sel_co]
            fig2  = go.Figure()
            fig2.add_trace(go.Scatter(
                x=cdata['Date'], y=cdata['MA_200'], mode='lines',
                name='200-Day MA',
                line=dict(color='rgba(239,83,80,0.6)', width=1.5, dash='dot'),
                hovertemplate='200-MA: $%{y:,.2f}<extra></extra>',
            ))
            fig2.add_trace(go.Scatter(
                x=cdata['Date'], y=cdata['MA_50'], mode='lines',
                name='50-Day MA',
                line=dict(color='rgba(95,159,143,0.8)', width=1.5, dash='dash'),
                hovertemplate='50-MA: $%{y:,.2f}<extra></extra>',
            ))
            fig2.add_trace(go.Scatter(
                x=cdata['Date'], y=cdata['Close'], mode='lines',
                name='Price', line=dict(color=ACCENT_GREEN, width=2.5),
                fill='tozeroy', fillcolor='rgba(61,127,111,0.08)',
                hovertemplate='<b>$%{y:,.2f}</b><extra></extra>',
            ))
            fig2.update_layout(
                **plotly_theme(),
                title=dict(text=f"<b>{sel_co}</b> — Price Action",
                           font=dict(size=16, color=TEXT_WHITE), x=0.02),
                xaxis_title="", yaxis_title="Price (USD)",
                height=480, showlegend=True,
                legend=dict(orientation="h", yanchor="top", y=-0.18,
                            xanchor="left", x=0, bgcolor='rgba(0,0,0,0)',
                            font=dict(size=11)),
            )
            st.plotly_chart(fig2, use_container_width=True)

        with tab3:
            fig3 = go.Figure()
            for idx, company in enumerate(display_stocks):
                cdata = display_df[display_df['Company'] == company]
                fig3.add_trace(go.Bar(
                    x=cdata['Date'], y=cdata['Volume'], name=company,
                    marker=dict(color=COLOR_PALETTE[idx % len(COLOR_PALETTE)],
                                opacity=0.85, line=dict(width=0)),
                    hovertemplate='<b>%{fullData.name}</b><br>%{y:,.0f}<extra></extra>',
                ))
            fig3.update_layout(
                **plotly_theme(),
                title=dict(text="<b>Trading Volume</b>",
                           font=dict(size=16, color=TEXT_WHITE), x=0.02),
                xaxis_title="", yaxis_title="Volume",
                barmode='group', bargap=0.2, height=480, showlegend=True,
                legend=dict(orientation="h", yanchor="top", y=-0.18,
                            xanchor="left", x=0, bgcolor='rgba(0,0,0,0)',
                            font=dict(size=11)),
            )
            st.plotly_chart(fig3, use_container_width=True)

        with tab4:
            fig4 = go.Figure()
            for idx, company in enumerate(display_stocks):
                cdata = display_df[display_df['Company'] == company]
                fig4.add_trace(go.Scatter(
                    x=cdata['Date'], y=cdata['Volatility_30D'],
                    mode='lines', name=company,
                    line=dict(width=2,
                              color=COLOR_PALETTE[idx % len(COLOR_PALETTE)],
                              shape='spline'),
                    hovertemplate='<b>%{fullData.name}</b><br>%{y:.2f}%<extra></extra>',
                ))
            fig4.update_layout(
                **plotly_theme(),
                title=dict(text="<b>30-Day Volatility</b>",
                           font=dict(size=16, color=TEXT_WHITE), x=0.02),
                xaxis_title="", yaxis_title="Volatility (%)",
                height=480, showlegend=True,
                legend=dict(orientation="h", yanchor="top", y=-0.18,
                            xanchor="left", x=0, bgcolor='rgba(0,0,0,0)',
                            font=dict(size=11)),
            )
            st.plotly_chart(fig4, use_container_width=True)

    with right_col:
        stocks_data = []
        for company in selected_stocks:
            row = summary[summary['Company'] == company]
            if not row.empty:
                r = row.iloc[0]
                stocks_data.append({
                    'name':   company,
                    'price':  float(r['Latest_Price']),
                    'ret_1y': float(r['1Y_Return_%']),
                    'ytd':    float(r['YTD_Return_%']),
                    'vol':    float(r['30D_Volatility_%']),
                })

        watchlist_html = build_watchlist_html(stocks_data, active_filters)
        components.html(watchlist_html, height=PANEL_HEIGHT_PX, scrolling=False)

    st.markdown("---")
    filtered_label = (
        f" <span style='font-size:0.8rem;font-weight:400;color:{LIGHT_GREEN};'>"
        f"(filtered view)</span>"
        if active_filters else ""
    )
    st.markdown(
        f"<h2 style='font-size:1.1rem;margin-bottom:0.75rem;'>"
        f"Summary Stats{filtered_label}</h2>",
        unsafe_allow_html=True,
    )

    disp = (
        summary[summary['Company'].isin(display_stocks)]
        .copy()
        .sort_values('1Y_Return_%', ascending=False)
        .rename(columns={
            'Latest_Price':     'Price',
            'YTD_Return_%':     'YTD %',
            '1Y_Return_%':      '1Y Return %',
            '30D_Volatility_%': 'Volatility %',
            'Avg_Volume':       'Avg Volume',
            'Latest_Date':      'Updated',
        })
        .drop(columns=['Ticker'])
        [['Company', 'Price', 'YTD %', '1Y Return %', 'Volatility %', 'Avg Volume', 'Updated']]
    )
    disp['Price']        = disp['Price'].apply(lambda x: f'${x:,.2f}')
    disp['YTD %']        = disp['YTD %'].apply(lambda x: f'{x:+.2f}%')
    disp['1Y Return %']  = disp['1Y Return %'].apply(lambda x: f'{x:+.2f}%')
    disp['Volatility %'] = disp['Volatility %'].apply(lambda x: f'{x:.2f}%')
    disp['Avg Volume']   = disp['Avg Volume'].apply(lambda x: f'{x:,.0f}')

    st.dataframe(
        disp, use_container_width=True, hide_index=True,
        column_config={
            'Company':      st.column_config.TextColumn('Company',      width='medium'),
            'Price':        st.column_config.TextColumn('Price',        width='small'),
            'YTD %':        st.column_config.TextColumn('YTD %',        width='small'),
            '1Y Return %':  st.column_config.TextColumn('1Y Return %',  width='small'),
            'Volatility %': st.column_config.TextColumn('Volatility %', width='small'),
            'Avg Volume':   st.column_config.TextColumn('Avg Volume',   width='medium'),
            'Updated':      st.column_config.TextColumn('Updated',      width='small'),
        },
    )

    st.markdown(f"""
    <div class="footer">
        Data Source: Yahoo Finance &nbsp;|&nbsp;
        Last Updated: {df['Date'].max().strftime('%Y-%m-%d')}
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()