import os

from google import genai
from google.genai import types
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
)

from libs.hacker_news import get_top_stories

# ---- Client (Vertex mode; uses project/location like your old code) ----
client = genai.Client(
    vertexai=True,
    project=os.environ.get("PROJECT_ID", "dev-projects-476011"),
    location="asia-northeast1",
)

# --- LINE Configuration ---
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")

# --- Vertex AI Configuration ---
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "dev-projects-476011")


def summarize_stories_with_vertex_ai(stories_text):
    """Summarizes a list of stories using Vertex AI."""
    if not GOOGLE_CLOUD_PROJECT:
        print("Error: GOOGLE_CLOUD_PROJECT environment variable not set.")
        return "Summary is unavailable."

    try:
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
    except Exception as e:
        print(f"Error generating summary with Vertex AI: {e}")
        return "Could not generate a summary at this time."


def main():
    """
    Fetches, summarizes, and broadcasts top 10 Hacker News stories.
    """
    if not all([LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET]):
        print("Error: Please set LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET.")
        return

    top_stories = get_top_stories(10)

    if not top_stories:
        print("No stories fetched from Hacker News.")
        return

    message_lines = []
    for story in top_stories:
        title = story.get("title", "No Title")
        url = story.get("url", "No URL")
        message_lines.append(f"- {title}: {url}")

    stories_as_text = "\n".join(message_lines)

    print("Generating summary with Vertex AI...")
    summary_message = summarize_stories_with_vertex_ai(stories_as_text)

    print("Prepared message to broadcast:", summary_message)

    configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
    api_client = ApiClient(configuration)
    line_bot_api = MessagingApi(api_client)

    # try:
    #     broadcast_request = BroadcastRequest(
    #         messages=[TextMessage(text=summary_message)]
    #     )
    #     line_bot_api.broadcast(broadcast_request)
    #     print("Successfully broadcasted summary to LINE.")
    # except ApiException as e:
    #     print(f"Error sending message to LINE: {e.body}")


if __name__ == "__main__":
    main()
