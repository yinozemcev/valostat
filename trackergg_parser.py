import requests
from bs4 import BeautifulSoup

from time import sleep
import csv


stat_names = ("WinPercentage", "KDRatio", "Playtime", "Clutches", "ScorePerRound", "KillsPerRound", "DamageDeltaPerRound")

def get_stat(stat_name: str, page_num: int, tier: str = "immortal", region: str = "eu"):
    response = requests.get(f"https://tracker.gg/valorant/leaderboards/stats/all/{stat_name}?page={page_num}&region={region}&tier={tier}")
    while not response.ok:
        sleep(2)
        response = requests.get(f"https://tracker.gg/valorant/leaderboards/stats/all/{stat_name}?page={page_num}&region={region}&tier={tier}")
    soup = BeautifulSoup(response.text, "html.parser")
    return ([player.div.span.span.text for player in soup.find_all("td", {"class": "username"})],
            [str(stat.text).lstrip() for stat in soup.find_all("td", {"class": "stat highlight"})])


if __name__ == "__main__":
    for name in stat_names:
        print(name)
        players = []
        stats = []
        for i in range(1, 100):
            new_players, new_stats = get_stat(name, i, "platinum")
            if new_players and new_stats:
                players.extend(new_players)
                stats.extend(new_stats)
            else:
                break
            sleep(2)

        with open(f"./out2/{name}.csv", "w", newline="") as f:
            csv.writer(f).writerows(list(zip(players, stats)))
        
        sleep(20)