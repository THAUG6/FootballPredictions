from APIClass import *
import os
import pandas as pd
from enum import Enum

def validate_request(txt : str):
    os.system('')  # Enables ANSI escape characters in terminal (Windows)
    invalid = True
    while invalid:
        val = input(f"\033[1m\033[4m\033[38;5;226m{txt}\033[95m")

        print('\033[0m', end='')  # Reset text to normal before confirmation input
        confirmation = input("Input y/n to confirm/cancel: ")
        if confirmation == "y":
            invalid = False
    print('\033[0m', end='')  # Reset text to normal before confirmation input
    return val

def request(txt : str):
    val = input(f"\033[1m\033[4m\033[38;5;226m{txt}\033[95m")
    print('\033[0m', end='')  # Reset text to normal before confirmation input
    return val

def validate_score(score):
    if score is None or not isinstance(score, str):
        return False

    parts = score.split('-')
    if len(parts) != 2:
        return False

    try:
        home_score = int(parts[0].strip())
        away_score = int(parts[1].strip())
        return home_score >= 0 and away_score >= 0
    except ValueError:
        return False


if __name__ == "__main__":

    user_name = validate_request("Input Username: ")
    
    current_season = request("Input Season: ")

    current_week = request("Input Week: ")

    scores_key =  "7518f371e6f5436ab76e84ac83d9239c"
    nflScoresByWeek = NFLApi(scores_key)
    scoresByWeek = nflScoresByWeek.get_scores_by_week(current_season, current_week)

    log_file = open(f"Predictions_{user_name}_Week{current_week}_{current_season}.txt", "w")
        
    for _, game in scoresByWeek.iterrows():
        print(f"Game \033[95m{game["AwayTeam"]}\033[0m at \033[95m{game["HomeTeam"]}\033[0m")
        game_winner = None
        while not (game_winner in [game["AwayTeam"], game["HomeTeam"]]):
            game_winner = request(f"Select Winning Team ({game['AwayTeam']}/{game['HomeTeam']}): ")
            
        
        game_score = None
        while not validate_score(game_score):
            game_score = request(f"Select Final Score (Winner-Loser): ")

        log_file.write(f"Game: {game['AwayTeam']} at {game['HomeTeam']}, Predicted Winner: {game_winner}, Predicted Score: {game_score}\n")