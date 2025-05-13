from core.player import Player
from stable_baselines3 import DQN
from itertools import combinations
import numpy as np

class RLPlayer(Player):
    def __init__(self, name, model_path="models/discard_dqn_agent.zip"):
        super().__init__(name)
        self.model = DQN.load(model_path)
        self.discard_combos = list(combinations(range(6), 2))

    def discard_to_crib(self, is_dealer):
        # Format observation: 6 cards → 6x2 matrix of [rank, suit_index]
        obs = np.array([
            [card.rank, 'CDHS'.index(card.suit)]
            for card in self.hand
        ], dtype=np.int32)

        # Predict discard action
        action, _ = self.model.predict(obs, deterministic=True)

        # Map action to cards to discard
        combo = self.discard_combos[action]
        discarded = [self.hand[i] for i in combo]
        self.hand = [c for i, c in enumerate(self.hand) if i not in combo]
        return discarded
