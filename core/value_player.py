import json
from itertools import combinations
from .player import Player

class ValuePlayer(Player):
    def __init__(self, name, value_file_path="data/expected_value_v1.json"):
        super().__init__(name)
        with open(value_file_path) as f:
            self.values = json.load(f)

    def discard_to_crib(self, is_dealer):
        discard_combos = list(combinations(range(6), 2))
        best_score = float("-inf")
        best_combo = None

        for combo in discard_combos:
            discard = [self.hand[i] for i in combo]
            score = 0
            for card in discard:
                rank_str = {1: "A", 11: "J", 12: "Q", 13: "K"}.get(card.rank, str(card.rank))
                if is_dealer:
                    score += self.values.get(rank_str, {}).get("with_crib", 0)
                else:
                    score += self.values.get(rank_str, {}).get("against_crib", 0)
            if score > best_score:
                best_score = score
                best_combo = combo

        discarded = [self.hand[i] for i in best_combo]
        self.hand = [c for i, c in enumerate(self.hand) if i not in best_combo]
        return discarded
