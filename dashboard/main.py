import streamlit as st
import sqlite3
import pandas as pd
import os
import plotly.express as px
import datetime

# Page config
st.set_page_config(
    page_title="Stock Sentiment Dashboard",
    layout="wide",
    page_icon="📈"
)

# Database connection
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ticker_analysis.db')
conn = sqlite3.connect(DB_PATH)

# Load all data

df = pd.read_sql_query("SELECT * FROM mentions ORDER BY timestamp DESC", conn)
conn.close()

# Normalize sentiment column to lowercase for consistency
if 'sentiment' in df.columns:
    df['sentiment'] = df['sentiment'].astype(str).str.lower()

# Sentiment icons (keep keys lowercase)
SENTIMENT_ICONS = {
    'bullish': '🟢',
    'bearish': '🔴', 
    'neutral': '⚪'
}

# Sidebar filters
st.sidebar.header("Filters")

# Date filter: default last month
min_date = pd.to_datetime(df['video_published']).min()
max_date = pd.to_datetime(df['video_published']).max()
def_last_month = (max_date - pd.DateOffset(months=1)).date() if not pd.isnull(max_date) else datetime.date.today()
default_date = max(def_last_month, min_date.date()) if not pd.isnull(min_date) else datetime.date.today()

selected_date = st.sidebar.date_input(
    "Show mentions from (>=)",
    value=default_date,
    min_value=min_date.date() if not pd.isnull(min_date) else datetime.date.today(),
    max_value=max_date.date() if not pd.isnull(max_date) else datetime.date.today()
)

selected_ticker = st.sidebar.selectbox(
    "Select Ticker", 
    ['All'] + sorted(df['ticker'].unique())
)

selected_provider = st.sidebar.multiselect(
    "AI Provider",
    options=df['ai_provider'].unique(),
    default=df['ai_provider'].unique()
)

selected_sentiment = st.sidebar.multiselect(
    "Sentiment",
    options=['bullish', 'bearish', 'neutral'],
    default=['bullish', 'bearish', 'neutral']
)

# Debug toggle
DEBUG = st.sidebar.checkbox("Show debug", value=False)

if DEBUG:
    st.write("DEBUG: Dati caricati dal DB", df)
    st.write("DEBUG: selected_ticker", selected_ticker)
    st.write("DEBUG: selected_provider", selected_provider)
    st.write("DEBUG: selected_sentiment", selected_sentiment)
    st.write("DEBUG: unique tickers", df['ticker'].unique())
    st.write("DEBUG: unique ai_provider", df['ai_provider'].unique())
    st.write("DEBUG: unique sentiment", df['sentiment'].unique())
    st.write("DEBUG: selected_date", selected_date)

# Apply filters
filtered_df = df.copy()
if DEBUG:
    st.write("DEBUG: after copy", filtered_df)

# Apply date filter (>= selected_date)
filtered_df = filtered_df[pd.to_datetime(filtered_df['video_published']).dt.date >= selected_date]
if DEBUG:
    st.write("DEBUG: after date filter", filtered_df)

if selected_ticker != 'All':
    filtered_df = filtered_df[filtered_df['ticker'] == selected_ticker]
    if DEBUG:
        st.write("DEBUG: after ticker filter", filtered_df)

filtered_df = filtered_df[filtered_df['ai_provider'].isin(selected_provider)]
if DEBUG:
    st.write("DEBUG: after provider filter", filtered_df)

# Apply sentiment filter (now all lowercase)
filtered_df = filtered_df[filtered_df['sentiment'].isin(selected_sentiment)]
if DEBUG:
    st.write("DEBUG: after sentiment filter", filtered_df)

# Add sentiment icons
filtered_df['sentiment_icon'] = filtered_df['sentiment'].map(SENTIMENT_ICONS)

# Main dashboard
st.title("📈 Stock Sentiment Analysis Dashboard")

# Metrics row
col1, col2, col3 = st.columns(3)
col1.metric("Total Mentions", len(filtered_df))
col2.metric("Unique Tickers", filtered_df['ticker'].nunique())
col3.metric("Providers Used", ", ".join(filtered_df['ai_provider'].unique()))

# Tabs for different views
tab1, tab2 = st.tabs(["Detailed View", "Aggregated Analysis"])

with tab1:
    # Detailed mentions view
    st.subheader("Recent Mentions")
    for _, row in filtered_df.iterrows():
        with st.expander(f"{row['sentiment_icon']} {row['ticker']} - {row['video_title']}"):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric("Sentiment", row['sentiment'])
                st.caption(f"Source: {row['channel']}")
                st.caption(f"Analyzed by: {row['ai_provider']}")
                st.caption(f"Date: {pd.to_datetime(row['timestamp']).strftime('%Y-%m-%d %H:%M')}")
            with col2:
                st.write("**Summary:**")
                st.info(row['summary'])

with tab2:
    # Aggregated analysis
    st.subheader("Ticker Sentiment Aggregation")
    
    # Grouped data
    grouped = filtered_df.groupby(['ticker', 'sentiment']).size().reset_index(name='count')
    pivot_df = grouped.pivot(index='ticker', columns='sentiment', values='count').fillna(0)
    
    # Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Sentiment Distribution by Ticker**")
        fig = px.bar(
            grouped,
            x='ticker',
            y='count',
            color='sentiment',
            color_discrete_map={
                'bullish': 'green',
                'bearish': 'red',
                'neutral': 'gray'
            },
            labels={'count': 'Number of Mentions'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**Sentiment Heatmap**")
        fig = px.imshow(
            pivot_df,
            labels=dict(x="Sentiment", y="Ticker", color="Mentions"),
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Raw data table
    st.write("**Detailed Aggregation Data**")
    grouped['sentiment_icon'] = grouped['sentiment'].map(SENTIMENT_ICONS)
    st.dataframe(
        grouped.sort_values(['ticker', 'count'], ascending=[True, False]),
        column_config={
            "sentiment_icon": st.column_config.Column(
                "Sentiment",
                help="Sentiment indicator",
                width="small"
            ),
            "count": st.column_config.NumberColumn(
                "Mentions",
                help="Number of mentions",
                format="%d"
            )
        },
        hide_index=True,
        use_container_width=True
    )

# Add some styling
st.markdown("""
<style>
    .stExpander {
        border-left: 3px solid #4e79a7;
        border-radius: 4px;
    }
    .st-b7 {
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)