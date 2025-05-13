from itertools import combinations

def card_value(card):
    return min(card.rank, 10)

def card_rank(card):
    return card.rank

def card_suit(card):
    return card.suit

def score_fifteens(cards):
    total = 0
    for r in range(2, len(cards)+1):
        for combo in combinations(cards, r):
            if sum(card_value(c) for c in combo) == 15:
                total += 2
    return total

def score_pairs(cards):
    total = 0
    for c1, c2 in combinations(cards, 2):
        if card_rank(c1) == card_rank(c2):
            total += 2
    return total

def score_runs(cards):
    total = 0
    sorted_cards = sorted(cards, key=lambda c: c.rank)
    ranks = [c.rank for c in sorted_cards]

    max_run = 0
    for r in range(3, 6):  # check for 3, 4, and 5-card runs
        for combo in combinations(ranks, r):
            if list(combo) == list(range(min(combo), min(combo)+r)):
                count = ranks.count(combo[0])
                for val in combo[1:]:
                    count *= ranks.count(val)
                max_run = max(max_run, r * count)
    return max_run

def score_flush(hand, cut_card, is_crib=False):
    suits = [card_suit(c) for c in hand]
    if len(set(suits)) == 1:  # all 4 hand cards same suit
        if card_suit(cut_card) == suits[0]:
            return 5  # 5-card flush
        elif not is_crib:
            return 4  # 4-card flush only counts outside crib
    return 0

def score_knobs(hand, cut_card):
    for card in hand:
        if card.rank == 11 and card.suit == cut_card.suit:  # Jack of same suit
            return 1
    return 0

def score_hand(hand, cut_card, is_crib=False):
    all_cards = hand + [cut_card]
    score = 0
    score += score_fifteens(all_cards)
    score += score_pairs(all_cards)
    score += score_runs(all_cards)
    score += score_flush(hand, cut_card, is_crib)
    score += score_knobs(hand, cut_card)
    return score
