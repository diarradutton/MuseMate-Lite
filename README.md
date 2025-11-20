📘 MuseMate Lite — AI Daily Spark

MuseMate Lite is a tiny AI-powered productivity companion designed to help users start their day with clarity, intention, and emotional grounding.

It delivers one personalized “Daily Spark” and one simple micro-action, tailored to your mood and goal for the day.

Built for speed, simplicity, and warmth — MuseMate Lite is a small slice of the full MuseMate product vision.

🌐 Live Demo

🔗 https://musemate-litediarradutton.streamlit.app

🎯 What MuseMate Lite Does

MuseMate Lite asks two simple questions:

How are you feeling today?

What do you want — Create, Plan, Move, or Reflect?

Then it generates:

✨ A personalized Spark

A 1–2 sentence, gentle nudge that meets the user where they are emotionally.

🎯 A Focus micro-task

A tiny, achievable action that keeps users moving toward clarity or progress.

🎭 Multiple AI Tones

Users can choose the feel of their guidance:

Warm Big Sis

Therapist-Gentle

Direct-but-Loving


🧠 How AI Is Used

MuseMate Lite uses an OpenAI GPT model to:

Understand emotional context

Interpret the user’s intent (Create / Plan / Move / Reflect)

Adapt tone and guidance style

Produce empathetic, human-feeling micro advice

Maintain short-term session memory

Generate shareable PNG cards

All prompts are carefully structured for warmth, clarity, and emotional intelligence.

🏗️ Tech Stack

Python 3.9+

Streamlit (UI, session state, deployment)

OpenAI API (AI generation)

Pillow (PNG export)

httpx (networking)

GitHub + Streamlit Cloud (hosting)

📁 Project Structure
musemate-lite/
│
├── app.py                # Main Streamlit app
├── core/
│   ├── ai.py             # AI client + inference logic
│   ├── prompts.py        # Tone prompts + system prompt
│   └── render.py         # Display logic + PNG generation
│
├── theme.css             # UI theme override
├── requirements.txt      # Dependencies
├── .streamlit/
│   └── config.toml       # Theme + settings
│
└── README.md             # You are here

🚀 Run Locally
1. Clone the repo
git clone https://github.com/diarradutton/MuseMate-Lite.git
cd MuseMate-Lite

2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Add your OpenAI key
Create .streamlit/secrets.toml:
OPENAI_API_KEY = "your-key-here"

5. Run the app
python3 -m streamlit run app.py

🔮 Future Vision (Full MuseMate)

MuseMate Lite is just the beginning.
The full MuseMate will include:

Habit tracking

Daily reflections & journaling

Creative challenges

Mood insights & mini dashboards

Streaks + gentle accountability

Multi-language support

iOS + Android versions

Theme personalization (Dark/Light/Soft Blush)

Subscription tiers: Free daily spark vs unlimited access

MuseMate aims to fuse AI coaching + emotional support + productivity into one warm, simple experience.

🧑‍💻 Built By

Diarra Dutton
AI Builder • Product Thinker • Future Cybersecurity + AI Engineer
2025 Block Fellowship Applicant