from agent.parser import ActionParser
from .card import Deck
from .hand import Hand

class BlackjackGame:
    def __init__(self) -> None:
        self.deck = Deck(num_decks=6) # Casino standard
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.status = "INITIALIZING" # in_progress, player_bust, dealer_win, player_win, push
        self.history = [] # To store agent reasoning later
    
    def start_new_game(self):
        """Resets hands and deals initial 2 cards."""
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.deck.reset_deck()

        # Initial Deal
        self.player_hand.add_card(self.deck.deal()[0])
        self.dealer_hand.add_card(self.deck.deal()[0])
        self.player_hand.add_card(self.deck.deal()[0])
        self.dealer_hand.add_card(self.deck.deal()[0])

        self.status = "IN_PROGRESS"

        # Check for immediate Blackjack
        if self.player_hand.is_blackjack():
            self.resolve_dealer_turn()

    def player_hit(self):
        """Player takes a card."""
        if self.status == "IN_PROGRESS":
            self.player_hand.add_card(self.deck.deal()[0])
            if self.player_hand.value > 21:
                self.status = "PLAYER_BUST"
        return self.get_state()
    
    def player_stand(self):
        """Player stops; Dealer must now play."""
        if self.status == "IN_PROGRESS":
            self.resolve_dealer_turn()
        return self.get_state()
    
    def resolve_dealer_turn(self):
        """Dealer hits until they reach at least 17."""
        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.deal()[0])

        self.determine_winner()
    
    def determine_winner(self):
        p_val = self.player_hand.value
        d_val = self.dealer_hand.value

        if p_val > 21:
            self.status = "PLAYER_BUST"
        elif d_val > 21:
            self.status = "DEALER_BUST"
        elif p_val > d_val:
            self.status = "PAYER_WIN"
        elif d_val > p_val:
             self.status = "PAYER_WIN"
        else:
            self.status = "PUSH" # Tie
    
    def get_state(self):
        """
        Full table snapshot: agent fields plus UI fields (hands + history).
        """
        return {
            "player_cards": [str(c) for c in self.player_hand.cards],
            "player_hand": [str(c) for c in self.player_hand.cards],
            "player_score": self.player_hand.value,
            "dealer_upcard": str(self.dealer_hand.cards[0]),
            "dealer_hand": [str(c) for c in self.dealer_hand.cards],
            "status": self.status,
            "can_hit": self.status == "IN_PROGRESS" and self.player_hand.value < 21,
            "history": self.history,
        }
    
    def play_agent_turn(self, agent_brain):
        """
            1. Get the current state
            2. Ask the LLM for a decision
            3. Parse and Execute the move
        """
        if self.status != "INPROGRESS":
            return self.get_state()
        
        state = self.get_state()
        # 1. Get current state
        state = self.get_state()
        
        # 2. Ask the Brain (agent/brain.py)
        decision = agent_brain.get_decision(state)

        # 3. Use the Parser (newly created logic)
        parser = ActionParser(self)
        parser.execute_agent_move(decision)

        return self.get_state()

    def to_dict(self):
        """Converts the current game instance into a dictionary for the session."""
        return {
            "player_hand": [str(c) for c in self.player_hand.cards],
            "player_score": self.player_hand.value,
            "dealer_hand": [str(c) for c in self.dealer_hand.cards],
            "dealer_score": self.dealer_hand.value,
            "status": self.status,
            "history": self.history,
            # We store the remaining deck as a list of strings/values
            "deck": [f"{c.rank}{c.suit}" for c in self.deck.cards] 
        }
    
    @classmethod
    def from_dict(cls, data):
        """Rebuilds a BlackjackGame instance from session data."""
        game = cls()
        game.status = data.get("status", "INITIALIZING")
        game.history = data.get("history", [])
        
        # Logic to rebuild Hands and Deck from the strings would go here
        # For now, we'll keep it simple and focus on the Route logic
        return game


if __name__ == "__main__":
    from engine.game_manager import BlackjackGame
    from agent.brain import BlackjackAgent

    game = BlackjackGame()
    agent = BlackjackAgent()
    
    game.start_new_game()
    print(f"Game Started! Player: {game.player_hand} | Dealer: {game.dealer_hand.cards[0]}")

    # The Agent takes over until the game is over
    while game.status == "IN_PROGRESS":
        state = game.play_agent_turn(agent)
        last_move = game.history[-1]
        print(f"🤖 Agent decided to: {last_move['action_taken']}")
        print(f"🧠 Reasoning: {last_move['agent_thought']}")
        print(f"🃏 New Hand: {game.player_hand} (Score: {game.player_hand.value})")
    
    print(f"🏁 Final Result: {game.status}")
# if __name__ == "__main__":
#     game = BlackjackGame()
#     game.start_new_game()
#     print(f"Game Started! Dealer shows: {game.get_state()['dealer_upcard']}")
#     print(f"Your Hand: {game.player_hand} (Score: {game.player_hand.value})")
    
#     # Simple loop for manual testing
#     while game.status == "IN_PROGRESS":
#         action = input("Type 'h' to Hit or 's' to Stand: ").lower()
#         if action == 'h':
#             game.player_hit()
#         else:
#             game.player_stand()
#         print(f"Current State: {game.get_state()}")
    
#     print(f"Final Outcome: {game.status}")
