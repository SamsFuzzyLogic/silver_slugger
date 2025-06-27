import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("images", exist_ok=True)

url = "https://en.wikipedia.org/wiki/List_of_Silver_Slugger_Award_winners_at_catcher"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
tables = soup.find_all("table", {"class": "wikitable sortable"})

data = []
for idx, table in enumerate(tables):
    league = "AL" if idx == 0 else "NL"
    rows = table.find_all("tr")[1:]
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 3:
            year = cols[0].get_text(strip=True)
            player = cols[1].get_text(strip=True)
            team = cols[2].get_text(strip=True)
            data.append({"League": league, "Year": year, "Player": player, "Team": team})

df = pd.DataFrame(data)

total_awards_per_league = df.groupby("League")["Year"].count().to_dict()

league_team_counts = df.groupby(["League", "Team"]).size().reset_index(name="Wins")
league_team_counts["Total League Awards"] = league_team_counts["League"].map(total_awards_per_league)
league_team_counts["Percentage of Total"] = (
    league_team_counts["Wins"] / league_team_counts["Total_League_Awards"] * 100
).round(2)

league_team_counts.to_csv("silver_slugger_by_league.csv", index=False)

for league in ["AL", "NL"]:
    league_df = league_team_counts[league_team_counts["League"] == league].sort_values("Wins", ascending=False).head(10)

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

print("✅ Data and charts generated.")
