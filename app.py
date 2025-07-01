import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Silver Slugger Awards at Catcher", layout="wide")
st.title("🏆 Silver Slugger Awards at Catcher (AL & NL)")

# Load full dataset (not pre-aggregated)
df = pd.read_csv("silver_slugger_full_data.csv")

# Get year range
year_min, year_max = df["Year"].min(), df["Year"].max()

# Controls
league = st.selectbox("Select League", ["AL", "NL"])
view_mode = st.radio("View by", ["Team", "Player"], horizontal=True)
selected_years = st.slider("Select Year Range", year_min, year_max, (year_min, year_max))
start_year, end_year = selected_years

# Determine group field
group_field = "Team" if view_mode == "Team" else "Player"

# Filter by year and league
filtered_df = df[
    (df["League"] == league) & 
    (df["Year"] >= start_year) & 
    (df["Year"] <= end_year)
]

# Aggregate
agg_df = filtered_df.groupby(group_field).size().reset_index(name="Wins")
agg_df = agg_df.sort_values("Wins", ascending=False).head(10)

# Altair bar chart
st.subheader(f"Top 10 {view_mode}s ({start_year}-{end_year}) - {league}")
bar_chart = alt.Chart(agg_df).mark_bar().encode(
    x=alt.X(group_field, sort='-y'),
    y='Wins'
).properties(width=700, height=400)
st.altair_chart(bar_chart)

# Optional search
search = st.text_input(f"Search {view_mode}s:")
if search:
    result_df = filtered_df[filtered_df[group_field].str.contains(search, case=False, na=False)]
    st.subheader(f"Results for '{search}'")
    st.dataframe(result_df.reset_index(drop=True))

# Final table
st.subheader("Award Breakdown")
st.table(agg_df.reset_index(drop=True))


