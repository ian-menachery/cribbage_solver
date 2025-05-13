from cribbage_game import CribbageGame
from value_player import ValuePlayer
from player import Player

class CribbageMatch:
    def __init__(self):
        self.p1_wins = 0
        self.p2_wins = 0
        self.score_diffs = []

    def run_game(self):
        # Create a new game with ValueBot vs RandomBot
        game = CribbageGame("ValueBot", "RandomBot")
        game.p1 = ValuePlayer("ValueBot")
        game.p2 = Player("RandomBot")

        # Play until one player reaches 121
        while not game.winner:
            game.play_round()

        # Record winner
        if game.winner.name == "ValueBot":
            self.p1_wins += 1
        else:
            self.p2_wins += 1

        # Track score difference
        diff = game.p1.score - game.p2.score
        self.score_diffs.append(diff)

    def run(self, num_games=100):
        for i in range(num_games):
            print(f"\n--- Game {i+1} ---")
            self.run_game()

        total_games = self.p1_wins + self.p2_wins
        win_rate = self.p1_wins / total_games * 100
        avg_diff = sum(self.score_diffs) / total_games

        print("\n=== Match Results ===")
        print(f"Total Games: {total_games}")
        print(f"ValueBot Wins: {self.p1_wins}")
        print(f"RandomBot Wins: {self.p2_wins}")
        print(f"ValueBot Win Rate: {win_rate:.2f}%")
        print(f"Average Score Difference (ValueBot - RandomBot): {avg_diff:.2f}")

if __name__ == "__main__":
    match = CribbageMatch()
    match.run(num_games=100)
