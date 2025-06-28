import streamlit as st
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Silver Slugger Awards at Catcher", layout="wide")
st.title("🏆 Silver Slugger Awards at Catcher (AL & NL)")

# Load data
team_df = pd.read_csv("silver_slugger_by_league.csv")
player_df = pd.read_csv("silver_slugger_by_player.csv")
full_df = pd.read_csv("silver_slugger_by_league.csv")  # for year range

# Extract year range
df_all = pd.read_csv("silver_slugger_by_league.csv")
year_min, year_max = df_all["Year"].astype(int).min(), df_all["Year"].astype(int).max()

# League and view mode selectors
league = st.selectbox("Select League", ["AL", "NL"])
view_mode = st.radio("View by", ["Team", "Player"], horizontal=True)

# Year range slider
selected_years = st.slider("Select Year Range", year_min, year_max, (year_min, year_max))
start_year, end_year = selected_years

# Apply year filtering
df_source = team_df if view_mode == "Team" else player_df
df_source["Year"] = df_source["Year"].astype(int)
filtered_df = df_source[
    (df_source["League"] == league) & 
    (df_source["Year"] >= start_year) & 
    (df_source["Year"] <= end_year)
]

# Recalculate groupings
group_field = "Team" if view_mode == "Team" else "Player"
agg_df = filtered_df.groupby(group_field).size().reset_index(name="Wins")
agg_df = agg_df.sort_values("Wins", ascending=False).head(10)

# Chart display
st.subheader(f"Top 10 {view_mode}s ({start_year} - {end_year})")
st.bar_chart(data=agg_df.set_index(group_field))

# Optional: add search
search = st.text_input(f"Search for a {view_mode.lower()} name:")
if search:
    search_df = filtered_df[filtered_df[group_field].str.contains(search, case=False, na=False)]
    st.subheader(f"Search Results for '{search}'")
    st.dataframe(search_df)

# Show full breakdown
st.subheader("📋 Award Breakdown")
st.dataframe(agg_df.reset_index(drop=True))
