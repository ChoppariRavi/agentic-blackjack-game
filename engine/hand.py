class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'A':
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        """
        If total value is > 21 and we have aces, 
        change an ace from 11 to 1 by subtracting 10.
        """
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1
        
    def is_blackjack(self):
        return self.value == 21 and len(self.cards) == 2
    
    def __repr__(self):
        return f"{', '.join([str(c) for c in self.cards])} (Value: {self.value})"

if __name__ =='__main__':
    from card import Card # Assuming your previous code is in card.py
    
    my_hand = Hand()
    
    # Test 1: Dealing two Aces
    my_hand.add_card(Card('♠', 'A'))
    my_hand.add_card(Card('♥', 'A'))
    print(f"Hand 1: {my_hand}") # Should be 12 (11 + 1)

    # Test 2: Adding a King (Bust protection)
    my_hand.add_card(Card('♦', 'K'))
    print(f"Hand 2: {my_hand}") # Should be 12 (1 + 1 + 10)