# agent/brain.py
from openai import OpenAI
from agent.prompts import SYSTEM_PROMPTS, get_user_prompt

class BlackjackAgent:
    def __init__(self, api_key, model):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def get_decision(self, game_state, personality="pro_gambler"):
        """Refactored to support different personalities and cleaner error handling."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPTS[personality]},
                    {"role": "user", "content": get_user_prompt(game_state)}
                ],
                response_format={"type": "json_object"}
            )
            import json
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Agent Refactor Error: {e}")
            return {"action": "STAND", "reasoning": "System error, playing safe."}