# core/ai.py
import json
import re
import time
from typing import Dict, List, Optional

# Friendly offline fallback if the API isn't reachable or key/billing is missing
FALLBACK: Dict[str, str] = {
    "spark": "Take one gentle step. You do not need to earn your own support.",
    "focus": "Set a 5-minute timer and write three bullet points about what you want today.",
}

def _extract_json(s: str) -> Dict[str, str]:
    """
    Try to parse JSON strictly; if the model wrapped JSON in extra text,
    pull the first {...} block and parse that.
    """
    if not s:
        return {}
    # 1) Strict parse
    try:
        d = json.loads(s)
        return {
            "spark": (d.get("spark") or "").strip(),
            "focus": (d.get("focus") or "").strip(),
        }
    except Exception:
        pass
    # 2) Lenient parse from first JSON-like block
    m = re.search(r"\{.*\}", s, flags=re.S)
    if m:
        try:
            d = json.loads(m.group(0))
            return {
                "spark": (d.get("spark") or "").strip(),
                "focus": (d.get("focus") or "").strip(),
            }
        except Exception:
            pass
    return {}

def _call_chat(messages: List[Dict], api_key: str, temperature: float, model: str) -> Dict[str, str]:
    """
    Primary path: Chat Completions API.
    Requires openai>=1.44.0.
    """
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        response_format={"type": "json_object"},
        messages=messages,
        timeout=30,
    )
    content = (resp.choices[0].message.content or "").strip()
    return _extract_json(content)

def _call_responses(messages: List[Dict], api_key: str, temperature: float, model: str) -> Dict[str, str]:
    """
    Fallback path: Responses API.
    NOTE: Do NOT pass response_format here to support older SDKs.
    """
    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    sys = next((m["content"] for m in messages if m.get("role") == "system"), "")
    user = next((m["content"] for m in messages if m.get("role") == "user"), "")
    prompt = f"{sys}\n\nReturn JSON with keys: spark, focus (no extra text).\n\nUSER: {user}"

    resp = client.responses.create(
        model=model,
        input=prompt,
        temperature=temperature,
        timeout=30,
    )

    # Try to read unified text from Responses API
    content = ""
    try:
        # Newer SDKs often expose text at resp.output[0].content[0].text
        content = resp.output[0].content[0].text  # type: ignore[attr-defined]
    except Exception:
        # Fallback to .content or stringifying the object
        content = getattr(resp, "content", "") or str(resp)

    return _extract_json(content)

def generate_spark(messages: List[Dict], api_key: Optional[str]) -> Dict[str, str]:
    """
    Main entry used by the app. Tries chat.completions (temp 0.8),
    then Responses API (temp 0.3). Returns {spark, focus} and, on failure,
    adds a hidden '_error' string for the UI expander.
    """
    if not api_key:
        return {**FALLBACK, "_error": "No API key loaded"}

    first_err = None
    second_err = None

    # Attempt 1: Chat Completions (creative)
    try:
        data = _call_chat(messages, api_key=api_key, temperature=0.8, model="gpt-4o")
        if data.get("spark") or data.get("focus"):
            return data
        first_err = "chat(0.8) returned empty/invalid JSON"
    except Exception as e:
        first_err = f"chat(0.8) {type(e).__name__}: {e}"

    # Small backoff then Attempt 2: Responses API (safer)
    time.sleep(0.4)
    try:
        data = _call_responses(messages, api_key=api_key, temperature=0.3, model="gpt-4o")
        if data.get("spark") or data.get("focus"):
            return data
        second_err = "responses(0.3) returned empty/invalid JSON"
    except Exception as e:
        second_err = f"responses(0.3) {type(e).__name__}: {e}"

    # Final safety
    combined = " | ".join([e for e in [first_err, second_err] if e])
    return {**FALLBACK, "_error": combined or "Unknown error"}
