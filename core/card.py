import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank  # 1 (Ace) to 13 (King)
        self.suit = suit  # 'C', 'D', 'H', 'S'

    def cribbage_value(self):
        return min(self.rank, 10)

    def __repr__(self):
        rank_str = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}.get(self.rank, str(self.rank))
        return f"{rank_str}{self.suit}"

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        return hash((self.rank, self.suit))

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in range(1, 14) for suit in 'CDHS']
        random.shuffle(self.cards)

    def deal(self, num_cards):
        return [self.cards.pop() for _ in range(num_cards)]

    def draw(self):
        return self.cards.pop()

    def remaining(self):
        return len(self.cards)
