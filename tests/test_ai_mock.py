from core.ai import generate_spark

def test_fallback_without_key():
    data = generate_spark(messages=[{"role": "user", "content": "{}"}], api_key=None)
    assert "spark" in data and "focus" in data
    assert isinstance(data["spark"], str) and isinstance(data["focus"], str)
    assert len(data["spark"]) > 0 and len(data["focus"]) > 0
