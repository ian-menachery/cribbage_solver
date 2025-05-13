import gym
from gym import spaces
import numpy as np
from itertools import combinations
import random

from core.card import Deck, Card
from core.scoring import score_hand

class CribDiscardEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = spaces.Discrete(15)  # 15 discard combos
        self.observation_space = spaces.Box(low=0, high=13, shape=(6, 2), dtype=np.int32)

        self.discard_combos = list(combinations(range(6), 2))
        self.deck = None
        self.hand = None
        self.is_dealer = None
        self.cut_card = None

    def reset(self):
        self.deck = Deck()
        self.hand = self.deck.deal(6)
        self.is_dealer = random.choice([True, False])
        self.cut_card = self.deck.draw()
        return self._get_obs()

    def _get_obs(self):
        return np.array([[card.rank, 'CDHS'.index(card.suit)] for card in self.hand], dtype=np.int32)

    def step(self, action):
        combo = self.discard_combos[action]
        discard = [self.hand[i] for i in combo]
        keep = [card for i, card in enumerate(self.hand) if i not in combo]

        # Simulate opponent discard (random filler)
        opponent_discards = [Card(random.randint(1, 13), random.choice('CDHS')) for _ in range(2)]
        crib = discard + opponent_discards

        hand_score = score_hand(keep, self.cut_card)
        crib_score = score_hand(crib, self.cut_card, is_crib=True)
        reward = hand_score + crib_score if self.is_dealer else hand_score - crib_score

        done = True
        return self._get_obs(), reward, done, {}
