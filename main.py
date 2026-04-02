# main.py (In the root folder)
from engine.game_manager import BlackjackGame
from agent.brain import BlackjackAgent
from agent.parser import ActionParser
from config import Config

def main():
    game = BlackjackGame()
    agent = BlackjackAgent(api_key=Config.OPENAI_API_KEY, model=Config.MODEL_NAME)
    parser = ActionParser(game) # Pass the game instance TO the parser

    game.start_new_game()
    print(f"Initial Hand: {game.player_hand} | Dealer Upcard: {game.get_state()['dealer_upcard']}")

    while game.status == "IN_PROGRESS":
        # 1. Get current state from engine
        current_state = game.get_state()
        
        # NEW: Check if we even need the AI's opinion
        if current_state['player_score'] >= 21:
            print("🎯 Automatic Stand: Player at 21 or higher.")
            game.player_stand()
            break

        # 2. Get decision from AI
        decision = agent.get_decision(current_state)
        
        # 3. Use Parser to apply decision to Engine
        parser.execute_agent_move(decision)
        
        # Show what happened
        last_move = game.history[-1]
        print(f"🤖 Agent Action: {last_move['action_taken']}")
        print(f"🧠 Reasoning: {last_move['agent_thought']}")
        print(f"🃏 Current Hand: {game.player_hand}")

    print(f"--- Game Over: {game.status} ---")

if __name__ == "__main__":
    main()