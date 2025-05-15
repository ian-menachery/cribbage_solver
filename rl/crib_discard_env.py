import gymnasium as gym
from gymnasium import spaces
import numpy as np
from itertools import combinations
import random
import json
import logging

from core.card import Deck, Card
from core.scoring import score_hand

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CribDiscardEnv(gym.Env):
    def __init__(self):
        super().__init__()
        logger.info("Initializing CribDiscardEnv")
        self.action_space = spaces.Discrete(15)  # 15 discard combos
        
        # Enhanced observation space:
        # - 6 cards (rank, suit) = 6x2
        # - dealer status = 1
        # - current score = 1
        # - opponent's score = 1
        # - cards remaining in deck = 1
        self.observation_space = spaces.Box(
            low=np.array([0, 0] * 6 + [0, 0, 0, 0, 0]),
            high=np.array([13, 3] * 6 + [1, 121, 121, 52, 1]),
            dtype=np.int32
        )

        self.discard_combos = list(combinations(range(6), 2))
        self.deck = None
        self.hand = None
        self.is_dealer = None
        self.cut_card = None
        self.my_score = 0
        self.opponent_score = 0
        self.cards_remaining = 52

    def reset(self, seed=None, options=None):
        try:
            super().reset(seed=seed)
            logger.info("Resetting environment")
            self.deck = Deck()
            self.hand = self.deck.deal(6)
            self.is_dealer = random.choice([True, False])
            self.cut_card = self.deck.draw()
            self.my_score = 0
            self.opponent_score = 0
            self.cards_remaining = 52 - 14  # 6 cards each + cut card
            obs = self._get_obs()
            logger.info(f"Reset complete. Hand size: {len(self.hand)}, Dealer: {self.is_dealer}")
            return obs, {}
        except Exception as e:
            logger.error(f"Error in reset: {str(e)}")
            raise

    def _get_obs(self):
        try:
            # Basic card information
            card_info = np.array([[card.rank, 'CDHS'.index(card.suit)] for card in self.hand], dtype=np.int32).flatten()
            
            # Additional state information
            state_info = np.array([
                int(self.is_dealer),
                self.my_score,
                self.opponent_score,
                self.cards_remaining,
                int(self.cards_remaining < 10)  # Flag for endgame
            ], dtype=np.int32)
            
            return np.concatenate([card_info, state_info])
        except Exception as e:
            logger.error(f"Error in _get_obs: {str(e)}")
            raise

    def _calculate_reward(self, hand_score, crib_score, is_dealer):
        try:
            # Simplified reward structure
            base_reward = hand_score + crib_score if is_dealer else hand_score - crib_score
            
            # Endgame rewards/penalties
            if self.my_score >= 121:
                return 100  # Win bonus
            elif self.opponent_score >= 121:
                return -100  # Loss penalty
                
            return base_reward
        except Exception as e:
            logger.error(f"Error in _calculate_reward: {str(e)}")
            raise

    def step(self, action):
        try:
            logger.info(f"Step with action {action}")
            combo = self.discard_combos[action]
            discard = [self.hand[i] for i in combo]
            keep = [card for i, card in enumerate(self.hand) if i not in combo]

            # Simulate opponent discard using value-based strategy
            opponent_discards = self._simulate_opponent_discard()
            crib = discard + opponent_discards

            hand_score = score_hand(keep, self.cut_card)
            crib_score = score_hand(crib, self.cut_card, is_crib=True)
            
            # Update scores
            self.my_score += hand_score
            if self.is_dealer:
                self.my_score += crib_score
            else:
                self.opponent_score += crib_score
                
            # Update cards remaining
            self.cards_remaining -= 4  # 2 discards each

            reward = self._calculate_reward(hand_score, crib_score, self.is_dealer)
            done = self.my_score >= 121 or self.opponent_score >= 121
            
            # Reset the environment for the next step
            if not done:
                self.deck = Deck()
                self.hand = self.deck.deal(6)
                self.is_dealer = random.choice([True, False])
                self.cut_card = self.deck.draw()
            
            truncated = False
            logger.info(f"Step complete. Scores: {self.my_score}-{self.opponent_score}, Reward: {reward}")
            return self._get_obs(), reward, done, truncated, {}
        except Exception as e:
            logger.error(f"Error in step: {str(e)}")
            raise

    def _simulate_opponent_discard(self):
        try:
            # Simulate ValuePlayer's discard strategy
            if len(self.hand) < 2:
                return [Card(random.randint(1, 13), random.choice('CDHS')) for _ in range(2)]
                
            # Load expected values
            try:
                with open("data/expected_value_v1.json") as f:
                    values = json.load(f)
            except:
                # Fallback to simple rank-based strategy if values not available
                sorted_cards = sorted(self.hand, key=lambda c: c.rank)
                return sorted_cards[:2]
                
            # Score each possible discard combination
            discard_combos = list(combinations(range(len(self.hand)), 2))
            best_score = float("-inf")
            best_combo = None
            
            for combo in discard_combos:
                discard = [self.hand[i] for i in combo]
                score = 0
                for card in discard:
                    rank_str = {1: "A", 11: "J", 12: "Q", 13: "K"}.get(card.rank, str(card.rank))
                    if not self.is_dealer:  # Opponent is dealer when we're not
                        score += values.get(rank_str, {}).get("with_crib", 0)
                    else:
                        score += values.get(rank_str, {}).get("against_crib", 0)
                if score > best_score:
                    best_score = score
                    best_combo = combo
                    
            return [self.hand[i] for i in best_combo]
        except Exception as e:
            logger.error(f"Error in _simulate_opponent_discard: {str(e)}")
            raise
