from card import Card
from scoring import score_hand

def test_perfect_hand():
    # 29-point hand: three 5s and a Jack, plus cut 5
    hand = [Card(5, 'H'), Card(5, 'C'), Card(5, 'D'), Card(11, 'S')]  # J♠
    cut = Card(5, 'S')
    assert score_hand(hand, cut) == 29
    print("Perfect hand test passed.")

def test_flush_only():
    hand = [Card(2, 'H'), Card(4, 'H'), Card(6, 'H'), Card(8, 'H')]
    cut = Card(10, 'C')
    assert score_hand(hand, cut) == 4
    print("Flush test passed.")

def test_flush_with_cut():
    hand = [Card(2, 'H'), Card(4, 'H'), Card(6, 'H'), Card(8, 'H')]
    cut = Card(10, 'H')
    assert score_hand(hand, cut) == 5
    print("5-card flush test passed.")

def test_flush_in_crib_fail():
    hand = [Card(2, 'H'), Card(4, 'H'), Card(6, 'H'), Card(8, 'H')]
    cut = Card(10, 'C')
    assert score_hand(hand, cut, is_crib=True) == 0
    print("Crib flush restriction test passed.")

def test_knobs():
    hand = [Card(11, 'S'), Card(13, 'H'), Card(7, 'C'), Card(9, 'D')]
    cut = Card(2, 'S')
    assert score_hand(hand, cut) == 1
    print("Knobs test passed.")

def test_runs_and_pairs():
    hand = [Card(3, 'H'), Card(4, 'D'), Card(5, 'S'), Card(5, 'C')]
    cut = Card(6, 'H')  # Run: 3-4-5-6, pair of 5s
    assert score_hand(hand, cut) == 14
    print("Runs & pairs test passed.")

if __name__ == "__main__":
    test_perfect_hand()
    test_flush_only()
    test_flush_with_cut()
    test_flush_in_crib_fail()
    test_knobs()
    test_runs_and_pairs()
