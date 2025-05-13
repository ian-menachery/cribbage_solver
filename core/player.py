class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.discards = []
        self.score = 0

    def receive_hand(self, cards):
        self.hand = cards
        self.discards = []

    def discard_to_crib(self, is_dealer):
        """
        Choose 2 cards to discard to the crib.
        For now, randomly discard the last 2 cards.
        Smarter logic or RL will replace this later.
        """
        discard = self.hand[-2:]
        self.hand = self.hand[:-2]
        self.discards = discard
        return discard

    def reset(self):
        self.hand = []
        self.discards = []

    def __str__(self):
        return f"{self.name} - Score: {self.score}"
