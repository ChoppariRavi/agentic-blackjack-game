"""Agent returns valid decision JSON (mocked LLM)."""

import json
from unittest.mock import MagicMock, patch

from agent.brain import Brain


def test_brain_decide_parses_json():
    fake_payload = {"action": "hit", "reasoning": "Low total."}
    mock_resp = MagicMock()
    mock_resp.choices = [MagicMock(message=MagicMock(content=json.dumps(fake_payload)))]
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_resp

    with patch("agent.brain.config.OPENAI_API_KEY", "sk-test"):
        with patch("agent.brain.OpenAI", return_value=mock_client):
            brain = Brain()
            out = brain.decide({"player_total": 12, "dealer_up": "K"})
    assert out["action"] == "hit"
    assert out["reasoning"] == "Low total."


def test_brain_no_key_returns_stand():
    with patch("agent.brain.config.OPENAI_API_KEY", ""):
        brain = Brain()
        out = brain.decide({})
        assert out["action"] == "stand"
