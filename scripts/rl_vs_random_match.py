import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.rl_player import RLPlayer
from core.value_player import ValuePlayer
from core.cribbage_game import CribbageGame
from tqdm import tqdm

class CribbageMatch:
    def __init__(self):
        self.p1_wins = 0
        self.p2_wins = 0
        self.score_diffs = []

    def run_game(self):
        try:
            rl_bot = RLPlayer("RLBot", model_path="models/discard_dqn_agent_final.zip")
            value_bot = ValuePlayer("ValueBot")

            game = CribbageGame(rl_bot, value_bot)

            while not game.winner:
                game.play_round()

            if game.winner.name == "RLBot":
                self.p1_wins += 1
            else:
                self.p2_wins += 1

            diff = game.p1.score - game.p2.score
            self.score_diffs.append(diff)
        except Exception as e:
            print(f"Error in game: {str(e)}")
            raise

    def run(self, num_games=100):
        print("\nStarting RL Bot vs Value Bot match...")
        for i in tqdm(range(num_games), desc="Running games"):
            self.run_game()

        win_rate = self.p1_wins / num_games * 100
        avg_diff = sum(self.score_diffs) / num_games

        print("\n=== Match Results ===")
        print(f"RLBot Wins: {self.p1_wins}")
        print(f"ValueBot Wins: {self.p2_wins}")
        print(f"RLBot Win Rate: {win_rate:.2f}%")
        print(f"Average Score Difference: {avg_diff:.2f}")

if __name__ == "__main__":
    match = CribbageMatch()
    match.run(num_games=100)
