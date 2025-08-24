import requests
import pandas as pd

class NFLApi:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sportsdata.io/v3/nfl/scores/json"
        self.headers = {"Ocp-Apim-Subscription-Key": self.api_key}

    def get_scores_by_week(self, season: int, week: int) -> pd.DataFrame:

        url = f"{self.base_url}/ScoresByWeekFinal/{season}/{week}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)

            return df[["Week", "HomeTeam", "AwayTeam", "HomeScore", "AwayScore"]]
        else:
            raise Exception(f"Erreur API {response.status_code}: {response.text}")
        
    def get_teams(self) -> pd.DataFrame:
        url = f"{self.base_url}/Teams"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return pd.DataFrame(response.json())
        
        else:   
            raise Exception(f"Erreur API {response.status_code}: {response.text}")
        


if __name__ == "__main__":
    scores_key =  "7518f371e6f5436ab76e84ac83d9239c"
    nflScoresByWeek = NFLApi(scores_key)
    scoresByWeek = nflScoresByWeek.get_scores_by_week(2025, 1)
    print(scoresByWeek)

