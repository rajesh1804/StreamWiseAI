import os
import requests
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_retention_tip(input_title, recommendations, user_history=None):
    """
    recommendations: List of dicts with keys - title, genres, overview
    user_history: Optional list of past watched movies
    """
    if not OPENROUTER_API_KEY:
        raise ValueError("Missing OpenRouter API key. Set OPENROUTER_API_KEY as env variable.")

    prompt = build_prompt(input_title, recommendations, user_history)

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": os.getenv("HTTP_REFERER"),  # or your repo or site
        "X-Title": "StreamWiseAI Retention Coach"
    }


    payload = {
        "model": "mistralai/mistral-7b-instruct:free",  # Free, fast
        "messages": [
            {"role": "system", "content": "You are a Retention Coach AI who helps users stay engaged by suggesting patterns in what they enjoy."},
            {"role": "user", "content": prompt}
        ]
    }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type((requests.exceptions.RequestException,))
    )
    def call_openrouter():
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    try:
        return call_openrouter()
    except Exception as e:
        print("Retry failed:", e)
        return "⚠️ Unable to generate retention tip right now."


def build_prompt(input_title, recommendations, user_history=None):
    recs_text = ""
    for rec in recommendations:
        recs_text += f"- Title: {rec['title']}\n  Genres: {rec['genres']}\n  Overview: {rec['overview'][:200]}...\n"

    history_text = ""
    if user_history:
        history_text = "Previously liked movies:\n" + "\n".join(f"- {title}" for title in user_history)

    prompt = f"""
The user searched for the movie: "{input_title}".

Here are the top recommendations:
{recs_text}

{history_text}

Based on this, suggest a 1–2 line insight about what the user might enjoy and a content retention tip.
Only output the tip, no extra text.
"""
    return prompt.strip()
