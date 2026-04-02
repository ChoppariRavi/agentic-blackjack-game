"""Blackjack engine rule tests."""

import config
from engine.card import Card, Deck, Rank, Suit
from engine.game_manager import GameManager, GamePhase
from engine.hand import Hand


def test_hand_ace_soft_hard():
    h = Hand()
    h.add(Card(Suit.HEARTS, Rank.ACE))
    h.add(Card(Suit.HEARTS, Rank.SIX))
    total, soft = h.value()
    assert total == 17
    assert soft is True


def test_hand_blackjack():
    h = Hand()
    h.add(Card(Suit.SPADES, Rank.ACE))
    h.add(Card(Suit.SPADES, Rank.KING))
    assert h.is_blackjack() is True


def test_deck_draw_and_reshuffle():
    d = Deck(1)
    n = d.remaining()
    d.draw()
    assert d.remaining() == n - 1


def test_game_round_flow():
    gm = GameManager()
    gm.start_round()
    assert gm.phase == GamePhase.PLAYER_TURN
    assert len(gm.player.cards) == 2
    assert len(gm.dealer.cards) == 2


def test_dealer_hits_until_stand_threshold(monkeypatch):
    gm = GameManager()
    gm.phase = GamePhase.PLAYER_TURN
    gm.player.clear()
    gm.dealer.clear()
    # Force dealer low then stand path via internal stand
    gm.dealer.add(Card(Suit.CLUBS, Rank.FIVE))
    gm.stand_player()
    assert gm.phase == GamePhase.SETTLE
    total, _ = gm.dealer.value()
    assert total >= config.DEALER_STANDS_ON or gm.dealer.is_bust()
