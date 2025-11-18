# MuseMate Lite - AI Daily Spark (Fellowship Edition)

A night-sky themed, chat-style web app that turns your mood and intent into a warm **Spark** (clarity prompt) and **Focus** (one micro-action). It is a tiny slice of the larger MuseMate vision: daily sparks, reminders, and supportive coaching.

## Quick start (local)

```bash
pip install -r requirements.txt
# set your OpenAI key
export OPENAI_API_KEY="sk-..."
streamlit run app.py
```

## Deploy on Streamlit Cloud (recommended)

1. Push this folder to a new GitHub repo (e.g., `musemate-lite`).
2. Go to share.streamlit.io and select your repo.
3. In App Settings -> Secrets, add:
```
OPENAI_API_KEY = "sk-..."
```
4. Deploy. Your app will have a public URL to share.

## Deploy on Hugging Face Spaces (alternative)

1. Create a Space using the Streamlit template.
2. Upload these files.
3. In the Space's Variables and secrets, add `OPENAI_API_KEY`.
4. Deploy.

## Tests and quality checks

```bash
pytest -q
pre-commit install
pre-commit run --all-files
```

## What to show in the fellowship application

- Live App: <your URL>
- Demo Video: <your Loom link>
- Code/Case Study: <your GitHub repo>

## Notes

- If the API errors or you have no key set, the app returns a graceful fallback Spark/Focus so the UI never breaks.
- The PNG download is generated locally with Pillow for easy sharing.
- Colors: deep navy to violet gradient, lavender accent, warm beige text.
