import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# Ensure output directory exists
os.makedirs("images", exist_ok=True)

# Target Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_Silver_Slugger_Award_winners_at_catcher"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
tables = soup.find_all("table", {"class": "wikitable sortable"})

# Parse AL and NL tables
data = []
for idx, table in enumerate(tables):
    league = "AL" if idx == 0 else "NL"
    rows = table.find_all("tr")[1:]
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 3:
            raw_year = cols[0].get_text(strip=True)
            year = re.sub(r'\D', '', raw_year)
            if not year.isdigit():
                print(f"⚠️ Skipping invalid year: {raw_year}")
                continue

            # Clean Player name
            raw_player = cols[1].get_text(strip=True)
            player = re.sub(r"\(\d+\)", "", raw_player)  # remove (number)
            player = re.sub(r"[^\w\s.'-]", "", player)     # remove footnote characters/symbols
            player = player.strip()
            if raw_player != player:
                print(f"Sanitized Player: '{raw_player}' → '{player}'")

            team = cols[2].get_text(strip=True)
            data.append({"League": league, "Year": int(year), "Player": player, "Team": team})

# Create DataFrame
df = pd.DataFrame(data)

# Save full clean data
df.to_csv("silver_slugger_full_data.csv", index=False)

# Total awards per league
total_awards_per_league = df.groupby("League")["Year"].count().to_dict()

# === TEAM ANALYSIS ===
team_counts = df.groupby(["League", "Team"]).size().reset_index(name="Wins")
team_counts["Total_League_Awards"] = team_counts["League"].map(total_awards_per_league)
team_counts["Percentage_of_Total"] = (team_counts["Wins"] / team_counts["Total_League_Awards"] * 100).round(2)
team_counts.to_csv("silver_slugger_by_league.csv", index=False)

for league in ["AL", "NL"]:
    league_df = team_counts[team_counts["League"] == league].sort_values("Wins", ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    plt.bar(league_df["Team"], league_df["Percentage_of_Total"])
    plt.xticks(rotation=45, ha="right")
    plt.title(f"{league} - Top 10 Teams: Silver Sluggers at Catcher")
    plt.xlabel("Team")
    plt.ylabel("Percentage of League Total (%)")
    plt.tight_layout()
    plt.savefig(f"images/{league}_top_10_bar_chart.png")
    plt.close()

    plt.figure(figsize=(8, 8))
    plt.pie(league_df["Percentage_of_Total"], labels=league_df["Team"],
            autopct='%1.1f%%', startangle=140)
    plt.title(f"{league} - Top 10 Teams: Silver Sluggers at Catcher\n(% of League Total)")
    plt.tight_layout()
    plt.savefig(f"images/{league}_top_10_pie_chart.png")
    plt.close()

# === PLAYER ANALYSIS ===
player_counts = df.groupby(["League", "Player"]).size().reset_index(name="Wins")
player_counts["Total_League_Awards"] = player_counts["League"].map(total_awards_per_league)
player_counts["Percentage_of_Total"] = (player_counts["Wins"] / player_counts["Total_League_Awards"] * 100).round(2)
player_counts.to_csv("silver_slugger_by_player.csv", index=False)

for league in ["AL", "NL"]:
    league_df = player_counts[player_counts["League"] == league].sort_values("Wins", ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    plt.bar(league_df["Player"], league_df["Percentage_of_Total"])
    plt.xticks(rotation=45, ha="right")
    plt.title(f"{league} - Top Catchers by Silver Slugger Wins")
    plt.xlabel("Player")
    plt.ylabel("Percentage of League Total (%)")
    plt.tight_layout()
    plt.savefig(f"images/{league}_top_10_players_bar_chart.png")
    plt.close()

print("✅ All data and charts generated.")
