from typing import Dict, List

SYSTEM_PROMPT = (
    "You are MuseMate, a supportive coach for productivity and creativity. "
    "Your style is warm, concise, and human. "
    "Return JSON with keys: spark, focus. "
    "spark is 1-2 lines that clarify, encourage, or inspire. "
    "focus is one tiny, concrete step the user can take today. "
    "Match the selected tone: Warm Big-Sis (playful hype), Therapist-Gentle (calm, validating), "
    "Direct-but-Loving (clear but kind). Avoid cliches. Keep total under ~70 words. "
    "If the user expresses distress, use grounding language and suggest seeking support as appropriate."
)

def build_messages(payload: Dict) -> List[Dict]:
    # Pull fields safely and keep them short/sane
    mood = (payload.get("mood") or "")[:600]
    intent = (payload.get("intent") or "Plan").strip()
    tone = (payload.get("tone") or "Therapist-Gentle").strip()

    # Prevent quote issues in the tiny JSON blob we send as user content
    esc = lambda s: s.replace('"', "'")

    user_content = (
        '{'
        f'"mood":"{esc(mood)}",'
        f'"intent":"{esc(intent)}",'
        f'"tone":"{esc(tone)}"'
        '}'
    )

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]
