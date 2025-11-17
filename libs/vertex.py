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

    prompt = f"""Please summarize the following list of top 10 Hacker News stories.
    Provide a brief, engaging overview of the main topics and trends.
    Keep it concise and suitable for a notification message.

    Stories:
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
