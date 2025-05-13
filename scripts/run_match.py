import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from core.bots import get_bot
from core.cribbage_game import CribbageGame

def main():
    parser = argparse.ArgumentParser(description="Run a Cribbage match between two bots.")
    parser.add_argument("bot1", nargs="?", default="rl", help="First bot (default: rl)")
    parser.add_argument("bot2", nargs="?", default="value", help="Second bot (default: value)")
    parser.add_argument("--games", type=int, default=100, help="Number of games to play (default: 100)")
    args = parser.parse_args()

    p1_wins = 0
    p2_wins = 0
    score_diffs = []

    for i in range(args.games):
        bot1 = get_bot(args.bot1)
        bot2 = get_bot(args.bot2)
        game = CribbageGame(bot1, bot2)
        while not game.winner:
            game.play_round()
        if game.winner.name == bot1.name:
            p1_wins += 1
        else:
            p2_wins += 1
        diff = game.p1.score - game.p2.score
        score_diffs.append(diff)
        print(f"Game {i+1}: {game.winner.name} wins ({game.p1.score} - {game.p2.score})")

    win_rate = p1_wins / args.games * 100
    avg_diff = sum(score_diffs) / args.games
    print("\n=== Match Results ===")
    print(f"{bot1.name} Wins: {p1_wins}")
    print(f"{bot2.name} Wins: {p2_wins}")
    print(f"{bot1.name} Win Rate: {win_rate:.2f}%")
    print(f"Average Score Difference: {avg_diff:.2f}")

if __name__ == "__main__":
    main() 