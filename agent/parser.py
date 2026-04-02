import json

class ActionParser:
    def __init__(self, game_engine) -> None:
        self.game = game_engine
    
    def execute_agent_move(self, llm_response):
        """
        Parses the JSON response and triggers the game engine.
        llm_response: dict from the LLM (e.g., {"action": "HIT", "reasoning": "..."})
        """
        action = llm_response.get("action", "").upper()
        reasoning = llm_response.get("reasoning", "No response provided")

        self.game.history.append({
            "agent_thought": reasoning,
            "action_taken": action
        })

        # Trigger the corresponding engine method
        if action == 'HIT':
            return self.game.player_hit()
        elif action =='STAND':
            return self.game.player_stand() 
        elif action == 'DOUBLE':
            # Simple check: Can only double on the first two cards
            if len(self.game.player_hand.cards) == 2:
                self.game.player_hit()
                return self.game.player_stand()
            else:
                # Fallback if AI tries to double late: just Stand
                return self.game.player_stand()
        else:
            # Default safety move if the AI sends back garbage
            print(f"⚠️ Warning: Unknown action '{action}'. Defaulting to STAND.")
            return self.game.player_stand()