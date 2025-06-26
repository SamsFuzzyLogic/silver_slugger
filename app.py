import streamlit as st
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Silver Slugger Awards at Catcher", layout="wide")

st.title("🏆 Silver Slugger Awards at Catcher (AL & NL)")

df = pd.read_csv("silver_slugger_by_league.csv")

league = st.selectbox("Select League", ["AL", "NL"])

league_df = df[df["League"] == league].sort_values("Wins", ascending=False).head(10)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Top 10 Teams - Bar Chart")
    bar_path = f"images/{league}_top_10_bar_chart.png"
    if os.path.exists(bar_path):
        st.image(Image.open(bar_path), use_column_width=True)

with col2:
    st.subheader("🥧 Top 10 Teams - Pie Chart")
    pie_path = f"images/{league}_top_10_pie_chart.png"
    if os.path.exists(pie_path):
        st.image(Image.open(pie_path), use_column_width=True)

st.subheader("📋 Award Breakdown")
st.dataframe(league_df.reset_index(drop=True))
