import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hotel Review Dashboard", layout="wide")
st.title("🏨 Hotel Review Sentiment Analyzer Dashboard")

# Load output file
try:
    df = pd.read_csv("output/results.csv")
except FileNotFoundError:
    st.error("❌ Output file not found. Please run `main.py` first to generate results.")
    st.stop()

# Sidebar filters
st.sidebar.header("📊 Filters")
sentiment_filter = st.sidebar.multiselect("Filter by Sentiment", df["Sentiment"].dropna().unique())
topic_input = st.sidebar.text_input("Filter by Topics (comma-separated)", "")

# Apply filters
filtered_df = df.copy()

if sentiment_filter:
    filtered_df = filtered_df[filtered_df["Sentiment"].isin(sentiment_filter)]

if topic_input:
    topic_list = [t.strip().lower() for t in topic_input.split(",") if t.strip()]
    filtered_df = filtered_df[filtered_df["Topics"].fillna("").astype(str).str.lower().apply(
        lambda x: any(t in x for t in topic_list)
    )]

# Show filtered results
st.markdown("### 🔍 Filtered Reviews")
st.dataframe(filtered_df, use_container_width=True)

# Sentiment Distribution Chart
st.markdown("### 📈 Sentiment Distribution")
sentiment_counts = filtered_df["Sentiment"].value_counts()

if sentiment_counts.empty:
    st.info("No sentiment data available for the current filters.")
else:
    st.bar_chart(sentiment_counts)

# Topic Frequency Chart
st.markdown("### 📌 Top Topics Mentioned")
topic_series = filtered_df["Topics"].dropna().astype(str).str.split(", ")
exploded_topics = topic_series.explode().str.strip()
topic_counts = exploded_topics.value_counts().head(10)

if topic_counts.empty:
    st.info("No topic data available for the current filters.")
else:
    st.bar_chart(topic_counts)
