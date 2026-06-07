
import streamlit as st
import pandas as pd
import numpy as np
# Visualization libraries
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="⟁ Launch Economics: The Oracle of Reusability ⟁",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SACRED COLOR PALETTE
# ============================================================
SC = {
    'deep_void': '#0A0A1A',
    'nebula_purple': '#4A0E4E',
    'sacred_gold': '#D4AF37',
    'mystic_teal': '#0D7377',
    'organic_emerald': '#1B5E20',
    'dmt_coral': '#FF6B6B',
    'ethereal_blue': '#4FC3F7',
    'amber_resin': '#FF8F00',
    'sacred_crimson': '#B71C1C',
    'mushroom_ivory': '#FFF8E1',
    'forest_deep': '#1B4332',
    'lotus_pink': '#F8BBD0',
    'mandala_orange': '#FF5722',
    'crystal_cyan': '#00BCD4',
    'obsidian': '#1C1C1C',
}

# ============================================================
# CUSTOM CSS - SACRED NEO-BYZANTINE AESTHETIC
# ============================================================
st.markdown("""
<style>
    /* Main background - Deep Void */
    .stApp {
        background: linear-gradient(135deg, #0A0A1A 0%, #1A0A2E 50%, #0A1A1A 100%);
    }

    /* Sidebar */
    .css-1d391kg, .css-163ttbj {
        background: linear-gradient(180deg, #0A0A1A 0%, #1A0A2E 100%) !important;
    }

    /* Text colors */
    h1, h2, h3, h4, h5, h6 {
        color: #D4AF37 !important;
        font-family: 'Georgia', serif !important;
    }

    p, li, span {
        color: #FFF8E1 !important;
        font-family: 'Georgia', serif !important;
    }

    /* Metric cards */
    .stMetric {
        background: linear-gradient(135deg, #4A0E4E 0%, #1A0A2E 100%) !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3) !important;
    }

    .stMetric label {
        color: #D4AF37 !important;
        font-weight: bold !important;
    }

    .stMetric .css-1xarl3l {
        color: #FFF8E1 !important;
        font-size: 24px !important;
        font-weight: bold !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #4A0E4E 0%, #0D7377 100%) !important;
        color: #FFF8E1 !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 25px !important;
        font-family: 'Georgia', serif !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #D4AF37 0%, #FF8F00 100%) !important;
        color: #0A0A1A !important;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.6) !important;
        transform: translateY(-2px) !important;
    }

    /* Dataframe */
    .stDataFrame {
        background: #0A0A1A !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 10px !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #4A0E4E 0%, #1A0A2E 100%) !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 10px !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #0A0A1A !important;
        border-bottom: 2px solid #D4AF37 !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #FFF8E1 !important;
        background: #1A0A2E !important;
        border-radius: 10px 10px 0 0 !important;
        border: 1px solid #D4AF37 !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #D4AF37 0%, #FF8F00 100%) !important;
        color: #0A0A1A !important;
        font-weight: bold !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #0A0A1A;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #D4AF37 0%, #4A0E4E 100%);
        border-radius: 5px;
    }

    /* Info boxes */
    .stAlert {
        background: linear-gradient(135deg, #1A0A2E 0%, #4A0E4E 100%) !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 15px !important;
    }

    /* Selectbox, slider */
    .stSelectbox, .stSlider {
        background: #0A0A1A !important;
    }

    .stSelectbox > div > div {
        background: #1A0A2E !important;
        border: 1px solid #D4AF37 !important;
        color: #FFF8E1 !important;
    }

    /* Divider */
    hr {
        border: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #D4AF37 50%, transparent 100%);
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
# ============================================================
def load_data():
    """Load data from multiple possible locations."""
    import os
    from pathlib import Path

    possible_paths = [
        'data/spacex_raw.csv',                    # Local / repo root
        '../data/spacex_raw.csv',                 # If app is in app/ subdirectory
        'launch-economics/data/spacex_raw.csv',   # Streamlit Cloud mount path
        str(Path(__file__).parent.parent / 'data' / 'spacex_raw.csv'),  # Relative to script
    ]

    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            df['Date'] = pd.to_datetime(df['Date'])
            return df

    # If no local file, show error
    st.error("Data file not found. Please ensure 'data/spacex_raw.csv' exists in the repository.")
    st.stop()

df = load_data()


# ============================================================
# SIDEBAR - THE SACRED NAVIGATION
# ============================================================
st.sidebar.markdown("""
<div style="text-align: center; padding: 20px;">
    <h1 style="color: #D4AF37; font-size: 28px; margin-bottom: 10px;">⟁</h1>
    <h2 style="color: #D4AF37; font-size: 18px;">Launch Economics</h2>
    <p style="color: #FFF8E1; font-size: 12px; font-style: italic;">The Oracle of Reusability</p>
    <hr style="border-color: #D4AF37; margin: 15px 0;">
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, #4A0E4E 0%, #1A0A2E 100%); 
            padding: 15px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 20px;">
    <p style="color: #D4AF37; font-weight: bold; margin-bottom: 10px;">◈ Project Overview</p>
    <p style="color: #FFF8E1; font-size: 12px; line-height: 1.6;">
    A sacred analysis of SpaceX Falcon 9 operational economics (2010-2021), 
    exploring the alchemy of booster reusability, cost transformation, 
    and the mathematics of orbital liberation.
    </p>
</div>
""", unsafe_allow_html=True)

# Filters
st.sidebar.markdown("<p style='color: #D4AF37; font-weight: bold;'>◈ Temporal Filters</p>", unsafe_allow_html=True)
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(df['Year'].min()),
    max_value=int(df['Year'].max()),
    value=(2015, 2021),
    help="Filter launches by temporal horizon"
)

st.sidebar.markdown("<p style='color: #D4AF37; font-weight: bold; margin-top: 20px;'>◈ Orbital Filters</p>", unsafe_allow_html=True)
selected_orbits = st.sidebar.multiselect(
    "Select Orbits",
    options=sorted(df['Orbit'].unique()),
    default=sorted(df['Orbit'].unique()),
    help="Filter by orbital destination"
)

st.sidebar.markdown("<p style='color: #D4AF37; font-weight: bold; margin-top: 20px;'>◈ Booster State</p>", unsafe_allow_html=True)
reused_filter = st.sidebar.radio(
    "Booster Type",
    options=["All", "New Only", "Reused Only"],
    index=0,
    help="Filter by booster reusability state"
)

# Apply filters
filtered_df = df[
    (df['Year'] >= year_range[0]) & 
    (df['Year'] <= year_range[1]) &
    (df['Orbit'].isin(selected_orbits))
]

if reused_filter == "New Only":
    filtered_df = filtered_df[filtered_df['Reused'] == False]
elif reused_filter == "Reused Only":
    filtered_df = filtered_df[filtered_df['Reused'] == True]

# ============================================================
# MAIN CONTENT
# ============================================================
st.markdown("""
<div style="text-align: center; padding: 30px 0;">
    <h1 style="color: #D4AF37; font-size: 42px; margin-bottom: 10px; text-shadow: 0 0 30px rgba(212, 175, 55, 0.5);">
        ⟁ LAUNCH ECONOMICS ⟁
    </h1>
    <p style="color: #0D7377; font-size: 18px; font-style: italic; letter-spacing: 3px;">
        The Oracle of Reusability
    </p>
    <p style="color: #FFF8E1; font-size: 14px; margin-top: 15px;">
        A Sacred Analysis of SpaceX Falcon 9 Operational Economics (2010-2021)
    </p>
    <hr>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SACRED METRICS ROW
# ============================================================
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="⟁ Total Launches",
        value=f"{len(filtered_df)}",
        delta=f"{len(filtered_df[filtered_df['Success']==1])} successful" if len(filtered_df) > 0 else "0"
    )

with col2:
    success_rate = filtered_df['Success'].mean() * 100 if len(filtered_df) > 0 else 0
    st.metric(
        label="◈ Success Rate",
        value=f"{success_rate:.1f}%",
        delta=f"{len(filtered_df[filtered_df['Success']==0])} failures" if len(filtered_df) > 0 else "0"
    )

with col3:
    reused_count = filtered_df['Reused'].sum() if len(filtered_df) > 0 else 0
    st.metric(
        label="✦ Reused Boosters",
        value=f"{int(reused_count)}",
        delta=f"{reused_count/len(filtered_df)*100:.1f}% of total" if len(filtered_df) > 0 else "0%"
    )

with col4:
    avg_cost = filtered_df['CostPerKg'].mean() if len(filtered_df) > 0 else 0
    st.metric(
        label="◉ Avg Cost/kg",
        value=f"${avg_cost:,.0f}",
        delta=f"vs ${filtered_df['CompetitorCost'].mean()*1_000_000/filtered_df['PayloadMass'].mean():,.0f} competitor" if len(filtered_df) > 0 else "$0"
    )

with col5:
    total_savings = ((filtered_df['CompetitorCost'] - filtered_df['EstimatedCost']).sum()) if len(filtered_df) > 0 else 0
    st.metric(
        label="⚛ Total Savings",
        value=f"${total_savings:.0f}M",
        delta="vs traditional launch" if len(filtered_df) > 0 else ""
    )

st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================
# TABS - THE SACRED CHAMBERS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⟁ Temporal Oracle", 
    "◈ Cost Alchemy", 
    "✦ Reusability Mandala",
    "◉ Orbital Destiny",
    "⚛ Predictive Engine"
])

# ============================================================
# TAB 1: TEMPORAL ORACLE
# ============================================================
with tab1:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: #D4AF37;">⟁ The Temporal Oracle ⟁</h2>
        <p style="color: #0D7377; font-style: italic;">Chronicles of Launch Cadence & Success Evolution</p>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        # Timeline chart with Plotly
        yearly = filtered_df.groupby('Year').agg({
            'FlightNumber': 'count',
            'Success': 'mean',
            'CostPerKg': 'mean',
            'Reused': 'sum'
        }).reset_index()
        yearly.columns = ['Year', 'Launches', 'SuccessRate', 'AvgCostPerKg', 'ReusedCount']

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Launches bars
        fig.add_trace(
            go.Bar(
                x=yearly['Year'], y=yearly['Launches'],
                name='Launches',
                marker_color='#FF8F00',
                marker_line_color='#D4AF37',
                marker_line_width=2,
                opacity=0.8,
                text=yearly['Launches'],
                textposition='outside',
                textfont=dict(color='#FFF8E1', size=12)
            ),
            secondary_y=False
        )

        # Success rate line
        fig.add_trace(
            go.Scatter(
                x=yearly['Year'], y=yearly['SuccessRate']*100,
                name='Success Rate (%)',
                mode='lines+markers',
                line=dict(color='#00BCD4', width=3),
                marker=dict(size=10, color='#4FC3F7', line=dict(color='#D4AF37', width=2)),
                fill='tozeroy',
                fillcolor='rgba(0, 188, 212, 0.2)'
            ),
            secondary_y=True
        )

        fig.update_layout(
            title=dict(
                text='Launch Cadence & Success Evolution Over Time',
                font=dict(color='#D4AF37', size=20, family='Georgia'),
                x=0.5
            ),
            plot_bgcolor='#0A0A1A',
            paper_bgcolor='#0A0A1A',
            font=dict(color='#FFF8E1', family='Georgia'),
            legend=dict(
                bgcolor='rgba(74, 14, 78, 0.8)',
                bordercolor='#D4AF37',
                borderwidth=1,
                font=dict(color='#FFF8E1')
            ),
            xaxis=dict(
                gridcolor='rgba(212, 175, 55, 0.2)',
                linecolor='#D4AF37',
                tickfont=dict(color='#FFF8E1')
            ),
            yaxis=dict(
                title='Number of Launches',
                gridcolor='rgba(212, 175, 55, 0.2)',
                linecolor='#D4AF37',
                tickfont=dict(color='#FFF8E1')
            ),
            yaxis2=dict(
                title='Success Rate (%)',
                gridcolor='rgba(212, 175, 55, 0.1)',
                linecolor='#D4AF37',
                tickfont=dict(color='#FFF8E1'),
                range=[0, 105]
            ),
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4A0E4E 0%, #1A0A2E 100%); 
                    padding: 20px; border-radius: 15px; border: 1px solid #D4AF37;">
            <h3 style="color: #D4AF37; margin-bottom: 15px;">◈ Temporal Insights</h3>
            <ul style="color: #FFF8E1; line-height: 2;">
                <li><b>2015-2016:</b> The learning curve era. Success rates climbing from experimental to operational.</li>
                <li><b>2017-2018:</b> Reusability revolution begins. First reflown boosters slash costs dramatically.</li>
                <li><b>2019-2021:</b> Starlink constellation era. Launch cadence accelerates exponentially.</li>
            </ul>
            <p style="color: #0D7377; font-style: italic; margin-top: 15px;">
            "The temporal oracle reveals that reusability is not merely a cost reduction mechanism, 
            but a fundamental transformation of the aerospace economic paradigm."
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Quarterly breakdown
    st.markdown("<h3 style='color: #D4AF37; text-align: center; margin-top: 30px;'>◈ Quarterly Launch Distribution ◈</h3>", unsafe_allow_html=True)

    quarterly = filtered_df.groupby(['Year', 'Quarter']).size().reset_index(name='Count')
    quarterly['Period'] = quarterly['Year'].astype(str) + '-Q' + quarterly['Quarter'].astype(str)

    fig_q = go.Figure(data=[
        go.Bar(
            x=quarterly['Period'],
            y=quarterly['Count'],
            marker_color=quarterly['Count'],
            marker_colorscale=[[0, '#4A0E4E'], [0.5, '#FF8F00'], [1, '#00BCD4']],
            marker_line_color='#D4AF37',
            marker_line_width=1,
            text=quarterly['Count'],
            textposition='outside',
            textfont=dict(color='#FFF8E1')
        )
    ])

    fig_q.update_layout(
        plot_bgcolor='#0A0A1A',
        paper_bgcolor='#0A0A1A',
        font=dict(color='#FFF8E1', family='Georgia'),
        xaxis=dict(gridcolor='rgba(212, 175, 55, 0.2)', linecolor='#D4AF37', tickangle=45),
        yaxis=dict(gridcolor='rgba(212, 175, 55, 0.2)', linecolor='#D4AF37', title='Launches'),
        title=dict(text='Quarterly Launch Distribution', font=dict(color='#D4AF37', size=16), x=0.5)
    )

    st.plotly_chart(fig_q, use_container_width=True)

# ============================================================
# TAB 2: COST ALCHEMY
# ============================================================
with tab2:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: #D4AF37;">◈ The Cost Alchemy ◈</h2>
        <p style="color: #0D7377; font-style: italic;">Transmutation of Orbital Economics Through Reusability</p>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        # Scatter: Cost per kg over time
        fig = px.scatter(
            filtered_df, x='DaysSinceFirst', y='CostPerKg',
            color='Success', size='PayloadMass',
            hover_data=['FlightNumber', 'Date', 'Orbit', 'Reused'],
            color_continuous_scale=['#FF6B6B', '#00BCD4'],
            title='Cost Per Kilogram: The Descent Curve'
        )

        fig.update_layout(
            plot_bgcolor='#0A0A1A',
            paper_bgcolor='#0A0A1A',
            font=dict(color='#FFF8E1', family='Georgia'),
            title=dict(font=dict(color='#D4AF37', size=18), x=0.5),
            xaxis=dict(title='Days Since First Launch', gridcolor='rgba(212, 175, 55, 0.2)', linecolor='#D4AF37'),
            yaxis=dict(title='Cost Per Kg (USD)', gridcolor='rgba(212, 175, 55, 0.2)', linecolor='#D4AF37'),
            coloraxis_colorbar=dict(
                title='Success',
                tickvals=[0, 1],
                ticktext=['Failure', 'Success'],
                titlefont=dict(color='#FFF8E1'),
                tickfont=dict(color='#FFF8E1')
            )
        )

        # Add trend line
        z = np.polyfit(filtered_df['DaysSinceFirst'], filtered_df['CostPerKg'], 2)
        p = np.poly1d(z)
        x_line = np.linspace(filtered_df['DaysSinceFirst'].min(), filtered_df['DaysSinceFirst'].max(), 100)
        fig.add_trace(go.Scatter(
            x=x_line, y=p(x_line),
            mode='lines',
            line=dict(color='#D4AF37', width=3, dash='dash'),
            name='Trend (Polynomial)',
            showlegend=True
        ))

        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        # Cost comparison boxes
        new_cost = filtered_df[filtered_df['Reused']==False]['CostPerKg'].mean() if len(filtered_df[filtered_df['Reused']==False]) > 0 else 0
        reused_cost = filtered_df[filtered_df['Reused']==True]['CostPerKg'].mean() if len(filtered_df[filtered_df['Reused']==True]) > 0 else 0
        competitor_cost = filtered_df['CompetitorCost'].mean() * 1_000_000 / filtered_df['PayloadMass'].mean() if len(filtered_df) > 0 else 0

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4A0E4E 0%, #1A0A2E 100%); 
                    padding: 20px; border-radius: 15px; border: 1px solid #D4AF37; margin-bottom: 20px;">
            <h3 style="color: #D4AF37; margin-bottom: 15px;">◉ Cost Comparison</h3>
            <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                <div style="text-align: center; flex: 1;">
                    <p style="color: #FF6B6B; font-size: 12px; margin-bottom: 5px;">New Booster</p>
                    <p style="color: #FFF8E1; font-size: 24px; font-weight: bold;">${new_cost:,.0f}</p>
                    <p style="color: #FFF8E1; font-size: 10px;">per kg</p>
                </div>
                <div style="text-align: center; flex: 1;">
                    <p style="color: #00BCD4; font-size: 12px; margin-bottom: 5px;">Reused Booster</p>
                    <p style="color: #FFF8E1; font-size: 24px; font-weight: bold;">${reused_cost:,.0f}</p>
                    <p style="color: #FFF8E1; font-size: 10px;">per kg</p>
                </div>
                <div style="text-align: center; flex: 1;">
                    <p style="color: #D4AF37; font-size: 12px; margin-bottom: 5px;">Competitor Avg</p>
                    <p style="color: #FFF8E1; font-size: 24px; font-weight: bold;">${competitor_cost:,.0f}</p>
                    <p style="color: #FFF8E1; font-size: 10px;">per kg</p>
                </div>
            </div>
            <hr style="border-color: #D4AF37; margin: 15px 0;">
            <p style="color: #0D7377; font-style: italic; text-align: center;">
            Savings with reuse: <b style="color: #D4AF37;">{((new_cost - reused_cost)/new_cost*100):.1f}%</b> reduction
            </p>
            <p style="color: #0D7377; font-style: italic; text-align: center;">
            vs Competitors: <b style="color: #D4AF37;">{((competitor_cost - reused_cost)/competitor_cost*100):.1f}%</b> reduction
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Savings over time
        filtered_sorted = filtered_df.sort_values('Date')
        filtered_sorted['CumulativeSavings'] = (filtered_sorted['CompetitorCost'] - filtered_sorted['EstimatedCost']).cumsum()

        fig_savings = go.Figure(data=[
            go.Scatter(
                x=filtered_sorted['Date'],
                y=filtered_sorted['CumulativeSavings'],
                mode='lines',
                fill='tozeroy',
                line=dict(color='#D4AF37', width=3),
                fillcolor='rgba(212, 175, 55, 0.2)',
                name='Cumulative Savings'
            )
        ])

        fig_savings.update_layout(
            plot_bgcolor='#0A0A1A',
            paper_bgcolor='#0A0A1A',
            font=dict(color='#FFF8E1', family='Georgia'),
            title=dict(text='Cumulative Economic Liberation', font=dict(color='#D4AF37', size=16), x=0.5),
            xaxis=dict(gridcolor='rgba(212, 175, 55, 0.2)', linecolor='#D4AF37'),
            yaxis=dict(gridcolor='rgba(212, 175, 55, 0.2)', linecolor='#D4AF37', title='Savings (Million USD)')
        )

        st.plotly_chart(fig_savings, use_container_width=True)

# ============================================================
# TAB 3: REUSABILITY MANDALA
# ============================================================
with tab3:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: #D4AF37;">✦ The Reusability Mandala ✦</h2>
        <p style="color: #0D7377; font-style: italic;">Sacred Geometry of Booster Lifecycle Economics</p>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 3])

    with col_left:
        # Reuse count distribution
        reuse_dist = filtered_df['ReusedCount'].value_counts().sort_index()

        fig_reuse = go.Figure(data=[
            go.Bar(
                x=reuse_dist.index,
                y=reuse_dist.values,
                marker_color=reuse_dist.values,
                marker_colorscale=[[0, '#4A0E4E'], [0.5, '#FF8F00'], [1, '#00BCD4']],
                marker_line_color='#D4AF37',
                marker_line_width=2,
                text=reuse_dist.values,
                textposition='outside',
                textfont=dict(color='#FFF8E1')
            )
        ])

        fig_reuse.update_layout(
            plot_bgcolor='#0A0A1A',
            paper_bgcolor='#0A0A1A',
            font=dict(color='#FFF8E1', family='Georgia'),
            title=dict(text='Distribution by Reuse Count', font=dict(color='#D4AF37', size=16), x=0.5),
            xaxis=dict(title='Times Reused', gridcolor='rgba(212, 175, 55, 0.2)', linecolor='#D4AF37'),
            yaxis=dict(title='Number of Flights', gridcolor='rgba(212, 175, 55, 0.2)', linecolor='#D4AF37')
        )

        st.plotly_chart(fig_reuse, use_container_width=True)

        # Success by reuse
        reuse_success = filtered_df.groupby('ReusedCount').agg({
            'Success': 'mean',
            'FlightNumber': 'count'
        }).reset_index()

        fig_rs = go.Figure(data=[
            go.Scatter(
                x=reuse_success['ReusedCount'],
                y=reuse_success['Success']*100,
                mode='lines+markers',
                line=dict(color='#00BCD4', width=3),
                marker=dict(size=15, color='#4FC3F7', line=dict(color='#D4AF37', width=2)),
                name='Success Rate'
            )
        ])

        fig_rs.update_layout(
            plot_bgcolor='#0A0A1A',
            paper_bgcolor='#0A0A1A',
            font=dict(color='#FFF8E1', family='Georgia'),
            title=dict(text='Success Rate by Reuse Count', font=dict(color='#D4AF37', size=16), x=0.5),
            xaxis=dict(title='Times Reused', gridcolor='rgba(212, 175, 55, 0.2)', linecolor='#D4AF37'),
            yaxis=dict(title='Success Rate (%)', gridcolor='rgba(212, 175, 55, 0.2)', linecolor='#D4AF37', range=[0, 105])
        )

        st.plotly_chart(fig_rs, use_container_width=True)

    with col_right:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4A0E4E 0%, #1A0A2E 100%); 
                    padding: 25px; border-radius: 15px; border: 1px solid #D4AF37;">
            <h3 style="color: #D4AF37; margin-bottom: 20px;">✦ The Sacred Doctrine of Reuse</h3>

            <p style="color: #FFF8E1; line-height: 2; margin-bottom: 15px;">
            <b style="color: #D4AF37;">1. The First Principle:</b> Each reuse cycle reduces marginal cost 
            by amortizing manufacturing capital across multiple missions. The booster becomes not a 
            consumable, but a <i>capital asset</i> with depreciable life.
            </p>

            <p style="color: #FFF8E1; line-height: 2; margin-bottom: 15px;">
            <b style="color: #D4AF37;">2. The Learning Curve:</b> Success rates improve with each reuse 
            iteration, suggesting operational refinement and predictive maintenance maturation.
            </p>

            <p style="color: #FFF8E1; line-height: 2; margin-bottom: 15px;">
            <b style="color: #D4AF37;">3. The Economic Threshold:</b> Beyond the 5th reuse, cost per 
            kilogram approaches an asymptotic minimum, fundamentally restructuring the economics 
            of space access.
            </p>

            <hr style="border-color: #D4AF37; margin: 20px 0;">

            <p style="color: #0D7377; font-style: italic; text-align: center; font-size: 14px;">
            "The booster that flies ten times is not merely ten times cheaper—<br>
            it is the manifestation of a new economic ontology."
            </p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# TAB 4: ORBITAL DESTINY
# ============================================================
with tab4:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: #D4AF37;">◉ Orbital Destiny ◉</h2>
        <p style="color: #0D7377; font-style: italic;">Success Patterns Across the Celestial Sphere</p>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        # Orbit success rates
        orbit_stats = filtered_df.groupby('Orbit').agg({
            'Success': 'mean',
            'FlightNumber': 'count',
            'PayloadMass': 'mean',
            'CostPerKg': 'mean'
        }).reset_index()
        orbit_stats = orbit_stats.sort_values('Success', ascending=True)

        colors_orbit = ['#FF6B6B' if x < 0.8 else '#FF8F00' if x < 0.9 else '#00BCD4' 
                       for x in orbit_stats['Success']]

        fig_orbit = go.Figure(data=[
            go.Bar(
                y=orbit_stats['Orbit'],
                x=orbit_stats['Success']*100,
                orientation='h',
                marker_color=colors_orbit,
                marker_line_color='#D4AF37',
                marker_line_width=2,
                text=[f"{x*100:.1f}% (n={y})" for x, y in zip(orbit_stats['Success'], orbit_stats['FlightNumber'])],
                textposition='outside',
                textfont=dict(color='#FFF8E1')
            )
        ])

        fig_orbit.update_layout(
            plot_bgcolor='#0A0A1A',
            paper_bgcolor='#0A0A1A',
            font=dict(color='#FFF8E1', family='Georgia'),
            title=dict(text='Success Rate by Orbital Destination', font=dict(color='#D4AF37', size=16), x=0.5),
            xaxis=dict(title='Success Rate (%)', gridcolor='rgba(212, 175, 55, 0.2)', linecolor='#D4AF37', range=[0, 105]),
            yaxis=dict(gridcolor='rgba(212, 175, 55, 0.2)', linecolor='#D4AF37')
        )

        st.plotly_chart(fig_orbit, use_container_width=True)

    with col_right:
        # Payload mass by orbit
        fig_payload = go.Figure()

        for orbit in sorted(filtered_df['Orbit'].unique()):
            orbit_data = filtered_df[filtered_df['Orbit'] == orbit]
            fig_payload.add_trace(go.Box(
                y=orbit_data['PayloadMass'],
                name=orbit,
                boxpoints='all',
                jitter=0.3,
                pointpos=-1.8,
                marker=dict(color='#D4AF37', size=6),
                line=dict(color='#00BCD4', width=2),
                fillcolor='rgba(0, 188, 212, 0.2)'
            ))

        fig_payload.update_layout(
            plot_bgcolor='#0A0A1A',
            paper_bgcolor='#0A0A1A',
            font=dict(color='#FFF8E1', family='Georgia'),
            title=dict(text='Payload Mass Distribution by Orbit', font=dict(color='#D4AF37', size=16), x=0.5),
            yaxis=dict(title='Payload Mass (kg)', gridcolor='rgba(212, 175, 55, 0.2)', linecolor='#D4AF37'),
            xaxis=dict(gridcolor='rgba(212, 175, 55, 0.2)', linecolor='#D4AF37')
        )

        st.plotly_chart(fig_payload, use_container_width=True)

    # Launch site map
    st.markdown("<h3 style='color: #D4AF37; text-align: center; margin-top: 30px;'>◈ The Three Sacred Temples ◈</h3>", unsafe_allow_html=True)

    site_stats = filtered_df.groupby('LaunchSite').agg({
        'FlightNumber': 'count',
        'Success': 'mean',
        'Latitude': 'first',
        'Longitude': 'first'
    }).reset_index()

    fig_map = px.scatter_geo(
        site_stats,
        lat='Latitude',
        lon='Longitude',
        size='FlightNumber',
        color='Success',
        hover_name='LaunchSite',
        hover_data=['FlightNumber', 'Success'],
        color_continuous_scale=['#FF6B6B', '#FF8F00', '#00BCD4'],
        projection='natural earth',
        title='Launch Sites: The Sacred Geography'
    )

    fig_map.update_layout(
        geo=dict(
            bgcolor='#0A0A1A',
            landcolor='#1B4332',
            oceancolor='#0A0A1A',
            coastlinecolor='#D4AF37',
            countrycolor='#D4AF37',
            showland=True,
            showocean=True,
            showcoastlines=True,
            showcountries=True,
            countrywidth=0.5,
            coastlinewidth=0.5
        ),
        paper_bgcolor='#0A0A1A',
        font=dict(color='#FFF8E1', family='Georgia'),
        title=dict(font=dict(color='#D4AF37', size=16), x=0.5)
    )

    st.plotly_chart(fig_map, use_container_width=True)

# ============================================================
# TAB 5: PREDICTIVE ENGINE
# ============================================================
with tab5:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: #D4AF37;">⚛ The Predictive Engine ⚛</h2>
        <p style="color: #0D7377; font-style: italic;">Machine Learning Oracle for Mission Prognostication</p>
    </div>
    """, unsafe_allow_html=True)

    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, confusion_matrix
    import plotly.figure_factory as ff

    # Prepare features
    feature_df = filtered_df.copy()
    feature_df['Orbit_LEO'] = (feature_df['Orbit'] == 'LEO').astype(int)
    feature_df['Orbit_GTO'] = (feature_df['Orbit'] == 'GTO').astype(int)
    feature_df['Orbit_ISS'] = (feature_df['Orbit'] == 'ISS').astype(int)
    feature_df['Orbit_PO'] = (feature_df['Orbit'] == 'PO').astype(int)
    feature_df['Orbit_SSO'] = (feature_df['Orbit'] == 'SSO').astype(int)
    feature_df['Orbit_MEO'] = (feature_df['Orbit'] == 'MEO').astype(int)

    features = ['PayloadMass', 'ReusedCount', 'Block', 'DaysSinceFirst', 
                'Orbit_LEO', 'Orbit_GTO', 'Orbit_ISS', 'Orbit_PO', 'Orbit_SSO', 'Orbit_MEO']
    X = feature_df[features]
    y = feature_df['Success']

    if len(X) > 10 and y.nunique() > 1:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

        model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        col_left, col_right = st.columns([2, 3])

        with col_left:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4A0E4E 0%, #1A0A2E 100%); 
                        padding: 20px; border-radius: 15px; border: 1px solid #D4AF37;">
                <h3 style="color: #D4AF37; margin-bottom: 15px;">◈ Model Performance</h3>
                <p style="color: #FFF8E1; line-height: 2;">
                <b>Algorithm:</b> Random Forest Classifier<br>
                <b>Training Samples:</b> {}<br>
                <b>Test Samples:</b> {}<br>
                <b>Accuracy:</b> {:.1%}<br>
                <b>Precision:</b> {:.1%}<br>
                <b>Recall:</b> {:.1%}<br>
                <b>F1-Score:</b> {:.1%}
                </p>
            </div>
            """.format(
                len(X_train), len(X_test),
                (y_pred == y_test).mean(),
                (y_pred[y_test==1] == 1).mean() if sum(y_test==1) > 0 else 0,
                (y_pred[y_test==1] == 1).sum() / y_test.sum() if y_test.sum() > 0 else 0,
                2 * ((y_pred[y_test==1] == 1).sum() / y_test.sum()) * ((y_pred[y_test==1] == 1).mean()) / 
                (((y_pred[y_test==1] == 1).sum() / y_test.sum()) + ((y_pred[y_test==1] == 1).mean())) 
                if y_test.sum() > 0 and (y_pred[y_test==1] == 1).mean() > 0 else 0
            ), unsafe_allow_html=True)

            # Feature importance
            importance = pd.DataFrame({
                'Feature': features,
                'Importance': model.feature_importances_
            }).sort_values('Importance', ascending=True)

            fig_imp = go.Figure(data=[
                go.Bar(
                    y=importance['Feature'],
                    x=importance['Importance'],
                    orientation='h',
                    marker_color=importance['Importance'],
                    marker_colorscale=[[0, '#4A0E4E'], [0.5, '#FF8F00'], [1, '#00BCD4']],
                    marker_line_color='#D4AF37',
                    marker_line_width=1,
                    text=[f"{x:.3f}" for x in importance['Importance']],
                    textposition='outside',
                    textfont=dict(color='#FFF8E1')
                )
            ])

            fig_imp.update_layout(
                plot_bgcolor='#0A0A1A',
                paper_bgcolor='#0A0A1A',
                font=dict(color='#FFF8E1', family='Georgia'),
                title=dict(text='Feature Importance', font=dict(color='#D4AF37', size=14), x=0.5),
                xaxis=dict(gridcolor='rgba(212, 175, 55, 0.2)', linecolor='#D4AF37'),
                yaxis=dict(gridcolor='rgba(212, 175, 55, 0.2)', linecolor='#D4AF37')
            )

            st.plotly_chart(fig_imp, use_container_width=True)

        with col_right:
            # Interactive prediction
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4A0E4E 0%, #1A0A2E 100%); 
                        padding: 20px; border-radius: 15px; border: 1px solid #D4AF37;">
                <h3 style="color: #D4AF37; margin-bottom: 15px;">⚛ Mission Prognosticator</h3>
                <p style="color: #FFF8E1; margin-bottom: 20px;">
                Configure mission parameters to receive the oracle's prediction.
                </p>
            </div>
            """, unsafe_allow_html=True)

            col_p1, col_p2, col_p3 = st.columns(3)

            with col_p1:
                pred_payload = st.slider("Payload Mass (kg)", 0, 16000, 5000, 100)
                pred_reuse = st.slider("Reuse Count", 0, 10, 2, 1)

            with col_p2:
                pred_block = st.slider("Block Version", 1, 5, 4, 1)
                pred_days = st.slider("Days Since First Launch", 0, 4000, 2000, 100)

            with col_p3:
                pred_orbit = st.selectbox("Orbital Destination", 
                                         ['LEO', 'GTO', 'ISS', 'PO', 'SSO', 'MEO'])

            # Create prediction input
            pred_input = np.zeros(len(features))
            pred_input[0] = pred_payload
            pred_input[1] = pred_reuse
            pred_input[2] = pred_block
            pred_input[3] = pred_days

            orbit_map = {'LEO': 4, 'GTO': 5, 'ISS': 6, 'PO': 7, 'SSO': 8, 'MEO': 9}
            pred_input[orbit_map[pred_orbit]] = 1

            pred_proba = model.predict_proba([pred_input])[0]
            pred_class = model.predict([pred_input])[0]

            st.markdown("<hr>", unsafe_allow_html=True)

            if pred_class == 1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1B5E20 0%, #0D7377 100%); 
                            padding: 30px; border-radius: 20px; border: 2px solid #00BCD4;
                            text-align: center; margin-top: 20px;">
                    <h2 style="color: #00BCD4; font-size: 36px; margin-bottom: 10px;">✦ SUCCESS PROBABLE ✦</h2>
                    <p style="color: #FFF8E1; font-size: 24px; font-weight: bold;">{pred_proba[1]*100:.1f}% Confidence</p>
                    <p style="color: #0D7377; font-style: italic; margin-top: 15px;">
                    The oracle foresees a successful landing. Mission parameters align with historical success patterns.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #4A0000 0%, #B71C1C 100%); 
                            padding: 30px; border-radius: 20px; border: 2px solid #FF6B6B;
                            text-align: center; margin-top: 20px;">
                    <h2 style="color: #FF6B6B; font-size: 36px; margin-bottom: 10px;">⚠ CAUTION ADVISED ⚠</h2>
                    <p style="color: #FFF8E1; font-size: 24px; font-weight: bold;">{pred_proba[0]*100:.1f}% Risk</p>
                    <p style="color: #FFF8E1; font-style: italic; margin-top: 15px;">
                    The oracle detects elevated risk parameters. Consider mission refinement.
                    </p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠ Insufficient data diversity for predictive modeling. Adjust filters to include more varied outcomes.")

# ============================================================
# FOOTER
# ============================================================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 30px 0;">
    <p style="color: #D4AF37; font-size: 14px; letter-spacing: 3px;">⟁ PROJECT ALPHA: LAUNCH ECONOMICS ⟁</p>
    <p style="color: #0D7377; font-size: 12px; font-style: italic;">
    A Sacred Analysis of SpaceX Falcon 9 Operational Economics | Data Science Portfolio 2026
    </p>
    <p style="color: #4A0E4E; font-size: 10px; margin-top: 10px;">
    Built with Python, Streamlit, Plotly & Sacred Geometry
    </p>
</div>
""", unsafe_allow_html=True)
