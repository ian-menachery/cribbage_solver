from card import Deck, Card
from scoring import score_hand
from itertools import combinations
from collections import defaultdict
import random
import json
import os

def simulate_card_value_stats(num_hands=5000):
    dealer_scores = defaultdict(list)
    nondealer_scores = defaultdict(list)

    for _ in range(num_hands):
        for is_dealer in [True, False]:  # simulate both roles each round
            deck = Deck()
            hand = deck.deal(6)
            cut = deck.draw()
            discard_combos = list(combinations(range(6), 2))

            for combo in discard_combos:
                discard = [hand[i] for i in combo]
                keep = [card for i, card in enumerate(hand) if i not in combo]

                # Add two random filler cards to complete the crib
                filler = [Card(random.randint(1, 13), random.choice('CDHS')) for _ in range(2)]
                crib = discard + filler

                hand_score = score_hand(keep, cut)
                crib_score = score_hand(crib, cut, is_crib=True)
                reward = hand_score + crib_score if is_dealer else hand_score - crib_score

                target = dealer_scores if is_dealer else nondealer_scores
                for card in discard:
                    target[card.rank].append(reward)

    return dealer_scores, nondealer_scores

def compute_relative_values(score_dict):
    all_scores = [score for scores in score_dict.values() for score in scores]
    global_avg = sum(all_scores) / len(all_scores)

    return {
        rank: (sum(scores) / len(scores)) - global_avg
        for rank, scores in score_dict.items()
    }

def print_ranked_comparison(with_crib, against_crib):
    print("Relative discard value by rank:")
    print("(0 = neutral, + = safer to discard, - = valuable to keep)\n")
    print(f"{'Rank':<5} {'With Crib':>10} {'Opponents Crib':>18}")
    print("-" * 35)

    all_ranks = sorted(set(with_crib.keys()).union(against_crib.keys()))
    for rank in all_ranks:
        label = {1: "A", 11: "J", 12: "Q", 13: "K"}.get(rank, str(rank))
        wc = with_crib.get(rank, 0)
        ac = against_crib.get(rank, 0)
        print(f"{label:<5} {wc:>10.2f} {ac:>18.2f}")

def rank_label(rank):
    return {1: "A", 11: "J", 12: "Q", 13: "K"}.get(rank, str(rank))

if __name__ == "__main__":
    dealer_scores, nondealer_scores = simulate_card_value_stats(num_hands=5000)
    avg_with_crib = compute_relative_values(dealer_scores)
    avg_against_crib = compute_relative_values(nondealer_scores)
    
    print_ranked_comparison(avg_with_crib, avg_against_crib)

    # Combine and format for saving
    combined = {
        rank_label(rank): {
            "with_crib": round(avg_with_crib.get(rank, 0), 4),
            "against_crib": round(avg_against_crib.get(rank, 0), 4)
        }
        for rank in range(1, 14)
    }

    # Save to JSON
    os.makedirs("data", exist_ok=True)
    with open("data/expected_value_v1.json", "w") as f:
        json.dump(combined, f, indent=2)

    print("\nSaved expected values to data/expected_value_v1.json")
