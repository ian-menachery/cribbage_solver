from core.card import Deck
from core.player import Player
from core.scoring import score_hand
from core.value_player import ValuePlayer
import random


class CribbageGame:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

        # Randomly assign dealer and non-dealer
        if random.choice([True, False]):
            self.dealer = self.p1
            self.non_dealer = self.p2
        else:
            self.dealer = self.p2
            self.non_dealer = self.p1

        self.winner = None

    def switch_dealer(self):
        self.dealer, self.non_dealer = self.non_dealer, self.dealer

    def play_round(self):
        deck = Deck()
        full_hand1 = deck.deal(6)
        full_hand2 = deck.deal(6)
        self.p1.receive_hand(full_hand1[:])  # pass a copy
        self.p2.receive_hand(full_hand2[:])  # pass a copy

        print(f"\n{self.p1.name}'s full hand before discard: {full_hand1}")
        print(f"{self.p2.name}'s full hand before discard: {full_hand2}")

        crib = []
        crib += self.p1.discard_to_crib(self.p1 == self.dealer)
        crib += self.p2.discard_to_crib(self.p2 == self.dealer)

        cut_card = deck.draw()

        print(f"Cut card: {cut_card}")
        print(f"{self.p1.name}'s hand: {self.p1.hand}")
        print(f"{self.p2.name}'s hand: {self.p2.hand}")
        print(f"Crib: {crib} (dealer: {self.dealer.name})")

        p1_score = score_hand(self.p1.hand, cut_card)
        p2_score = score_hand(self.p2.hand, cut_card)
        crib_score = score_hand(crib, cut_card, is_crib=True)

        self.p1.score += p1_score
        self.p2.score += p2_score
        self.dealer.score += crib_score

        print(f"{self.p1.name} scored {p1_score}")
        print(f"{self.p2.name} scored {p2_score}")
        print(f"{self.dealer.name} scored {crib_score} from crib")

        print(f"Scores: {self.p1.name}: {self.p1.score}, {self.p2.name}: {self.p2.score}")

        if self.p1.score >= 121:
            self.winner = self.p1
        elif self.p2.score >= 121:
            self.winner = self.p2

        self.p1.reset()
        self.p2.reset()
        self.switch_dealer()

    def play_game(self):
        print("Starting Cribbage Match")
        round_num = 1
        while not self.winner:
            print(f"\n--- Round {round_num} ---")
            self.play_round()
            round_num += 1
        print(f"\n{self.winner.name} wins with {self.winner.score} points!")
