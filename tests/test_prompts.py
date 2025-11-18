from core.prompts import build_messages

def test_build_messages_keys():
    payload = {"mood": "test", "intent": "Plan", "tone": "Therapist-Gentle"}
    msgs = build_messages(payload)
    assert isinstance(msgs, list) and len(msgs) == 2
    assert msgs[0]["role"] == "system"
    assert msgs[1]["role"] == "user"
    assert "mood" in msgs[1]["content"]
    assert "intent" in msgs[1]["content"]
    assert "tone" in msgs[1]["content"]
