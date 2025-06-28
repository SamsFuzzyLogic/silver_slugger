import streamlit as st
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Silver Slugger Awards at Catcher", layout="wide")
st.title("🏆 Silver Slugger Awards at Catcher (AL & NL)")

# Load both CSV files
team_df = pd.read_csv("silver_slugger_by_league.csv")
player_df = pd.read_csv("silver_slugger_by_player.csv")

# User selects league
league = st.selectbox("Select League", ["AL", "NL"])

# User selects view mode
view_mode = st.radio("View by", ["Team", "Player"], horizontal=True)

# Determine appropriate dataframe and image paths
if view_mode == "Team":
    display_df = team_df[team_df["League"] == league].sort_values("Wins", ascending=False).head(10)
    bar_path = f"images/{league}_top_10_bar_chart.png"
    pie_path = f"images/{league}_top_10_pie_chart.png"
else:
    display_df = player_df[player_df["League"] == league].sort_values("Wins", ascending=False).head(10)
    bar_path = f"images/{league}_top_10_players_bar_chart.png"
    pie_path = None  # no pie chart for players in this version

# Layout: Bar chart and optional pie chart
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Top 10 - Bar Chart")
    if os.path.exists(bar_path):
        st.image(Image.open(bar_path), use_container_width=True)
    else:
        st.write("Bar chart not found.")

with col2:
    if view_mode == "Team" and pie_path and os.path.exists(pie_path):
        st.subheader("🥧 Top 10 Teams - Pie Chart")
        st.image(Image.open(pie_path), use_container_width=True)
    else:
        st.subheader("📋 Data Table")
        st.dataframe(display_df.reset_index(drop=True))

# Show data table below charts as well
if view_mode == "Team" and not pie_path:
    st.subheader("📋 Award Breakdown")
    st.dataframe(display_df.reset_index(drop=True))
elif view_mode == "Player":
    st.subheader("📋 Player Award Breakdown")
    st.dataframe(display_df.reset_index(drop=True))
