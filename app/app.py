import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Falcon 9 — Launch Economics",
    page_icon="◌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── PALETTE ────────────────────────────────────────────────────────────────────
# Warm scientific paper: cream base, ink text, single cobalt accent
P = {
    'paper':   '#F7F4EF',
    'cream':   '#EDE9E1',
    'rule':    '#D4CEC4',
    'ink':     '#1A1714',
    'ink2':    '#3D3830',
    'muted':   '#8A8278',
    'faint':   '#C4BEB5',
    'cobalt':  '#1B3FAB',
    'cobalt2': '#2D5BE3',
    'ember':   '#C44B1A',
    'sage':    '#3A6B4A',
    'bg':      '#F2EEE8',
}

# ── PLOTLY BASE ────────────────────────────────────────────────────────────────
def base_layout(title='', h=380):
    return dict(
        plot_bgcolor=P['paper'],
        paper_bgcolor=P['paper'],
        font=dict(color=P['ink2'], family='Georgia, serif', size=11),
        height=h,
        margin=dict(l=52, r=24, t=48, b=44),
        title=dict(
            text=title, x=0, y=0.97,
            font=dict(color=P['muted'], size=10, family='Georgia, serif')
        ),
        xaxis=dict(
            gridcolor=P['rule'], linecolor=P['rule'], linewidth=1,
            tickfont=dict(color=P['muted'], size=10, family='Georgia, serif'),
            zerolinecolor=P['rule'],
        ),
        yaxis=dict(
            gridcolor=P['rule'], linecolor=P['rule'], linewidth=1,
            tickfont=dict(color=P['muted'], size=10, family='Georgia, serif'),
            zerolinecolor=P['rule'],
        ),
        legend=dict(
            bgcolor=P['paper'], bordercolor=P['rule'], borderwidth=1,
            font=dict(color=P['muted'], size=10, family='Georgia, serif'),
        ),
        hoverlabel=dict(
            bgcolor=P['ink'], bordercolor=P['ink'],
            font=dict(color=P['paper'], size=11, family='Georgia, serif'),
        ),
        hovermode='x unified',
    )

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Mono:ital,wght@0,300;0,400;1,300&display=swap');

html, body, [class*="css"] {{
    font-family: 'EB Garamond', Georgia, serif !important;
}}

.stApp {{
    background: {P['bg']} !important;
}}

[data-testid="stSidebar"] {{
    background: {P['cream']} !important;
    border-right: 1px solid {P['rule']} !important;
}}
[data-testid="stSidebar"] * {{
    font-family: 'EB Garamond', Georgia, serif !important;
}}

/* Headings */
h1, h2, h3, h4, h5, h6 {{
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    color: {P['ink']} !important;
    font-weight: 300 !important;
    letter-spacing: 0.01em !important;
}}

/* Labels / small text */
.label-mono {{
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: {P['muted']};
}}

/* Metrics */
[data-testid="stMetric"] {{
    background: {P['paper']} !important;
    border: none !important;
    border-top: 1px solid {P['ink']} !important;
    border-radius: 0 !important;
    padding: 16px 0 12px !important;
}}
[data-testid="stMetricLabel"] p {{
    font-family: 'DM Mono', monospace !important;
    font-size: 9px !important;
    color: {P['muted']} !important;
    text-transform: uppercase !important;
    letter-spacing: 0.14em !important;
}}
[data-testid="stMetricValue"] {{
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 28px !important;
    font-weight: 300 !important;
    color: {P['ink']} !important;
}}
[data-testid="stMetricDelta"] {{
    font-family: 'DM Mono', monospace !important;
    font-size: 9px !important;
    color: {P['muted']} !important;
}}
[data-testid="stMetricDelta"] svg {{ display: none !important; }}

/* Tabs */
[data-baseweb="tab-list"] {{
    background: transparent !important;
    border-bottom: 1px solid {P['rule']} !important;
    gap: 4px !important;
}}
[data-baseweb="tab"] {{
    font-family: 'DM Mono', monospace !important;
    font-size: 9px !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: {P['faint']} !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid transparent !important;
    padding: 10px 18px !important;
    transition: color 0.15s !important;
}}
button[aria-selected="true"][data-baseweb="tab"] {{
    color: {P['ink']} !important;
    border-bottom: 1px solid {P['ink']} !important;
    background: transparent !important;
}}

/* Sliders */
[data-testid="stSlider"] label {{
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    color: {P['muted']} !important;
    letter-spacing: 0.08em !important;
}}
[data-testid="stSlider"] [data-baseweb="slider"] div div div div {{
    background: {P['cobalt']} !important;
}}

/* Selectbox */
[data-baseweb="select"] > div {{
    background: {P['paper']} !important;
    border: 1px solid {P['rule']} !important;
    border-radius: 0 !important;
    font-family: 'EB Garamond', serif !important;
    font-size: 13px !important;
    color: {P['ink']} !important;
}}

/* Multiselect */
[data-baseweb="tag"] {{
    background: {P['ink']} !important;
    border-radius: 0 !important;
}}
[data-baseweb="tag"] span {{
    font-family: 'DM Mono', monospace !important;
    font-size: 9px !important;
    color: {P['paper']} !important;
}}

/* Radio */
[data-baseweb="radio"] span {{
    font-family: 'EB Garamond', serif !important;
    font-size: 13px !important;
    color: {P['ink2']} !important;
}}

/* Sidebar labels */
[data-testid="stSidebar"] label {{
    font-family: 'DM Mono', monospace !important;
    font-size: 9px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    color: {P['muted']} !important;
}}

/* HR */
hr {{
    border: none !important;
    border-top: 1px solid {P['rule']} !important;
    margin: 28px 0 !important;
}}

/* Warning */
[data-testid="stAlert"] {{
    background: {P['cream']} !important;
    border: 1px solid {P['rule']} !important;
    border-left: 2px solid {P['ember']} !important;
    border-radius: 0 !important;
    font-family: 'EB Garamond', serif !important;
}}

::-webkit-scrollbar {{ width: 4px; background: {P['cream']}; }}
::-webkit-scrollbar-thumb {{ background: {P['faint']}; }}
</style>
""", unsafe_allow_html=True)


# ── DATA ───────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    import os
    from pathlib import Path
    for path in [
        'data/spacex_raw.csv',
        '../data/spacex_raw.csv',
        'launch-economics/data/spacex_raw.csv',
        str(Path(__file__).parent.parent / 'data' / 'spacex_raw.csv'),
    ]:
        if os.path.exists(path):
            df = pd.read_csv(path)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
    st.error("Data file not found: data/spacex_raw.csv")
    st.stop()

df = load_data()


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
st.sidebar.markdown(f"""
<div style="padding:28px 20px 20px; border-bottom:1px solid {P['rule']}; margin-bottom:24px;">
  <div style="font-family:'DM Mono',monospace; font-size:8px; color:{P['faint']};
              letter-spacing:0.2em; text-transform:uppercase; margin-bottom:10px;">
    Project Alpha · 2026
  </div>
  <div style="font-family:'Cormorant Garamond',Georgia,serif; font-size:22px;
              font-weight:300; color:{P['ink']}; line-height:1.15; margin-bottom:6px;">
    Launch<br>Economics
  </div>
  <div style="font-family:'DM Mono',monospace; font-size:9px; color:{P['cobalt']};
              letter-spacing:0.06em;">
    SpaceX Falcon 9 · 2010 – 2021
  </div>
</div>
""", unsafe_allow_html=True)

year_range = st.sidebar.slider("Year range", int(df['Year'].min()), int(df['Year'].max()), (2015, 2021))
selected_orbits = st.sidebar.multiselect("Orbit", options=sorted(df['Orbit'].unique()), default=sorted(df['Orbit'].unique()))
reused_filter = st.sidebar.radio("Configuration", ["All", "New only", "Reused only"])

st.sidebar.markdown(f"""
<div style="padding:16px 20px; margin-top:20px; border-top:1px solid {P['rule']};">
  <div style="font-family:'EB Garamond',serif; font-size:12px; color:{P['muted']};
              line-height:1.9; font-style:italic;">
    91 launches analysed.<br>
    Dataset: IBM Applied Data<br>Science Capstone.
  </div>
</div>
""", unsafe_allow_html=True)

# Apply filters
filtered_df = df[
    (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1]) &
    (df['Orbit'].isin(selected_orbits))
].copy()
if reused_filter == "New only":
    filtered_df = filtered_df[filtered_df['Reused'] == False]
elif reused_filter == "Reused only":
    filtered_df = filtered_df[filtered_df['Reused'] == True]

n = len(filtered_df)


# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="padding:52px 0 40px; border-bottom:1px solid {P['rule']}; margin-bottom:40px;">
  <div style="font-family:'DM Mono',monospace; font-size:8px; color:{P['cobalt']};
              letter-spacing:0.22em; text-transform:uppercase; margin-bottom:14px;">
    Aerospace Systems Economics · SpaceX Falcon 9
  </div>
  <div style="font-family:'Cormorant Garamond',Georgia,serif; font-size:52px;
              font-weight:300; color:{P['ink']}; line-height:1.0; margin-bottom:18px;
              letter-spacing:-0.01em;">
    Booster Reusability<br>
    <span style="font-style:italic; color:{P['muted']};">and the Economics of</span><br>
    Orbital Access
  </div>
  <div style="font-family:'EB Garamond',serif; font-size:15px; color:{P['muted']};
              max-width:560px; line-height:1.9; font-style:italic;">
    A quantitative analysis of cost-per-kilogram trajectories, success rate
    convergence, and predictive classification of landing outcomes across
    91 Falcon 9 missions, 2010 – 2021.
  </div>
</div>
""", unsafe_allow_html=True)


# ── METRICS ────────────────────────────────────────────────────────────────────
success_rate = filtered_df['Success'].mean() * 100 if n > 0 else 0
reused_n = int(filtered_df['Reused'].sum()) if n > 0 else 0
avg_cost = filtered_df['CostPerKg'].mean() if n > 0 else 0
total_savings = (filtered_df['CompetitorCost'] - filtered_df['EstimatedCost']).sum() if n > 0 else 0
avg_payload = filtered_df['PayloadMass'].mean() if n > 0 else 1
competitor_avg = 165_000_000 / avg_payload if avg_payload > 0 else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Missions", f"{n}")
c2.metric("Landing success", f"{success_rate:.1f}%")
c3.metric("Reused boosters", f"{reused_n}")
c4.metric("Mean cost / kg", f"${avg_cost:,.0f}")
c5.metric("Cumul. savings", f"${total_savings:.0f} M")

st.markdown("<hr>", unsafe_allow_html=True)


# ── TABS ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Temporal",
    "Cost Dynamics",
    "Reusability",
    "Orbital",
    "Prediction"
])

# ───────────────────────────────────────────────────────────────────────────────
# TAB 1 · TEMPORAL
# ───────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown(f"""
    <div style="padding:32px 0 24px;">
      <div style="font-family:'DM Mono',monospace; font-size:8px; color:{P['muted']};
                  letter-spacing:0.2em; text-transform:uppercase; margin-bottom:8px;">§ 1</div>
      <div style="font-family:'Cormorant Garamond',serif; font-size:30px; font-weight:300;
                  color:{P['ink']}; line-height:1.1;">
        Launch Cadence &amp; Success Rate Progression
      </div>
    </div>
    """, unsafe_allow_html=True)

    yearly = filtered_df.groupby('Year').agg(
        Launches=('FlightNumber', 'count'),
        SuccessRate=('Success', 'mean'),
    ).reset_index()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=yearly['Year'], y=yearly['Launches'],
        name='Missions',
        marker_color=P['cream'],
        marker_line_color=P['ink2'],
        marker_line_width=1,
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=yearly['Year'], y=yearly['SuccessRate'] * 100,
        name='Success rate',
        mode='lines+markers',
        line=dict(color=P['cobalt'], width=1.5),
        marker=dict(size=6, color=P['cobalt'],
                    line=dict(color=P['paper'], width=1.5)),
    ), secondary_y=True)

    layout = base_layout('Annual mission count (bars) and landing success rate (line)', h=360)
    layout['xaxis']['dtick'] = 1
    fig.update_layout(**layout)
    fig.update_yaxes(title_text='Missions', secondary_y=False,
                     title_font=dict(color=P['muted'], size=9, family='DM Mono, monospace'))
    fig.update_yaxes(title_text='Success rate (%)', secondary_y=True,
                     range=[0, 108],
                     title_font=dict(color=P['muted'], size=9, family='DM Mono, monospace'))
    st.plotly_chart(fig, use_container_width=True)

    col_a, col_b = st.columns([3, 2])
    with col_a:
        quarterly = filtered_df.groupby(['Year', 'Quarter']).size().reset_index(name='Count')
        pivot = quarterly.pivot(index='Quarter', columns='Year', values='Count').fillna(0)
        fig_h = go.Figure(go.Heatmap(
            z=pivot.values,
            x=pivot.columns.astype(str),
            y=[f'Q{q}' for q in pivot.index],
            colorscale=[[0, P['paper']], [0.5, '#BBCBF0'], [1, P['cobalt']]],
            showscale=False,
            text=pivot.values.astype(int),
            texttemplate='%{text}',
            textfont=dict(size=11, color=P['ink2'], family='DM Mono, monospace'),
        ))
        fig_h.update_layout(**base_layout('Quarterly mission distribution', h=220))
        st.plotly_chart(fig_h, use_container_width=True)

    with col_b:
        st.markdown(f"""
        <div style="margin-top:8px; padding:20px 0; border-top:1px solid {P['rule']};">
          <div style="font-family:'DM Mono',monospace; font-size:8px; color:{P['muted']};
                      letter-spacing:0.16em; text-transform:uppercase; margin-bottom:14px;">
            Periodisation
          </div>
          <div style="font-family:'EB Garamond',serif; font-size:14px; color:{P['ink2']};
                      line-height:2.1;">
            <span style="font-family:'DM Mono',monospace; font-size:9px;
                         color:{P['cobalt']};">2013 – 2015</span><br>
            Early operational phase. Iterative hardware refinement.
            Landing success below 50 %.<br><br>
            <span style="font-family:'DM Mono',monospace; font-size:9px;
                         color:{P['cobalt']};">2016 – 2018</span><br>
            Block 4 / 5 transition. First booster recoveries.
            Reliability exceeds 90 %.<br><br>
            <span style="font-family:'DM Mono',monospace; font-size:9px;
                         color:{P['cobalt']};">2019 – 2021</span><br>
            Constellation deployment era. Launch frequency triples.
            Near-unity landing success.
          </div>
        </div>
        """, unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────────────────────
# TAB 2 · COST DYNAMICS
# ───────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown(f"""
    <div style="padding:32px 0 24px;">
      <div style="font-family:'DM Mono',monospace; font-size:8px; color:{P['muted']};
                  letter-spacing:0.2em; text-transform:uppercase; margin-bottom:8px;">§ 2</div>
      <div style="font-family:'Cormorant Garamond',serif; font-size:30px; font-weight:300;
                  color:{P['ink']}; line-height:1.1;">
        Cost-per-Kilogram Dynamics
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])
    with col_a:
        fig_s = px.scatter(
            filtered_df.dropna(subset=['DaysSinceFirst', 'CostPerKg']),
            x='DaysSinceFirst', y='CostPerKg',
            color='Success',
            size='PayloadMass', size_max=16,
            hover_data=['FlightNumber', 'Orbit', 'Reused', 'ReusedCount'],
            color_continuous_scale=[[0, P['ember']], [1, P['sage']]],
            labels={'DaysSinceFirst': 'Days since first launch',
                    'CostPerKg': 'Cost per kg (USD)'},
        )
        mask = filtered_df[['DaysSinceFirst', 'CostPerKg']].dropna()
        if len(mask) > 5:
            z = np.polyfit(mask['DaysSinceFirst'], mask['CostPerKg'], 2)
            p_fn = np.poly1d(z)
            xr = np.linspace(mask['DaysSinceFirst'].min(), mask['DaysSinceFirst'].max(), 200)
            fig_s.add_trace(go.Scatter(
                x=xr, y=p_fn(xr), mode='lines',
                line=dict(color=P['cobalt'], width=1.5, dash='dot'),
                name='Polynomial trend', showlegend=True,
            ))
        fig_s.update_layout(**base_layout(
            'Cost per kg over operational lifetime  ·  bubble area ∝ payload mass', h=400))
        fig_s.update_coloraxes(colorbar=dict(
            title=dict(text='Success', font=dict(color=P['muted'], size=9)),
            tickfont=dict(color=P['muted'], size=9),
            tickvals=[0, 1], ticktext=['0', '1'],
        ))
        st.plotly_chart(fig_s, use_container_width=True)

    with col_b:
        new_c = filtered_df[filtered_df['Reused'] == False]['CostPerKg'].mean() if len(filtered_df[filtered_df['Reused'] == False]) > 0 else 0
        reu_c = filtered_df[filtered_df['Reused'] == True]['CostPerKg'].mean() if len(filtered_df[filtered_df['Reused'] == True]) > 0 else 0
        red_pct = (new_c - reu_c) / new_c * 100 if new_c > 0 else 0
        vs_pct = (competitor_avg - reu_c) / competitor_avg * 100 if competitor_avg > 0 else 0

        st.markdown(f"""
        <div style="margin-top:8px; border-top:1px solid {P['ink']}; padding-top:20px;">
          <div style="font-family:'DM Mono',monospace; font-size:8px; color:{P['muted']};
                      letter-spacing:0.16em; text-transform:uppercase; margin-bottom:20px;">
            Cost benchmark  ·  USD / kg
          </div>
          <div style="margin-bottom:20px;">
            <div style="font-family:'DM Mono',monospace; font-size:9px; color:{P['muted']};
                        margin-bottom:3px;">Expendable (new booster)</div>
            <div style="font-family:'Cormorant Garamond',serif; font-size:34px;
                        font-weight:300; color:{P['ember']};">${new_c:,.0f}</div>
          </div>
          <div style="border-top:1px solid {P['rule']}; padding-top:16px; margin-bottom:20px;">
            <div style="font-family:'DM Mono',monospace; font-size:9px; color:{P['muted']};
                        margin-bottom:3px;">Reused booster</div>
            <div style="font-family:'Cormorant Garamond',serif; font-size:34px;
                        font-weight:300; color:{P['sage']};">${reu_c:,.0f}</div>
          </div>
          <div style="border-top:1px solid {P['rule']}; padding-top:16px; margin-bottom:20px;">
            <div style="font-family:'DM Mono',monospace; font-size:9px; color:{P['muted']};
                        margin-bottom:3px;">Competitor baseline</div>
            <div style="font-family:'Cormorant Garamond',serif; font-size:34px;
                        font-weight:300; color:{P['muted']};">${competitor_avg:,.0f}</div>
          </div>
          <div style="border-top:1px solid {P['rule']}; padding-top:14px;">
            <div style="font-family:'EB Garamond',serif; font-size:13px;
                        color:{P['ink2']}; line-height:1.9; font-style:italic;">
              Reuse vs. new: &minus;{red_pct:.1f}%<br>
              Reuse vs. competitor: &minus;{vs_pct:.1f}%
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Cumulative savings sparkline
        sdf = filtered_df.sort_values('Date').copy()
        sdf['CumSav'] = (sdf['CompetitorCost'] - sdf['EstimatedCost']).cumsum()
        fig_sav = go.Figure(go.Scatter(
            x=sdf['Date'], y=sdf['CumSav'],
            mode='lines', fill='tozeroy',
            line=dict(color=P['cobalt'], width=1.5),
            fillcolor='rgba(27,63,171,0.07)',
        ))
        fig_sav.update_layout(**base_layout('Cumulative savings vs. expendable baseline (M USD)', h=200))
        fig_sav.update_layout(showlegend=False)
        st.plotly_chart(fig_sav, use_container_width=True)


# ───────────────────────────────────────────────────────────────────────────────
# TAB 3 · REUSABILITY
# ───────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown(f"""
    <div style="padding:32px 0 24px;">
      <div style="font-family:'DM Mono',monospace; font-size:8px; color:{P['muted']};
                  letter-spacing:0.2em; text-transform:uppercase; margin-bottom:8px;">§ 3</div>
      <div style="font-family:'Cormorant Garamond',serif; font-size:30px; font-weight:300;
                  color:{P['ink']}; line-height:1.1;">
        Booster Lifecycle Economics
      </div>
    </div>
    """, unsafe_allow_html=True)

    ra = filtered_df.groupby('ReusedCount').agg(
        Flights=('FlightNumber', 'count'),
        SuccessRate=('Success', 'mean'),
        AvgCost=('CostPerKg', 'mean'),
    ).reset_index()

    c1, c2, c3 = st.columns(3)
    with c1:
        f1 = go.Figure(go.Bar(
            x=ra['ReusedCount'], y=ra['Flights'],
            marker_color=P['cream'], marker_line_color=P['ink2'], marker_line_width=1,
            text=ra['Flights'], textposition='outside',
            textfont=dict(size=9, color=P['muted'], family='DM Mono, monospace'),
        ))
        f1.update_layout(**base_layout('Mission count by reuse iteration', h=300))
        f1.update_layout(showlegend=False)
        f1.update_xaxes(title_text='Reuse count', title_font=dict(size=9, color=P['muted']))
        f1.update_yaxes(title_text='Missions', title_font=dict(size=9, color=P['muted']))
        st.plotly_chart(f1, use_container_width=True)

    with c2:
        f2 = go.Figure(go.Scatter(
            x=ra['ReusedCount'], y=ra['SuccessRate'] * 100,
            mode='lines+markers',
            line=dict(color=P['cobalt'], width=1.5),
            marker=dict(size=7, color=P['cobalt'],
                        line=dict(color=P['paper'], width=1.5)),
            fill='tozeroy', fillcolor='rgba(27,63,171,0.06)',
        ))
        f2.update_layout(**base_layout('Landing success rate by reuse iteration', h=300))
        f2.update_layout(showlegend=False)
        f2.update_yaxes(range=[0, 108], title_text='Success rate (%)',
                        title_font=dict(size=9, color=P['muted']))
        f2.update_xaxes(title_text='Reuse count', title_font=dict(size=9, color=P['muted']))
        st.plotly_chart(f2, use_container_width=True)

    with c3:
        f3 = go.Figure(go.Scatter(
            x=ra['ReusedCount'], y=ra['AvgCost'],
            mode='lines+markers',
            line=dict(color=P['ember'], width=1.5),
            marker=dict(size=7, color=P['ember'],
                        line=dict(color=P['paper'], width=1.5)),
            fill='tozeroy', fillcolor='rgba(196,75,26,0.06)',
        ))
        f3.update_layout(**base_layout('Mean cost per kg by reuse iteration', h=300))
        f3.update_layout(showlegend=False)
        f3.update_yaxes(title_text='USD / kg', title_font=dict(size=9, color=P['muted']))
        f3.update_xaxes(title_text='Reuse count', title_font=dict(size=9, color=P['muted']))
        st.plotly_chart(f3, use_container_width=True)

    # Block version
    ba = filtered_df.groupby('Block').agg(
        Flights=('FlightNumber', 'count'),
        SuccessRate=('Success', 'mean'),
    ).reset_index().dropna(subset=['Block'])

    fig_bl = make_subplots(specs=[[{"secondary_y": True}]])
    fig_bl.add_trace(go.Bar(
        x=ba['Block'].astype(str), y=ba['Flights'],
        name='Missions', marker_color=P['cream'],
        marker_line_color=P['ink2'], marker_line_width=1,
    ), secondary_y=False)
    fig_bl.add_trace(go.Scatter(
        x=ba['Block'].astype(str), y=ba['SuccessRate'] * 100,
        name='Success rate', mode='lines+markers',
        line=dict(color=P['cobalt'], width=1.5),
        marker=dict(size=7, color=P['cobalt'],
                    line=dict(color=P['paper'], width=1.5)),
    ), secondary_y=True)
    fig_bl.update_layout(**base_layout('Block version: mission count and landing success rate', h=300))
    fig_bl.update_yaxes(title_text='Missions', secondary_y=False,
                        title_font=dict(color=P['muted'], size=9))
    fig_bl.update_yaxes(title_text='Success rate (%)', secondary_y=True, range=[0, 108],
                        title_font=dict(color=P['muted'], size=9))
    st.plotly_chart(fig_bl, use_container_width=True)


# ───────────────────────────────────────────────────────────────────────────────
# TAB 4 · ORBITAL
# ───────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown(f"""
    <div style="padding:32px 0 24px;">
      <div style="font-family:'DM Mono',monospace; font-size:8px; color:{P['muted']};
                  letter-spacing:0.2em; text-transform:uppercase; margin-bottom:8px;">§ 4</div>
      <div style="font-family:'Cormorant Garamond',serif; font-size:30px; font-weight:300;
                  color:{P['ink']}; line-height:1.1;">
        Orbital Regime &amp; Site Performance
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        os_ = filtered_df.groupby('Orbit').agg(
            Flights=('FlightNumber', 'count'),
            SuccessRate=('Success', 'mean'),
        ).reset_index().sort_values('SuccessRate')

        bar_c = [P['ember'] if x < 0.8 else P['muted'] if x < 0.9 else P['cobalt']
                 for x in os_['SuccessRate']]
        fo = go.Figure(go.Bar(
            y=os_['Orbit'], x=os_['SuccessRate'] * 100,
            orientation='h',
            marker_color=bar_c,
            marker_line_width=0,
            text=[f"{x*100:.0f}%  n={y}" for x, y in zip(os_['SuccessRate'], os_['Flights'])],
            textposition='outside',
            textfont=dict(size=9, color=P['muted'], family='DM Mono, monospace'),
        ))
        fo.update_layout(**base_layout('Landing success rate by orbital regime', h=380))
        fo.update_layout(showlegend=False)
        fo.update_xaxes(range=[0, 118], title_text='Success (%)',
                        title_font=dict(size=9, color=P['muted']))
        st.plotly_chart(fo, use_container_width=True)

    with col_b:
        palette_orb = [P['cobalt'], P['ember'], P['sage'], P['muted'],
                       '#7B5EA7', '#4A8B8B', '#8B6914', '#2D7A4F']
        fb = go.Figure()
        for i, orb in enumerate(sorted(filtered_df['Orbit'].unique())):
            odata = filtered_df[filtered_df['Orbit'] == orb]
            c_hex = palette_orb[i % len(palette_orb)]
            r, g, b2 = int(c_hex[1:3], 16), int(c_hex[3:5], 16), int(c_hex[5:7], 16)
            fb.add_trace(go.Box(
                y=odata['PayloadMass'], name=orb,
                boxpoints='outliers',
                marker=dict(color=c_hex, size=4),
                line=dict(color=c_hex, width=1.2),
                fillcolor=f'rgba({r},{g},{b2},0.12)',
            ))
        fb.update_layout(**base_layout('Payload mass distribution by orbital regime (kg)', h=380))
        fb.update_layout(showlegend=False)
        fb.update_yaxes(title_text='Payload mass (kg)', title_font=dict(size=9, color=P['muted']))
        st.plotly_chart(fb, use_container_width=True)

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
        color_continuous_scale=[[0, P['ember']], [0.5, P['muted']], [1, P['cobalt']]],
        range_color=[0, 1],
        projection='natural earth',
    )
    fig_map.update_layout(
        geo=dict(
            bgcolor=P['paper'], landcolor=P['cream'], oceancolor=P['bg'],
            coastlinecolor=P['rule'], countrycolor=P['rule'],
            showland=True, showocean=True, showcoastlines=True, showcountries=True,
        ),
        paper_bgcolor=P['paper'],
        font=dict(color=P['ink2'], family='Georgia, serif', size=11),
        title=dict(text='Geographic distribution of launch sites and success rates', x=0,
                   font=dict(color=P['muted'], size=10, family='Georgia, serif')),
        height=320,
        margin=dict(l=0, r=0, t=40, b=0),
        coloraxis_colorbar=dict(
            title=dict(text='Success', font=dict(color=P['muted'], size=9)),
            tickfont=dict(color=P['muted'], size=9),
        ),
    )
    st.plotly_chart(fig_map, use_container_width=True)


# ───────────────────────────────────────────────────────────────────────────────
# TAB 5 · PREDICTION
# ───────────────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown(f"""
    <div style="padding:32px 0 24px;">
      <div style="font-family:'DM Mono',monospace; font-size:8px; color:{P['muted']};
                  letter-spacing:0.2em; text-transform:uppercase; margin-bottom:8px;">§ 5</div>
      <div style="font-family:'Cormorant Garamond',serif; font-size:30px; font-weight:300;
                  color:{P['ink']}; line-height:1.1;">
        Predictive Classification — Landing Outcome
      </div>
    </div>
    """, unsafe_allow_html=True)

    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

    feat_df = filtered_df.copy()
    for orb in ['LEO', 'GTO', 'ISS', 'PO', 'SSO', 'MEO']:
        feat_df[f'O_{orb}'] = (feat_df['Orbit'] == orb).astype(int)

    features = ['PayloadMass', 'ReusedCount', 'Block', 'DaysSinceFirst',
                'O_LEO', 'O_GTO', 'O_ISS', 'O_PO', 'O_SSO', 'O_MEO']
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
            <div style="border-top:1px solid {P['ink']}; padding-top:20px; margin-bottom:20px;">
              <div style="font-family:'DM Mono',monospace; font-size:8px; color:{P['muted']};
                          letter-spacing:0.16em; text-transform:uppercase; margin-bottom:16px;">
                Model metrics
              </div>
              <table style="width:100%; border-collapse:collapse; font-family:'EB Garamond',serif;">
                <tr style="border-bottom:1px solid {P['rule']};">
                  <td style="font-size:13px; color:{P['muted']}; padding:7px 0;">Algorithm</td>
                  <td style="font-size:13px; color:{P['ink2']}; text-align:right;">Random Forest</td>
                </tr>
                <tr style="border-bottom:1px solid {P['rule']};">
                  <td style="font-size:13px; color:{P['muted']}; padding:7px 0;">Train / Test</td>
                  <td style="font-size:13px; color:{P['ink2']}; text-align:right;">{len(X_train)} / {len(X_test)}</td>
                </tr>
                <tr style="border-bottom:1px solid {P['rule']};">
                  <td style="font-size:13px; color:{P['muted']}; padding:7px 0;">Accuracy</td>
                  <td style="font-family:'Cormorant Garamond',serif; font-size:20px;
                             font-weight:300; color:{P['cobalt']}; text-align:right;">{acc:.1%}</td>
                </tr>
                <tr style="border-bottom:1px solid {P['rule']};">
                  <td style="font-size:13px; color:{P['muted']}; padding:7px 0;">Precision</td>
                  <td style="font-size:13px; color:{P['ink2']}; text-align:right;">{prec:.1%}</td>
                </tr>
                <tr style="border-bottom:1px solid {P['rule']};">
                  <td style="font-size:13px; color:{P['muted']}; padding:7px 0;">Recall</td>
                  <td style="font-size:13px; color:{P['ink2']}; text-align:right;">{rec:.1%}</td>
                </tr>
                <tr>
                  <td style="font-size:13px; color:{P['muted']}; padding:7px 0;">F1-score</td>
                  <td style="font-size:13px; color:{P['ink2']}; text-align:right;">{f1:.1%}</td>
                </tr>
              </table>
            </div>
            """, unsafe_allow_html=True)

            imp_df = pd.DataFrame({
                'Feature': features, 'Importance': model.feature_importances_
            }).sort_values('Importance', ascending=True)

            fi = go.Figure(go.Bar(
                y=imp_df['Feature'], x=imp_df['Importance'],
                orientation='h',
                marker_color=[P['cobalt'] if v > 0.08 else P['faint']
                              for v in imp_df['Importance']],
                marker_line_width=0,
                text=[f"{x:.3f}" for x in imp_df['Importance']],
                textposition='outside',
                textfont=dict(size=8, color=P['muted'], family='DM Mono, monospace'),
            ))
            fi.update_layout(**base_layout('Feature importance (Gini impurity reduction)', h=290))
            fi.update_layout(showlegend=False)
            fi.update_xaxes(title_text='Importance',
                            title_font=dict(size=9, color=P['muted']))
            st.plotly_chart(fi, use_container_width=True)

        with col_b:
            st.markdown(f"""
            <div style="border-top:1px solid {P['rule']}; padding-top:20px; margin-bottom:20px;">
              <div style="font-family:'DM Mono',monospace; font-size:8px; color:{P['muted']};
                          letter-spacing:0.16em; text-transform:uppercase; margin-bottom:12px;">
                Mission parameters
              </div>
            </div>
            """, unsafe_allow_html=True)

            p1, p2, p3 = st.columns(3)
            with p1:
                pp = st.slider("Payload (kg)", 0, 16000, 5000, 100)
                pr = st.slider("Reuse count", 0, 10, 2, 1)
            with p2:
                pb = st.slider("Block version", 1, 5, 4, 1)
                pd_ = st.slider("Days elapsed", 0, 4000, 2000, 100)
            with p3:
                po = st.selectbox("Target orbit", ['LEO', 'GTO', 'ISS', 'PO', 'SSO', 'MEO'])

            inp = np.zeros(len(features))
            inp[0], inp[1], inp[2], inp[3] = pp, pr, pb, pd_
            inp[{'LEO': 4, 'GTO': 5, 'ISS': 6, 'PO': 7, 'SSO': 8, 'MEO': 9}[po]] = 1

            proba = model.predict_proba([inp])[0]
            pred_class = model.predict([inp])[0]
            conf = proba[1] * 100
            outcome = "Landing success" if pred_class == 1 else "Landing failure"
            out_color = P['cobalt'] if pred_class == 1 else P['ember']
            bar_fill = int(conf)

            st.markdown(f"""
            <div style="border:1px solid {P['rule']}; padding:28px 24px; margin-top:8px;">
              <div style="font-family:'DM Mono',monospace; font-size:8px; color:{P['muted']};
                          letter-spacing:0.16em; text-transform:uppercase; margin-bottom:16px;">
                Prediction
              </div>
              <div style="font-family:'Cormorant Garamond',serif; font-size:36px;
                          font-weight:300; color:{out_color}; margin-bottom:6px;">
                {outcome}
              </div>
              <div style="font-family:'EB Garamond',serif; font-size:14px;
                          color:{P['muted']}; margin-bottom:24px; font-style:italic;">
                {conf:.1f} % success probability
              </div>
              <div style="height:2px; background:{P['rule']}; margin-bottom:4px;">
                <div style="height:100%; width:{bar_fill}%; background:{out_color};"></div>
              </div>
              <div style="display:flex; justify-content:space-between;">
                <span style="font-family:'DM Mono',monospace; font-size:8px; color:{P['faint']};">0%</span>
                <span style="font-family:'DM Mono',monospace; font-size:8px; color:{P['faint']};">100%</span>
              </div>
              <div style="margin-top:24px; padding-top:16px; border-top:1px solid {P['rule']};
                          font-family:'DM Mono',monospace; font-size:8px; color:{P['faint']};
                          line-height:2.0; letter-spacing:0.04em;">
                RandomForestClassifier · 100 estimators · max depth 5<br>
                70 / 30 stratified split · scikit-learn 1.2+
              </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("Insufficient data variance for classification. Broaden the filter selection.")


# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:baseline;
            padding:8px 0 32px; font-family:'DM Mono',monospace;">
  <div>
    <span style="font-size:10px; color:{P['ink2']}; letter-spacing:0.04em;">
      Project Alpha — Launch Economics
    </span>
    <span style="font-size:9px; color:{P['muted']}; margin-left:24px;">
      SpaceX Falcon 9 · Operational Economics Analysis · 2010 – 2021
    </span>
  </div>
  <div style="font-size:8px; color:{P['faint']}; text-align:right; letter-spacing:0.08em;">
    Python · Streamlit · Plotly · scikit-learn · 2026
  </div>
</div>
""", unsafe_allow_html=True)
