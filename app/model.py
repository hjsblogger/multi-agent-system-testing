import os
import time
from types import SimpleNamespace

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise RuntimeError(
        "Missing GEMINI_API_KEY. Add your Gemini API key to .env"
    )

client = genai.Client(api_key=api_key)

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")


class GeminiModel:

    def invoke(self, prompt: str):

        max_attempts = 3

        for attempt in range(max_attempts):

            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt,
                )

                return SimpleNamespace(
                    content=response.text or ""
                )

            except errors.ServerError as e:

                if attempt == max_attempts - 1:
                    raise

                wait_time = 2 ** attempt

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_time}s..."
                )

                time.sleep(wait_time)


model = GeminiModel()