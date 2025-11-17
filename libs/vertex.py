import os

from google import genai
from google.genai import types


def get_vertex_ai_client():
    """Initializes and returns a Vertex AI GenAI client."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "dev-projects-476011")
    return genai.Client(
        vertexai=True,
        project=project_id,
        location="asia-northeast1",
    )


def summarize_with_vertex_ai(stories_text):
    """Summarizes a list of stories using Vertex AI."""
    client = get_vertex_ai_client()

    prompt = f"""Summarize these Hacker News links in a LINE-friendly message.
      Use short paragraphs, no markdown, no fluff.
      Each item should look like:
      - Title, use '-' at the start of each line
      - 1–2 sentence summary
      - Why it matters (1 short sentence)
      - Keep the tone simple and direct.
      Here are the stories:
    {stories_text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            # system_instruction=SYSTEM,
            temperature=0.1,
        ),
    )
    return response.text
