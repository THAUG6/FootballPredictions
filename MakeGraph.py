from APIClass import *
import os
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg


scores_key = "7518f371e6f5436ab76e84ac83d9239c"
nflScoresByWeek = NFLApi(scores_key)

Result = {"Giroux": [], "ThomPere": [], "Chevito": [], "Beli": []}

def process_predictions(id):
    number_correct_prediction = []
    for i in range(1, 19):
        scoresByWeek = nflScoresByWeek.get_scores_by_week(2024, i)
        scoresByWeek = scoresByWeek[scoresByWeek['HomeScore'].notna()]
        
        if not scoresByWeek.empty:
            #print(f"\nWeek {i} results:")
            #print(scoresByWeek)
            for filename in os.listdir("Predictions"):
                predicted_winners = []
                predicted_scores = []
                
                if filename.endswith(".txt") and f"Week{i}_" in filename and id in filename:
                    print(f"Processing file: {filename}")
                    with open(os.path.join("Predictions", filename), "r") as file:
                        predictions = file.readlines()
                        for prediction in predictions:
                            parts = prediction.strip().split(", ")
                            winner_part = [p for p in parts if "Predicted Winner" in p][0]
                            winner = winner_part.split(": ")[1]
                            score_part = [p for p in parts if "Predicted Score" in p][0]
                            score = score_part.split(": ")[1]
                            predicted_winners.append(winner)
                            predicted_scores.append(score)
                        winners_list = scoresByWeek['Winner'].dropna().tolist()
                        number_correct_prediction.append(sum(1 for item in winners_list if item in predicted_winners))
                        return number_correct_prediction


def plot_results_by_week(Result, user_icons):
    plt.figure(figsize=(10, 6))
    max_weeks = max(len(wins_list) for wins_list in Result.values())
    
    for user_id, wins_list in Result.items():
        weeks = [i+1 for i in range(len(wins_list))]

        plt.plot(weeks, wins_list, linestyle='-', label=user_id)

        img = mpimg.imread(user_icons[user_id])

        for x, y in zip(weeks, wins_list):
            imagebox = OffsetImage(img, zoom=0.1)
            ab = AnnotationBbox(imagebox, (x, y), frameon=False)
            plt.gca().add_artist(ab)
    
    plt.xlabel("Week")
    plt.ylabel("Number of Wins")
    plt.title("Number of Wins per Week for Each User")
    plt.legend()
    plt.xlim(0.5, 18)
    plt.ylim(0, 16)
    plt.xticks(range(1, 19))
    plt.yticks(range(0, 17))
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()
    
def plot_total_wins(Result):
    total_wins = {user: sum(wins_list) for user, wins_list in Result.items()}
    users = list(total_wins.keys())
    wins = list(total_wins.values())
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    plt.figure(figsize=(8, 6))
    plt.bar(users, wins, color=colors[:len(users)], edgecolor='black')
    plt.xlabel("User")
    plt.ylabel("Total Wins")
    plt.title("Total Wins per User")
    
    for i, v in enumerate(wins):
        plt.text(i, v + 0.2, str(v), ha='center', fontweight='bold')
    
    plt.ylim(0, max(wins) + 5)
    plt.grid(axis='y', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()
    
    
if __name__ == "__main__":
    for user_id in ["Giroux", "ThomPere", "Chevito", "Beli"]:
        Result[user_id] = process_predictions(user_id)
        
    print(Result)

    #test
    Result = {
        "Giroux": [10, 12, 9, 11],
        "ThomPere": [8, 11, 10, 12],
        "Chevito": [9, 10, 8, 11],
        "Beli": [7, 9, 11, 10]}
    
    user_icons = {"Giroux": "Images/giroux.png", "ThomPere": "Images/thom.png", "Chevito": "Images/cheche.png", "Beli": "Images/Beli.png"}
    plot_results_by_week(Result, user_icons)   
    plot_total_wins(Result)

