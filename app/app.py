import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Falcon 9 Launch Economics — Project Alpha",
    page_icon="🛰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── DESIGN SYSTEM ──────────────────────────────────────────────────────────────
# Palette: deep space navy + cold white + electric cyan accent + amber warning
COLORS = {
    'bg':        '#04070F',
    'surface':   '#080E1C',
    'border':    '#112240',
    'border2':   '#1E3A5F',
    'text':      '#C8D8E8',
    'muted':     '#5A7A9A',
    'accent':    '#00D4FF',
    'accent2':   '#0099CC',
    'amber':     '#F5A623',
    'red':       '#E84040',
    'green':     '#1FD0A0',
    'white':     '#EEF4FA',
}

PLOTLY_LAYOUT = dict(
    plot_bgcolor=COLORS['bg'],
    paper_bgcolor=COLORS['surface'],
    font=dict(color=COLORS['text'], family='monospace', size=12),
    margin=dict(l=50, r=30, t=50, b=50),
    xaxis=dict(
        gridcolor='rgba(17,34,64,0.8)',
        linecolor=COLORS['border2'],
        tickfont=dict(color=COLORS['muted'], size=11),
        zerolinecolor=COLORS['border2'],
    ),
    yaxis=dict(
        gridcolor='rgba(17,34,64,0.8)',
        linecolor=COLORS['border2'],
        tickfont=dict(color=COLORS['muted'], size=11),
        zerolinecolor=COLORS['border2'],
    ),
    legend=dict(
        bgcolor='rgba(8,14,28,0.9)',
        bordercolor=COLORS['border2'],
        borderwidth=1,
        font=dict(color=COLORS['text'], size=11),
    ),
    hoverlabel=dict(
        bgcolor=COLORS['surface'],
        bordercolor=COLORS['accent'],
        font=dict(color=COLORS['white'], size=12, family='monospace'),
    ),
    hovermode='x unified',
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;500;600;700;800&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}

.stApp {{
    background: {COLORS['bg']};
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(0,180,255,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(0,212,255,0.04) 0%, transparent 50%);
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: {COLORS['surface']} !important;
    border-right: 1px solid {COLORS['border']} !important;
}}
[data-testid="stSidebar"] > div:first-child {{
    padding-top: 0;
}}

/* All headings */
h1, h2, h3, h4, h5, h6 {{
    font-family: 'Syne', sans-serif !important;
    color: {COLORS['white']} !important;
    letter-spacing: -0.02em;
}}

/* Body text */
p, li, span, div, label {{
    font-family: 'Space Mono', monospace !important;
    color: {COLORS['text']};
    font-size: 12px;
}}

/* Metrics */
[data-testid="stMetric"] {{
    background: {COLORS['surface']} !important;
    border: 1px solid {COLORS['border2']} !important;
    border-top: 2px solid {COLORS['accent']} !important;
    border-radius: 2px !important;
    padding: 16px 20px !important;
}}
[data-testid="stMetricLabel"] {{
    font-family: 'Space Mono', monospace !important;
    font-size: 10px !important;
    color: {COLORS['muted']} !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
}}
[data-testid="stMetricValue"] {{
    font-family: 'Syne', sans-serif !important;
    font-size: 26px !important;
    font-weight: 700 !important;
    color: {COLORS['white']} !important;
}}
[data-testid="stMetricDelta"] {{
    font-family: 'Space Mono', monospace !important;
    font-size: 10px !important;
}}

/* Tabs */
[data-baseweb="tab-list"] {{
    background: transparent !important;
    border-bottom: 1px solid {COLORS['border2']} !important;
    gap: 0 !important;
}}
[data-baseweb="tab"] {{
    font-family: 'Space Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: {COLORS['muted']} !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 12px 20px !important;
    margin-right: 0 !important;
}}
[aria-selected="true"][data-baseweb="tab"] {{
    color: {COLORS['accent']} !important;
    border-bottom: 2px solid {COLORS['accent']} !important;
    background: rgba(0,212,255,0.04) !important;
}}

/* Sliders */
[data-testid="stSlider"] > div > div > div > div {{
    background: {COLORS['accent']} !important;
}}

/* Selectbox */
[data-baseweb="select"] > div {{
    background: {COLORS['surface']} !important;
    border: 1px solid {COLORS['border2']} !important;
    border-radius: 2px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    color: {COLORS['text']} !important;
}}

/* Buttons */
.stButton > button {{
    background: transparent !important;
    border: 1px solid {COLORS['accent']} !important;
    color: {COLORS['accent']} !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border-radius: 2px !important;
    transition: all 0.2s ease !important;
}}
.stButton > button:hover {{
    background: rgba(0,212,255,0.1) !important;
}}

/* Radio */
[data-baseweb="radio"] span {{
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    color: {COLORS['text']} !important;
}}

/* Divider */
hr {{
    border: none !important;
    border-top: 1px solid {COLORS['border']} !important;
    margin: 24px 0 !important;
}}

/* Scrollbar */
::-webkit-scrollbar {{ width: 6px; background: {COLORS['bg']}; }}
::-webkit-scrollbar-thumb {{ background: {COLORS['border2']}; border-radius: 3px; }}

/* Multiselect */
[data-baseweb="tag"] {{
    background: rgba(0,212,255,0.15) !important;
    border: 1px solid {COLORS['accent2']} !important;
}}

/* Alert/info boxes */
[data-testid="stAlert"] {{
    background: rgba(0,212,255,0.06) !important;
    border: 1px solid {COLORS['border2']} !important;
    border-left: 3px solid {COLORS['accent']} !important;
    border-radius: 2px !important;
    font-family: 'Space Mono', monospace !important;
}}
</style>
""", unsafe_allow_html=True)


# ── DATA LOADING ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    import os
    from pathlib import Path
    paths = [
        'data/spacex_raw.csv',
        '../data/spacex_raw.csv',
        'launch-economics/data/spacex_raw.csv',
        str(Path(__file__).parent.parent / 'data' / 'spacex_raw.csv'),
    ]
    for path in paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
    st.error("Data file not found. Please ensure 'data/spacex_raw.csv' exists.")
    st.stop()

df = load_data()


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
st.sidebar.markdown(f"""
<div style="padding: 24px 16px 16px; border-bottom: 1px solid {COLORS['border']}; margin-bottom: 20px;">
    <div style="font-family: 'Space Mono', monospace; font-size: 9px; color: {COLORS['muted']};
                letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 6px;">
        Project Alpha / 2026
    </div>
    <div style="font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 800;
                color: {COLORS['white']}; line-height: 1.1; margin-bottom: 4px;">
        Launch<br>Economics
    </div>
    <div style="font-family: 'Space Mono', monospace; font-size: 10px; color: {COLORS['accent']};
                letter-spacing: 0.05em;">
        Falcon 9 · 2010–2021
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div style="font-family: 'Space Mono', monospace; font-size: 9px; color: {COLORS['muted']};
            letter-spacing: 0.15em; text-transform: uppercase; padding: 0 4px; margin-bottom: 8px;">
    Filters
</div>
""", unsafe_allow_html=True)

year_range = st.sidebar.slider(
    "Year range",
    min_value=int(df['Year'].min()),
    max_value=int(df['Year'].max()),
    value=(2015, 2021),
)

selected_orbits = st.sidebar.multiselect(
    "Orbit type",
    options=sorted(df['Orbit'].unique()),
    default=sorted(df['Orbit'].unique()),
)

reused_filter = st.sidebar.radio(
    "Booster configuration",
    options=["All", "New only", "Reused only"],
    index=0,
)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown(f"""
<div style="font-family: 'Space Mono', monospace; font-size: 10px;
            color: {COLORS['muted']}; line-height: 1.8; padding: 0 4px;">
    Booster reusability analysis across {len(df)} launches.<br>
    Dataset: IBM / Coursera Applied Data Science Capstone.
</div>
""", unsafe_allow_html=True)

# Apply filters
filtered_df = df[
    (df['Year'] >= year_range[0]) &
    (df['Year'] <= year_range[1]) &
    (df['Orbit'].isin(selected_orbits))
].copy()
if reused_filter == "New only":
    filtered_df = filtered_df[filtered_df['Reused'] == False]
elif reused_filter == "Reused only":
    filtered_df = filtered_df[filtered_df['Reused'] == True]


# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="padding: 40px 0 32px; border-bottom: 1px solid {COLORS['border']}; margin-bottom: 32px;">
    <div style="font-family: 'Space Mono', monospace; font-size: 9px; color: {COLORS['accent']};
                letter-spacing: 0.25em; text-transform: uppercase; margin-bottom: 10px;">
        Aerospace Systems Analysis · SpaceX Falcon 9
    </div>
    <h1 style="font-family: 'Syne', sans-serif !important; font-size: 42px !important;
               font-weight: 800 !important; color: {COLORS['white']} !important;
               line-height: 1.0 !important; margin: 0 0 12px !important; letter-spacing: -0.03em;">
        Launch Cost Reduction<br>Through Booster Reusability
    </h1>
    <p style="font-family: 'Space Mono', monospace; font-size: 11px; color: {COLORS['muted']};
              letter-spacing: 0.05em; margin: 0; max-width: 600px; line-height: 1.8;">
        Quantitative analysis of operational economics across 91 missions (2010–2021).
        Examines cost-per-kilogram trajectories, success rate convergence, and
        predictive modeling of booster landing outcomes.
    </p>
</div>
""", unsafe_allow_html=True)


# ── KPI METRICS ────────────────────────────────────────────────────────────────
n = len(filtered_df)
success_rate = filtered_df['Success'].mean() * 100 if n > 0 else 0
reused_n = int(filtered_df['Reused'].sum()) if n > 0 else 0
avg_cost = filtered_df['CostPerKg'].mean() if n > 0 else 0
total_savings = (filtered_df['CompetitorCost'] - filtered_df['EstimatedCost']).sum() if n > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total missions", f"{n}", delta=f"{year_range[0]}–{year_range[1]}")
col2.metric("Success rate", f"{success_rate:.1f}%", delta=f"{int(filtered_df['Success'].sum())} successful" if n > 0 else "—")
col3.metric("Reused boosters", f"{reused_n}", delta=f"{reused_n/n*100:.0f}% of set" if n > 0 else "—")
col4.metric("Avg cost / kg", f"${avg_cost:,.0f}", delta=f"vs ${165_000_000 / filtered_df['PayloadMass'].mean():,.0f} competitor" if n > 0 else "—")
col5.metric("Cumulative savings", f"${total_savings:.0f}M", delta="vs. expendable baseline")

st.markdown("<hr>", unsafe_allow_html=True)


# ── TABS ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "01 / Temporal Analysis",
    "02 / Cost Dynamics",
    "03 / Reusability Economics",
    "04 / Orbital Performance",
    "05 / Predictive Model"
])


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — TEMPORAL ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown(f"""
    <div style="margin: 24px 0 20px;">
        <div style="font-family:'Space Mono',monospace; font-size:9px; color:{COLORS['accent']};
                    letter-spacing:0.2em; text-transform:uppercase; margin-bottom:6px;">Section 01</div>
        <h2 style="font-family:'Syne',sans-serif !important; font-size:22px !important;
                   font-weight:700 !important; color:{COLORS['white']} !important; margin:0 !important;">
            Launch Cadence &amp; Success Rate Progression
        </h2>
    </div>
    """, unsafe_allow_html=True)

    yearly = filtered_df.groupby('Year').agg(
        Launches=('FlightNumber', 'count'),
        SuccessRate=('Success', 'mean'),
        ReusedCount=('Reused', 'sum')
    ).reset_index()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=yearly['Year'], y=yearly['Launches'],
        name='Missions',
        marker_color=COLORS['border2'],
        marker_line_color=COLORS['accent2'],
        marker_line_width=1,
        opacity=0.9,
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=yearly['Year'], y=yearly['SuccessRate'] * 100,
        name='Success rate (%)',
        mode='lines+markers',
        line=dict(color=COLORS['accent'], width=2.5),
        marker=dict(size=7, color=COLORS['accent'], line=dict(color=COLORS['bg'], width=2)),
    ), secondary_y=True)

    fig.update_layout(**PLOTLY_LAYOUT,
        title=dict(text='Annual mission volume and booster landing success rate', x=0,
                   font=dict(color=COLORS['muted'], size=11, family='Space Mono')),
        height=380,
        showlegend=True,
    )
    fig.update_yaxes(title_text='Mission count', secondary_y=False,
                     title_font=dict(color=COLORS['muted'], size=10, family='Space Mono'))
    fig.update_yaxes(title_text='Success rate (%)', secondary_y=True,
                     range=[0, 105],
                     title_font=dict(color=COLORS['muted'], size=10, family='Space Mono'))
    st.plotly_chart(fig, use_container_width=True)

    col_a, col_b = st.columns([3, 2])
    with col_a:
        # Quarterly heatmap
        quarterly = filtered_df.groupby(['Year', 'Quarter']).size().reset_index(name='Count')
        pivot = quarterly.pivot(index='Quarter', columns='Year', values='Count').fillna(0)
        fig_h = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns.astype(str),
            y=[f'Q{q}' for q in pivot.index],
            colorscale=[[0, COLORS['surface']], [0.3, COLORS['border2']],
                        [0.7, COLORS['accent2']], [1, COLORS['accent']]],
            showscale=True,
            text=pivot.values.astype(int),
            texttemplate='%{text}',
            textfont=dict(size=11, color=COLORS['white']),
            hoverongaps=False,
        ))
        fig_h.update_layout(**PLOTLY_LAYOUT,
            title=dict(text='Quarterly mission distribution', x=0,
                       font=dict(color=COLORS['muted'], size=11, family='Space Mono')),
            height=260,
            xaxis=dict(side='bottom'),
        )
        st.plotly_chart(fig_h, use_container_width=True)

    with col_b:
        st.markdown(f"""
        <div style="background:{COLORS['surface']}; border:1px solid {COLORS['border2']};
                    border-left:3px solid {COLORS['accent']}; padding:20px 18px;
                    margin-top:0; font-family:'Space Mono',monospace;">
            <div style="font-size:9px; color:{COLORS['accent']}; letter-spacing:0.15em;
                        text-transform:uppercase; margin-bottom:12px;">Key observations</div>
            <div style="font-size:11px; color:{COLORS['text']}; line-height:2.0;">
                <span style="color:{COLORS['muted']}">2013–2015</span> &mdash; Early operational phase.
                Success rates below 50%. Iterative hardware refinement.<br><br>
                <span style="color:{COLORS['muted']}">2016–2018</span> &mdash; Block 4/5 transition.
                First booster recoveries. Reliability exceeds 90%.<br><br>
                <span style="color:{COLORS['muted']}">2019–2021</span> &mdash; Constellation deployment era.
                Launch frequency triples. Near-unity landing success.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — COST DYNAMICS
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown(f"""
    <div style="margin: 24px 0 20px;">
        <div style="font-family:'Space Mono',monospace; font-size:9px; color:{COLORS['accent']};
                    letter-spacing:0.2em; text-transform:uppercase; margin-bottom:6px;">Section 02</div>
        <h2 style="font-family:'Syne',sans-serif !important; font-size:22px !important;
                   font-weight:700 !important; color:{COLORS['white']} !important; margin:0 !important;">
            Cost-Per-Kilogram Dynamics
        </h2>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])
    with col_a:
        fig_scatter = px.scatter(
            filtered_df, x='DaysSinceFirst', y='CostPerKg',
            color='Success',
            size='PayloadMass',
            size_max=18,
            hover_data=['FlightNumber', 'Orbit', 'Reused', 'ReusedCount'],
            color_continuous_scale=[[0, COLORS['red']], [1, COLORS['green']]],
            labels={'DaysSinceFirst': 'Days since first launch',
                    'CostPerKg': 'Cost per kg (USD)',
                    'Success': 'Landing success'}
        )
        # Polynomial trend
        mask = filtered_df[['DaysSinceFirst', 'CostPerKg']].dropna()
        if len(mask) > 5:
            z = np.polyfit(mask['DaysSinceFirst'], mask['CostPerKg'], 2)
            p = np.poly1d(z)
            xr = np.linspace(mask['DaysSinceFirst'].min(), mask['DaysSinceFirst'].max(), 200)
            fig_scatter.add_trace(go.Scatter(
                x=xr, y=p(xr),
                mode='lines',
                line=dict(color=COLORS['amber'], width=2, dash='dot'),
                name='Polynomial trend',
                showlegend=True
            ))
        fig_scatter.update_layout(**PLOTLY_LAYOUT,
            title=dict(text='Cost-per-kg decline over operational lifetime (bubble size = payload mass)', x=0,
                       font=dict(color=COLORS['muted'], size=11, family='Space Mono')),
            height=400,
            coloraxis_colorbar=dict(
                title=dict(text='Success', font=dict(color=COLORS['muted'], size=10)),
                tickfont=dict(color=COLORS['muted'], size=9),
                tickvals=[0, 1], ticktext=['Failure', 'Success'],
            )
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_b:
        new_cost = filtered_df[filtered_df['Reused'] == False]['CostPerKg'].mean() if len(filtered_df[filtered_df['Reused'] == False]) > 0 else 0
        reused_cost = filtered_df[filtered_df['Reused'] == True]['CostPerKg'].mean() if len(filtered_df[filtered_df['Reused'] == True]) > 0 else 0
        competitor_cost = 165_000_000 / filtered_df['PayloadMass'].mean() if n > 0 else 0
        reduction = (new_cost - reused_cost) / new_cost * 100 if new_cost > 0 else 0
        vs_comp = (competitor_cost - reused_cost) / competitor_cost * 100 if competitor_cost > 0 else 0

        st.markdown(f"""
        <div style="background:{COLORS['surface']}; border:1px solid {COLORS['border2']};
                    padding:22px 18px; font-family:'Space Mono',monospace; margin-bottom:16px;">
            <div style="font-size:9px; color:{COLORS['accent']}; letter-spacing:0.15em;
                        text-transform:uppercase; margin-bottom:16px;">Cost benchmarking (USD/kg)</div>
            <div style="display:flex; flex-direction:column; gap:12px;">
                <div>
                    <div style="font-size:9px; color:{COLORS['muted']}; margin-bottom:2px;">New booster</div>
                    <div style="font-size:22px; font-weight:700; color:{COLORS['red']};
                                font-family:'Syne',sans-serif;">${new_cost:,.0f}</div>
                </div>
                <div style="height:1px; background:{COLORS['border']};"></div>
                <div>
                    <div style="font-size:9px; color:{COLORS['muted']}; margin-bottom:2px;">Reused booster</div>
                    <div style="font-size:22px; font-weight:700; color:{COLORS['green']};
                                font-family:'Syne',sans-serif;">${reused_cost:,.0f}</div>
                </div>
                <div style="height:1px; background:{COLORS['border']};"></div>
                <div>
                    <div style="font-size:9px; color:{COLORS['muted']}; margin-bottom:2px;">Competitor baseline</div>
                    <div style="font-size:22px; font-weight:700; color:{COLORS['amber']};
                                font-family:'Syne',sans-serif;">${competitor_cost:,.0f}</div>
                </div>
            </div>
            <div style="margin-top:18px; padding-top:16px; border-top:1px solid {COLORS['border']};">
                <div style="font-size:10px; color:{COLORS['text']}; line-height:2.0;">
                    Reuse vs. new: <span style="color:{COLORS['green']}; font-weight:700;">&minus;{reduction:.1f}%</span><br>
                    Reuse vs. competitor: <span style="color:{COLORS['green']}; font-weight:700;">&minus;{vs_comp:.1f}%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Cumulative savings line
        sorted_df = filtered_df.sort_values('Date')
        sorted_df['CumSavings'] = (sorted_df['CompetitorCost'] - sorted_df['EstimatedCost']).cumsum()
        fig_sav = go.Figure(go.Scatter(
            x=sorted_df['Date'], y=sorted_df['CumSavings'],
            mode='lines',
            fill='tozeroy',
            line=dict(color=COLORS['accent'], width=2),
            fillcolor='rgba(0,212,255,0.07)',
            name='Cumulative savings (M USD)'
        ))
        fig_sav.update_layout(**PLOTLY_LAYOUT,
            title=dict(text='Cumulative savings vs. expendable baseline', x=0,
                       font=dict(color=COLORS['muted'], size=11, family='Space Mono')),
            height=220,
            showlegend=False,
        )
        fig_sav.update_yaxes(title_text='Savings (M USD)',
                             title_font=dict(color=COLORS['muted'], size=10))
        st.plotly_chart(fig_sav, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — REUSABILITY ECONOMICS
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown(f"""
    <div style="margin: 24px 0 20px;">
        <div style="font-family:'Space Mono',monospace; font-size:9px; color:{COLORS['accent']};
                    letter-spacing:0.2em; text-transform:uppercase; margin-bottom:6px;">Section 03</div>
        <h2 style="font-family:'Syne',sans-serif !important; font-size:22px !important;
                   font-weight:700 !important; color:{COLORS['white']} !important; margin:0 !important;">
            Booster Reusability — Lifecycle Economics
        </h2>
    </div>
    """, unsafe_allow_html=True)

    reuse_agg = filtered_df.groupby('ReusedCount').agg(
        Flights=('FlightNumber', 'count'),
        SuccessRate=('Success', 'mean'),
        AvgCostPerKg=('CostPerKg', 'mean'),
        AvgPayload=('PayloadMass', 'mean'),
    ).reset_index()

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        fig1 = go.Figure(go.Bar(
            x=reuse_agg['ReusedCount'],
            y=reuse_agg['Flights'],
            marker_color=COLORS['border2'],
            marker_line_color=COLORS['accent2'],
            marker_line_width=1,
            text=reuse_agg['Flights'],
            textposition='outside',
            textfont=dict(size=10, color=COLORS['muted']),
        ))
        fig1.update_layout(**PLOTLY_LAYOUT,
            title=dict(text='Mission count by reuse iteration', x=0,
                       font=dict(color=COLORS['muted'], size=11, family='Space Mono')),
            height=300, showlegend=False,
            xaxis=dict(title='Reuse count', title_font=dict(size=10)),
            yaxis=dict(title='Missions', title_font=dict(size=10)),
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        fig2 = go.Figure(go.Scatter(
            x=reuse_agg['ReusedCount'],
            y=reuse_agg['SuccessRate'] * 100,
            mode='lines+markers',
            line=dict(color=COLORS['accent'], width=2.5),
            marker=dict(size=8, color=COLORS['accent'],
                        line=dict(color=COLORS['bg'], width=2)),
            fill='tozeroy',
            fillcolor='rgba(0,212,255,0.06)',
        ))
        fig2.update_layout(**PLOTLY_LAYOUT,
            title=dict(text='Success rate by reuse iteration', x=0,
                       font=dict(color=COLORS['muted'], size=11, family='Space Mono')),
            height=300, showlegend=False,
            yaxis=dict(title='Success rate (%)', range=[0, 105], title_font=dict(size=10)),
            xaxis=dict(title='Reuse count', title_font=dict(size=10)),
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col_c:
        fig3 = go.Figure(go.Scatter(
            x=reuse_agg['ReusedCount'],
            y=reuse_agg['AvgCostPerKg'],
            mode='lines+markers',
            line=dict(color=COLORS['amber'], width=2.5),
            marker=dict(size=8, color=COLORS['amber'],
                        line=dict(color=COLORS['bg'], width=2)),
            fill='tozeroy',
            fillcolor='rgba(245,166,35,0.06)',
        ))
        fig3.update_layout(**PLOTLY_LAYOUT,
            title=dict(text='Avg cost per kg by reuse iteration', x=0,
                       font=dict(color=COLORS['muted'], size=11, family='Space Mono')),
            height=300, showlegend=False,
            yaxis=dict(title='Cost / kg (USD)', title_font=dict(size=10)),
            xaxis=dict(title='Reuse count', title_font=dict(size=10)),
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Block version analysis
    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace; font-size:9px; color:{COLORS['muted']};
                letter-spacing:0.15em; text-transform:uppercase; margin:24px 0 12px;">
        Block version performance matrix
    </div>
    """, unsafe_allow_html=True)

    block_agg = filtered_df.groupby('Block').agg(
        Flights=('FlightNumber', 'count'),
        SuccessRate=('Success', 'mean'),
        AvgCostPerKg=('CostPerKg', 'mean'),
    ).reset_index().dropna(subset=['Block'])

    fig_block = make_subplots(specs=[[{"secondary_y": True}]])
    fig_block.add_trace(go.Bar(
        x=block_agg['Block'].astype(str),
        y=block_agg['Flights'],
        name='Missions',
        marker_color=COLORS['border2'],
        marker_line_color=COLORS['accent2'],
        marker_line_width=1,
    ), secondary_y=False)
    fig_block.add_trace(go.Scatter(
        x=block_agg['Block'].astype(str),
        y=block_agg['SuccessRate'] * 100,
        name='Success rate (%)',
        mode='lines+markers',
        line=dict(color=COLORS['accent'], width=2.5),
        marker=dict(size=9, color=COLORS['accent'],
                    line=dict(color=COLORS['bg'], width=2)),
    ), secondary_y=True)
    fig_block.update_layout(**PLOTLY_LAYOUT,
        title=dict(text='Block-version generational reliability improvement', x=0,
                   font=dict(color=COLORS['muted'], size=11, family='Space Mono')),
        height=320,
    )
    fig_block.update_yaxes(title_text='Mission count', secondary_y=False,
                           title_font=dict(color=COLORS['muted'], size=10))
    fig_block.update_yaxes(title_text='Success rate (%)', secondary_y=True,
                           range=[0, 105],
                           title_font=dict(color=COLORS['muted'], size=10))
    st.plotly_chart(fig_block, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — ORBITAL PERFORMANCE
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown(f"""
    <div style="margin: 24px 0 20px;">
        <div style="font-family:'Space Mono',monospace; font-size:9px; color:{COLORS['accent']};
                    letter-spacing:0.2em; text-transform:uppercase; margin-bottom:6px;">Section 04</div>
        <h2 style="font-family:'Syne',sans-serif !important; font-size:22px !important;
                   font-weight:700 !important; color:{COLORS['white']} !important; margin:0 !important;">
            Orbital Regime &amp; Launch Site Performance
        </h2>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        orbit_stats = filtered_df.groupby('Orbit').agg(
            Flights=('FlightNumber', 'count'),
            SuccessRate=('Success', 'mean'),
            AvgPayload=('PayloadMass', 'mean'),
            AvgCost=('CostPerKg', 'mean'),
        ).reset_index().sort_values('SuccessRate')

        bar_colors = [COLORS['red'] if x < 0.8 else COLORS['amber'] if x < 0.9 else COLORS['green']
                      for x in orbit_stats['SuccessRate']]

        fig_orb = go.Figure(go.Bar(
            y=orbit_stats['Orbit'],
            x=orbit_stats['SuccessRate'] * 100,
            orientation='h',
            marker_color=bar_colors,
            marker_line_color=COLORS['bg'],
            marker_line_width=1,
            text=[f"{x*100:.0f}% · n={y}" for x, y in zip(orbit_stats['SuccessRate'], orbit_stats['Flights'])],
            textposition='outside',
            textfont=dict(size=10, color=COLORS['muted'], family='Space Mono'),
        ))
        fig_orb.update_layout(**PLOTLY_LAYOUT,
            title=dict(text='Landing success rate by orbital regime', x=0,
                       font=dict(color=COLORS['muted'], size=11, family='Space Mono')),
            height=380, showlegend=False,
            xaxis=dict(title='Success rate (%)', range=[0, 115], title_font=dict(size=10)),
        )
        st.plotly_chart(fig_orb, use_container_width=True)

    with col_b:
        fig_box = go.Figure()
        palette = [COLORS['accent'], COLORS['amber'], COLORS['green'], COLORS['red'],
                   COLORS['accent2'], '#B983FF', '#FF83B9', '#83FFB9']
        for i, orbit in enumerate(sorted(filtered_df['Orbit'].unique())):
            odata = filtered_df[filtered_df['Orbit'] == orbit]
            fig_box.add_trace(go.Box(
                y=odata['PayloadMass'],
                name=orbit,
                boxpoints='outliers',
                marker=dict(color=palette[i % len(palette)], size=4),
                line=dict(color=palette[i % len(palette)], width=1.5),
                fillcolor=f"rgba({int(palette[i%len(palette)][1:3],16)},"
                           f"{int(palette[i%len(palette)][3:5],16)},"
                           f"{int(palette[i%len(palette)][5:7],16)},0.15)",
            ))
        fig_box.update_layout(**PLOTLY_LAYOUT,
            title=dict(text='Payload mass distribution by orbital regime', x=0,
                       font=dict(color=COLORS['muted'], size=11, family='Space Mono')),
            height=380, showlegend=False,
            yaxis=dict(title='Payload mass (kg)', title_font=dict(size=10)),
        )
        st.plotly_chart(fig_box, use_container_width=True)

    # Map
    site_stats = filtered_df.groupby('LaunchSite').agg(
        Flights=('FlightNumber', 'count'),
        SuccessRate=('Success', 'mean'),
        Lat=('Latitude', 'first'),
        Lon=('Longitude', 'first'),
    ).reset_index()

    fig_map = px.scatter_geo(
        site_stats, lat='Lat', lon='Lon',
        size='Flights', color='SuccessRate',
        hover_name='LaunchSite',
        hover_data={'Flights': True, 'SuccessRate': ':.1%', 'Lat': False, 'Lon': False},
        color_continuous_scale=[[0, COLORS['red']], [0.5, COLORS['amber']], [1, COLORS['green']]],
        range_color=[0, 1],
        projection='natural earth',
    )
    fig_map.update_layout(
        geo=dict(
            bgcolor=COLORS['bg'],
            landcolor='#0A1628',
            oceancolor=COLORS['bg'],
            coastlinecolor=COLORS['border2'],
            countrycolor=COLORS['border'],
            showland=True, showocean=True,
            showcoastlines=True, showcountries=True,
        ),
        paper_bgcolor=COLORS['surface'],
        font=dict(color=COLORS['text'], family='Space Mono', size=11),
        title=dict(text='Launch site geographic distribution and success rates', x=0,
                   font=dict(color=COLORS['muted'], size=11, family='Space Mono')),
        height=340,
        coloraxis_colorbar=dict(
            title=dict(text='Success', font=dict(color=COLORS['muted'], size=10)),
            tickfont=dict(color=COLORS['muted'], size=9),
        ),
        margin=dict(l=0, r=0, t=40, b=0),
    )
    st.plotly_chart(fig_map, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — PREDICTIVE MODEL
# ─────────────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown(f"""
    <div style="margin: 24px 0 20px;">
        <div style="font-family:'Space Mono',monospace; font-size:9px; color:{COLORS['accent']};
                    letter-spacing:0.2em; text-transform:uppercase; margin-bottom:6px;">Section 05</div>
        <h2 style="font-family:'Syne',sans-serif !important; font-size:22px !important;
                   font-weight:700 !important; color:{COLORS['white']} !important; margin:0 !important;">
            Random Forest Classifier — Landing Success Prediction
        </h2>
    </div>
    """, unsafe_allow_html=True)

    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

    feat_df = filtered_df.copy()
    for orb in ['LEO', 'GTO', 'ISS', 'PO', 'SSO', 'MEO']:
        feat_df[f'Orbit_{orb}'] = (feat_df['Orbit'] == orb).astype(int)

    features = ['PayloadMass', 'ReusedCount', 'Block', 'DaysSinceFirst',
                'Orbit_LEO', 'Orbit_GTO', 'Orbit_ISS', 'Orbit_PO', 'Orbit_SSO', 'Orbit_MEO']
    X = feat_df[features].fillna(0)
    y = feat_df['Success']

    if len(X) > 10 and y.nunique() > 1:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y)
        model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        col_a, col_b = st.columns([2, 3])

        with col_a:
            st.markdown(f"""
            <div style="background:{COLORS['surface']}; border:1px solid {COLORS['border2']};
                        padding:20px 18px; font-family:'Space Mono',monospace; margin-bottom:16px;">
                <div style="font-size:9px; color:{COLORS['accent']}; letter-spacing:0.15em;
                            text-transform:uppercase; margin-bottom:14px;">Model metrics</div>
                <table style="width:100%; border-collapse:collapse;">
                    <tr>
                        <td style="color:{COLORS['muted']}; font-size:10px; padding:6px 0;">Algorithm</td>
                        <td style="color:{COLORS['white']}; font-size:10px; text-align:right;">Random Forest</td>
                    </tr>
                    <tr>
                        <td style="color:{COLORS['muted']}; font-size:10px; padding:6px 0;">Training samples</td>
                        <td style="color:{COLORS['white']}; font-size:10px; text-align:right;">{len(X_train)}</td>
                    </tr>
                    <tr>
                        <td style="color:{COLORS['muted']}; font-size:10px; padding:6px 0;">Test samples</td>
                        <td style="color:{COLORS['white']}; font-size:10px; text-align:right;">{len(X_test)}</td>
                    </tr>
                    <tr style="border-top:1px solid {COLORS['border']};">
                        <td style="color:{COLORS['muted']}; font-size:10px; padding:8px 0 4px;">Accuracy</td>
                        <td style="color:{COLORS['accent']}; font-size:14px; font-weight:700;
                                   text-align:right; font-family:'Syne',sans-serif;">{acc:.1%}</td>
                    </tr>
                    <tr>
                        <td style="color:{COLORS['muted']}; font-size:10px; padding:4px 0;">Precision</td>
                        <td style="color:{COLORS['text']}; font-size:12px; text-align:right;">{prec:.1%}</td>
                    </tr>
                    <tr>
                        <td style="color:{COLORS['muted']}; font-size:10px; padding:4px 0;">Recall</td>
                        <td style="color:{COLORS['text']}; font-size:12px; text-align:right;">{rec:.1%}</td>
                    </tr>
                    <tr>
                        <td style="color:{COLORS['muted']}; font-size:10px; padding:4px 0;">F1-score</td>
                        <td style="color:{COLORS['text']}; font-size:12px; text-align:right;">{f1:.1%}</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

            # Feature importance
            imp_df = pd.DataFrame({
                'Feature': features,
                'Importance': model.feature_importances_
            }).sort_values('Importance', ascending=True)

            imp_colors = [COLORS['accent'] if v > 0.1 else COLORS['border2']
                          for v in imp_df['Importance']]
            fig_imp = go.Figure(go.Bar(
                y=imp_df['Feature'],
                x=imp_df['Importance'],
                orientation='h',
                marker_color=imp_colors,
                marker_line_width=0,
                text=[f"{x:.3f}" for x in imp_df['Importance']],
                textposition='outside',
                textfont=dict(size=9, color=COLORS['muted'], family='Space Mono'),
            ))
            fig_imp.update_layout(**PLOTLY_LAYOUT,
                title=dict(text='Feature importance (Gini impurity)', x=0,
                           font=dict(color=COLORS['muted'], size=11, family='Space Mono')),
                height=300, showlegend=False,
                xaxis=dict(title='Importance', title_font=dict(size=10)),
            )
            st.plotly_chart(fig_imp, use_container_width=True)

        with col_b:
            st.markdown(f"""
            <div style="background:{COLORS['surface']}; border:1px solid {COLORS['border2']};
                        border-left:3px solid {COLORS['accent']};
                        padding:18px; font-family:'Space Mono',monospace; margin-bottom:20px;">
                <div style="font-size:9px; color:{COLORS['accent']}; letter-spacing:0.15em;
                            text-transform:uppercase; margin-bottom:10px;">Mission parameter input</div>
                <div style="font-size:10px; color:{COLORS['muted']};">
                    Configure the parameters below to generate a landing success probability estimate.
                </div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                pred_payload = st.slider("Payload mass (kg)", 0, 16000, 5000, 100)
                pred_reuse = st.slider("Reuse count", 0, 10, 2, 1)
            with c2:
                pred_block = st.slider("Block version", 1, 5, 4, 1)
                pred_days = st.slider("Days since first launch", 0, 4000, 2000, 100)
            with c3:
                pred_orbit = st.selectbox("Target orbit", ['LEO', 'GTO', 'ISS', 'PO', 'SSO', 'MEO'])

            pred_input = np.zeros(len(features))
            pred_input[0] = pred_payload
            pred_input[1] = pred_reuse
            pred_input[2] = pred_block
            pred_input[3] = pred_days
            orbit_idx = {'LEO': 4, 'GTO': 5, 'ISS': 6, 'PO': 7, 'SSO': 8, 'MEO': 9}
            pred_input[orbit_idx[pred_orbit]] = 1

            proba = model.predict_proba([pred_input])[0]
            pred_class = model.predict([pred_input])[0]
            confidence = proba[1] * 100

            bar_w = int(confidence)
            bar_color = COLORS['green'] if pred_class == 1 else COLORS['red']
            label = "LANDING SUCCESS" if pred_class == 1 else "LANDING FAILURE"
            label_color = COLORS['green'] if pred_class == 1 else COLORS['red']

            st.markdown(f"""
            <div style="background:{COLORS['surface']}; border:1px solid {COLORS['border2']};
                        padding:24px; margin-top:4px; font-family:'Space Mono',monospace;">
                <div style="font-size:9px; color:{COLORS['muted']}; letter-spacing:0.15em;
                            text-transform:uppercase; margin-bottom:16px;">Prediction output</div>
                <div style="font-size:28px; font-weight:800; color:{label_color};
                            font-family:'Syne',sans-serif; margin-bottom:8px;">{label}</div>
                <div style="font-size:13px; color:{COLORS['text']}; margin-bottom:20px;">
                    Landing success probability:
                    <span style="color:{COLORS['white']}; font-weight:700; font-size:16px;"> {confidence:.1f}%</span>
                </div>
                <div style="height:6px; background:{COLORS['border']}; border-radius:1px; margin-bottom:8px;">
                    <div style="height:100%; width:{bar_w}%; background:{bar_color};
                                border-radius:1px; transition:width 0.3s ease;"></div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:9px; color:{COLORS['muted']};">
                    <span>0%</span><span>Confidence interval</span><span>100%</span>
                </div>
                <div style="margin-top:18px; padding-top:14px; border-top:1px solid {COLORS['border']};
                            font-size:10px; color:{COLORS['muted']}; line-height:1.8;">
                    Model: RandomForestClassifier · Estimators: 100 · Max depth: 5<br>
                    Train/test split: 70/30 · Stratified sampling
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.warning("Insufficient data variance for classification. Adjust filters to include a broader sample.")


# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center;
            padding:12px 0 24px; font-family:'Space Mono',monospace;">
    <div>
        <div style="font-size:10px; color:{COLORS['white']}; font-weight:700; margin-bottom:3px;">
            Project Alpha — Launch Economics
        </div>
        <div style="font-size:9px; color:{COLORS['muted']};">
            SpaceX Falcon 9 · Operational Economics Analysis · 2010–2021
        </div>
    </div>
    <div style="font-size:9px; color:{COLORS['muted']}; text-align:right;">
        Python · Streamlit · Plotly · scikit-learn<br>
        Data Science Portfolio · 2026
    </div>
</div>
""", unsafe_allow_html=True)
