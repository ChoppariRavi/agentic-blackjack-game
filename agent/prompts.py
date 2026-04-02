# agent/prompts.py

SYSTEM_PROMPTS = {
    "pro_gambler": """
        You are a professional Blackjack Agent. 
        Return ONLY a JSON object:
        {
          "action": "HIT" | "STAND" | "DOUBLE",
          "reasoning": "Short professional explanation."
        }
    """,
    "risky_ai": "You are a chaotic AI that loves high stakes. Always prefer HIT over STAND."
}

def get_user_prompt(state):
    return f"""
    Table State:
    - Player: {state['player_cards']} (Total: {state['player_score']})
    - Dealer Upcard: {state['dealer_upcard']}
    - Options: {['HIT', 'STAND'] if state['can_hit'] else ['STAND']}
    """