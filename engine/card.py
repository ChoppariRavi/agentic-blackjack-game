import random

class Card:
    def __init__(self, suit: str, rank: str) -> None:
        self.suit = suit
        self.rank = rank

        if rank in ["J", "Q", "K"]:
            self.value = 10
        elif rank == "A":
            self.value = 11
        else:
            self.value = int(rank)
        
    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"
    
    def __repr__(self) -> str:
        return f"Card(suit={self.suit}, rank={self.rank}, value={self.value})"

class Deck:
    def __init__(self, num_decks: int = 1) -> None:
        self.num_decks = num_decks
        self.cards = []
        self.reset_deck()
    
    def reset_deck(self):
        """Creates a fresh set of cards and shuffles them."""
        suits = ['♠', '♣', '♥', '♦']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

        # Multiply by num_decks for "Casino Style" (usually 6-8 decks)
        self.cards = [Card(s, r) for _ in range(self.num_decks) for s in suits for r in ranks]
        self.shuffle()
    
    def shuffle(self):
        """Randomizes the order of the cards."""
        random.shuffle(self.cards)

    def deal(self, num = 1):
        """Removes and returns 'num' cards from the top of the deck."""
        dealt_cards = []
        for _ in range(num):
            if len(self.cards) > 0:
                dealt_cards.append(self.cards.pop())
            else:
                # Optional: Auto-reshuffle if deck is empty
                print("Deck empty! Reshuffling...")
                self.reset_deck()
                dealt_cards.append(self.cards.pop())
        return dealt_cards;
    
    def __len__(self):
        return len(self.cards)

# --- Quick Test ---
if __name__ == "__main__":
    deck = Deck(num_decks=1)
    print(f"Total cards: {len(deck)}")

    hand = deck.deal(2)
    print(f"Dealt Hand: {hand}")
    print(f"Cards remaining: {len(deck)}")
