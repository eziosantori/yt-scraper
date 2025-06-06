import streamlit as st
import sqlite3
import pandas as pd
import os

# Set page configuration
st.set_page_config(page_title="Stock Ticker Monitor", layout="wide")

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ticker_analysis.db')

# Connect to database
conn = sqlite3.connect(DB_PATH)
# Read data into DataFrame
df = pd.read_sql_query("SELECT * FROM mentions ORDER BY timestamp DESC", conn)
conn.close()

# Sidebar filters
st.sidebar.header("Filters")
selected_ticker = st.sidebar.selectbox("Select Ticker", ['All'] + sorted(df['ticker'].unique()))
selected_sentiment = st.sidebar.multiselect(
    "Sentiment", 
    options=['bullish', 'bearish', 'neutral'], 
    default=['bullish', 'bearish', 'neutral']
)

# Apply filters
filtered_df = df.copy()
if selected_ticker != 'All':
    filtered_df = filtered_df[filtered_df['ticker'] == selected_ticker]
filtered_df = filtered_df[filtered_df['sentiment'].isin(selected_sentiment)]

# Main layout
st.title("📈 Stock Ticker Analysis Dashboard")
st.markdown(f"**Total Mentions Found:** {len(filtered_df)}")

# Add sentiment icons for visual distinction
sentiment_icons = {
    'bullish': '🟢',  # Green circle
    'bearish': '🔴',  # Red circle
    'neutral': '⚪'   # White circle
}
filtered_df['sentiment_icon'] = filtered_df['sentiment'].map(sentiment_icons)

# Display each mention in an expandable section
for _, row in filtered_df.iterrows():
    with st.expander(f"{row['sentiment_icon']} {row['ticker']} - {row['video_title']}"):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric("Sentiment", row['sentiment'])
            st.caption(f"Channel: {row['channel']}")
            st.caption(f"Date: {pd.to_datetime(row['timestamp']).strftime('%Y-%m-%d %H:%M')}")
        with col2:
            st.write("**Summary:**")
            st.info(row['summary'])