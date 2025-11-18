# app.py
import os
from datetime import datetime
from typing import Dict, Any, List

import streamlit as st

from core.prompts import build_messages
from core.ai import generate_spark
from core.render import make_share_card

APP_TITLE = "MuseMate Lite - AI Daily Spark"
APP_TAGLINE = "Tiny coach energy: one clarity spark plus one micro-action."

# --------- Page + theme ----------
st.set_page_config(page_title="MuseMate Lite", page_icon="🌙", layout="centered")

css_path = os.path.join(os.path.dirname(__file__), "theme.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(
    f"<div class='hero'><h1>{APP_TITLE}</h1><p>{APP_TAGLINE}</p></div>",
    unsafe_allow_html=True,
)

# --------- Load API key ----------
api_key = None
try:
    # Streamlit secret first
    api_key = st.secrets.get("OPENAI_API_KEY")
except Exception:
    api_key = None
if not api_key:
    # Fallback to environment variable
    api_key = os.environ.get("OPENAI_API_KEY")

# --------- Session state ----------
if "history" not in st.session_state:
    st.session_state.history = []  # type: List[Dict[str, Any]]
if "intent" not in st.session_state:
    st.session_state.intent = "Plan"

# --------- Inputs ----------
st.subheader("How are you feeling and what do you want today?")

cols = st.columns(4)
for i, label in enumerate(["Create", "Plan", "Move", "Reflect"]):
    if cols[i].button(label):
        st.session_state.intent = label

mood = st.text_area(
    "Mood and context",
    placeholder="Short is perfect. Example: nervous about a presentation but excited to contribute",
    height=110,
)

tone = st.selectbox(
    "Tone",
    ["Warm Big-Sis", "Therapist-Gentle", "Direct-but-Loving"],
    index=1,
)

left, right = st.columns(2)
with left:
    run = st.button("✨ Spark me", use_container_width=True)
with right:
    clear = st.button("Clear history", use_container_width=True)

if clear:
    st.session_state.history = []
    st.experimental_rerun()

# Helpful banner if no key loaded (still works with graceful fallback)
if not api_key:
    st.info(
        "🔑 Add your OPENAI_API_KEY via `.streamlit/secrets.toml` or an environment variable to enable live AI. "
        "The app will still work with a gentle fallback.",
        icon="🔑",
    )

# --------- Generate ----------
if run:
    if not mood.strip():
        st.warning("Add a short mood or intent first.", icon="💡")
    else:
        payload = {"mood": mood.strip(), "intent": st.session_state.intent, "tone": tone}
        messages = build_messages(payload)
        result = generate_spark(messages=messages, api_key=api_key)

        spark = (result.get("spark") or "").strip()
        focus = (result.get("focus") or "").strip()

        # Store most recent first
        st.session_state.history.insert(
            0,
            {
                "ts": datetime.utcnow().isoformat(timespec="seconds") + "Z",
                "intent": st.session_state.intent,
                "tone": tone,
                "spark": spark,
                "focus": focus,
                "_error": result.get("_error"),
            },
        )
        st.session_state.history = st.session_state.history[:5]

# --------- Output card + PNG ----------
if st.session_state.history:
    latest = st.session_state.history[0]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### Spark")
    st.write(latest.get("spark") or "—")
    st.markdown("#### Focus")
    st.write(latest.get("focus") or "—")
    st.markdown("</div>", unsafe_allow_html=True)

    png_bytes = make_share_card(latest.get("spark") or "Your spark goes here")
    st.download_button(
        "Download PNG",
        data=png_bytes,
        file_name=f"musemate_spark_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.png",
        mime="image/png",
    )

    # Developer-only diagnostics (collapsed by default)
    if latest.get("_error"):
        with st.expander("Developer info (hidden in demo)"):
            st.code(latest["_error"])

# --------- History ----------
if st.session_state.history:
    st.markdown("### Recent sparks")
    for item in st.session_state.history:
        st.markdown("<div class='history'>", unsafe_allow_html=True)
        st.caption(f"{item['ts']} • {item['intent']} • {item['tone']}")
        st.write(f"**Spark:** {item.get('spark','')}")
        st.write(f"**Focus:** {item.get('focus','')}")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("MuseMate Lite — Fellowship edition. A tiny slice of a bigger vision.")
